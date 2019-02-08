import os
import sys

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
	sys.path.append(module_path)
import pandas as pd

from FAA import Ohare
from FAA import Hanger
from FAA.model_airplanes import AirportModels
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import *


def print_metrics(y_true, y_prediction):
	f1 = f1_score(y_true, y_prediction)
	presc = precision_score(y_true, y_prediction)
	auc = roc_auc_score(y_true, y_prediction)
	recl = recall_score(y_true, y_prediction)
	
	print(
		f'The F1 Score is: {f1}\n The Precision score is: {presc}\n The Recall Score is: {recl} \n The AUC score is {auc}'
		)
	print(confusion_matrix(y_true, y_prediction, labels=[True, False]))


# no_write
faa = Ohare.Ohare(table_name='ord_w_wthr', sql=True \
                  , sql_user='ubuntu', host_name='localhost')


db = faa.get_modeling_df()
modeling = AirportModels(db)


# ######################################################################################
# #Random Forest Hyperparameter Search
#
# ## Pre over-sampling
# grid_search_rf = GridSearchCV(modeling.rf, {'n_estimators': [12, 50, 100, 500]
#                                         ,'max_depth': [5, 10, 20]
#                                         ,'criterion': ['gini', 'entropy']
#                                         ,'max_features': ['auto', 'log2']
#                                         ,'n_jobs': [-1]
#                                         ,'random_state': [51]
#                                         })
#
#
# X, y = modeling.get_training_setsXY()
#
# grid_search_rf.fit(X,y)
#
#
#
# print('RANDOM FOREST HYPERPARAMETER SEARCH RESUTS')
# print(grid_search_rf.cv_results_)
#
# print('#################################################')
# print('BEST SCORE')
# print(grid_search_rf.best_score_)
#
#
# print('#################################################')
# print('BEST PARAMETERS')
# print(grid_search_rf.best_params_)


######################################################################################
#Logistic Regression Hyperparameter Search
grid_search_lr = GridSearchCV(modeling.logr, {'penalty': ['l1', 'l2']
                                              ,'C': [1.0, 2**-1, 2**-2, 2**-4, 2**-10]
                                              ,'random_state': [51]
                                              #, 'solver': ['liblinear', 'saga', 'newton-cg']
                                              , 'n_jobs': [-1]})

X_scl, y_scl = modeling.get_scaled_training_setsXY()

grid_search_lr.fit(X_scl, y_scl)

print('LOGISTIC REGRESSION HYPERPARAMETER SEARCH RESULTS')
print(grid_search_lr.cv_results_)

print('#################################################')
print('BEST SCORE')
print(grid_search_lr.best_score_)


print('#################################################')
print('BEST PARAMETERS')
print(grid_search_lr.best_params_)

with open('logistic_reg_hyp_params.out', 'w') as fl:
	fl.write('LOGISTIC REGRESSION HYPERPARAMETER SEARCH RESULTS')
	
	fl.write(grid_search_lr.cv_results_)
	
	fl.write('#################################################\nBEST SCORE')
	fl.write(grid_search_lr.best_score_)
	fl.write('#################################################\nBEST PARAMETERS')
	fl.write(grid_search_lr.best_params_)