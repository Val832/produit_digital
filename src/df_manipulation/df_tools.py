import pandas as pd 
from collections import defaultdict
import ast

def create_column_from_match(df, reference_column, word=None, words_list=None):
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
        The word to search for in the reference column. If provided, an indicator column 
        with this name will be added to the DataFrame.

    words_list : list of str, optional
        List of words to search for in the reference column. For each word, an indicator 
        column will be added to the DataFrame.

    Returns:
    --------
    df : pd.DataFrame
        DataFrame with the new indicator columns added.

    Remarks:
    ----------
    - At least one of the 'word' or 'words_list' arguments must be provided.
    - Only one of the 'word' or 'words_list' arguments should be provided, but not both simultaneously.
    - Word search is case insensitive due to (?i) in the regex expression.
    """

    # The argument df must be a pandas.DataFrame
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The df argument must take a pandas.DataFrame object as input")

    if reference_column not in df.columns:
        raise ValueError(f"The reference column '{reference_column}' is not present in the DataFrame.")

    # At least one parameter must be provided
    if word is None and words_list is None:
        raise ValueError("You must provide a word or a list of words")

    # Both parameters cannot be provided at the same time
    if word and words_list:
        raise ValueError("If you have multiple columns to create, please include them in a list and use only the 'words_list' argument")

    if word:
        # Type error handling
        if not isinstance(word, str):
            raise TypeError("The word argument must be of type 'str'")
        # Create a dummy column from the provided word if a match is found with dummies
        # (?i) allows matching regardless of capitalization
        df[word] = df[reference_column].str.contains(rf'(?i){word}').astype(int)

    else:
        # Type error handling
        if not isinstance(words_list, list):
            raise TypeError("The words argument takes a list as input")

        for i in words_list:
            if not isinstance(i, str):
                raise TypeError("The words_list argument only takes a list containing 'str' type objects as input")
        # Create dummy columns from the provided list of words if a match is found
        for new_column in words_list:
            df[new_column] = df[reference_column].str.contains(rf'(?i){new_column}').astype(int)

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
    sorted_amenities = sorted(distinct_amenities.items(), key=lambda x: x[1], reverse=True)
    df_amenities = pd.DataFrame(sorted_amenities, columns=['Amenity', 'Frequency'])

    return df_amenities
