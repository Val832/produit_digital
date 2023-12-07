# Loading necessary packages and modules
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

# Extract features and target variable 'price'
pb = d.iloc[:, 7:]
X = pb.copy()
y = X.pop('price')

# Compute mutual information scores
mi_scores = detect_functions.make_mi_scores(X, y)
mi_select = mi_scores.loc[mi_scores > .02].index

# Identify and delete columns with more than 300 missing values
vars = list(d.iloc[:, :8].columns)
d = detect_functions.delete_na(d, vars, 300)
vars.extend(list(mi_select))
d = d[vars].copy()

# Create squared columns for certain continuous columns
con_cols = ['accommodates', 'bedrooms', 'bathrooms', 'beds']
for i in con_cols:
    d[i + '_squared'] = d[i] ** 2

# Perform one-hot encoding
df = pd.get_dummies(d)
X = df.copy()
y = X.pop('price')

# Log transformation of target variable 'price'
y = np.log(y)

# Separate continuous and other columns
continuous_cols = ['accommodates', 'bedrooms', 'beds', 'bathrooms', 'accommodates_squared', 'bedrooms_squared', 'bathrooms_squared', 'beds_squared']
delo = continuous_cols + ['price']
other_cols = list(df.drop(delo, axis=1).columns)

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=23)

# Define preprocessing steps for continuous and other columns
continuous_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Combine transformers using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('cont', continuous_transformer, continuous_cols),
        ('other', 'passthrough', other_cols)
    ]
)

# Create a full pipeline including preprocessing
full_pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

# Fit the pipeline on training data and transform it
X_train_transformed = full_pipeline.fit_transform(X_train)
X_test_transformed = full_pipeline.transform(X_test)

# Initialize a LassoCV model and fit it on transformed training data
model = LassoCV(cv=20).fit(X_train_transformed, y_train)
coef = pd.Series(model.coef_, index=X.columns)

# Select features with non-zero coefficients
select = list(coef[coef != 0].index)
X_train_lr = X_train[select]
X_test_lr = X_test[select]

# Initialize a Linear Regression model
lr = LinearRegression()

# Perform Sequential Forward Selection (SFS) for feature selection
sfs = SFS(lr, 
          k_features="parsimonious", 
          forward=True, 
          floating=False, 
          scoring='neg_mean_squared_error',
          cv=10)

sfs = sfs.fit(X_train_lr, y_train)

# Select final features based on SFS results
final_select = list(X_train_lr.iloc[:, list(sfs.k_feature_idx_)].columns)

# Further separate continuous columns
X_train_final = X_train[final_select]
X_test_final = X_test[final_select]

# Train an Ordinary Least Squares (OLS) model on the selected features
model = sm.OLS(y_train, sm.add_constant(X_train_final)).fit()

# Save the trained model to a file
# with open('best_model_2023.pkl', 'wb') as file:
#     pickle.dump(model, file)
