from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score, recall_score
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

def split_and_train(df):
    nrows = len(df)
    df = df.reset_index(drop=True)
    y = df['category'].to_numpy()
    X = df.drop(columns='category')
    X = X.to_numpy()
    train_split = round(0.8*nrows)

    print(f'Training on {train_split} events')
    X_train, X_test = X[:train_split], X[train_split:]
    y_train, y_test = y[:train_split], y[train_split:]

    svm_clf = Pipeline([
                ("scaler",StandardScaler()),
                ("svm_clf",SVC(kernel="poly",degree=3,coef0=1,C=5))
            ])
    svm_clf.fit(X_train,y_train)
    #print(f'Prediciton: {svm_clf.predict([X[802]])} vs. Truth: {y[802]}')
    print(cross_val_score(svm_clf,X_train,y_train,cv=3,scoring="accuracy"))

json_name = 'variable_list.json'
# Load data from json file
with open(json_name) as j:
    data = json.load(j)

# Name of pickle files to be loaded
file_list = data['pickle_files_to_load']

# define a blank dataframe for later use
df = pd.DataFrame()
# Loop over files to be loaded and add them together
for x in file_list:
    file_name = '../Data/background_selection/'+x
    print(f'Opening file: {file_name}')
    df_tmp = pd.read_pickle(file_name)
    print(f'Number of events: {len(df_tmp)}\n')
    df = pd.concat([df,df_tmp], ignore_index=True)

print(f'Total dataframe rows: {len(df)}')

# Use .sample() to randomize the order of events
df = df.sample(frac=1).reset_index(drop=True)

# turn booleans into integers and drop infinities if any exist
df = df.astype({col: 'int' for col in df.select_dtypes('bool').columns})
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

split_and_train(df)
