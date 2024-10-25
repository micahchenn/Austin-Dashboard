import os
import json
import pandas as pd

# Define the directory to save CSVs and the directory where JSONs are stored
csv_directory = "CSV_Data"
json_directory = "API_Data"
combined_csv_file = "combined_data.csv"  # Combined CSV output file

# Create the CSV directory if it doesn't exist
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Initialize an empty list to store DataFrames
df_list = []

# Loop through each JSON file in the directory
for json_file in os.listdir(json_directory):
    if json_file.endswith('_pm_data.json'):
        # Extract the alias and date range from the filename
        parts = json_file.split('_')
        
        # Check if the file has enough parts to extract alias and date range
        if len(parts) >= 3:
            alias = "_".join(parts[:-2])  # Join all but the last two parts for the alias
            date_range = parts[-2]  # The second last part is the date range (e.g., Month, Week)

            # Step 1: Load the JSON data from the file
            json_path = os.path.join(json_directory, json_file)
            with open(json_path, 'r') as file:
                data = json.load(file)

            # Step 2: Normalize the JSON data
            df = pd.json_normalize(data)

            # Remove unwanted suffix if it exists in the data
            if 'alias' in df.columns:
                df['alias'] = df['alias'].str.replace('pm', '', regex=False)  # Remove 'Pm' if it exists

            # Add a column for the alias to differentiate the rows in the combined file
            df['alias'] = alias

            # Add a column for the date range used
            df['date_range'] = date_range.capitalize()  # Capitalize the date range for consistency

            # Step 3: Save the DataFrame to a CSV file, using the alias and date range as the filename
            csv_path = os.path.join(csv_directory, f'{alias}_{date_range}_data.csv')
            df.to_csv(csv_path, index=False)

            print(f"Successfully extracted {alias} JSON data to {csv_path}")

            # Add the DataFrame to the list for combining later
            df_list.append(df)

# Step 4: Combine all DataFrames into one
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)

    # Remove unwanted suffix from combined DataFrame if necessary
    if 'alias' in combined_df.columns:
        combined_df['alias'] = combined_df['alias'].str.replace('Pm', '', regex=False)  # Clean up 'Pm' if it exists

    # Step 5: Save the combined DataFrame to a single CSV file
    combined_df.to_csv(combined_csv_file, index=False)
    print(f"Successfully combined all CSV files into {combined_csv_file}")
else:
    print("No data to combine.")
