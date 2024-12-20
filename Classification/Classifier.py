from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import time as t
import argparse

def binary_classifier_NN(var_num,X_train, X_test, y_train, y_test):
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Input, Dropout
    from tensorflow.keras.callbacks import EarlyStopping
    print('Running binary_classifier_NN()')
    num_features = X_train.shape[1]
    print(f'Number of features: {num_features}')

    # Want to quickly choose number of neurons for hidden layers
    # Based on number of features for quick testing of different features
    if num_features > 128:
        neuron1 = 512
    elif num_features < 128 and num_features > 64:
        neuron1 = 256
    elif num_features < 64 and num_features > 32:
        neuron1 = 128
    elif num_features < 32 and num_features > 16:
        neuron1 = 64
    elif num_features < 16 and num_features > 8:
        neuron1 = 32
    elif num_features < 8 and num_features > 4:
        neuron1 = 16
    elif num_features < 4 and num_features > 2:
        neuron1 = 8
    else:
        neuron1 = 4

    neuron2 = int(neuron1/4)
    print(f'Number of neurons in hidden layers: {neuron1}, {neuron2}')

    # Build the model
    model = Sequential([
        Input(shape=(num_features,)),  # Input layer
        Dense(neuron1, activation='relu'),
        Dropout(0.2),
        Dense(neuron2, activation='relu'),
        #Dropout(0.2),
        Dense(1, activation='sigmoid')  # Output layer for binary classification
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    #history = model.fit(X_train, y_train, epochs=20, 
    #                    validation_data=(X_test, y_test), 
    #                    batch_size=32)

    early_stop = EarlyStopping(monitor='val_loss', 
                               patience=10, 
                               restore_best_weights=True)
    history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, 
              callbacks=[early_stop])

    # Extract data
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    accuracy = history.history.get('accuracy', None)
    val_accuracy = history.history.get('val_accuracy', None)
    epochs = range(1, len(loss) + 1)

    # Plot Loss
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)  # Create subplot for loss
    plt.plot(epochs, loss, 'bo-', label='Training Loss')
    plt.plot(epochs, val_loss, 'r*-', label='Validation Loss')
    plt.title('Training and Validation Loss')
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.legend()

    if accuracy and val_accuracy:
        plt.subplot(1, 2, 2)  # Create subplot for accuracy
        plt.plot(epochs, accuracy, 'bo-', label='Training Accuracy')
        plt.plot(epochs, val_accuracy, 'r*-', label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()

    plt.tight_layout()
    plt.savefig(f'../Plots/background_selection/accuracy_and_loss_{var_num}.png',dpi=1000)


    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test Loss: {round(loss,2)}, Test Accuracy: {round(accuracy,2)}\n")

def binary_classifier_sgd(X_train, X_test, y_train, y_test):
    print('Running binary_classifier_sgd()')
    sgd_clf = Pipeline([
                ("scaler",StandardScaler()),
                ("sgd_clf",SGDClassifier(random_state=42))
            ])
    #sgd_clf = SGDClassifier(random_state=42)
    sgd_clf.fit(X_train,y_train)
    y_train_pred = cross_val_predict(sgd_clf, X_train, y_train, cv=100)
    y_train_score = cross_val_score(sgd_clf, X_train, y_train, cv=100)
    #print(f'The average accuracy from cross validation is {round(np.mean(y_train_score),2)}')
    print(f'Scores: {y_train_score}')
    print(f'Mean score: {round(np.mean(y_train_score),2)}')
    print(f'Standard deviation: {round(y_train_score.std(),2)}\n')

def multicategory_classifier_svm(X_train, X_test, y_train, y_test):
    print('Running multicategory_classifier_svm()')

    svm_clf = Pipeline([
                ("scaler",StandardScaler()),
                ("svm_clf",SVC(kernel="poly",degree=3,coef0=1,C=5))
            ])
    svm_clf.fit(X_train,y_train)

    y_train_pred = cross_val_predict(svm_clf, X_train, y_train, cv=3)

    y_train_pred = cross_val_predict(svm_clf, X_train, y_train, cv=100)
    y_train_score = cross_val_score(svm_clf, X_train, y_train, cv=100)
    #print(f'The average accuracy from cross validation is {round(np.mean(y_train_score),2)}')
    print(f'Scores: {y_train_score}')
    print(f'Mean score: {round(np.mean(y_train_score),2)}')
    print(f'Standard deviation: {round(y_train_score.std(),2)}\n')

def plot_correlations(df,var_num):
    # Save a plot of correlations to assist in evaluating chosen variables
    matrix = df.corr()
    variables = []
    for i in matrix.columns:
        variables.append(i)

    plt.imshow(matrix, cmap='Blues')
    plt.colorbar()
    plt.xticks(range(len(matrix)),variables,rotation=45,ha='right',fontsize=4)
    plt.yticks(range(len(matrix)),variables,fontsize=5)
    plt.xlabel('xlabel',fontsize=10)
    plt.ylabel('ylabel',fontsize=10)
    print('Saving matrix of correlations')
    plt.savefig(f'../Plots/background_selection/correlations_{var_num}.png',dpi=1000)
    plt.close()

# Log the start time 
start_time = t.time()

# Parse the argument option
# This argument will be a number corresponding to one of the variable sets
parser = argparse.ArgumentParser(description='variable file to use')
parser.add_argument('--var_num')
args = parser.parse_args()

# Load data from json file
json_name = (f"variables_{args.var_num}.json")
print(f'loading: {json_name}')
with open(json_name) as j:
    data = json.load(j)

# Name of pickle files to be loaded
#file_list = data['files_all_categories']
file_list = data['files_binary']

# define a blank dataframe for later use
df = pd.DataFrame()
# Loop over files to be loaded and add them together
for x in file_list:
    x += (f'_{args.var_num}.pkl')
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

# Plot correlations to determine if any variables can be dropped
plot_correlations(df,args.var_num)

nrows = len(df)
df = df.reset_index(drop=True)
y = df['category'].to_numpy()
y = df['category']
X = df.drop(columns='category')
X = X.to_numpy()
X = X
train_split = round(0.8*nrows)

print(f'Training on {train_split} events')
X_train, X_test = X[:train_split], X[train_split:]
y_train, y_test = y[:train_split], y[train_split:]
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, stratify=y)

# Carry out training
#binary_classifier_sgd(X_train, X_test, y_train, y_test)
binary_classifier_NN(args.var_num,X_train, X_test, y_train, y_test)
#multicategory_classifier_svm(X_train, X_test, y_train, y_test)

time_diff = t.time() - start_time
if time_diff > 60:
    time_diff = time_diff/60
    time_diff = round(time_diff,1)
    print(f'This program took {time_diff} m to run')
else:
    time_diff = round(time_diff,1)
    print(f'This program took {time_diff} s to run')

