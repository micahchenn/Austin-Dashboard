import pandas as pd
import json
import os
from SETTINGS import PM_DATE_RANGE, SEGMENT_CONFIGS, PROBE_POLLING_INTERVAL

json_directory = 'API_Data/'
csv_directory = 'Cleaning_Data/'
combined_csv_file = 'Connected_Data/combined_PM_data.csv'



'''


'''





# Create the CSV directory if it doesn't exist
if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)

# Initialize an empty list to store DataFrames
df_list = []

# Loop through each JSON file in the directory
for json_file in os.listdir(json_directory):
    if json_file.endswith('pm_data.json'):
        # Extract the alias from the filename (removing .json extension)
        alias = os.path.splitext(json_file)[0]
        
        # Step 1: Load the JSON data from the file
        json_path = os.path.join(json_directory, json_file)
        with open(json_path, 'r') as file:
            data = json.load(file)
        
        # Step 2: Normalize the JSON data
        df = pd.json_normalize(data)

        # Add a column for the alias to differentiate the rows in the combined file
        df['alias'] = alias

        # Add the DataFrame to the list
        df_list.append(df)

        # Step 3: Save the DataFrame to a CSV file, using the alias as the filename
        csv_path = os.path.join(csv_directory, f'{alias}_data.csv')
        df.to_csv(csv_path, index=False)

        print(f"Successfully extracted {alias} JSON data to {csv_path}")



# Step 4: Combine all DataFrames into one
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True)

    # Step 5: Save the combined DataFrame to a single CSV file
    combined_df.to_csv(combined_csv_file, index=False)
    print(f"Successfully combined all CSV files into {combined_csv_file}")
else:
    print("No data to combine.")






import zipfile

# Define the paths
zip_file_path = 'API_Data/probe_data.zip'  # Path to the ZIP file
destination_folder = 'Connected_Data'  # Path to the folder where you want to extract the files

# Create the destination folder if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Extract the ZIP file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(destination_folder)

print(f'Extracted {zip_file_path} to {destination_folder}')
