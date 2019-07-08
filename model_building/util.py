import numpy as np
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import f1_score

models = ['dt', 'svm', 'rf', 'adaboost']

def train_evaluate(X, y, model, params):
    # print("--------")
    # print(params)

    # X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=1234)

    if (model == models[0]):
        clf = tree.DecisionTreeClassifier().set_params(**params)
    elif (model == models[1]):
        clf = SVC().set_params(**params)
    elif (model == models[2]):
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
    