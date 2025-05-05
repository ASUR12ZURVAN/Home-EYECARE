import os
import pandas as pd
import numpy as np
from django.conf import settings

class DiopterDataModel:
    def __init__(self, csv_file=None):
        """
        Initialize the model with data from the combined CSV file.
        """
        if csv_file is None:
            csv_file = os.path.join(settings.BASE_DIR, "MLmodel", "diopter_data_combined2.csv")

        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file not found: {csv_file}")

        self.data = pd.read_csv(csv_file).sort_values(by="Diopter (D)").reset_index(drop=True)

        # Columns corresponding to each resolution
        self.resolution_columns = [
            "1920x1080 (FHD, 24\")",
            "2560x1440 (2K, 27\")",
            "3840x2160 (4K, 32\")"
        ]

        for col in self.resolution_columns:
            self.data[col] = pd.to_numeric(self.data[col], errors="coerce")

        # Remove duplicate diopters, keeping the last one
        self.data = self.data.drop_duplicates(subset="Diopter (D)", keep="last")

    def get_diopter(self, value, tolerance=1.0, resolution=None, distance=None):
        """
        Get the diopter value for a given pixel size, resolution, and viewing distance.
        Enforces:
            - positive diopters for hypermetropia (0.25m)
            - negative diopters for myopia (3.0m)
            - includes 0 for both conditions
        """
        if resolution:
            if resolution not in self.resolution_columns:
                raise ValueError(f"Resolution '{resolution}' not found in dataset.")
            candidates = self.data[np.isclose(self.data[resolution], value, atol=tolerance)]
        else:
            candidates = self.data[
                np.any([np.isclose(self.data[col], value, atol=tolerance)
                        for col in self.resolution_columns], axis=0)
            ]

        if not candidates.empty and distance is not None:
            if distance == 0.25:
                candidates = candidates[candidates["Diopter (D)"] >= 0]  # hypermetropia includes 0 and positive
            elif distance == 3.0:
                candidates = candidates[candidates["Diopter (D)"] <= 0]  # myopia includes 0 and negative

        if not candidates.empty:
            return candidates["Diopter (D)"].values[0]

        return None

    def get_pixel_sizes(self, diopter):
        """
        Get all pixel sizes for a given diopter value.
        :param diopter: The diopter value to look up.
        :return: Dict of resolution: pixel_size or None.
        """
        row = self.data[self.data["Diopter (D)"] == diopter]
        if not row.empty:
            return row.iloc[0][self.resolution_columns].to_dict()
        return None

    def get_condition_type(self, distance):
        """
        Determine the condition type based on viewing distance.
        """
        if distance == 0.25:
            return "Hypermetropia (farsightedness)"
        elif distance == 3.0:
            return "Myopia (nearsightedness)"
        else:
            return "Unknown condition"

    def get_all_data(self):
        """
        Return the full dataset as a DataFrame.
        """
        return self.data
