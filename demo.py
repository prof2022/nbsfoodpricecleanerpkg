from nbsfoodpricecleaner import data_cleaner as dc  

if __name__ == "__main__":
    # File paths
    input_filepath = r"D:\gigs\nbs\raw_data\NBS_Crowdsource_Food_Price_Form_8th JAN.csv"
    output_filepath = "cleaned_nbs_data.csv"
    invalid_filepath = "invalid_records.csv"
    contributor_details_filepath = "contributor_details.csv"
    
    print("Initializing NBS Food Price Cleaner...")
    cleaner = dc.NBSFoodPriceCleaner(input_filepath=input_filepath, output_filepath=output_filepath)

    try:
        print("\nLoading data...")
        cleaner.load_data()
        print("Data loaded successfully.")
        
        print("\nCleaning data...")
        cleaner.clean_data()
        print("Data cleaned successfully.")
        
        print("\nSaving cleaned data...")
        cleaner.save_cleaned_data()
        print(f"Cleaned data saved to {output_filepath}")
    
    
    except Exception as e:
        print(f"An error occurred: {e}")
