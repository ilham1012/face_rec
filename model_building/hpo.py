import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix  
import joblib
from util import train_evaluate, axes2fig
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize

from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize, forest_minimize, gbrt_minimize
from skopt.plots import plot_convergence, plot_evaluations

import matplotlib.pyplot as plt
plt.set_cmap("viridis")

import argparse


# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-m", "--model",
    default="svm",
    help="choose in ['decision_tree', 'svm', 'rf', 'adaboost']"
    )
ap.add_argument(
    "-o", "--optimizer",
    default="forest",
    help="choose in ['forest', 'gbrt', 'gp']"
)
ap.add_argument(
    "-n", "--ncalls",
    type=int,
    default=100,
    help="iteration of optimization"
)
args = vars(ap.parse_args())



known_faces = ['aris', 'jony', 'rian', 'ilham']
models = ['dt', 'svm', 'rf', 'adaboost']
optimizers = ['forest', 'gbrt', 'gp']

def set_unknown(name):
    if name in known_faces:
        return name
    else:
        return 'unknown'

# Load data
df  = pd.read_csv('dataset/face_encodings.csv')
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




# The list of hyper-parameters we want to optimize. For each one we define the bounds,
# the corresponding scikit-learn parameter name, as well as how to sample values
# from that dimension (`'log-uniform'` for the learning rate)
space = []

if (args["model"] == models[0]):
    # Decision Tree
    space  = [Categorical(['gini', 'entropy'], name='criterion'),
            Integer(1, 1000, name='max_depth'),
            Integer(2, 100, name='min_samples_split'),
            Integer(1, 100, name='min_samples_leaf')]

elif (args["model"] == models[1]):
    # SVM
    space  = [Real(1e-6, 1e+6, prior='log-uniform', name='C'),
            Categorical(['linear', 'poly', 'rbf'], name='kernel'),
            Integer(1, 8, name='degree'),
            Real(1e-6, 1e+1, prior='log-uniform', name='gamma')]

elif (args["model"] == models[2]):
    # Random Forest
    space  = [Integer(1, 200, name='n_estimators'),
            Integer(1, 1000, name='max_depth'),
            Integer(2, 100, name='min_samples_split'),
            Integer(1, 100, name='min_samples_leaf')]

else:
    # Adaboost
    space  = [Integer(1, 200, name='n_estimators'),
            Real(1e-6, 1e+1, prior='log-uniform', name='learning_rate'),
            Categorical(['SAMME', 'SAMME.R'], name='algorithm')]


# this decorator allows your objective function to receive a the parameters as
# keyword arguments. This is particularly convenient when you want to set scikit-learn
# estimator parameters
@use_named_args(space)
def objective(**params):

    return -1.0 * train_evaluate(X_train, y_train, args["model"], params)


if (args["optimizer"] == optimizers[0]):
    result_hpo = forest_minimize(objective, space, n_calls=args["ncalls"], random_state=0)
elif (args["optimizer"] == optimizers[1]):
    result_hpo = gbrt_minimize(objective, space, n_calls=args["ncalls"], random_state=0)
else:
    result_hpo = gp_minimize(objective, space, n_calls=args["ncalls"], random_state=0)


print("----------")
print("Clf: " + args["model"])
print("Best score=%.4f" % result_hpo.fun)


print(result_hpo.x)

if (args["model"] == models[0]):
    print("""Best parameters:
        - criterion=%s
        - max_depth=%d
        - min_samples_split=%d
        - min_samples_leaf=%d"""
        % (result_hpo.x[0], result_hpo.x[1], 
            result_hpo.x[2], result_hpo.x[3]))

elif (args["model"] == models[1]):
    print("""Best parameters:
        - C=%f
        - kernel=%s
        - degree=%d
        - gamma=%f"""
        % (result_hpo.x[0], result_hpo.x[1], 
            result_hpo.x[2], result_hpo.x[3]))

elif (args["model"] == models[2]):
    print("""Best parameters:
            - n_estimators=%d
            - max_depth=%d
            - min_samples_split=%d
            - min_samples_leaf=%d"""
            % (result_hpo.x[0], result_hpo.x[1], 
                result_hpo.x[2], result_hpo.x[3]))
else:
    print("""Best parameters:
        - n_estimators=%d
        - learning_rate=%f
        - algorithm=%s"""
        % (result_hpo.x[0], result_hpo.x[1], 
            result_hpo.x[2]))


axes = plot_convergence(result_hpo)

# axes = plot_evaluations(result_hpo, bins=10)
fig = axes2fig(axes, figsize=(16,12))
plt.show()