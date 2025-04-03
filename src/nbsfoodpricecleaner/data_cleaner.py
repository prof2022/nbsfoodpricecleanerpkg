# import pandas as pd
# from typing import Optional, Dict, List


# class NBSFoodPriceCleaner:
#     """
#     A class for cleaning and processing NBS food price data.
#     """

#     def __init__(self, input_filepath: Optional[str] = None, output_filepath: str = "cleaned_nbs_data.csv") -> None:
#         """
#         Initialize the cleaner with file paths.

#         Args:
#             input_filepath (Optional[str]): Path to the raw CSV file.
#             output_filepath (str): Path to save the cleaned CSV file.
#         """
#         self.input_filepath = input_filepath
#         self.output_filepath = output_filepath
#         self.data: Optional[pd.DataFrame] = None

#     def load_data(self) -> None:
#         """
#         Load the raw data from the input CSV file.
#         """
#         if not self.input_filepath:
#             raise ValueError("Input file path is not specified.")

#         try:
#             self.data = pd.read_csv(self.input_filepath)
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Error: The file '{self.input_filepath}' was not found.")
#         except pd.errors.EmptyDataError:
#             raise ValueError("Error: The file is empty.")
#         except Exception as e:
#             raise Exception(f"An error occurred while loading data: {e}")

#     def clean_data(self) -> None:
#         """
#         Clean and process the loaded data.
#         """
#         if self.data is None:
#             raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

#         # Drop irrelevant columns
#         columns_to_drop: List[str] = [
#             "_tags",
#             "_notes",
#             "_duration",
#             "_id",
#             "_uuid",
#             "meta/instanceID",
#             "_submission_time",
#             "_date_modified",
#             "_version",
#             "_submitted_by",
#             "_total_media",
#             "_media_count",
#             "_media_all_received",
#             "_xform_id",
#         ]
#         self.data.drop(columns=columns_to_drop, errors="ignore", inplace=True)

#         # Rename columns for consistency
#         self.data.rename(
#             columns={
#                 "today": "Date",
#                 "STATELABEL": "State",
#                 "lgalabel": "LGA",
#                 "g_consent/Section_A/market_type": "Outlet Type",
#                 "_gps_latitude": "Latitude",
#                 "_gps_longitude": "Longitude",
#                 "sector": "Sector",
#                 "VC_ID": "CONTRIBUTOR ID",
#             },
#             inplace=True,
#         )

#         # Add default country
#         self.data["Country"] = "Nigeria"

#         # Map food items to their respective columns
#         food_mapping: Dict[str, Dict[str, str]] = {
#             "g_consent/Section_B1/maize_yellow": {
#                 "uom": "g_consent/Section_B1/uom_Ymaize",
#                 "quantity": "g_consent/Section_B1/Q_Ymaize",
#                 "price": "g_consent/Section_B1/price_Ymaize",
#             },
#             "g_consent/Section_B2/maize_white": {
#                 "uom": "g_consent/Section_B2/uom_Wmaize",
#                 "quantity": "g_consent/Section_B2/Q_Wmaize",
#                 "price": "g_consent/Section_B2/price_Wmaize",
#             },
#             "g_consent/Section_B3/sorghum": {
#                 "uom": "g_consent/Section_B3/uom_sorghum",
#                 "quantity": "g_consent/Section_B3/Q_sorghum",
#                 "price": "g_consent/Section_B3/price_sorghum",
#             },
#             "g_consent/Section_B4/imported_rice": {
#                 "uom": "g_consent/Section_B4/uom_imported_rice",
#                 "quantity": "g_consent/Section_B4/Q_rice",
#                 "price": "g_consent/Section_B4/price_imported_rice",
#             },
#             "g_consent/Section_B5/local_rice": {
#                 "uom": "g_consent/Section_B5/uom_local_rice",
#                 "quantity": "g_consent/Section_B5/Q_local_rice",
#                 "price": "g_consent/Section_B5/price_local_rice",
#             },
#             "g_consent/Section_B6/brown_beans": {
#                 "uom": "g_consent/Section_B6/uom_brownbeans",
#                 "quantity": "g_consent/Section_B6/Q_brownbeans",
#                 "price": "g_consent/Section_B6/price_brown_beans",
#             },
#             "g_consent/Section_B7/White_beans": {
#                 "uom": "g_consent/Section_B7/uom_whitebeans",
#                 "quantity": "g_consent/Section_B7/Q_whitebeans",
#                 "price": "g_consent/Section_B7/price_White_beans",
#             },
#             "g_consent/Section_B8/garri_confirm": {
#                 "uom": "g_consent/Section_B8/uom_garri",
#                 "quantity": "g_consent/Section_B8/Q_garri",
#                 "price": "g_consent/Section_B8/price_garri",
#             },
#             "g_consent/Section_B9/yam_confirm": {
#                 "uom": "g_consent/Section_B9/uom_yam",
#                 "quantity": "g_consent/Section_B9/Q_yam",
#                 "price": "g_consent/Section_B9/price_yam",
#             },
#             "g_consent/Section_B10/Soyabeans": {
#                 "uom": "g_consent/Section_B10/uom_soyabeans",
#                 "quantity": "g_consent/Section_B10/Q_soyabeans",
#                 "price": "g_consent/Section_B10/price_soyabeans",
#             },
#         }

