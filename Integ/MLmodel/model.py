import os
import pandas as pd
import numpy as np
from django.conf import settings

class DiopterDataModel:
    def __init__(self, csv_file=None):
        """
        Initialize the model with data from the combined CSV file.
        :param csv_file: Path to the CSV file containing the data (default: project directory).
        """
        # Default to the CSV file in the Django project
        if csv_file is None:
            csv_file = os.path.join(settings.BASE_DIR,"MLmodel", "diopter_data_combined2.csv")

        # Check if the file exists before loading
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        # Load and clean data
        self.data = pd.read_csv(csv_file).sort_values(by="Diopter (D)").reset_index(drop=True)

        # Convert relevant columns to float
        resolution_columns = [
            "1920x1080 (FHD, 24\")",
            "2560x1440 (2K, 27\")",
            "3840x2160 (4K, 32\")"
        ]

        for col in resolution_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors="coerce")  # Handle conversion errors safely

    def get_diopter(self, value, tolerance=1.0):
        """
        Get the diopter value corresponding to the given resolution value.
        :param value: The resolution value to search for.
        :param tolerance: Acceptable difference for approximate matching.
        :return: The corresponding diopter value or None if not found.
        """
        # Filter for close matches in any resolution column
        match = self.data[
            (np.isclose(self.data["1920x1080 (FHD, 24\")"], value, atol=tolerance)) |
            (np.isclose(self.data["2560x1440 (2K, 27\")"], value, atol=tolerance)) |
            (np.isclose(self.data["3840x2160 (4K, 32\")"], value, atol=tolerance))
        ]

        return match["Diopter (D)"].values[0] if not match.empty else None

    def get_all_data(self):
        """
        Get the full dataset as a DataFrame.
        :return: Pandas DataFrame containing all data.
        """
        return self.data
