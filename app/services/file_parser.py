import os
import pandas as pd
from PyPDF2 import PdfReader

class FileParser:
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read the content of a file and return as text."""
        _, file_extension = os.path.splitext(file_path)

        if file_extension.lower() == ".csv":
            return pd.read_csv(file_path).to_string()
        elif file_extension.lower() in [".xls", ".xlsx"]:
            return pd.read_excel(file_path).to_string()
        elif file_extension.lower() == ".pdf":
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() for page in reader.pages)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