#         # Prepare long-format data
#         long_format_data: List[pd.DataFrame] = []
#         for food_col, mapping in food_mapping.items():
#             uom_col = mapping["uom"]
#             quantity_col = mapping["quantity"]
#             price_col = mapping["price"]

#             if all(col in self.data.columns for col in [uom_col, quantity_col, price_col]):
#                 temp_df = self.data[
#                     [
#                         "Date",
#                         "State",
#                         "CONTRIBUTOR ID",
#                         "LGA",
#                         "Outlet Type",
#                         "Latitude",
#                         "Longitude",
#                         "Country",
#                         "Sector",
#                     ]
#                 ].copy()
#                 temp_df["Food Item"] = food_col.split("/")[-1].replace("_", " ").capitalize()
#                 temp_df["UOM"] = self.data[uom_col].astype(str)
#                 temp_df["Quantity"] = pd.to_numeric(self.data[quantity_col], errors="coerce")
#                 temp_df["Price"] = pd.to_numeric(self.data[price_col], errors="coerce")

#                 # Calculate weight as Quantity * UOM (numeric part)
#                 temp_df["Weight"] = temp_df["Quantity"] * temp_df["UOM"].str.extract(r"(\d+\.?\d*)")[0].astype(float)

#                 # Calculate unit price
#                 temp_df["UPRICE"] = (temp_df["Price"] / temp_df["Weight"]).round(2)
#                 temp_df["Price Category"] = self.data.get("g_consent/Section_A/price_category", None)

#                 # Clean outlet type
#                 temp_df["Outlet Type"] = temp_df["Outlet Type"].str.replace("_", " ", regex=False)

#                 # Create Cont_ID_Count
#                 temp_df["Cont_ID_Count"] = temp_df["State"] + temp_df["CONTRIBUTOR ID"].astype(str)

#                 long_format_data.append(temp_df)

#         # Combine the cleaned data
#         if long_format_data:
#             self.data = pd.concat(long_format_data, ignore_index=True)
#         else:
#             raise ValueError("No valid data found to clean.")

#         # Reorder columns
#         column_order = [
#             "Date",
#             "State",
#             "CONTRIBUTOR ID",
#             "Cont_ID_Count",
#             "LGA",
#             "Outlet Type",
#             "Latitude",
#             "Longitude",
#             "Country",
#             "Sector",
#             "Food Item",
#             "UOM",
#             "Quantity",
#             "Price Category",
#             "Price",
#             "Weight",
#             "UPRICE",
#         ]
#         self.data = self.data[column_order]

#         # Convert 'Date' to datetime
#         self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")

#         # Drop rows with missing essential values
#         essential_cols = [
#             "State",
#             "LGA",
#             "Date",
#             "Food Item",
#             "UPRICE",
#             "UOM",
#             "Quantity",
#             "Price",
#             "Weight",
#             "Latitude",
#             "Longitude",
#         ]
#         self.data.dropna(subset=essential_cols, inplace=True)

#     def save_cleaned_data(self) -> None:
#         """
#         Save the cleaned data to the specified output file.
#         """
#         if self.data is None:
#             raise ValueError("No cleaned data available to save. Run `clean_data()` first.")

#         self.data.to_csv(self.output_filepath, index=False)
#         print(f"Cleaned data saved to {self.output_filepath}")

#     def setup_ano_ai_connection(self) -> None:
#         """
#         Placeholder for setting up a connection with the ano.ai platform.
#         """
#         pass  # Future implementation goes here

# import pandas as pd
# from typing import Optional, Dict, List


# class NBSFoodPriceCleaner:
#     """
#     A class for cleaning and processing NBS food price data.
#     """

#     def __init__(self, input_filepath: Optional[str] = None, output_filepath: str = "cleaned_nbs_data.csv") -> None:
#         """
#         Initialize the cleaner with file paths.

#         Args:
#             input_filepath (Optional[str]): Path to the raw CSV file.
#             output_filepath (str): Path to save the cleaned CSV file.
#         """
#         self.input_filepath = input_filepath
#         self.output_filepath = output_filepath
#         self.data: Optional[pd.DataFrame] = None

#     def load_data(self) -> None:
#         """
#         Load the raw data from the input CSV file.
#         """
#         if not self.input_filepath:
#             raise ValueError("Input file path is not specified.")

#         try:
#             self.data = pd.read_csv(self.input_filepath)
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Error: The file '{self.input_filepath}' was not found.")
#         except pd.errors.EmptyDataError:
#             raise ValueError("Error: The file is empty.")
#         except Exception as e:
#             raise Exception(f"An error occurred while loading data: {e}")

#     def clean_data(self) -> None:
#         """
#         Clean and process the loaded data.
#         """
#         if self.data is None:
#             raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

#         # Drop irrelevant columns
#         columns_to_drop: List[str] = [
#             "_tags",
#             "_notes",
#             "_duration",
#             "_id",
#             "_uuid",
#             "meta/instanceID",
#             "_submission_time",
#             "_date_modified",
#             "_version",
#             "_submitted_by",
#             "_total_media",
#             "_media_count",
#             "_media_all_received",
#             "_xform_id",
#         ]
#         self.data.drop(columns=columns_to_drop, errors="ignore", inplace=True)

