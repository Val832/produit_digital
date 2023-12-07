# Loading packages and modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns

from sklearn import set_config
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge, RidgeCV, ElasticNet, LassoCV, LassoLarsCV, Lasso, LinearRegression, LassoLarsIC

from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.model_selection import train_test_split, GridSearchCV, cross_validate
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, OneHotEncoder
from sklearn.feature_selection import mutual_info_regression

import pickle
import detect_functions  # import detect_columns
import xgboost as xgb

from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error, max_error

import statsmodels.api as sm
import pylab as pl


# Read the dataset
d = pd.read_csv('../../data/airbnb2023/airbnb2023_dummies.csv', low_memory=False)

# Extract numerical values from 'bathrooms_text' and 'price' columns
d['bathrooms'] = d['bathrooms_text'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
d['price'] = d.price.replace('[\$,]', '', regex=True).astype(float)

# Columns to drop
drp = list(d.iloc[:, 0:10].columns)
drp.extend(['neighbourhood_group_cleansed', 'amenities', 'bathrooms_text', 'availability_365', 'minimum_nights', 'latitude', 'longitude'])

# Drop specified columns from the dataset
d.drop(drp, axis=1, inplace=True)

# Create a subset of the dataset and square certain continuous columns
df = d.iloc[:, :8].copy()
con_cols = ['accommodates', 'bedrooms', 'bathrooms', 'beds']
for i in con_cols:
    df[i + '_squared'] = d[i] ** 2

# Identify and delete columns with more than 300 missing values
vars = list(df.columns)
df = detect_functions.delete_na(df, vars, 300)

# One-hot encode categorical variables
df = pd.get_dummies(df)
X = df.copy()
y = X.pop('price')

# Log transformation of target variable 'price'
y = np.log(y)

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=23)

# Initialize a Linear Regression model
lr = LinearRegression()

# Perform Sequential Forward Selection for feature selection
sfs = SFS(lr,
          k_features="parsimonious",
          forward=True,
          floating=False,
          scoring='neg_mean_squared_error',
          cv=5)

sfs = sfs.fit(X_train, y_train)

# Select final features
final_select = list(X_train.iloc[:, list(sfs.k_feature_idx_)].columns)
X_train_final = X_train[final_select]
X_test_final = X_test[final_select]

# Train the Ordinary Least Squares (OLS) model on the training data
model = sm.OLS(y_train, sm.add_constant(X_train_final)).fit()

# Save the trained model to a pickle file
# with open('../src/data_science/model_simple_2023.pkl', 'wb') as file:
#     pickle.dump(model, file)
