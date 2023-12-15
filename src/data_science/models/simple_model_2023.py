#Chargement des packages et modules
import numpy as np
import pandas as pd

from sklearn.linear_model import  LinearRegression
from sklearn.model_selection import train_test_split
import src.data_science.data_science_tools as data_science_tools #import detect_columns
from mlxtend.feature_selection import SequentialFeatureSelector as SFS

import statsmodels.api as sm

d=pd.read_csv('../data/rbnb_with_dummies.csv',low_memory=False)

d['bathrooms'] = d['bathrooms_text'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
d['price'] = d.price.replace('[\$,]', '', regex=True).astype(float)

drp = list(d.iloc[:,0:10].columns)
drp.extend(['neighbourhood_group_cleansed', 'amenities', 'bathrooms_text', 'availability_365', 'minimum_nights', 'latitude', 'longitude'])

d.drop(drp, axis=1, inplace=True)

df = d.iloc[:,:8].copy()#.loc[:,lst].copy()
con_cols = ['accommodates','bedrooms','bathrooms','beds']
for i in con_cols:
    df[i + '_squared'] = d[i]**2
vars = list(df.columns)
df = data_science_tools.delete_na(df, vars, 300)
df = pd.get_dummies(df)
X = df.copy()
y = X.pop('price')

y = np.log(y)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=23)

lr = LinearRegression()

sfs = SFS(lr, 
          k_features="parsimonious", 
          forward=True, 
          floating=False, 
          scoring='neg_mean_squared_error',
          cv=5)

sfs = sfs.fit(X_train, y_train)

final_select = list(X_train.iloc[:,list(sfs.k_feature_idx_)].columns)

X_train_final = X_train[final_select]
X_test_final = X_test[final_select]

# Supposons que vous ayez déjà vos données d'entraînement (X_train, y_train)
# et vos données de test (X_test)

# Entraîner votre modèle de régression linéaire sur les données d'entraînement
model = sm.OLS(y_train, sm.add_constant(X_train_final)).fit()

#with open('../src/data_science/model_simple_2023.pkl', 'wb') as file:
 #   pickle.dump(model, file)