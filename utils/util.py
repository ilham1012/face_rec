import time

import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
from sklearn.calibration import CalibratedClassifierCV

from utils import constant

def calc_centroid(rect):
    (startY, endX, endY, startX) = rect
    centroidX = int((endX - startX) / 2) + startX
    centroidY = int((endY - startY) / 2) + startY

    centroid = (centroidX, centroidY)

    return centroid


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
    y = df[class_col]
    
    return X, y


def split_xy_train_test(train, test):
    X_train, y_train = split_x_y(train)
    X_test, y_test = split_x_y(test)

    return X_train, X_test, y_train, y_test


def load_data__split_xy_train_test(csv_file):
    df = load_data(csv_file)
    train, test = train_test_split(df, test_size=0.2)
    return split_xy_train_test(train, test)


def set_unknown(name):
    if name in constant.REG_FACES:
        return name
    else:
        return 'unknown'


def init_model(model, params):
    if (model == constant.MODELS[0]):
        clf_algo = tree.DecisionTreeClassifier().set_params(**params)
    elif (model == constant.MODELS[1]):
        clf_algo = SVC().set_params(**params)
    elif (model == constant.MODELS[2]):
        clf_algo = RandomForestClassifier().set_params(**params)
    else:
        clf_algo = AdaBoostClassifier().set_params(**params)

    clf = CalibratedClassifierCV(clf_algo)
    
    return clf


def train_evaluate(X, y, clf, cv=3):   
    # y_pred = clf.fit(X_train, y_train).predict(X_valid)
    # score = f1_score(y_valid, y_pred, average='macro') #, average='macro', 'micro', 'weighted')

    start_time = time.time()
    score = cross_val_score(clf, X, y, cv, n_jobs=-1)
    print(score)
    print("--- %s seconds ---" % (time.time() - start_time))

    return np.mean(score)
        