#         # Rename columns for consistency
#         self.data.rename(
#             columns={
#                 "today": "Date",
#                 "STATELABEL": "State",
#                 "lgalabel": "LGA",
#                 "g_consent/Section_A/market_type": "Outlet Type",
#                 "_gps_latitude": "Latitude",
#                 "_gps_longitude": "Longitude",
#                 "sector": "Sector",
#                 "VC_ID": "Contributor_ID",
#             },
#             inplace=True,
#         )

#         # Add default country
#         self.data["Country"] = "Nigeria"

#         # Map food items to their respective columns
#         food_mapping: Dict[str, Dict[str, str]] = {
#             "g_consent/Section_B1/maize_yellow": {
#                 "uom": "g_consent/Section_B1/uom_Ymaize",
#                 "quantity": "g_consent/Section_B1/Q_Ymaize",
#                 "price": "g_consent/Section_B1/price_Ymaize",
#             },
#             "g_consent/Section_B2/maize_white": {
#                 "uom": "g_consent/Section_B2/uom_Wmaize",
#                 "quantity": "g_consent/Section_B2/Q_Wmaize",
#                 "price": "g_consent/Section_B2/price_Wmaize",
#             },
#             "g_consent/Section_B3/sorghum": {
#                 "uom": "g_consent/Section_B3/uom_sorghum",
#                 "quantity": "g_consent/Section_B3/Q_sorghum",
#                 "price": "g_consent/Section_B3/price_sorghum",
#             },
#             "g_consent/Section_B4/imported_rice": {
#                 "uom": "g_consent/Section_B4/uom_imported_rice",
#                 "quantity": "g_consent/Section_B4/Q_rice",
#                 "price": "g_consent/Section_B4/price_imported_rice",
#             },
#             "g_consent/Section_B5/local_rice": {
#                 "uom": "g_consent/Section_B5/uom_local_rice",
#                 "quantity": "g_consent/Section_B5/Q_local_rice",
#                 "price": "g_consent/Section_B5/price_local_rice",
#             },
#             "g_consent/Section_B6/brown_beans": {
#                 "uom": "g_consent/Section_B6/uom_brownbeans",
#                 "quantity": "g_consent/Section_B6/Q_brownbeans",
#                 "price": "g_consent/Section_B6/price_brown_beans",
#             },
#             "g_consent/Section_B7/White_beans": {
#                 "uom": "g_consent/Section_B7/uom_whitebeans",
#                 "quantity": "g_consent/Section_B7/Q_whitebeans",
#                 "price": "g_consent/Section_B7/price_White_beans",
#             },
#             "g_consent/Section_B8/garri_confirm": {
#                 "uom": "g_consent/Section_B8/uom_garri",
#                 "quantity": "g_consent/Section_B8/Q_garri",
#                 "price": "g_consent/Section_B8/price_garri",
#             },
#             "g_consent/Section_B9/yam_confirm": {
#                 "uom": "g_consent/Section_B9/uom_yam",
#                 "quantity": "g_consent/Section_B9/Q_yam",
#                 "price": "g_consent/Section_B9/price_yam",
#             },
#             "g_consent/Section_B10/Soyabeans": {
#                 "uom": "g_consent/Section_B10/uom_soyabeans",
#                 "quantity": "g_consent/Section_B10/Q_soyabeans",
#                 "price": "g_consent/Section_B10/price_soyabeans",
#             },
#         }

#         # Prepare long-format data
#         long_format_data: List[pd.DataFrame] = []
#         for food_col, mapping in food_mapping.items():
#             uom_col = mapping["uom"]
#             quantity_col = mapping["quantity"]
#             price_col = mapping["price"]

#             if all(col in self.data.columns for col in [uom_col, quantity_col, price_col]):
#                 temp_df = self.data[
#                     [
#                         "Date",
#                         "State",
#                         "Contributor_ID",
#                         "LGA",
#                         "Outlet Type",
#                         "Latitude",
#                         "Longitude",
#                         "Country",
#                         "Sector",
#                     ]
#                 ].copy()
#                 temp_df["Food Item"] = food_col.split("/")[-1].replace("_", " ").capitalize()
#                 temp_df["UOM"] = self.data[uom_col].astype(str)
#                 temp_df["Quantity"] = pd.to_numeric(self.data[quantity_col], errors="coerce")
#                 temp_df["Price"] = pd.to_numeric(self.data[price_col], errors="coerce")

#                 # Calculate weight as Quantity * UOM (numeric part)
#                 temp_df["Weight"] = temp_df["Quantity"] * temp_df["UOM"].str.extract(r"(\d+\.?\d*)")[0].astype(float)

#                 # Calculate unit price
#                 temp_df["UPRICE"] = (temp_df["Price"] / temp_df["Weight"]).round(2)
#                 temp_df["Price Category"] = self.data.get("g_consent/Section_A/price_category", None)

#                 # Clean outlet type
#                 temp_df["Outlet Type"] = temp_df["Outlet Type"].str.replace("_", " ", regex=False)

#                 # Create Contributor_State_ID
#                 temp_df["Contributor_State_ID"] = temp_df["State"] + temp_df["Contributor_ID"].astype(str)

#                 long_format_data.append(temp_df)

