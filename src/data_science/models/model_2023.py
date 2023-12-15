#Chargement des packages et modules
import numpy as np
import pandas as pd


from sklearn.linear_model import  LassoCV, LinearRegression

from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import src.data_science.data_science_tools as data_science_tools #import detect_columns
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
import statsmodels.api as sm

d=pd.read_csv('../../data/rbnb_with_dummies.csv',low_memory=False)

d['bathrooms'] = d['bathrooms_text'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
d['price'] = d.price.replace('[\$,]', '', regex=True).astype(float)

drp = list(d.iloc[:,0:10].columns)
drp.extend(['neighbourhood_group_cleansed', 'amenities', 'bathrooms_text', 'availability_365', 'minimum_nights', 'latitude', 'longitude'])

d.drop(drp, axis=1, inplace=True)
#d.dropna(inplace=True)

pb = d.iloc[:,7:]
X = pb.copy()
y = X.pop('price')

mi_scores = data_science_tools.make_mi_scores(X, y)
mi_select = mi_scores.loc[mi_scores>.02].index

vars = list(d.iloc[:,:8].columns)

d = data_science_tools.delete_na(d, vars, 300)
vars.extend(list(mi_select))
d = d[vars].copy()

con_cols = ['accommodates','bedrooms','bathrooms','beds']
for i in con_cols:
    d[i + '_squared'] = d[i]**2
    
df = d.copy()#.loc[:,lst].copy()
df = pd.get_dummies(df)
X = df.copy()
y = X.pop('price')

y = np.log(y)

#categorical_cols = ['neighbourhood_cleansed','property_type','room_type']
continuous_cols = ['accommodates','bedrooms','beds','bathrooms','accommodates_squared','bedrooms_squared','bathrooms_squared','beds_squared']
delo = continuous_cols + ['price']
other_cols = list(df.drop(delo, axis=1).columns)




X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=23)

continuous_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Combine transformers using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        #('cat', categorical_transformer, categorical_cols),
        ('cont', continuous_transformer, continuous_cols),
        ('other', 'passthrough', other_cols)
    ]
)

# Create a full pipeline including preprocessing and any model(s) you want to apply
full_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                # Add additional steps for modeling if needed
                                # ('lr', LinearRegression()())
                               ])


# Assuming 'X_train' is your training data
full_pipeline.fit(X_train)

# Transform the training data
X_train_transformedls = full_pipeline.transform(X_train)
X_train_transformed = full_pipeline.transform(X_train)

# Transform the testing data (if applicable)
X_test_transformedls = full_pipeline.transform(X_test)
X_test_transformed = full_pipeline.transform(X_test)

model = LassoCV(cv=20).fit(X_train_transformed, y_train)
coef = pd.Series(model.coef_, index=X.columns)

coef = pd.Series(model.coef_, index=X.columns)
#cf = pd.Series(models.coef_, index=X.columns)
select = list(coef[coef!=0].index)

X_train_lr = X_train[select]
X_test_lr = X_test[select]

lr = LinearRegression()

sfs = SFS(lr, 
          k_features="parsimonious", 
          forward=True, 
          floating=False, 
          scoring='neg_mean_squared_error',
          cv=10)

sfs = sfs.fit(X_train_lr, y_train)


final_select = list(X_train_lr.iloc[:,list(sfs.k_feature_idx_)].columns)#.remove('translation missing: en.hosting_amenity_50')


continuous_colsf = ['accommodates','bathrooms', 'accommodates_squared', 'bathrooms_squared']

delo2 = continuous_colsf
other_colsf = list(df[final_select].drop(delo2, axis=1).columns)
X_train_final = X_train[final_select]
X_test_final = X_test[final_select]

# Supposons que vous ayez déjà vos données d'entraînement (X_train, y_train)
# et vos données de test (X_test)

# Entraîner votre modèle de régression linéaire sur les données d'entraînement
model = sm.OLS(y_train, sm.add_constant(X_train_final)).fit()

#with open('best_model_2023.pkl', 'wb') as file:
 #   pickle.dump(model, file)


