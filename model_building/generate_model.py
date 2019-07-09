import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix  
import joblib

import constant
from util import set_unknown, load_data



# Load data
X_train, X_test, y_train, y_test = load_data('dataset/face_encodings.csv')


# Create classifier
# clf = SVC(kernel='linear', gamma='auto')
clf = RandomForestClassifier()

# Train classifier
start_time = time.time()
clf.fit(X_train.values, y_train.values)
print("--- %s seconds ---" % (time.time() - start_time))

# Predict
y_pred = clf.predict(X_test.values)

print(confusion_matrix(y_test.values, y_pred))
print(classification_report(y_test.values, y_pred))

# Output a pickle file for the model
joblib.dump(clf, 'SVM-test.pkl') 
 