#         # Combine the cleaned data
#         if long_format_data:
#             self.data = pd.concat(long_format_data, ignore_index=True)
#         else:
#             raise ValueError("No valid data found to clean.")

#         # Reorder columns
#         column_order = [
#             "Date",
#             "State",
#             "Contributor_ID",
#             "Contributor_State_ID",
#             "LGA",
#             "Outlet Type",
#             "Latitude",
#             "Longitude",
#             "Country",
#             "Sector",
#             "Food Item",
#             "UOM",
#             "Quantity",
#             "Price Category",
#             "Price",
#             "Weight",
#             "UPRICE",
#         ]
#         self.data = self.data[column_order]

#         # Convert 'Date' to datetime
#         self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")

#         # Drop rows with missing essential values
#         essential_cols = [
#             "State",
#             "LGA",
#             "Date",
#             "Food Item",
#             "UPRICE",
#             "UOM",
#             "Quantity",
#             "Price",
#             "Weight",
#             "Latitude",
#             "Longitude",
#         ]
#         self.data.dropna(subset=essential_cols, inplace=True)

#         # Add Total Records Captured (TRC) column
#         trc_summary = self.data.groupby("Contributor_State_ID").size().reset_index(name="TRC")
#         self.data = self.data.merge(trc_summary, on="Contributor_State_ID", how="left")

#     def save_cleaned_data(self) -> None:
#         """
#         Save the cleaned data to the specified output file.
#         """
#         if self.data is None:
#             raise ValueError("No cleaned data available to save. Run `clean_data()` first.")

#         self.data.to_csv(self.output_filepath, index=False)
#         print(f"Cleaned data saved to {self.output_filepath}")

#     def setup_ano_ai_connection(self) -> None:
#         """
#         Placeholder for setting up a connection with the ano.ai platform.
#         """
#         pass  # Future implementation goes here


# import pandas as pd
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# from typing import Optional, Dict, List


# class NBSFoodPriceCleaner:
#     """
#     A class for cleaning and processing NBS food price data.
#     """

#     def __init__(self, input_filepath: Optional[str] = None, output_filepath: str = "cleaned_nbs_data.csv") -> None:
#         """
#         Initialize the cleaner with file paths.

#         Args:
#             input_filepath (Optional[str]): Path to the raw CSV file.
#             output_filepath (str): Path to save the cleaned CSV file.
#         """
#         self.input_filepath = input_filepath
#         self.output_filepath = output_filepath
#         self.data: Optional[pd.DataFrame] = None
#         self.invalid_data: Optional[pd.DataFrame] = None
#         self.cleaning_log: List[str] = []  # To track cleaning steps

#     def load_data(self) -> None:
#         """
#         Load the raw data from the input CSV file.
#         """
#         if not self.input_filepath:
#             raise ValueError("Input file path is not specified.")

#         try:
#             self.data = pd.read_csv(self.input_filepath)
#         except FileNotFoundError:
#             raise FileNotFoundError(f"Error: The file '{self.input_filepath}' was not found.")
#         except pd.errors.EmptyDataError:
#             raise ValueError("Error: The file is empty.")
#         except Exception as e:
#             raise Exception(f"An error occurred while loading data: {e}")

#     def check_duplicates(self, subset: Optional[List[str]] = None) -> None:
#         """
#         Check for and remove duplicate rows in the dataset.

#         Args:
#             subset (Optional[List[str]]): List of columns to check for duplicates.
#                                           If None, checks for duplicates across all columns.
#         """
#         if self.data is None:
#             raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

#         # Count duplicates
#         duplicate_count = self.data.duplicated(subset=subset).sum()
#         print(f"Number of duplicate rows found: {duplicate_count}")

#         # Remove duplicates
#         self.data = self.data.drop_duplicates(subset=subset, keep='first').reset_index(drop=True)
#         print("Duplicate rows have been removed.")

#     def clean_data(self) -> None:
#         """
#         Clean and process the loaded data.
#         """
#         if self.data is None:
#             raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

#         # Step 1: Check and remove duplicates
#         self.check_duplicates()

#         # Step 2: Drop irrelevant columns
#         columns_to_drop: List[str] = [
#             "_tags",
#             "_notes",
#             "_duration",
#             "_id",
#             "_uuid",
#             "meta/instanceID",
#             "_submission_time",
#             "_date_modified",
#             "_version",
#             "_submitted_by",
#             "_total_media",
#             "_media_count",
#             "_media_all_received",
#             "_xform_id",
#         ]
#         self.data.drop(columns=columns_to_drop, errors="ignore", inplace=True)

#         # Rename columns for consistency
#         self.data.rename(
#             columns={
#                 "today": "Date",
#                 "STATELABEL": "State",
#                 "lgalabel": "LGA",
#                 "g_consent/Section_A/market_type": "Outlet Type",
#                 "_gps_latitude": "Latitude",
#                 "_gps_longitude": "Longitude",
#                 "sector": "Sector",
#                 "VC_ID": "Contributor_ID",
#             },
#             inplace=True,
#         )

#         # Add default country
#         self.data["Country"] = "Nigeria"

