import os
import requests
import pandas as pd

# define parameters
site_number = "14144700"  # Columbia River at Vancouver, WA
start_date = "1994-01-01"
end_date = "2024-12-31"

# specify the save directory
save_directory = "C:/Users/ander/OneDrive - Oregon State University/Classes/2025/Winter/CS512/HW/Final Project"

# create the directory if it doesn't exist
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

# base URL for NWIS API (for discharge data)
base_url = f"https://waterservices.usgs.gov/nwis/iv/?site={site_number}&startDT={start_date}&endDT={end_date}&format=rdb"

# send the request to the USGS API
response = requests.get(base_url)

# check if the request was successful
if response.status_code == 200:
    # save the response to a text file in the specified directory
    response_file_path = os.path.join(save_directory, 'ColumbiaRiver_Vancouver_data.txt')
    with open(response_file_path, 'w') as file:
        file.write(response.text)
    
    # read the data into a pandas DataFrame (skip metadata lines)
    data = pd.read_csv(response_file_path, comment='#', delimiter='\t')
    
    # save the data to CSV in the specified directory
    csv_file_path = os.path.join(save_directory, "ColumbiaRiver_Vancouver_data.csv")
    data.to_csv(csv_file_path, index=False)

    print(f"Data saved successfully to {csv_file_path}!")
else:
    print(f"Error: {response.status_code} - {response.text}")
