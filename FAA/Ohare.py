import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from collections import defaultdict


class Ohare(object):
	"""
	faa = OrdUtils()

	faa.get_ob_delays()

	faa.get_ib_delays()

	faa.get_baselines()

	faa.get_mini_ob_flights()
	"""
	
	regions = {'SE': ['ATL', 'DFW'],
	           'SW': ['LAX', 'LAS'],
	           'NW': ['SFO', 'DEN'],
	           'NE': ['JFK', 'EWR']
	           }
	
	def __init__(self, monthly_tffx_csv='../data/ohare/01_2018_ORD_AIR_TFFX.csv'):
		
		self.ord_flights = pd.read_csv(monthly_tffx_csv, low_memory=False)
		
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
