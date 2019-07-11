import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score

from utils import constant


def load_data(csv_file):
    df  = pd.read_csv(csv_file)
    df['128'] = df['128'].apply(lambda row: set_unknown(row))

    return df


def load_train_test(csv_file_train, csv_file_test):
    train = pd.read_csv(csv_file_train)
    test = pd.read_csv(csv_file_test)
    
    return train, test


def split_x_y(df, class_col='128'):
    X = df.drop(class_col, axis=1)
    X = X.drop(['Unnamed: 0'], axis=1)
    y = df[class_col]
    
    return X, y


def split_xy_train_test(train, test):
    X_train, y_train = split_x_y(train)
    X_test, y_test = split_x_y(test)

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
    