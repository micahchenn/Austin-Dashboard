import json
import pandas as pd
from SETTINGS import SEGMENT_CONFIGS
import os

def process_udc_file(alias_name):
    # Step 1: Open and load the JSON file
    file_path = f'API_Data/{alias_name}_udc_data.json'
    try:
        with open(file_path, 'r') as file:
            udc_data = json.load(file)
    except FileNotFoundError:
        print(f"File not found for {alias_name}. Skipping...")
        return None

    # Step 2: Normalize the nested JSON data
    udc_df = pd.json_normalize(
        udc_data['daily_results'], 
        record_path=['values'], 
        meta=['day', ['daily_totals', 'commercial', 'volume'], 
              ['daily_totals', 'passenger', 'volume'], 
              ['daily_totals', 'combined', 'volume']],
        errors='ignore'
    )

    # Step 3: Add a column with the alias name
    udc_df['alias'] = alias_name
    return udc_df

# Function to loop through all alias names, process files, and combine them
def process_and_combine_udc_files():
    combined_data = []  # List to store each alias DataFrame

    # Process each alias file and add to the combined list
    for segment_config in SEGMENT_CONFIGS:
        alias_name = segment_config['alias']
        udc_df = process_udc_file(alias_name)
        
        if udc_df is not None:  # Add the DataFrame to the list if it exists
            combined_data.append(udc_df)

    # Concatenate all DataFrames in the list
    if combined_data:
        combined_udc_df = pd.concat(combined_data, ignore_index=True)
        # Save the combined DataFrame to a single CSV file
        combined_udc_df.to_csv('Connected_Data/UDC_Combined_Data.csv', index=False)
        print("All UDC data has been successfully combined and saved to UDC_Combined_Data.csv")
    else:
        print("No data was processed. Please check your files.")

# Run the function to process and combine all files
process_and_combine_udc_files()