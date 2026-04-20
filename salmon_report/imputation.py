# Oregon State University
# CS 512 - Final Project
# Date: 2025/03/16
# Author: Paul J Anderson

# final scrub: KNN Imputation for Missing Data

# path to your folder containing downloaded CSV files
file_path = "C:\\Users\\ander\\OneDrive - Oregon State University\\Classes\\2025\\Winter\\CS512\\HW\\Final Project"

# specify the save directory
save_directory = "C:\\Users\\ander\\OneDrive - Oregon State University\\Classes\\2025\\Winter\\CS512\\HW\\Final Project"

import pandas as pd
from sklearn.impute import KNNImputer

# load your dataset (replace this with the actual path to your dataset)
df = pd.read_csv('final_data_scrubbed.csv')

# initialize the KNNImputer with the number of neighbors you want (e.g., 5)
imputer = KNNImputer(n_neighbors=5)

# select the columns you want to impute (e.g., 'mean_SAR', 'juvenile_return')
columns_to_impute = ['mean_SAR', 'juvenile_return']

# apply KNN Imputer to your selected columns
df[columns_to_impute] = imputer.fit_transform(df[columns_to_impute])

# now, df will have the missing values filled using KNN imputation
# save the output to a new CSV or proceed with further analysis
df.to_csv('imputed_dataset.csv', index=False)

# preview the imputed data
print(df.head())