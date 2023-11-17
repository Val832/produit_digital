import pandas as pd 
import re
from collections import defaultdict
import ast


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
                                                       .astype(int)

    return df

def count_amenities(df_rbnb):
    """
    Counts the occurrences of each amenity in a DataFrame column 'amenities'.
    
    Args:
    df_rbnb (pd.DataFrame): DataFrame containing the 'amenities' column.
    
    Returns:
    pd.DataFrame: A new DataFrame with two columns, 'Amenity' and 'Frequency',
                  sorted by the frequency of each amenity in descending order.
    
    The function also saves the resulting DataFrame to a CSV file.
    """
    # Initialize a dictionary to count occurrences of each amenity
    distinct_amenities = defaultdict(int)

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
    sorted_amenities = sorted(distinct_amenities.items(), 
                              key=lambda x: x[1], 
                              reverse=True)
    
    df_amenities = pd.DataFrame(sorted_amenities, 
                                columns=['Amenity', 'Frequency'])

    return df_amenities
