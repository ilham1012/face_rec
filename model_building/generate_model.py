import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix  
import joblib



known_faces = ['aris', 'jony', 'rian', 'ilham']
models = ['dt', 'svm', 'rf', 'adaboost']


def set_unknown(name):
    if name in known_faces:
        return name
    else:
        return 'unknown'

# Load data
df  = pd.read_csv('dataset/face_encodings.csv')
df['128'] = df['128'].apply(lambda row: set_unknown(row))
# print(df)

# Split training & testing data
train, test = train_test_split(df, test_size=0.2)

# split feature & labels
X_train = train.drop('128', axis=1)
X_train = X_train.drop(['Unnamed: 0'],axis=1)
y_train = train['128']

X_test  = test.drop('128', axis=1)  
X_test  = X_test.drop(['Unnamed: 0'],axis=1)
y_test  = test['128']

# Create classifier
# clf = SVC(kernel='linear', gamma='auto')
clf = RandomForestClassifier()

# Train classifier
import time
start_time = time.time()
clf.fit(X_train.values, y_train.values)
print("--- %s seconds ---" % (time.time() - start_time))

# Predict
y_pred = clf.predict(X_test.values)

print(confusion_matrix(y_test.values, y_pred))
print(classification_report(y_test.values, y_pred))

# Output a pickle file for the model
joblib.dump(clf, 'SVM-test.pkl') 
 