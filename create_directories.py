import os

def create_file(file_path, content=""):
    """Creates a file with the specified content."""
    with open(file_path, 'w') as file:
        file.write(content)

def create_folder_structure(base_dir):
    """Creates the folder structure for the energy analyzer project."""

    structure = {
        "app": {
            "__init__.py": "",
            "main.py": "# Entry point for the application\n",
            "routes": {
                "__init__.py": "",
                "upload_routes.py": "# Routes for file uploads\n",
                "analytics_routes.py": "# Routes for visualizations\n",
            },
            "services": {
                "__init__.py": "",
                "file_parser.py": "# Logic to parse files (CSV, Excel, PDF)\n",
                "data_processor.py": "# Cleaning and processing data\n",
                "visualizer.py": "# Visualization functions\n",
            },
            "static": {},
            "templates": {},
        },
        "tests": {
            "test_file_parser.py": "# Unit tests for file parsing\n",
            "test_data_processor.py": "# Unit tests for data processing\n",
            "test_routes.py": "# Integration tests for API\n",
        },
        "data": {
            "sample.csv": "",
            "sample.xlsx": "",
            "sample.pdf": "",
        },
        "requirements.txt": "# Python dependencies\n",
        "README.md": "# Documentation\n",
    }

    def create_structure(base, structure):
        for name, content in structure.items():
            path = os.path.join(base, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                create_file(path, content)

    create_structure(base_dir, structure)

if __name__ == "__main__":
    base_directory = os.getcwd()  # Use the current directory
    create_folder_structure(base_directory)
    print(f"Folder structure created at {base_directory}")
