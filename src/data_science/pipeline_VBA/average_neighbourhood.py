# Import necessary libraries
import csv_excel_operations as ceo
import os
import numpy as np
import pandas as pd

# Define dataset path
current_directory = os.getcwd()
parent_directory = os.path.dirname(os.path.dirname(current_directory))
parent_directory_without_src = os.path.normpath(os.path.join(parent_directory, '..'))

file_path_dataset = os.path.join(parent_directory_without_src, 'data\\airbnb2023\\airbnb2023_clean.csv')
file_path_output = os.path.join(parent_directory_without_src, 'VBA\\average_neighbourhood.csv')

# Read dataset
dataset = pd.read_csv(file_path_dataset)

# Extract unique neighbourhood names
neighbourhood_name = dataset["neighbourhood_cleansed"].unique()

# Display neighbourhood names
print("Voici le nom de tous les arrondissements: \n", neighbourhood_name)
print("Il y en a ", len(neighbourhood_name), ".")

# Create a dataframe to store neighbourhood names and their corresponding average prices
average_neighbourhood = pd.DataFrame({'neighbourhood_name': neighbourhood_name})
average = np.array([])

# Calculate and display the average price for each neighbourhood
for name in neighbourhood_name:
    print("Dans le quartier", name, ", le prix moyen d'un logement airBNB est", ceo.average_price_neighborhood(dataset, name))
    average = np.append(average, round(ceo.average_price_neighborhood(dataset, name), 2))

# Add the 'average' column to the dataframe
average_neighbourhood['average'] = average

# Sort the dataframe based on the 'average' column
average_neighbourhood = average_neighbourhood.sort_values("average")

# Save the result to a CSV file
average_neighbourhood.to_csv(file_path_output, sep=';', index=False)
