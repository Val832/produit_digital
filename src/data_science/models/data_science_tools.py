import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_regression
import logging
import matplotlib.pyplot as plt

def detect_columns(data, select = True, nodollar = True): 
    
    """
        detect_columns permet de standariser les noms des variables. Elle detecte le présence de majuscule et 
        des espaces dans le nom des variables pour remplacer les majuscules par des miniscules et les espaces 
        par des undersocre (mininuscule et snake_case).
        Cette fonction permet aussi de selection les variables qui pourraient être intéressantes pour notre analyse
        ou de gérer le $ de la variable price.
        
        Paramètres
        ----------
        data (pd.DataFrame): la base de données des annonces Airbnb
        
        select (Boolean, default: True): permet la sélection de variables. les variables sélectionner sont:
            [
            'id','listing_url','scrape_id','last_scraped','name','space','description','neighborhood_overview',
            'street','neighbourhood', 'neighbourhood_cleansed','neighbourhood_group_cleansed', 'city', 'state', 
            'zipcode', 'market', 'smart_location', 'country_code', 'country', 'latitude', 'longitude',
            'property_type', 'room_type', 'accommodates', 'bathrooms', "bathrooms_text", 'bedrooms','beds', 
            'bed_type', 'amenities', 'square_feet', 'price',
            ]
            
        nodallar (Boolean, default: True): permet de gérer le $ de la variable price.
        
        Retourne
        --------
        data (pd.DataFrame): la base de données ayant sublie les traitements
    """
    
    
    data.columns =[column.strip().replace(" ", "_").lower() for column in data.columns]
    var = [
        'id','listing_url','scrape_id','last_scraped','name','space','description','neighborhood_overview',
        'street','neighbourhood', 'neighbourhood_cleansed','neighbourhood_group_cleansed', 'city', 'state', 'zipcode', 'market',
        'smart_location', 'country_code', 'country', 'latitude', 'longitude','property_type', 'room_type', 'accommodates', 
        'bathrooms', "bathrooms_text", 'bedrooms','beds', 'bed_type', 'amenities', 'square_feet', 'price',
        ]
    if select:
        va = []
        for i in var:
            if i in data.columns:
                va.append(i)
        data=data[va].copy()
    if nodollar:
        data['price'] = data.price.replace('[\$,]', '', regex=True).astype(float)
    return data

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
