from flask import Blueprint, request, jsonify, render_template
import os
import pandas as pd
from werkzeug.utils import secure_filename
from app.services.file_parser import FileParser
from app.services.data_processor import DataProcessor
from app.services.llmanalyzer import LLMAnalyzer
from app.services.responseprocessor import process_response

# Create the blueprint
upload_bp = Blueprint('upload_bp', __name__)

# Define the folder to save uploaded files
UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'pdf'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/", methods=["GET"])
def upload_home():
    """Render the upload form."""
    return render_template("upload.html")

@upload_bp.route("/", methods=["POST"])
def upload_file():
    """Handle file uploads, analyze, and process them."""
    if "files" not in request.files:
        return jsonify({"error": "No files uploaded!"}), 400

    uploaded_files = request.files.getlist("files")
    results = []

    for file in uploaded_files:
        if file.filename == "":
            continue

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        try:
            # Detect file type based on extension
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension in [".xls", ".xlsx"]:
                # Use pandas to read Excel files
                data = pd.read_excel(file_path)

                # Deduplicate columns
                data.columns = pd.Series(data.columns).apply(
                    lambda x: f"{x}_{data.columns.tolist().count(x)}" if data.columns.tolist().count(x) > 1 else x
                )

                # Validate column and data alignment
                for idx, row in data.iterrows():
                    if len(data.columns) != len(row):
                        raise ValueError(f"Mismatch in file {filename}: {len(data.columns)} columns, but {len(row)} values in row {idx + 1}.")

                file_content = data.to_csv(index=False)  # Convert to CSV format for LLM
            elif file_extension == ".csv":
                # Use pandas to read CSV files
                data = pd.read_csv(file_path)

                # Deduplicate columns
                data.columns = pd.Series(data.columns).apply(
                    lambda x: f"{x}_{data.columns.tolist().count(x)}" if data.columns.tolist().count(x) > 1 else x
                )

                # Validate column and data alignment
                for idx, row in data.iterrows():
                    if len(data.columns) != len(row):
                        raise ValueError(f"Mismatch in file {filename}: {len(data.columns)} columns, but {len(row)} values in row {idx + 1}.")

                file_content = data.to_csv(index=False)
            else:
                results.append({
                    "file_name": filename,
                    "error": f"Unsupported file type: {file_extension}",
                    "status": "Failed to analyze"
                })
                continue

            # Analyze the file content with LLM
            analysis_result = LLMAnalyzer.analyze_content(file_content)

            if "error" in analysis_result:
                results.append({
                    "file_name": filename,
                    "error": analysis_result["error"],
                    "status": "Failed to analyze"
                })
                continue

            # Process the LLM response
            metadata, df = process_response(analysis_result)

            if metadata is None or df is None:
                results.append({
                    "file_name": filename,
                    "error": "Failed to process the response.",
                    "status": "Failed to process"
                })
            else:
                results.append({
                    "file_name": filename,
                    "metadata": metadata,
                    "data_preview": df.head().to_dict(),
                    "status": "Processed successfully"
                })

        except Exception as e:
            results.append({
                "file_name": filename,
                "error": str(e),
                "status": "Failed to process"
            })

    return jsonify({"results": results})