# 03_ml_config.py
#
# Description:
# This file holds all static configuration variables for the Poverty-from-the-
# Sky ML pipeline.

import os
from sklearn.tree import DecisionTreeClassifier

######################
# 1. READ/WRITE DATA #
######################

DATA_PATH = os.path.join('..', '..', '..', 'Data', 'FinalData', 'BISP')
BISP_PATH = os.path.join(DATA_PATH, 'bisp_hh_income.csv')
SAT_PATH = os.path.join(DATA_PATH, 'bisp_satellite_data.csv')
CLEAN_DATA_PATH = os.path.join(DATA_PATH, 'bisp_sat_inc_data.csv')

LABEL = 'hhinc_2011'

######################
# 2. PREPROCESS DATA #
######################

TEST_SIZE = 0.3

#########################
# 4. FEATURE GENERATION #
#########################

# Feature groups
DAY_FEATURES = ['l7_2011_1', 'l7_2011_2', 'l7_2011_3', 'l7_2011_4', 'l7_2011_5',
                'l7_2011_6', 'l7_2011_7',
                'ratio_1_2', 'ratio_1_3', 'ratio_1_4', 'ratio_1_5', 'ratio_1_6',
                'ratio_1_7', 'ratio_2_3', 'ratio_2_4', 'ratio_2_5', 'ratio_2_6',
                'ratio_2_7', 'ratio_3_4', 'ratio_3_5', 'ratio_3_6', 'ratio_3_7',
                'ratio_4_5', 'ratio_4_6', 'ratio_4_7', 'ratio_5_6', 'ratio_5_7',
                 'ratio_6_7']

NIGHT_FEATURES = ['dmspols_2011', 'viirs_2012',
                  'dmspols_2011_imputed', 'viirs_2012_imputed']

ALL_FEATURES = ['dmspols_2011', 'viirs_2012',
                'dmspols_2011_imputed', 'viirs_2012_imputed',
                'l7_2011_1', 'l7_2011_2', 'l7_2011_3', 'l7_2011_4', 'l7_2011_5',
                'l7_2011_6', 'l7_2011_7',
                'ratio_1_2', 'ratio_1_3', 'ratio_1_4', 'ratio_1_5', 'ratio_1_6',
                'ratio_1_7', 'ratio_2_3', 'ratio_2_4', 'ratio_2_5', 'ratio_2_6',
                'ratio_2_7', 'ratio_3_4', 'ratio_3_5', 'ratio_3_6', 'ratio_3_7',
                'ratio_4_5', 'ratio_4_6', 'ratio_4_7', 'ratio_5_6', 'ratio_5_7',
                'ratio_6_7']


#######################
# 5. BUILD CLASSIFIER #
#######################

# Test grid to make sure everything works - limited models and parameters (regression)
GRID_TEST_REG = {
    'regressors': ['LinearRegression', 'Lasso', 'Ridge', 'LinearSVR',
                    'DecisionTreeRegressor', 'BaggingRegressor',
                    'GradientBoostingRegressor', 'RandomForestRegressor'],
    'LinearRegression': [
        {'n_jobs': -1}
    ],
    'Lasso': [
        {'alpha': alpha, 'max_iter': max_iter, 'selection': selection,
        'random_state': 0} \
        for alpha in (1e-2, ) \
        for max_iter in (1e3, ) \
        for selection in ('random', )
    ],
    'Ridge': [
        {'alpha': alpha, 'max_iter': max_iter, 'solver': solver,
        'random_state': 0} \
        for alpha in (1e-2, ) \
        for max_iter in (1e3, )  \
        for solver in ('cholesky', )
    ],
    'LinearSVR': [
        {'epsilon': epsilon, 'C': C, 'loss': loss, 'max_iter': max_iter,
        'random_state': 0} \
        for epsilon in (0, ) \
        for C in (1e-2, ) \
        for loss in ('epsilon_insensitive', ) \
        for max_iter in (1e3, )
    ],
    'DecisionTreeRegressor': [
        {'criterion': criterion, 'splitter': splitter, 'max_depth': max_depth,
        'max_features': max_features, 'random_state': 0} \
        for criterion in ('mse', ) \
        for splitter in ('best', ) \
        for max_depth in (1, ) \
        for max_features in ('sqrt', ) \
    ],
    'BaggingRegressor': [
        {'n_estimators': n_estimators, 'max_features': max_features,
        'random_state': 0, 'n_jobs': -1} \
        for n_estimators in (100, ) \
        for max_features in (1, )
    ],
    'GradientBoostingRegressor': [
        {'loss': loss, 'learning_rate': rate, 'n_estimators': n_estimators,
        'criterion': criterion, 'max_features': max_features,
        'random_state': 0} \
        for loss in ('ls', ) \
        for rate in (1e-4, )
        for n_estimators in (100, ) \
        for criterion in ('mse', ) \
        for max_features in ('sqrt', ) \
    ],
    'RandomForestRegressor': [
        {'n_estimators': n_estimators, 'criterion': criterion,
        'max_depth': max_depth, 'max_features': max_features, 'n_jobs': -1,
        'random_state': 0} \
        for n_estimators in (100, ) \
        for criterion in ('mse', ) \
        for max_depth in (1, ) \
        for max_features in ('sqrt', )
    ]
}

