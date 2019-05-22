import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix  
import joblib

# Load data
df  = pd.read_csv('dataset/face_encodings.csv')
# print(df.head)

# Split training & testing data
train, test = train_test_split(df, test_size=0.2)

# split feature & labels
X_train = train.drop('128', axis=1)
X_train = X_train.drop(['Unnamed: 0'],axis=1)
y_train = train['128']
# print(X_train)
print(type(X_train.values[0]))

X_test  = test.drop('128', axis=1)  
X_test  = X_test.drop(['Unnamed: 0'],axis=1)
y_test  = test['128']
print(y_test.values)

# # Create classifier
# clf = SVC(kernel='rbf') # (gamma='auto')
clf = RandomForestClassifier()

# Train classifier
clf.fit(X_train.values, y_train.values)

# Predict
y_pred = clf.predict(X_test.values)

print(confusion_matrix(y_test.values, y_pred))
print(classification_report(y_test.values, y_pred))

# Output a pickle file for the model
joblib.dump(clf, 'SVM-test.pkl') 
 
# Load the pickle file
# clf_load = joblib.load('saved_model.pkl') 