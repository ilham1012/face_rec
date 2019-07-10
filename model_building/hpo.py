import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix  
from skopt.space import Real, Integer
from skopt.utils import use_named_args
from skopt import gp_minimize
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize, forest_minimize, gbrt_minimize
from skopt.plots import plot_convergence, plot_evaluations

import constant
from util import train_evaluate, axes2fig, set_unknown, load_data


plt.set_cmap("viridis")

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument(
    "-m", "--model",
    default="svm",
    help="choose in ['dt', 'svm', 'rf', 'adaboost']"
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



# Load data
X_train, X_test, y_train, y_test = load_data('dataset/face_encodings.csv')


def find_optimal_hyperparam(model, optimizer, n_calls):
    # The list of hyper-parameters we want to optimize. For each one we define the bounds,
    # the corresponding scikit-learn parameter name, as well as how to sample values
    # from that dimension (`'log-uniform'` for the learning rate)
    space = []

    if (model == constant.MODELS[0]):
        # Decision Tree
        space  = [Categorical(['gini', 'entropy'], name='criterion'),
                Integer(1, 1000, name='max_depth'),
                Integer(2, 100, name='min_samples_split'),
                Integer(1, 100, name='min_samples_leaf')]

    elif (model == constant.MODELS[1]):
        # SVM
        space  = [Real(1e-6, 1e+6, prior='log-uniform', name='C'),
                Categorical(['linear', 'poly', 'rbf'], name='kernel'),
                Integer(1, 8, name='degree'),
                Real(1e-6, 1e+1, prior='log-uniform', name='gamma')]

    elif (model == constant.MODELS[2]):
        # Random Forest
        space  = [Integer(1, 200, name='n_estimators'),
                Integer(1, 1000, name='max_depth'),
                Integer(2, 100, name='min_samples_split'),
                Integer(1, 100, name='min_samples_leaf')]

    else:
        # Adaboost
        space  = [Integer(1, 200, name='n_estimators'),
                Real(1e-6, 1e-1, prior='log-uniform', name='learning_rate'),
                Categorical(['SAMME', 'SAMME.R'], name='algorithm')]


    # this decorator allows your objective function to receive a the parameters as
    # keyword arguments. This is particularly convenient when you want to set scikit-learn
    # estimator parameters
    @use_named_args(space)
    def objective(**params):
        return -1.0 * train_evaluate(X_train, y_train, model, params)


    if (optimizer == constant.OPTIMIZERS[0]):
        result_hpo = forest_minimize(objective, space, n_calls=n_calls, random_state=0)
    elif (optimizer == constant.OPTIMIZERS[1]):
        result_hpo = gbrt_minimize(objective, space, n_calls=n_calls, random_state=0)
    else:
        result_hpo = gp_minimize(objective, space, n_calls=n_calls, random_state=0)


    print("----------")
    print("Clf: " + model + " - opt: ", optimizer)
    print("Best score=%.4f" % result_hpo.fun)
    print("----------")


    # print(result_hpo.x)

    if (model == constant.MODELS[0]):
        print("""Best parameters:
            - criterion=%s
            - max_depth=%d
            - min_samples_split=%d
            - min_samples_leaf=%d"""
            % (result_hpo.x[0], result_hpo.x[1], 
                result_hpo.x[2], result_hpo.x[3]))

    elif (model == constant.MODELS[1]):
        print("""Best parameters:
            - C=%f
            - kernel=%s
            - degree=%d
            - gamma=%f"""
            % (result_hpo.x[0], result_hpo.x[1], 
                result_hpo.x[2], result_hpo.x[3]))

    elif (model == constant.MODELS[2]):
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

    return result_hpo

    # TODO: Save plot of convergence, evaluations, and objective to file 

    # axes = plot_convergence(result_hpo)
    # fig = axes2fig(axes, figsize=(16,12))
    # plt.show()

    # axes = plot_evaluations(result_hpo, bins=10)
    # fig = axes2fig(axes, figsize=(16,12))
    # plt.show()


# find_optimal_hyperparam(args["model"], args["optimizer"], args["ncalls"])

h_results = []
h_models = []
h_optimizers = []
h_params = []

for model in constant.MODELS:
    for optimizer in constant.OPTIMIZERS:
        result = find_optimal_hyperparam(model, optimizer, args["ncalls"])

        h_models.append(model)
        h_optimizers.append(optimizer)
        h_results.append(result.fun)
        h_params.append(result.x)


df1 = pd.DataFrame(list(zip(h_models, h_optimizers, h_results)), 
                   columns =['Classifier', 'Optimizer', 'Results'])

df2 = pd.DataFrame(h_params, columns =['x1', 'x2', 'x3', 'x4'])

print(df1)
print(df2)

df = pd.concat([df1, df2], axis=1, sort=False)
print(df)

df.to_csv('hpo_result.csv')