# Test grid to make sure everything works - limited models and parameters (classification)
GRID_TEST_CLASS = {
    'regressors': ['LinearSVC', 'DecisionTreeClassifier', 'BaggingClassifier',
                    'GradientBoostingClassifier', 'RandomForestClassifier'],
    'LinearSVC': [
        {'penalty': penalty, 'C': C, 'loss': loss, 'class_weight': class_weight,
        'random_state': 0} \
        for penalty in ('l2', 'l1') \
        for C in (1e-2, ) \
        for loss in ('squared_hinge', ) \
        for class_weight in ('balanced',)
    ],
    'DecisionTreeClassifier': [
        {'criterion': criterion, 'splitter': splitter, 'max_depth': max_depth,
        'max_features': max_features, 'random_state': 0} \
        for criterion in ('gini', ) \
        for splitter in ('best', ) \
        for max_depth in (1, ) \
        for max_features in ('sqrt', ) \
    ],
    'BaggingClassifier': [
        {'n_estimators': n_estimators, 'max_features': max_features,
        'random_state': 0, 'n_jobs': -1} \
        for n_estimators in (100, ) \
        for max_features in (1, )
    ],
    'GradientBoostingClassifier': [
        {'loss': loss, 'learning_rate': rate, 'n_estimators': n_estimators,
        'criterion': criterion, 'max_features': max_features,
        'random_state': 0} \
        for loss in ('deviance', ) \
        for rate in (1e-4, ) \
        for n_estimators in (100, ) \
        for criterion in ('friedman_mse', ) \
        for max_features in ('sqrt', ) \
    ],
    'RandomForestClassifier': [
        {'n_estimators': n_estimators, 'criterion': criterion,
        'max_depth': max_depth, 'max_features': max_features, 'n_jobs': -1,
        'random_state': 0} \
        for n_estimators in (100, ) \
        for criterion in ('gini', ) \
        for max_depth in (1, ) \
        for max_features in ('sqrt', )
    ]
}

# Main grid - most exhaustive option (regression)
GRID_MAIN_REG = {
    'regressors': ['LinearRegression', 'Lasso', 'Ridge', 'LinearSVR',
                    'DecisionTreeRegressor', 'BaggingRegressor',
                    'GradientBoostingRegressor', 'RandomForestRegressor'],
    'LinearRegression': [
        {'n_jobs': -1}
    ],
    'Lasso': [
        {'alpha': alpha, 'max_iter': max_iter, 'selection': selection,
        'random_state': 0} \
        for alpha in (1e-2, 1e-1, 1e0, 1e1, 1e2) \
        for max_iter in (1e3, 1e4, 1e5) \
        for selection in ('cyclic', 'random')
    ],
    'Ridge': [
        {'alpha': alpha, 'max_iter': max_iter, 'solver': solver,
        'random_state': 0} \
        for alpha in (1e-2, 1e-1, 1e0, 1e1, 1e2) \
        for max_iter in (1e3, 1e4, 1e5)  \
        for solver in ('svd', 'cholesky', 'lsqr', 'sparse_cg')
    ],
    'LinearSVR': [
        {'epsilon': epsilon, 'C': C, 'loss': loss, 'max_iter': max_iter,
        'random_state': 0} \
        for epsilon in (0, 0.1, 0.2, 0.3) \
        for C in (1e-2, 1e-1, 1e0, 1e1, 1e2) \
        for loss in ('epsilon_insensitive', 'squared_epsilon_insensitive') \
        for max_iter in (1e3, 1e4, 1e5)
    ],
    'DecisionTreeRegressor': [
        {'criterion': criterion, 'splitter': splitter, 'max_depth': max_depth,
        'max_features': max_features, 'random_state': 0} \
        for criterion in ('mse', 'friedman_mse', 'mae') \
        for splitter in ('best', 'random') \
        for max_depth in (1, 5, 10, 20) \
        for max_features in ('sqrt', 'log2', None) \
    ],
    'BaggingRegressor': [
        {'n_estimators': n_estimators, 'max_features': max_features,
        'random_state': 0, 'n_jobs': -1} \
        for n_estimators in (100, 1000, 10000) \
        for max_features in (0.3, 0.5, 1.0)
    ],
    'GradientBoostingRegressor': [
        {'learning_rate': rate, 'n_estimators': n_estimators,
        'criterion': criterion, 'max_features': max_features,
        'random_state': 0} \
        for rate in (1e-4, 1e-3, 1e-2, 1e-1)
        for n_estimators in (100, 1000, 10000) \
        for criterion in ('mse', 'friedman_mse', 'mae') \
        for max_features in ('sqrt', 'log2', None) \
    ],
    'RandomForestRegressor': [
        {'n_estimators': n_estimators, 'criterion': criterion,
        'max_depth': max_depth, 'max_features': max_features, 'n_jobs': -1,
        'random_state': 0} \
        for n_estimators in (10, 100, 1000) \
        for criterion in ('mse', 'mae') \
        for max_depth in (1, 5, 10, 20) \
        for max_features in ('sqrt', 'log2', None)
    ]
}

