from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.metrics import *
from sklearn.model_selection import cross_validate, cross_val_predict, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class AirportModels(object):
	
	metrics = ['roc_auc', 'f1', 'accuracy', 'precision', 'recall']
	rf = RandomForestClassifier()
	nb = GaussianNB()
	logr = LogisticRegression()
	
	def __init__(self, airport_df, split=.2):
		
		
		self.y = airport_df.Was_Delayed
		self.X = airport_df.drop(columns=['Was_Delayed'])
		
		self.X_traintest, self.X_holdout, self.y_traintest, self.y_holdout = train_test_split(self.X, self.y,
		                                                                                 random_state=51,
		                                                                  test_size=split)
		
		scaler = StandardScaler()
		scaler.fit(self.X_traintest)
		self.x_train_test_scaled = scaler.transform(self.X_traintest)
		
	def get_training_setsXY(self):
		
		return (self.X_traintest, self.y_traintest)
	
	def get_holdout_setsXY(self):
		return (self.X_holdout, self.y_holdout)
	
	def get_scaled_training_setsXY(self):
		return (self.x_train_test_scaled, self.y_traintest)
	
	
	def create_rand_forest(self, rfc):
		
		self.rf = rfc
	
	def create_nb(self, gnb):
		self.nb = gnb
	
	def create_logr(self, lr):
		self.logr = lr

	
	
	def cv_rand_forest(self):
		
		cv = cross_validate(self.rf, self.X_traintest, self.y_traintest, n_jobs=-1, cv=10, scoring=self.metrics,
		                    return_train_score=True)
		
		return cv #Printed?
	
	def cv_naive_bayes(self):
		cv = cross_validate(self.nb, self.X_traintest, self.y_traintest, n_jobs=-1, cv=10, scoring=self.metrics,
		                    return_train_score=True)
	
	def cv_log_regression(self):
		cv = cross_validate(self.logr, self.x_train_test_scaled, self.y_traintest, n_jobs=-1, cv=10, scoring=self.metrics,
		                    return_train_score=True)
		
	