import numpy as np
import pandas as pd


from sklearn.linear_model import  LassoCV, LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


import src.data_science.data_science_tools as data_science_tools
import statsmodels.api as sm                          
from mlxtend.feature_selection import SequentialFeatureSelector as SFS


dff = pd.read_csv('../../data/airbnb2017/airbnb2017_dummies.csv', low_memory= False)


vars = ['neighbourhood_cleansed','room_type','accommodates','bedrooms','bathrooms','beds','bed_type','price']
vars.extend(list(dff.columns[33:]))


data = data_science_tools.delete_na(dff, vars, 300)
data = data[vars].copy()

con_cols = ['accommodates','bedrooms','bathrooms','beds']
for i in con_cols:
    data[i + '_squared'] = data[i]**2
    
df_model = pd.get_dummies(data)
X = df_model.copy()
y = X.pop('price')
continuous_cols = ['accommodates','bedrooms','bathrooms','beds','accommodates_squared','bedrooms_squared','bathrooms_squared','beds_squared']
delo = continuous_cols + ['price']
other_cols = list(df_model.drop(delo, axis=1).columns)
y = np.log(y)
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
                                # ('lr', LinearRegression())
                               ])

# Assuming 'X_train' is your training data
full_pipeline.fit(X_train)

# Transform the training data
X_train_transformedls = full_pipeline.transform(X_train)

# Transform the testing data (if applicable)
X_test_transformedls = full_pipeline.transform(X_test)

models = LassoCV(cv=20).fit(X_train_transformedls, y_train)


cf = pd.Series(models.coef_, index=X.columns)
select = list(cf[cf!=0].index)

continuous_colsx = ['accommodates','bedrooms','bathrooms','beds']
delo2 = continuous_colsx
other_colsx = list(df_model[select].drop(delo2, axis=1).columns)
X_train_xgb = X_train[select]
X_test_xgb = X_test[select]


continuous_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

# Combine transformers using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        #('cat', categorical_transformer, categorical_cols),
        ('cont', continuous_transformer, continuous_colsx),
        ('other', 'passthrough', other_colsx)
    ]
)

# Create a full pipeline including preprocessing and any model(s) you want to apply
full_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                # Add additional steps for modeling if needed
                                # ('lr', LinearRegression()())
                               ])


# Assuming 'X_train' is your training data
full_pipeline.fit(X_train_xgb)

# Transform the training data
X_train_xgb_transformedls = full_pipeline.transform(X_train_xgb)

# Transform the testing data (if applicable)
X_test_xgb_transformedls = full_pipeline.transform(X_test_xgb)


lr = LinearRegression()

sfs = SFS(lr, 
          k_features="parsimonious", 
          forward=True, 
          floating=False, 
          scoring='neg_mean_squared_error',
          cv=10)

sfs = sfs.fit(X_train_xgb_transformedls, y_train)

final_select = list(X_train_xgb.iloc[:,list(sfs.k_feature_idx_)].columns)#.remove('translation missing: en.hosting_amenity_50')
final_select.remove('translation missing: en.hosting_amenity_50')

continuous_colsf = ['accommodates','bedrooms','bathrooms']
delo2 = continuous_colsf
other_colsf = list(df_model[final_select].drop(delo2, axis=1).columns)
X_train_final = X_train[final_select]
X_test_final = X_test[final_select]

model = sm.OLS(y_train, sm.add_constant(X_train_final)).fit()

#with open('best_model_2023.pkl', 'wb') as file:
 #   pickle.dump(model, file)


