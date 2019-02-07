import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from collections import defaultdict
from sqlalchemy import create_engine

class Ohare(object):
	"""
		ord_flights = all flights imported from csv.
	"""
	
	regions = {'SE': ['ATL', 'DFW'],
	           'SW': ['LAX', 'LAS'],
	           'NW': ['SFO', 'DEN'],
	           'NE': ['JFK', 'EWR']
	           }
	
	def __init__(self, monthly_tffx_csv='../data/ohare/test_files/01_2018_ORD_AIR_TFFX.csv', sql=False,
	             table_name='ORD_IB_OB',
	             sql_user='bjg', db_name='faa', host_name='localhost'):
		
		if sql == False:
			#Get the flight data from CSV, LEGACY
			self.ord_flights = pd.read_csv(monthly_tffx_csv, low_memory=False)
		else:
			# Get the flight data from the database
			username = sql_user  # or 'bjg'
			database_name = db_name
			params = {'host': host_name,
			          'port': 5432
			          }
			
			connection_string = f'postgres://{username}:{params["host"]}@{params["host"]}:{params["port"]}/{database_name}'
			
			#engine = create_engine(connection_string)
			
			self.ord_flights = pd.read_sql_table(table_name, connection_string)
			
		# Split the data between inbound and outbound flights
		mask_from_ord = self.ord_flights.Origin == 'ORD'
		mask_to_ord = self.ord_flights.Origin != 'ORD'
		self.flights_from_ohare = self.ord_flights[mask_from_ord]
		self.flights_to_ohare = self.ord_flights[mask_to_ord]
	
		self.baselines = self.get_baselines()
		
		
	
	def get_baselines(self):
		ob_del = self.flights_from_ohare.DepDelayMinutes.mean()
		ib_del = self.flights_to_ohare.DepDelayMinutes.mean()
		
		ob_taxi_del = self.flights_from_ohare.TaxiOut.max()
		ib_taxi_del = self.flights_to_ohare.TaxiOut.max()
		
		# ALL OHARE TRAFFIC
		return {
			
			'ob_del':     ob_del,
			'ib_del':     ib_del,
			'ob_taxi_tm': ob_taxi_del,
			'ib_taxi_tm': ib_taxi_del
		}
	
	def get_ports(self, port, column_name, df):
		"""Filters a DF on a given airport. Convenience Method"""
		mask = (df[column_name] == port)
		return df[mask]
	
	def get_ib_delays(self, as_df=True):
		"""For flights that are arriving to O'hare, how long are the delays?"""
		ohare_ib_delays = defaultdict(float)
		
		for reg, airports in self.regions.items():
			
			for port in airports:
				ohare_ib_delays[port] = self.get_ports(port, 'Origin', self.flights_to_ohare).DepDelayMinutes.mean()
		
		ohare_ib_delays['ORD_AVG'] = self.baselines['ib_del']
		
		if not as_df:
			return ohare_ib_delays
		else:
			return pd.DataFrame(ohare_ib_delays, index=[0])
	
	def get_ob_delays(self, as_df=True):
		"""For flights that are leaving from O'hare, how long are the delays?"""
		
		ohare_outb_delays = defaultdict(float)
		
		for reg, airports in self.regions.items():
			
			for port in airports:
				ohare_outb_delays[port] = self.get_ports(port, 'Dest', self.flights_from_ohare).DepDelayMinutes.mean()
		
		ohare_outb_delays['ORD_AVG'] = self.baselines['ob_del']
		
		if not as_df:
			return ohare_outb_delays
		else:
			return pd.DataFrame(ohare_outb_delays, index=[0])
	
	def get_mini_ob_flights(self):
		return self.flights_from_ohare[['DepDelay', 'Reporting_Airline', 'Dest', 'ArrDelay', 'Quarter', 'DayOfWeek']]

	def get_modeling_features(self):
		
		cols = self.flights_from_ohare.columns.tolist()
		
		features = cols[1:3] + cols[4:7] + cols[10:11] + cols[14:15] + cols[23:24] \
		           + cols[27:28] + cols[30:34] + cols[54:55] + cols[113:119]
		
		return features
	
	def append_dummies(self, df, column):
		
		df = pd.concat([df, pd.get_dummies(column)], axis=1)
		return df
	
	def time_cat(self, time_flt):
		# time categories - Early am, late am, early pm, late pm.
		
		if (time_flt <= 600):
			return 'early_am'
		elif (time_flt <= 1200):
			return 'late_am'
		elif (time_flt < 1800):
			return 'early_pm'
		else:
			return 'late_pm'
	
	def was_flight_delayed(self, time_flt):
		if time_flt > 0.0:
			return True
		else:
			return False
	
	def get_modeling_df(self):
		"""The dataframe to performe classification modeling is a subset of the all the data columns. This method
		filters out the unnecessary columns, and also gets dummy variables."""
		
		columns = self.get_modeling_features()
		
		modeling_df = self.flights_from_ohare[columns]
		
		modeling_df = self.append_dummies(modeling_df, modeling_df.Reporting_Airline)
		
		
		modeling_df = modeling_df.drop(columns=['DepDel15', 'Flight_Number_Reporting_Airline', 'Origin'\
                ,'DestStateName', 'DepDelayMinutes', 'pgtm', 'Dest'])
		
		modeling_df = modeling_df.drop(columns=['FlightDate']) # Probably want month
		
		time_dummies = pd.get_dummies(modeling_df[['DepTime']].applymap(lambda tm: self.time_cat(tm)))
		
		modeling_df = pd.concat([modeling_df, time_dummies], axis=1)
		
		modeling_df = modeling_df.drop(columns=['DepTime', 'Reporting_Airline'])
		
		was_delayed = modeling_df[['DepDelay']].applymap(lambda tm: self.was_flight_delayed(tm))
		was_delayed = was_delayed.rename(columns={'DepDelay': 'Was_Delayed'})
		
		modeling_df = pd.concat([modeling_df, was_delayed], axis=1)
		modeling_df = modeling_df.drop(columns=['DepDelay'])
		
		return modeling_df
		