from src.nbsfoodpricecleaner.data_cleaner import NBSFoodPriceCleaner

def main():
    # Initialize the cleaner with input and output file paths
    cleaner = NBSFoodPriceCleaner(
        input_filepath=r"D:\gigs\nbs\NBS_Crowdsource_Food_Price_Form_27th.csv",  # Replace with the actual raw data CSV path
        output_filepath="cleaned_data.csv"
    )

    # Load the raw data
    print("Loading data...")
    cleaner.load_data()

    # Clean the data
    print("Cleaning data...")
    cleaner.clean_data()

    # Save the cleaned data
    print("Saving cleaned data...")
    cleaner.save_cleaned_data()

    print("Data cleaning process completed successfully!")

if __name__ == "__main__":
    main()
