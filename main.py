# from src.nbsfoodpricecleaner.data_cleaner import NBSFoodPriceCleaner

# def main():
#     # Initialize the cleaner with input and output file paths
#     cleaner = NBSFoodPriceCleaner(
#         input_filepath=r"D:\gigs\nbs\NBS_Crowdsource_Food_Price_Form_DEC2nd.csv",  # Replace with the actual raw data CSV path
#         output_filepath="cleaned_data_2.csv"
#     )

#     # Load the raw data
#     print("Loading data...")
#     cleaner.load_data()

#     # Clean the data
#     print("Cleaning data...")
#     cleaner.clean_data()

#     # Save the cleaned data
#     print("Saving cleaned data...")
#     cleaner.save_cleaned_data()

#     print("Data cleaning process completed successfully!")

# if __name__ == "__main__":
#     main()


# from src.nbsfoodpricecleaner.data_cleaner import NBSFoodPriceCleaner

# def main():
#     # Initialize the cleaner with input and output file paths
#     cleaner = NBSFoodPriceCleaner(
#         input_filepath=r"D:\gigs\nbs\NBS_Crowdsource_Food_Price_Form_DEC2nd.csv",  # Replace with the actual raw data CSV path
#         output_filepath="cleaned_data_2.csv"
#     )

#     # Load the raw data
#     print("Loading data...")
#     cleaner.load_data()

#     # Clean the data
#     print("Cleaning data...")
#     cleaner.clean_data()

#     # Apply UPRICE bands to filter valid and invalid data
#     print("Applying UPRICE bands...")
#     cleaner.apply_uprice_bands()

#     # Save the cleaned data
#     print("Saving cleaned data...")
#     cleaner.save_cleaned_data()

#     # Save the invalid data
#     print("Saving invalid data...")
#     cleaner.save_invalid_data("invalid_records_2.csv")

#     print("Data cleaning process completed successfully!")

# if __name__ == "__main__":
#     main()

from src.nbsfoodpricecleaner.data_cleaner import NBSFoodPriceCleaner

def main():
    # Initialize the cleaner with input and output file paths
    cleaner = NBSFoodPriceCleaner(
        input_filepath=r"D:\gigs\nbs\raw_data\NBS_Crowdsource_Food_Price_Form_30TH NOV.csv",  # Replace with the actual raw data CSV path
        output_filepath=r"D:\gigs\nbs\cleaned_data\cleaned_data_nov30.csv"
    )

    # Load the raw data
    print("Loading data...")
    cleaner.load_data()

    # Clean the data
    print("Cleaning data...")
    cleaner.clean_data()

    # Apply UPRICE bands to filter valid and invalid data
    print("Applying UPRICE bands...")
    cleaner.apply_uprice_bands()

    # Save the cleaned data
    print("Saving cleaned data...")
    cleaner.save_cleaned_data()

    # Save the invalid data
    print("Saving invalid data...")
    cleaner.save_invalid_data(r"D:\gigs\nbs\cleaned_data\invalid_records_nov30.csv")

    # Generate and save submission details to a specified file
    print("Generating contributor details...")
    cleaner.count_submissions_per_contributor(output_filepath=r"D:\gigs\nbs\cleaned_data\contributor_details_nov30.csv")

    print("Data cleaning process completed successfully!")

if __name__ == "__main__":
    main()


