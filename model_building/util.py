import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score

import constant



def load_data(csv_file):
    # Load data
    df  = pd.read_csv(csv_file)
    df['128'] = df['128'].apply(lambda row: set_unknown(row))

    # Split training & testing data
    train, test = train_test_split(df, test_size=0.2)

    # split feature & labels
    X_train = train.drop('128', axis=1)
    X_train = X_train.drop(['Unnamed: 0'],axis=1)
    y_train = train['128']

    X_test  = test.drop('128', axis=1)  
    X_test  = X_test.drop(['Unnamed: 0'],axis=1)
    y_test  = test['128']
    # print(y_test.values)

    return X_train, X_test, y_train, y_test



def set_unknown(name):
    if name in constant.REG_FACES:
        return name
    else:
        return 'unknown'

def train_evaluate(X, y, model, params):

    if (model == constant.MODELS[0]):
        clf = tree.DecisionTreeClassifier().set_params(**params)
    elif (model == constant.MODELS[1]):
        clf = SVC().set_params(**params)
    elif (model == constant.MODELS[2]):
        clf = RandomForestClassifier().set_params(**params)
    else:
        clf = AdaBoostClassifier().set_params(**params)
        
    # y_pred = clf.fit(X_train, y_train).predict(X_valid)
    # score = f1_score(y_valid, y_pred, average='macro') #, average='macro', 'micro', 'weighted')

    score = cross_val_score(clf, X, y, cv=3)

    return np.mean(score)
        
    
def axes2fig(axes, figsize=(16,12)):
    fig = plt.figure(figsize=figsize)
    try:
        h, w = axes.shape
        for i in range(h):
            for j in range(w):
                fig._axstack.add(fig._make_key(axes[i, j]), axes[i, j])
    except AttributeError:
        fig._axstack.add(fig._make_key(axes), axes)
    return fig
    