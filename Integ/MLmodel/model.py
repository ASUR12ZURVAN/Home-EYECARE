import pandas as pd
import numpy as np

class DiopterDataModel:
    def __init__(self, csv_file):
        """
        Initialize the model with data from the combined CSV file.
        :param csv_file: Path to the CSV file containing the data.
        """
        self.data = pd.read_csv(csv_file).sort_values(by="Diopter (D)").reset_index(drop=True)
        
        self.data["1920x1080 (FHD, 24\")"] = self.data["1920x1080 (FHD, 24\")"].astype(float)
        self.data["2560x1440 (2K, 27\")"] = self.data["2560x1440 (2K, 27\")"].astype(float)
        self.data["3840x2160 (4K, 32\")"] = self.data["3840x2160 (4K, 32\")"].astype(float)

    def get_diopter(self, value, tolerance=1):
        """
        Get the diopter value corresponding to the given resolution value.
        :param value: The resolution value to search for.
        :param tolerance: Acceptable difference for approximate matching (default: 1)
        :return: The corresponding diopter value or None if not found.
        """
        result = self.data[
            (np.isclose(self.data["1920x1080 (FHD, 24\")"], value, atol=tolerance)) |
            (np.isclose(self.data["2560x1440 (2K, 27\")"], value, atol=tolerance)) |
            (np.isclose(self.data["3840x2160 (4K, 32\")"], value, atol=tolerance))
        ]
        return result["Diopter (D)"].values[0] if not result.empty else None

    def get_all_data(self):
        """
        Get the full dataset as a DataFrame.
        :return: Pandas DataFrame containing all data.
        """
        return self.data


