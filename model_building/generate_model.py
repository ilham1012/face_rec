import time
from datetime import datetime
import argparse

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, auc, cohen_kappa_score, f1_score, precision_score, recall_score
import joblib
import matplotlib.pyplot as plt

from utils import constant
from utils.util import set_unknown, split_xy_train_test, load_train_test, init_model, plot_confusion_matrix


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-m", "--model",
    default="svm",
    help="choose in ['dt', 'svm', 'rf', 'adaboost']"
    )
ap.add_argument(
    "-r", "--train",
    default="dataset/face_encodings__train.csv",
    help="location of train file"
    )
ap.add_argument(
    "-e", "--test",
    default="dataset/face_encodings__test.csv",
    help="location of test file"
    )
args = vars(ap.parse_args())


# Load data
train, test = load_train_test(args['train'], args['test'])
X_train, X_test, y_train, y_test = split_xy_train_test(train, test)
print(X_train.iloc[0, :])
print("train: ", len(X_train), " - test: ", len(X_test))

# Create classifier
if (args['model'] == constant.MODELS[0]): #dt
    params = {"criterion": "entropy", "max_depth":381, "min_samples_split": 2, "min_samples_leaf": 1}
elif (args['model'] == constant.MODELS[1]): #svm
    params = {"C": 36.77783910335444, "kernel":"rbf", "degree": 8, "gamma": 1.7575790771023974}
elif (args['model'] == constant.MODELS[2]): #rf
    params = {"n_estimators": 62, "max_depth":364, "min_samples_split": 2, "min_samples_leaf": 1}
else: #adaboost
    params = {"n_estimators": 23, "learning_rate":0.07733269343732768, "algorithm": "SAMME.R"}

clf = init_model(args['model'], params)

# Train classifier
start_time = time.time()
clf.fit(X_train.values, y_train.values)
print("--- %s seconds ---" % (time.time() - start_time))

# Predict
y_pred = clf.predict(X_test.values)
cm = confusion_matrix(y_test.values, y_pred)

print(cm)
print(classification_report(y_test.values, y_pred))
print('accuracy_score ', accuracy_score(y_test.values, y_pred))
print('cohen_kappa_score ', cohen_kappa_score(y_test.values, y_pred))
print('f1_score ', f1_score(y_test.values, y_pred, average='macro'))
print('precision_score ', precision_score(y_test.values, y_pred, average='macro'))
print('recall_score ', recall_score(y_test.values, y_pred, average='macro'))

output_filename = 'models/' + args['model'] + '__' + datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + '.pkl'

# Output a pickle file for the model
joblib.dump(clf, output_filename)

# Plot normalized confusion matrix
plot_confusion_matrix(cm, classes=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Unknown'],
                      title='Normalized confusion matrix - ' + args['model'], plt=plt)

plt.show()