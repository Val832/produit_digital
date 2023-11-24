import gzip
import os
import shutil
import re
from collections import defaultdict
import ast
import requests
import pandas as pd 

from tqdm import tqdm

def create_column_from_match(df, reference_column, word=None, words_dictionnary=None):
    """
    This function creates one or more indicator columns in a pandas DataFrame 
    based on regex matching of words in a reference column.

    Parameters:
    ----------
    df : pd.DataFrame
        The DataFrame to perform the operation on.

    reference_column : str
        The name of the column in which to search for words.

    word : str, optional
        A single word to search for in the reference column. If provided, an indicator column 
        with this name will be added to the DataFrame.

    words_dictionnary : dict, optional
        A dictionary where each key-value pair consists of a column name and a corresponding word 
        or list of words to search for in the reference column. An indicator column for each key
        will be added to the DataFrame.

    Returns:
    --------
    df : pd.DataFrame
        The DataFrame with the new indicator columns added.

    Remarks:
    ----------
    - At least one of the 'word' or 'words_dictionnary' arguments must be provided.
    - Only one of the 'word' or 'words_dictionnary' arguments should be provided, not both.
    - The word search is case insensitive due to the use of (?i) in the regex expression.
    """

    # Verify that df is a pandas DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The df argument must be a pandas.DataFrame object")

    # Ensure the reference column exists in the DataFrame
    if reference_column not in df.columns:
        raise ValueError(f"The reference column '{reference_column}' is not present in the DataFrame.")

    # Ensure that either 'word' or 'words_dictionnary' is provided
    if word is None and words_dictionnary is None:
        raise ValueError("A word or a words dictionary must be provided")

    # Prevent both 'word' and 'words_dictionnary' from being provided simultaneously
    if word and words_dictionnary:
        raise ValueError("Provide either a single word or a dictionary of words, not both")

    if word:
        # Check that word is a string
        if not isinstance(word, str):
            raise TypeError("The word argument must be a string")
        # Create an indicator column for the single provided word
        df[word] = df[reference_column].str \
                                       .contains(rf'(?i){word}') \
                                       .astype(int)

    else:
        # Check that words_dictionnary is a dictionary
        if not isinstance(words_dictionnary, dict):
            raise TypeError("The words_dictionnary argument must be a dictionary")
        for col_name, words_to_match in words_dictionnary.items():
            if not words_to_match:
                # Handle empty word list case by setting the column to 0
                df[col_name] = 0
            else:
                if isinstance(words_to_match, list):
                    # Create a regex pattern from a list of words
                    regex_pattern = '|'.join([re.escape(word) for word in words_to_match])
                    df[col_name] = df[reference_column].str \
                                                       .contains(rf'(?i){regex_pattern}', na=False) \
                                                       .astype(int) 
                else:
                    # Handle a single word string
                    df[col_name] = df[reference_column].str \
                                                       .contains(rf'(?i){words_to_match}') \
                                                       .fillna(0).astype('Int64')
                    

    return df

def count_amenities_2023(df_rbnb: pd.DataFrame) -> pd.DataFrame:
    """
    Counts the occurrences of each amenity in a DataFrame's 'amenities' column.

    :param df_rbnb: DataFrame containing the 'amenities' column.
    :type df_rbnb: pd.DataFrame
    :return: A DataFrame with two columns, 'Amenity' and 'Frequency', sorted by the 
             frequency of each amenity in descending order.
    :rtype: pd.DataFrame
    """
    distinct_amenities= defaultdict(int)

    for amenities in df_rbnb['amenities']:
        # Convert string representation of list to actual list
        real_list = ast.literal_eval(amenities)

        # Remove quotes and clean data
        list_without_quotes = [element.replace('"', '') for element in real_list]
        chain = ', '.join(list_without_quotes)
        chain_with_quotes = f'"{chain}"'
        final_list = chain_with_quotes.split(', ')

        # Adjust the first and last elements if they contain extra quotes
        if final_list[0][0] == '"':
            final_list[0] = final_list[0][1:]
        if final_list[-1][-1] == '"':
            final_list[-1] = final_list[-1][:-1]

        # Update the counter for each amenity
        for amenity in final_list:
            distinct_amenities[amenity] += 1

    # Sort and create a DataFrame from the dictionary
    sorted_amenities = sorted(distinct_amenities.items(), key=lambda x: x[1], reverse=True)
    df_amenities = pd.DataFrame(sorted_amenities, columns=['Amenity', 'Frequency'])

    return df_amenities

