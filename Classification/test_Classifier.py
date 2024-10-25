from sklearn.datasets import fetch_openml
from sklearn.model_selection import cross_val_score
from sklearn.metrics import precision_score, recall_score
from sklearn.svm import SVC
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mnist = fetch_openml('mnist_784',version=1)
print(mnist.keys())

# Define X as data and y as target
X, y = mnist["data"].to_numpy(), mnist["target"].to_numpy()
# Change y into an integer
y = y.astype(np.uint8)

# Split the data into training and testing sets
# Train on 60,000 entries
# Test on 10,000 entries
train_split = 60000
X_train, X_test = X[:train_split], X[train_split:]
y_train, y_test = y[:train_split], y[train_split:]

svm_clf = SVC()
svm_clf.fit(X_train,y_train)
svm_clf.predict(X[0])
