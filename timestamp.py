import os
from datetime import datetime

# Path to save the timestamp CSV file
timestamp_csv_path = 'CONNECTED_DATA/timestamp.csv'

# Create the CONNECTED_DATA folder if it doesn't exist
os.makedirs('CONNECTED_DATA', exist_ok=True)

# Get the current timestamp
current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Write the timestamp to a new CSV file
with open(timestamp_csv_path, mode='w', newline='') as timestamp_file:
    # Define field name for timestamp
    timestamp_file.write("Timestamp\n")  # Write the header
    timestamp_file.write(f"{current_timestamp}\n")  # Write the current timestamp

print(f'Timestamp has been saved to {timestamp_csv_path}.')
