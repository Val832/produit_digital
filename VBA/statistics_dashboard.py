import pandas as pd

def calculate_average_price(data_path, neighbourhood_cleansed):
    """
    Calculate the average price for a specified neighbourhood_cleansed.

    Parameters:
    - data_path (str): The path to the CSV file.
    - neighbourhood_cleansed (str): The specific neighbourhood_cleansed for filtering.

    Returns:
    - float: The average price for the specified neighbourhood_cleansed.
    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(data_path)

    # Filter the DataFrame based on the specified neighbourhood_cleansed
    filtered_df = df[df['neighbourhood_cleansed'] == neighbourhood_cleansed]

    # Calculate the average price for the filtered DataFrame
    average_price = filtered_df['price'].mean()

    return average_price

# Example usage
csv_path = r'C:\Users\garan\Desktop\produit_digital\data\airbnb2023\airbnb2023_clean.csv'
neighbourhood_to_check = 'MÃ©nilmontant'  # Replace with the desired neighbourhood

# Call the function to calculate the average price for the specified neighbourhood
result = calculate_average_price(csv_path, neighbourhood_to_check)

# Print the result
print(f"Average price for {neighbourhood_to_check} (for one night): {result}")