import csv
import os
from SETTINGS import SEGMENT_CONFIGS  # Import the segment configurations from settings.py
import pandas as pd

# Path to save the CSV file
output_csv_path = 'CONNECTED_DATA/tmc_segments_summary.csv'

# Create the CONNECTED_DATA folder if it doesn't exist
os.makedirs('CONNECTED_DATA', exist_ok=True)

# Summarize data and write to CSV
with open(output_csv_path, mode='w', newline='') as csv_file:
    fieldnames = ['Alias Name', 'TMC ID']  # Updated column names
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    # Write header
    writer.writeheader()

    # Write segment data
    for config in SEGMENT_CONFIGS:
        alias = config["alias"]
        tmc_ids = config["tmc_ids"]
        for tmc_id in tmc_ids:
            writer.writerow({'Alias Name': alias, 'TMC ID': tmc_id})  # Updated column names

print(f'Summary of TMC segments has been saved to {output_csv_path}.')



# Path to the combined data CSV file
input_csv_path = 'CONNECTED_DATA/combined_PM_data.csv'
output_csv_path = 'CONNECTED_DATA/combined_PM_data_time.csv'
import pandas as pd
import numpy as np


# Function to convert minutes (0-1440) to time string (e.g., 1:00 AM)
def convert_minutes_to_time(minutes):
    if pd.isna(minutes):  # Skip conversion if the value is NaN
        return np.nan
    minutes = int(minutes)  # Convert to integer
    hours = minutes // 60
    mins = minutes % 60
    time_str = f'{hours:02d}:{mins:02d}'
    return pd.to_datetime(time_str, format='%H:%M').strftime('%I:%M %p')

# Step 1: Load the CSV file
df = pd.read_csv(input_csv_path)

# Step 2: Convert the 'interval' column to time format, handling NaN values
if 'interval' in df.columns:
    df['interval'] = df['interval'].apply(convert_minutes_to_time)
else:
    print("No 'interval' column found in the CSV file.")

# Step 3: Save the updated DataFrame to a new CSV file
df.to_csv(output_csv_path, index=False)
print(f"Successfully converted 'interval' to time and saved the file as {output_csv_path}")