#         # Map food items to their respective columns
#         food_mapping: Dict[str, Dict[str, str]] = {
#             "g_consent/Section_B1/maize_yellow": {
#                 "uom": "g_consent/Section_B1/uom_Ymaize",
#                 "quantity": "g_consent/Section_B1/Q_Ymaize",
#                 "price": "g_consent/Section_B1/price_Ymaize",
#             },
#             "g_consent/Section_B2/maize_white": {
#                 "uom": "g_consent/Section_B2/uom_Wmaize",
#                 "quantity": "g_consent/Section_B2/Q_Wmaize",
#                 "price": "g_consent/Section_B2/price_Wmaize",
#             },
#             "g_consent/Section_B3/sorghum": {
#                 "uom": "g_consent/Section_B3/uom_sorghum",
#                 "quantity": "g_consent/Section_B3/Q_sorghum",
#                 "price": "g_consent/Section_B3/price_sorghum",
#             },
#             "g_consent/Section_B4/imported_rice": {
#                 "uom": "g_consent/Section_B4/uom_imported_rice",
#                 "quantity": "g_consent/Section_B4/Q_rice",
#                 "price": "g_consent/Section_B4/price_imported_rice",
#             },
#             "g_consent/Section_B5/local_rice": {
#                 "uom": "g_consent/Section_B5/uom_local_rice",
#                 "quantity": "g_consent/Section_B5/Q_local_rice",
#                 "price": "g_consent/Section_B5/price_local_rice",
#             },
#             "g_consent/Section_B6/brown_beans": {
#                 "uom": "g_consent/Section_B6/uom_brownbeans",
#                 "quantity": "g_consent/Section_B6/Q_brownbeans",
#                 "price": "g_consent/Section_B6/price_brown_beans",
#             },
#             "g_consent/Section_B7/White_beans": {
#                 "uom": "g_consent/Section_B7/uom_whitebeans",
#                 "quantity": "g_consent/Section_B7/Q_whitebeans",
#                 "price": "g_consent/Section_B7/price_White_beans",
#             },
#             "g_consent/Section_B8/garri_confirm": {
#                 "uom": "g_consent/Section_B8/uom_garri",
#                 "quantity": "g_consent/Section_B8/Q_garri",
#                 "price": "g_consent/Section_B8/price_garri",
#             },
#             "g_consent/Section_B9/yam_confirm": {
#                 "uom": "g_consent/Section_B9/uom_yam",
#                 "quantity": "g_consent/Section_B9/Q_yam",
#                 "price": "g_consent/Section_B9/price_yam",
#             },
#             "g_consent/Section_B10/Soyabeans": {
#                 "uom": "g_consent/Section_B10/uom_soyabeans",
#                 "quantity": "g_consent/Section_B10/Q_soyabeans",
#                 "price": "g_consent/Section_B10/price_soyabeans",
#             },
#         }

#         # Prepare long-format data
#         long_format_data: List[pd.DataFrame] = []
#         for food_col, mapping in food_mapping.items():
#             uom_col = mapping["uom"]
#             quantity_col = mapping["quantity"]
#             price_col = mapping["price"]

#             if all(col in self.data.columns for col in [uom_col, quantity_col, price_col]):
#                 temp_df = self.data[
#                     [
#                         "Date",
#                         "State",
#                         "Contributor_ID",
#                         "LGA",
#                         "Outlet Type",
#                         "Latitude",
#                         "Longitude",
#                         "Country",
#                         "Sector",
#                     ]
#                 ].copy()
#                 temp_df["Food Item"] = food_col.split("/")[-1].replace("_", " ").capitalize()
#                 temp_df["UOM"] = self.data[uom_col].astype(str)
#                 temp_df["Quantity"] = pd.to_numeric(self.data[quantity_col], errors="coerce")
#                 temp_df["Price"] = pd.to_numeric(self.data[price_col], errors="coerce")

#                 # Calculate weight as Quantity * UOM (numeric part)
#                 temp_df["Weight"] = temp_df["Quantity"] * temp_df["UOM"].str.extract(r"(\d+\.?\d*)")[0].astype(float)

#                 # Calculate unit price
#                 temp_df["UPRICE"] = (temp_df["Price"] / temp_df["Weight"]).round(2)
#                 temp_df["Price Category"] = self.data.get("g_consent/Section_A/price_category", None)

#                 # Clean outlet type
#                 temp_df["Outlet Type"] = temp_df["Outlet Type"].str.replace("_", " ", regex=False)

#                 # Rename "yam confirm" to "yam" and "garri confirm" to "garri"
#                 temp_df["Food Item"] = temp_df["Food Item"].replace({"Yam confirm": "Yam", "Garri confirm": "Garri"})

#                 long_format_data.append(temp_df)

#                 # Create Contributor_State_ID
#                 temp_df["Contributor_State_ID"] = temp_df["State"] + "_" + temp_df["Contributor_ID"].astype(str)

#         # Combine the cleaned data
#         if long_format_data:
#             self.data = pd.concat(long_format_data, ignore_index=True)
#         else:
#             raise ValueError("No valid data found to clean.")

#         # Reorder columns
#         column_order = [
#             "Date",
#             "State",
#             "Contributor_ID",
#             "LGA",
#             "Outlet Type",
#             "Latitude",
#             "Longitude",
#             "Country",
#             "Sector",
#             "Food Item",
#             "UOM",
#             "Quantity",
#             "Price Category",
#             "Price",
#             "Weight",
#             "UPRICE",
#             "Contributor_State_ID",
#         ]
#         self.data = self.data[column_order]