# Main grid - most exhaustive option (classification)
GRID_MAIN_CLASS = {
    'regressors': ['LinearSVC', 'DecisionTreeClassifier', 'BaggingClassifier',
                   'AdaBoostClassifier', 'KNeighborsClassifier', 'RandomForestClassifier', 
                   'GradientBoostingClassifier'],
    'LinearSVC': [
        {'penalty': penalty, 'C': C, 'loss': loss, 'max_iter': max_iter,
        'random_state': 0} \
        for penalty in ('l2', ) \
        for C in (1e-2,1,2) \
        for loss in ('epsilon_insensitive','squared_hinge', ) \
        for max_iter in (1e1, )
    ],
    'DecisionTreeClassifier': [
        {'criterion': criterion, 'splitter': splitter, 'max_depth': max_depth,
        'max_features': max_features, 'random_state': 0} \
        for criterion in ('gini', ) \
        for splitter in ('best', ) \
        for max_depth in (1,2,3,4, 5, 10, 20, 30, 50, 70, 100, ) \
        for max_features in ('sqrt', ) \
    ],
    'BaggingClassifier': [
        {'n_estimators': n_estimators, 'max_features': max_features,
        'random_state': 0, 'n_jobs': -1} \
        for n_estimators in (10, 50, 100, 1000,) \
        for max_features in (0.1, 0.2, 0.3,0.4, 0.5, 1.0,)
    ],
    'AdaBoostClassifier': [
        {'n_estimators': n_estimators, 
         'base_estimator': base_estimator,
        'random_state': 0} \
        for n_estimators in (5, 10, 50, 100) \
        for base_estimator in (None, 
                                DecisionTreeClassifier(max_depth=2), 
                                DecisionTreeClassifier(max_depth=5),
                              	DecisionTreeClassifier(max_depth=6),
                              	DecisionTreeClassifier(max_depth=10),
                              	DecisionTreeClassifier(max_depth=15))
    ],
    'KNeighborsClassifier': [
        {'n_neighbors': n_neighbors} \
        for n_neighbors in (2,5,10,15,) 
    ],
    'RandomForestClassifier': [
        {'n_estimators': n_estimators, 'criterion': criterion,
        'max_depth': max_depth, 'max_features': max_features, 'n_jobs': -1,
        'random_state': 0} \
        for n_estimators in (5, 10, 100, 1000, 5000) \
        for criterion in ('gini', ) \
        for max_depth in (1,2,3,4,5,6,7,8,9,10, ) \
        for max_features in ('sqrt','log2',None, )
    ],
    'GradientBoostingClassifier': [
        {'loss': loss, 'learning_rate': rate, 'n_estimators': n_estimators,
        'criterion': criterion, 'max_features': max_features,
        'random_state': 0} \
        for loss in ('deviance', ) \
        for rate in (1e-4, )
        for n_estimators in (100, ) \
        for criterion in ('friedman_mse', ) \
        for max_features in ('sqrt', ) \
    ]
}
