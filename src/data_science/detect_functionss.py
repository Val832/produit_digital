# Loading packages and modules
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
import logging
from sklearn.feature_selection import mutual_info_regression
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt


def detect_columns(data, select = True, nodollar = True):
    
    """
    detect_columns standardizes variable names by converting uppercase letters to lowercase and spaces to underscores (snake_case).
    This function also facilitates the selection of potentially relevant variables for analysis and manages the '$' sign in the 'price' variable.

    Parameters
    ----------
    
    data : pd.DataFrame
        The database containing Airbnb listing information.

    select : bool, default: True
        Enables variable selection. Selected variables include:
        ['id', 'listing_url', 'scrape_id', 'last_scraped', 'name', 'space', 'description', 'neighborhood_overview',
        'street', 'neighbourhood', 'neighbourhood_cleansed', 'neighbourhood_group_cleansed', 'city', 'state', 
        'zipcode', 'market', 'smart_location', 'country_code', 'country', 'latitude', 'longitude', 'property_type', 
        'room_type', 'accommodates', 'bathrooms', "bathrooms_text", 'bedrooms', 'beds', 'bed_type', 'amenities', 
        'square_feet', 'price']

    nodollar : bool, default: True
        Manages the '$' sign in the 'price' variable.

    Returns
    -------
    
    data : pd.DataFrame
        The processed database after transformations.
    """    
    
    data.columns =[column.strip().replace(" ", "_").lower() for column in data.columns]
    var = [
        'id','listing_url','scrape_id','last_scraped','name','space','description','neighborhood_overview','street','neighbourhood',
        'neighbourhood_cleansed','neighbourhood_group_cleansed', 'city', 'state', 'zipcode', 'market','smart_location', 
        'country_code', 'country', 'latitude', 'longitude','property_type', 'room_type', 'accommodates', 'bathrooms', 
        "bathrooms_text", 'bedrooms','beds', 'bed_type', 'amenities', 'square_feet','minimum_nights','availability_365', 'price'
        ]
    if select:
        va = []
        for i in var:
            if i in data.columns:
                va.append(i)
        data=data[va].copy()
    if nodollar:
        data['price'] = data.price.replace('[\$,]', '', regex=True).astype(float)
    return data.set_index('id')




def delete_na(data, vars, s):
    """
    Removes rows with missing values in specified columns and filters rows based on a condition.

    Parameters:
    -----------
    
    data : DataFrame
        The input pandas DataFrame.
        
    vars : list or str
        Columns to consider for missing value removal.
        
    s : int or float
        Threshold for filtering rows based on the 'price' column.

    Returns:
    --------
    
    dt : DataFrame 
        DataFrame after removing rows with missing values and applying the price condition.

    Example:
    --------
    
    Assume 'data' is a DataFrame and 'vars' contains the column names to check for missing values.
    's' is an integer or float value representing the threshold for price filtering.
    
    result = delete_na(data, vars=['column1', 'column2'], s=100)
    """
    
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logging.basicConfig(format='%(levelname)s - %(message)s')
    
    
    # Filter rows based on 'price' column and remove missing values in specified columns
    dt = data.query('price < @s & price > 0').dropna(subset=vars)
    
    # Calculate the number of rows deleted
    dell = (data.shape[0] - dt.shape[0])
    
    # Log the number of deleted rows
    logging.info(f"{dell} rows have been deleted")
    
    # Return the DataFrame after removing missing values
    return dt.dropna(subset=vars)





def make_mi_scores(X, y):
    """
    Computes mutual information scores for features in relation to the target variable.

    Parameters:
    -----------
    X : DataFrame
        Input pandas DataFrame containing features.

    y : Series or array-like
        Target variable.

    Returns:
    --------
    mi_scores : Series
        Mutual information scores for each feature with respect to the target variable.
        
    Example:
    --------
    # Assume 'X' is a DataFrame with features and 'y' is the target variable
    mi_scores = make_mi_scores(X, y)
    """

    X = X.copy()
    
    # Convert object or category columns to factors (integer encoding)
    for colname in X.select_dtypes(["object", "category"]):
        X[colname], _ = X[colname].factorize()
    
    # Check for discrete features with integer dtypes
    discrete_features = [pd.api.types.is_integer_dtype(t) for t in X.dtypes]
    
    # Compute mutual information scores using mutual_info_regression
    mi_scores = mutual_info_regression(X, y, discrete_features=discrete_features, random_state=0)
    
    # Create a Series with MI scores for each feature, sorted in descending order
    mi_scores = pd.Series(mi_scores, name="MI Scores", index=X.columns)
    mi_scores = mi_scores.sort_values(ascending=False)
    
    return mi_scores




def plot_mi_scores(scores):
    """
    Plots the mutual information scores for features.

    Parameters:
    -----------
    scores : Series
        Mutual information scores for each feature.

    Returns:
    --------
    None

    Example:
    --------
    # Assume 'scores' is a Series containing mutual information scores for features
    plot_mi_scores(scores)
    """
    
    scores = scores.sort_values(ascending=True)
    width = np.arange(len(scores))
    ticks = list(scores.index)
    
    # Create a horizontal bar plot for MI scores
    plt.barh(width, scores)
    
    # Set y-axis ticks and labels
    plt.yticks(width, ticks)
    
    # Set plot title
    plt.title("Mutual Information Scores")

    

    

def get_all_performances(value_train, values_test, metrics):
    
    """
    Computes multiple performance metrics for both training and test datasets.

    Parameters:
    -----------
    value_train : tuple or list
        Tuple or list containing values required for metrics computation on the training set.

    values_test : tuple or list
        Tuple or list containing values required for metrics computation on the test set.

    metrics : list
        List of metric functions to compute performance metrics.

    Returns:
    --------
    pd.DataFrame
        DataFrame containing performance metrics computed for both training and test datasets.

    Example:
    --------
    # Assume 'value_train' and 'values_test' contain the necessary values
    # 'metrics' is a list of metric functions to compute performance metrics
    performances = get_all_performances(value_train, values_test, metrics)
    """

    
    # Initialize lists to store performance values
    test_perfs = []
    train_perfs = []
    metric_names = []

    # Iterate through each metric function provided
    for metric_func in metrics:
        # Get the name of the metric function
        metric_name = metric_func.__name__
        metric_names.append(metric_name)

        # Calculate the metric value on the training set and append to the list
        train_perfs.append(metric_func(*value_train))

        # Calculate the metric value on the test set and append to the list
        test_perfs.append(metric_func(*values_test))

    # Create a dictionary with metric names and corresponding performance values
    perfs = {"metric": metric_names, "train": train_perfs, "test": test_perfs}

    # Convert the dictionary to a DataFrame and return
    return pd.DataFrame(perfs)