#         # Print missing values count and percentage
#         missing_count = self.data.isna().sum()
#         total_rows = len(self.data)
#         missing_percentage = (missing_count / total_rows) * 100

#         print("Missing values summary (counts and percentages):")
#         print(pd.DataFrame({
#             "Missing Count": missing_count,
#             "Missing Percentage (%)": missing_percentage.round(2)
#         }))

#         # Print summary statistics
#         print("\nSummary statistics of the dataset:")
#         print(self.data.describe().transpose())

#         # Convert 'Date' to datetime
#         self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")

#         # Drop rows with missing essential values
#         essential_cols = [
#             "State",
#             "LGA",
#             "Date",
#             "Food Item",
#             "UPRICE",
#             "UOM",
#             "Quantity",
#             "Price",
#             "Weight",
#             "Latitude",
#             "Longitude",
#         ]
#         self.data.dropna(subset=essential_cols, inplace=True)

#         # Add Total Records Captured (TRC) column
#         trc_summary = self.data.groupby("Contributor_State_ID").size().reset_index(name="TRC")
#         self.data = self.data.merge(trc_summary, on="Contributor_State_ID", how="left")

#     def apply_uprice_bands(self) -> None:
#         """
#         Filter the dataset to retain only rows with UPRICE within the defined bands for each food item.
#         Separates invalid records into a different DataFrame.
#         """
#         # Define the lower and upper bands for each food item
#         uprice_bands = {
#              "Brown beans": (1489.70, 3081.72),
#              "White beans": (1489.70, 3081.72),
#              "Garri": (578.89, 1135.39),
#              "Local rice": (1200.00, 3500.00),
#              "Imported rice": (1500.00, 3628.70),
#              "Maize white": (500.00, 3600.00),
#              "Maize yellow": (500.00, 3600.00),
#              "Sorghum": (628.00, 2100.00),
#              "Soyabeans": (1200.00, 3000.00),
#              "Yam": (1100.00, 3500.00),
#         }

#         # Initialize lists for valid and invalid rows
#         valid_data = []
#         invalid_data = []

#         for food_item, (lower_band, upper_band) in uprice_bands.items():
#             # Select valid rows for the current food item
#             valid_rows = self.data[
#                 (self.data["Food Item"] == food_item)
#                 & (self.data["UPRICE"] >= lower_band)
#                 & (self.data["UPRICE"] <= upper_band)
#             ]

#             # Select invalid rows for the current food item
#             invalid_rows = self.data[
#                 (self.data["Food Item"] == food_item)
#                 & ~((self.data["UPRICE"] >= lower_band) & (self.data["UPRICE"] <= upper_band))
#             ]

#             # Append to respective lists
#             valid_data.append(valid_rows)
#             invalid_data.append(invalid_rows)

#         # Combine all valid and invalid rows into separate DataFrames
#         self.data = pd.concat(valid_data, ignore_index=True)  # Valid records
#         self.invalid_data = pd.concat(invalid_data, ignore_index=True)  # Invalid records

#         print(f"Valid records retained: {self.data.shape[0]}")
#         print(f"Invalid records separated: {self.invalid_data.shape[0]}")


#     def save_cleaned_data(self) -> None:
#         """
#         Save the cleaned data to the specified output file.
#         """
#         if self.data is None:
#             raise ValueError("No cleaned data available to save. Run `clean_data()` first.")

#         self.data.to_csv(self.output_filepath, index=False)
#         print(f"Cleaned data saved to {self.output_filepath}")

#     def save_invalid_data(self, invalid_filepath: str = "invalid_records.csv") -> None:
#         """
#         Save the invalid data to a separate file.
#         """
#         if self.invalid_data is None:
#             raise ValueError("No invalid data available. Run `apply_uprice_bands()` first.")

#         self.invalid_data.to_csv(invalid_filepath, index=False)
#         print(f"Invalid data saved to {invalid_filepath}")


