# this script is used to inspect the column names of the CSV files downloaded from the NOAA Storm Events Database
# it is used to determine the column names and data types for the subsequent data processing steps
# heres the link to the database https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/

import pandas as pd
import glob

# Path to your folder containing downloaded CSV files
file_path = "C:\\Users\\ander\\OneDrive - Oregon State University\\Classes\\2025\\Winter\\CS512\\HW\\Final Project\\StormEvents*.csv"

# Use glob to match all CSV files in the folder
csv_files = glob.glob(file_path)

# Debugging: Check the list of matched files
print("CSV files found:", csv_files)

# Load the first file and check the column names
df = pd.read_csv(csv_files[0])

# Print the column names to inspect
print(df.columns)

