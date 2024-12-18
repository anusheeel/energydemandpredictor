import os
import pandas as pd
from PyPDF2 import PdfReader

class DataProcessor:
    @staticmethod
    def clean_data(data: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess the data."""
        if "Date" in data.columns:
            data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
        if "Energy Usage (kWh)" in data.columns:
            data["Energy Usage (kWh)"] = pd.to_numeric(data["Energy Usage (kWh)"], errors="coerce")

        # Drop rows with missing or invalid values
        data = data.dropna()
        return data

    @staticmethod
    def summarize_data(data: pd.DataFrame) -> dict:
        """Generate summary statistics for the data."""
        summary = {
            "total_energy": data["Energy Usage (kWh)"].sum(),
            "average_energy": data["Energy Usage (kWh)"].mean(),
            "max_energy": data["Energy Usage (kWh)"].max(),
            "min_energy": data["Energy Usage (kWh)"].min(),
        }
        return summary
