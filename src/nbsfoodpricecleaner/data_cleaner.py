import pandas as pd
from typing import Optional


class NBSFoodPriceCleaner:
    """
    A class for cleaning and processing NBS food price data.
    """

    def __init__(self, input_filepath: Optional[str] = None, output_filepath: str = "cleaned_nbs_data.csv") -> None:
        """
        Initialize the cleaner with file paths.

        Args:
            input_filepath (Optional[str]): Path to the raw CSV file.
            output_filepath (str): Path to save the cleaned CSV file.
        """
        self.input_filepath = input_filepath
        self.output_filepath = output_filepath
        self.data = None

    def load_data(self) -> None:
        """
        Load the raw data from the input CSV file.
        """
        if not self.input_filepath:
            raise ValueError("Input file path is not specified.")

        try:
            self.data = pd.read_csv(self.input_filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{self.input_filepath}' was not found.")
        except pd.errors.EmptyDataError:
            raise ValueError("Error: The file is empty.")
        except Exception as e:
            raise Exception(f"An error occurred while loading data: {e}")

    def clean_data(self) -> None:
        """
        Clean and process the loaded data.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

        # Drop irrelevant columns
        columns_to_drop = [
            "_tags",
            "_notes",
            "_duration",
            "_id",
            "_uuid",
            "meta/instanceID",
            "_submission_time",
            "_date_modified",
            "_version",
            "_submitted_by",
            "_total_media",
            "_media_count",
            "_media_all_received",
            "_xform_id",
        ]
        self.data.drop(columns=columns_to_drop, errors="ignore", inplace=True)

        # Rename columns for consistency
        self.data.rename(
            columns={
                "today": "Date",
                "STATELABEL": "State",
                "lgalabel": "LGA",
                "g_consent/Section_A/market_type": "Outlet Type",
                "g_consent/Section_A/_gps_latitude": "Latitude",
                "g_consent/Section_A/_gps_longitude": "Longitude",
                "sector": "Sector",
                "VC_ID": "CONTRIBUTOR ID",  # Contributor ID from VC_ID
            },
            inplace=True,
        )

        # Add default country
        self.data["Country"] = "Nigeria"

        # Ensure 'Locality' exists
        if "Locality" not in self.data.columns:
            self.data["Locality"] = None

    def save_cleaned_data(self) -> None:
        """
        Save the cleaned data to the specified output file.
        """
        if self.data is None:
            raise ValueError("No cleaned data available to save. Run `clean_data()` first.")

        self.data.to_csv(self.output_filepath, index=False)
        print(f"Cleaned data saved to {self.output_filepath}")
