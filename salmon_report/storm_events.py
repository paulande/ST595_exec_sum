import pandas as pd
import glob

# Path to your folder containing downloaded CSV files
file_path = "C:\\Users\\ander\\OneDrive - Oregon State University\\Classes\\2025\\Winter\\CS512\\HW\\Final Project\\StormEvents*.csv"

# Use glob to match all CSV files in the folder
csv_files = glob.glob(file_path)

# Create an empty list to store dataframes
all_data = []

# Load all CSV files into a list of DataFrames
for file in csv_files:
    df = pd.read_csv(file, low_memory=False)
    
    # Strip any leading/trailing whitespace from column names
    df.columns = df.columns.str.strip()

    # Append to the list of dataframes
    all_data.append(df)

# Concatenate all the dataframes in the list into a single dataframe
all_data = pd.concat(all_data, ignore_index=True)

# Filter data for flooding events and Oregon (state code is 'OR')
flooding_data = all_data[
    (all_data['EVENT_TYPE'] == 'Flood') & (all_data['STATE'] == 'OR')
]

# Filter data for events from 1994 to 2024 (based on the 'YEAR' column)
flooding_data = flooding_data[(flooding_data['YEAR'] >= 1994) & (flooding_data['YEAR'] <= 2024)]

# Display the first few rows of the filtered data
print(flooding_data.head())

# Optionally, save the filtered data to a new CSV
flooding_data.to_csv('oregon_flooding_events_1994_2024.csv', index=False)