import pandas as pd
from typing import Optional, Dict, List


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
        self.data: Optional[pd.DataFrame] = None
        self.invalid_data: Optional[pd.DataFrame] = None
        self.cleaning_log: List[str] = []

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

    def check_duplicates(self, subset: Optional[List[str]] = None) -> None:
        """
        Check for and remove duplicate rows in the dataset.

        Args:
            subset (Optional[List[str]]): List of columns to check for duplicates.
                                          If None, checks for duplicates across all columns.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

        duplicate_count = self.data.duplicated(subset=subset).sum()
        print(f"Number of duplicate rows found: {duplicate_count}")

        self.data = self.data.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)
        print("Duplicate rows have been removed.")

    def clean_data(self) -> None:
        """
        Clean and process the loaded data.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Use `load_data()` to load the data first.")

        self.check_duplicates()

        columns_to_drop: List[str] = [
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

        self.data.rename(
            columns={
                "today": "Date",
                "STATELABEL": "State",
                "lgalabel": "LGA",
                "g_consent/Section_A/market_type": "Outlet Type",
                "_gps_latitude": "Latitude",
                "_gps_longitude": "Longitude",
                "sector": "Sector",
                "VC_ID": "Contributor_ID",
            },
            inplace=True,
        )

        self.data["Country"] = "Nigeria"

        food_mapping: Dict[str, Dict[str, str]] = {
            "g_consent/Section_B1/maize_yellow": {
                "uom": "g_consent/Section_B1/uom_Ymaize",
                "quantity": "g_consent/Section_B1/Q_Ymaize",
                "price": "g_consent/Section_B1/price_Ymaize",
            },
            "g_consent/Section_B2/maize_white": {
                "uom": "g_consent/Section_B2/uom_Wmaize",
                "quantity": "g_consent/Section_B2/Q_Wmaize",
                "price": "g_consent/Section_B2/price_Wmaize",
            },
            "g_consent/Section_B3/sorghum": {
                "uom": "g_consent/Section_B3/uom_sorghum",
                "quantity": "g_consent/Section_B3/Q_sorghum",
                "price": "g_consent/Section_B3/price_sorghum",
            },
            "g_consent/Section_B4/imported_rice": {
                "uom": "g_consent/Section_B4/uom_imported_rice",
                "quantity": "g_consent/Section_B4/Q_rice",
                "price": "g_consent/Section_B4/price_imported_rice",
            },
            "g_consent/Section_B5/local_rice": {
                "uom": "g_consent/Section_B5/uom_local_rice",
                "quantity": "g_consent/Section_B5/Q_local_rice",
                "price": "g_consent/Section_B5/price_local_rice",
            },
            "g_consent/Section_B6/brown_beans": {
                "uom": "g_consent/Section_B6/uom_brownbeans",
                "quantity": "g_consent/Section_B6/Q_brownbeans",
                "price": "g_consent/Section_B6/price_brown_beans",
            },
            "g_consent/Section_B7/White_beans": {
                "uom": "g_consent/Section_B7/uom_whitebeans",
                "quantity": "g_consent/Section_B7/Q_whitebeans",
                "price": "g_consent/Section_B7/price_White_beans",
            },
            "g_consent/Section_B8/garri_confirm": {
                "uom": "g_consent/Section_B8/uom_garri",
                "quantity": "g_consent/Section_B8/Q_garri",
                "price": "g_consent/Section_B8/price_garri",
            },
            "g_consent/Section_B9/yam_confirm": {
                "uom": "g_consent/Section_B9/uom_yam",
                "quantity": "g_consent/Section_B9/Q_yam",
                "price": "g_consent/Section_B9/price_yam",
            },
            "g_consent/Section_B10/Soyabeans": {
                "uom": "g_consent/Section_B10/uom_soyabeans",
                "quantity": "g_consent/Section_B10/Q_soyabeans",
                "price": "g_consent/Section_B10/price_soyabeans",
            },
        }

        long_format_data: List[pd.DataFrame] = []
        for food_col, mapping in food_mapping.items():
            uom_col = mapping["uom"]
            quantity_col = mapping["quantity"]
            price_col = mapping["price"]

            if all(col in self.data.columns for col in [uom_col, quantity_col, price_col]):
                temp_df = self.data[
                    [
                        "Date",
                        "State",
                        "Contributor_ID",
                        "LGA",
                        "Outlet Type",
                        "Latitude",
                        "Longitude",
                        "Country",
                        "Sector",
                    ]
                ].copy()
                temp_df["Food Item"] = food_col.split("/")[-1].replace("_", " ").capitalize()
                temp_df["UOM"] = self.data[uom_col].astype(str)
                temp_df["Quantity"] = pd.to_numeric(self.data[quantity_col], errors="coerce")
                temp_df["Price"] = pd.to_numeric(self.data[price_col], errors="coerce")

                temp_df["Weight"] = temp_df["Quantity"] * temp_df["UOM"].str.extract(r"(\d+\.?\d*)")[0].astype(float)
                temp_df["UPRICE"] = (temp_df["Price"] / temp_df["Weight"]).round(2)
                temp_df["Price Category"] = self.data.get("g_consent/Section_A/price_category", None)

                temp_df["Outlet Type"] = temp_df["Outlet Type"].str.replace("_", " ", regex=False)
                temp_df["Food Item"] = temp_df["Food Item"].replace({"Yam confirm": "Yam", "Garri confirm": "Garri"})

                long_format_data.append(temp_df)
                temp_df["Contributor_State_ID"] = temp_df["State"] + "_" + temp_df["Contributor_ID"].astype(str)

        if long_format_data:
            self.data = pd.concat(long_format_data, ignore_index=True)
        else:
            raise ValueError("No valid data found to clean.")

        column_order = [
            "Date",
            "State",
            "Contributor_ID",
            "LGA",
            "Outlet Type",
            "Latitude",
            "Longitude",
            "Country",
            "Sector",
            "Food Item",
            "UOM",
            "Quantity",
            "Price Category",
            "Price",
            "Weight",
            "UPRICE",
            "Contributor_State_ID",
        ]
        self.data = self.data[column_order]

        missing_count = self.data.isna().sum()
        total_rows = len(self.data)
        missing_percentage = (missing_count / total_rows) * 100

        print("Missing values summary (counts and percentages):")
        print(pd.DataFrame({"Missing Count": missing_count, "Missing Percentage (%)": missing_percentage.round(2)}))

        print("\nSummary statistics of the dataset:")
        print(self.data.describe().transpose())

        self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")

        essential_cols = [
            "State",
            "LGA",
            "Date",
            "Food Item",
            "UPRICE",
            "UOM",
            "Quantity",
            "Price",
            "Weight",
            "Latitude",
            "Longitude",
        ]
        self.data.dropna(subset=essential_cols, inplace=True)

    def apply_uprice_bands(self) -> None:
        """
        Filter the dataset to retain only rows with UPRICE within the defined bands for each food item.
        """
        if self.data is None:
            raise ValueError("Data is not loaded. Run `clean_data()` first.")

        uprice_bands = {
            "Brown beans": (1489.70, 3081.72),
            "White beans": (1489.70, 3081.72),
            "Garri": (578.89, 1135.39),
            "Local rice": (1200.00, 3500.00),
            "Imported rice": (1500.00, 3628.70),
            "Maize white": (500.00, 3600.00),
            "Maize yellow": (500.00, 3600.00),
            "Sorghum": (628.00, 2100.00),
            "Soyabeans": (1100.00, 3000.00),
            "Yam": (1100.00, 3500.00),
        }

        valid_data = []
        invalid_data = []

        for food_item, (lower_band, upper_band) in uprice_bands.items():
            valid_rows = self.data[
                (self.data["Food Item"] == food_item)
                & (self.data["UPRICE"] >= lower_band)
                & (self.data["UPRICE"] <= upper_band)
            ]

            invalid_rows = self.data[
                (self.data["Food Item"] == food_item)
                & ~((self.data["UPRICE"] >= lower_band) & (self.data["UPRICE"] <= upper_band))
            ]

            valid_data.append(valid_rows)
            invalid_data.append(invalid_rows)

        self.data = pd.concat(valid_data, ignore_index=True)
        self.invalid_data = pd.concat(invalid_data, ignore_index=True)

        print(f"Valid records retained: {self.data.shape[0]}")
        print(f"Invalid records separated: {self.invalid_data.shape[0]}")

    def count_submissions_per_contributor(self, output_filepath: str = "contributor_details.csv") -> None:
        """
        Count the number of rows submitted by each contributor (VC_ID).
        """
        if self.input_filepath is None:
            raise ValueError("Input file path is not specified.")

        try:
            raw_data = pd.read_csv(self.input_filepath)
            print("Raw data reloaded successfully.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{self.input_filepath}' was not found.")
        except pd.errors.EmptyDataError:
            raise ValueError("Error: The file is empty.")
        except Exception as e:
            raise Exception(f"An error occurred while loading raw data: {e}")

        rename_mapping = {
            "g_consent/Section_A/market_type": "Outlet Type",
            "g_consent/Section_A/price_category": "Price Category",
            "g_consent/seller_phone": "PhoneNumber",
            "_gps_latitude": "Latitude",
            "_gps_longitude": "Longitude",
            "_gps_precision": "Accuracy",
            "g_consent/Section_B1/maize_yellow": "Maize Yellow",
            "g_consent/Section_B2/maize_white": "Maize White",
            "g_consent/Section_B3/sorghum": "Sorghum",
            "g_consent/Section_B4/imported_rice": "Imported Rice",
            "g_consent/Section_B5/local_rice": "Local Rice",
            "g_consent/Section_B6/brown_beans": "Brown Beans",
            "g_consent/Section_B7/White_beans": "White Beans",
            "g_consent/Section_B8/garri_confirm": "Garri",
            "g_consent/Section_B9/yam_confirm": "Yam",
            "g_consent/Section_B10/Soyabeans": "Soyabeans",
        }
        raw_data.rename(columns=rename_mapping, inplace=True)

        additional_columns = [
            "today",
            "_submission_time",
            "timeStart",
            "STATELABEL",
            "lgalabel",
            "sector",
            "Outlet Type",
            "Price Category",
            "Maize Yellow",
            "Maize White",
            "Sorghum",
            "Imported Rice",
            "Local Rice",
            "Brown Beans",
            "White Beans",
            "Garri",
            "Yam",
            "Soyabeans",
            "PhoneNumber",
            "Latitude",
            "Longitude",
            "Accuracy",
            "_id",
            "_version",
        ]

        valid_columns = [col for col in additional_columns if col in raw_data.columns]
        if valid_columns:
            submission_details = raw_data[["VC_ID"] + valid_columns].drop_duplicates()
            submission_details.to_csv(output_filepath, index=False)
            print(f"Contributor details have been saved to '{output_filepath}'")
        else:
            print("No valid additional columns found in the raw dataset.")

    def save_cleaned_data(self) -> None:
        """
        Save the cleaned data to the specified output file.
        """
        if self.data is None:
            raise ValueError("No cleaned data available to save. Run `clean_data()` first.")

        self.data.to_csv(self.output_filepath, index=False)
        print(f"Cleaned data saved to {self.output_filepath}")

    def save_invalid_data(self, invalid_filepath: str = "invalid_records.csv") -> None:
        """
        Save the invalid data to a separate file.
        """
        if self.invalid_data is None:
            raise ValueError("No invalid data available. Run `apply_uprice_bands()` first.")

        self.invalid_data.to_csv(invalid_filepath, index=False)
        print(f"Invalid data saved to {invalid_filepath}")
