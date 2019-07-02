import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix  
import joblib


def set_unknown(row):
    # if ((row == 'hanif') or (row == 'aris') or (row == 'jony') or (row == 'rian') or (row == 'irfan') or (row == 'ulfah') or (row == 'ilham')):
    #     return row

    if ((row == 'aris') or (row == 'jony') or (row == 'rian') or (row == 'ilham') or (row == 'arifin')):
        return row
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
# print(X_train)
# print(type(X_train.values[0]))

X_test  = test.drop('128', axis=1)  
X_test  = X_test.drop(['Unnamed: 0'],axis=1)
y_test  = test['128']
# print(y_test.values)

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
 
# Load the pickle file
# clf_load = joblib.load('saved_model.pkl')

# from util import train_evaluate

# params_dt = {
#     'criterion': 'gini',
#     'splitter': 'best',
#     'max_depth': None,
#     'min_samples_split': 2,
#     'min_samples_leaf': 1
#     }

# params_svm = {
#     'c': 1,
#     'kernel': 'linear',
#     'degree': 3,
#     'gamma': 'auto',
#     'coef0': 0.0
# }

# params_rf = {
#     'n_estimators': 100,
#     'criterion': 'gini',
#     'max_depth': None,
#     'min_samples_split': 2,
#     'min_samples_leaf': 1
#     }

# params_ab = {
#     'n_estimators': 50,
#     'learning_rate': .8,
#     'algorithm': 'SAMME.R'
# }

# score = train_evaluate(X_train, y_train, 'decision_tree', params_dt)

# print(score)