def count_amenities_2017(df_rbnb: pd.DataFrame) -> pd.DataFrame:
    """
    Counts the occurrences of each amenity in a DataFrame column 'amenities'.
    
    :param df_rbnb: DataFrame containing the 'amenities' column.
    :type df_rbnb: pd.DataFrame
    :return: A new DataFrame with two columns, 'Amenity' and 'Frequency',
             sorted by the frequency of each amenity in descending order.
    :rtype: pd.DataFrame
    """
    # Vérifiez si df_rbnb est un DataFrame pandas
    if not isinstance(df_rbnb, pd.DataFrame):
        raise ValueError("The input df_rbnb is not a pandas DataFrame.")

    distinct_amenities= defaultdict(int)

    for amenities in df_rbnb['amenities']:
        try:
            # Split the string into elements based on commas and clean each element
            elements = [element.strip() for element in amenities.split(',')]

            # Create a new list with quotes around each element
            liste_avec_guillemets = [f"{element}" for element in elements]
        except Exception as e:
            continue
        
        # Update the counter for each amenity
        for amenity in liste_avec_guillemets:
            distinct_amenities[amenity] += 1

    # Sort and create a DataFrame from the dictionary
    sorted_amenities = sorted(distinct_amenities.items(), key=lambda x: x[1], reverse=True)
    df_amenities = pd.DataFrame(sorted_amenities, columns=['Amenity', 'Frequency'])

    return df_amenities

def create_progress_bar(total, local_path):
    """
    Creates and configures a TQDM progress bar.

    Arguments:
    - total : Total size of the file in bytes.
    - local_path : Local path of the file to be downloaded.
    
    Returns:
    - A configured tqdm object.
    """
    # Color codes for the progress bar
    DARK_GREEN = "\033[32m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    ENDC = "\033[0m"

    # Custom format for tqdm using color codes
    bar_format = "{l_bar}" + DARK_GREEN + "█{bar:25}░" + ENDC + " " + RED + "{n_fmt}/{total_fmt}" + ENDC + " " + BLUE + "[{rate_fmt} eta {remaining}]" + ENDC

    # Creating the tqdm object
    return tqdm(
        desc=local_path,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
        bar_format=bar_format
    )

def download_file(url, local_path):
    """
    Downloads a file from a specified URL and saves it to a given local path.
    This function can handle both compressed (.gz) and regular files. It features
    a progress bar to display the download progress.

    Parameters:
    - url (str): The URL of the file to be downloaded.
    - local_path (str): The local path where the file will be saved.

    The function performs a HEAD request to determine the file size for the progress
    bar. If the size cannot be determined, a default value is used. For compressed
    files (.gz), the function will decompress the file after download and delete
    the original compressed version. The function includes error handling to catch
    and report issues during the download process.
    """

    try:
        # Sending a HEAD request to get the total size of the file
        response_head = requests.head(url)
        total_size = int(response_head.headers.get('content-length', 0))

        # Assigning a default size (186 MB) if the total size is not available
        if total_size == 0 : 
            total_size = 186 * 1024 * 1024

        # Creating a progress bar and downloading the file in chunks
        with requests.get(url, stream=True) as response, \
             open(local_path + ".gz" if url.endswith('.gz') else local_path, "wb") as file, \
             create_progress_bar(total_size, local_path) as bar:

            for data in response.iter_content(chunk_size=1024):
                # Writing each chunk to the file and updating the progress bar
                size = file.write(data)
                bar.update(size)

        # Decompressing the file if it is a .gz compressed file
        if url.endswith('.gz'):
            with gzip.open(local_path + ".gz", 'rb') as f_in, open(local_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
            # Removing the compressed file after decompression
            os.remove(local_path + ".gz")

        # Indicating completion of the download
        print("Download completed.")
    except Exception as e:
        # Handling any exceptions that occur and printing an error message
        print(f"An error occurred: {e}")
