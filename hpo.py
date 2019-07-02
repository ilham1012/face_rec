import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix  
import joblib
from util import train_evaluate, axes2fig
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize

from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize, forest_minimize
from skopt.plots import plot_convergence, plot_evaluations

import matplotlib.pyplot as plt
plt.set_cmap("viridis")


def set_unknown(row):
    # if ((row == 'hanif') or (row == 'aris') or (row == 'jony') or (row == 'rian') or (row == 'irfan') or (row == 'ulfah') or (row == 'ilham')):
    #     return row

    if ((row == 'aris') or (row == 'jony') or (row == 'rian')):
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




# The list of hyper-parameters we want to optimize. For each one we define the bounds,
# the corresponding scikit-learn parameter name, as well as how to sample values
# from that dimension (`'log-uniform'` for the learning rate)
space  = [Integer(1, 200, name='n_estimators'),
          Integer(1, 1000, name='max_depth'),
          Integer(2, 100, name='min_samples_split'),
          Integer(1, 100, name='min_samples_leaf')]

# this decorator allows your objective function to receive a the parameters as
# keyword arguments. This is particularly convenient when you want to set scikit-learn
# estimator parameters
@use_named_args(space)
def objective(**params):

    return -1.0 * train_evaluate(X_train, y_train, 'rf', params)


# result_hpo = gp_minimize(objective, space, n_calls=10, random_state=0)
result_hpo = forest_minimize(objective, space, n_calls=200, random_state=0)

print("Best score=%.4f" % result_hpo.fun)

print("""Best parameters:
- n_estimators=%d
- max_depth=%d
- min_samples_split=%d
- min_samples_leaf=%d""" % (result_hpo.x[0], result_hpo.x[1], 
                            result_hpo.x[2], result_hpo.x[3]))


# axes = plot_convergence(result_hpo)

axes = plot_evaluations(result_hpo, bins=10)
fig = axes2fig(axes, figsize=(16,12))
plt.show()