import pandas as pd
import copy
import seaborn as sns

class Hanger(object):
	
	@staticmethod
	def monthly_delay_report(ports_outbound_flights):
		"""For a given airport's monthly records, return its categorical delay statistics"""
		
		only_with_delay_record = ports_outbound_flights.dropna(
			subset=['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay'])
		
		delays = pd.DataFrame(only_with_delay_record.loc[:, 'CarrierDelay':'LateAircraftDelay'].mean())
		delays = delays.reset_index()
		delays = delays.rename(columns={0: 'Time', 'index': 'Reason'})
		
		return copy.deepcopy(delays)
	
	@staticmethod
	def chart_monthly_delay_report(ports_outbound_flights):
		
		delays = Hanger.monthly_delay_report(ports_outbound_flights)
		sns.barplot(x=delays['Reason'], y=delays['Time'])
		
	@staticmethod
	def get_airline_departures(outbound_flights_df):
		airport_volume = len(outbound_flights_df)
		late_dep = outbound_flights_df[outbound_flights_df.DepDelay > 0]
		early_dep = outbound_flights_df[outbound_flights_df.DepDelay <= 0]
		
		total_flights = pd.DataFrame(outbound_flights_df.groupby('Reporting_Airline').size())
		
		total_flights = total_flights.rename(columns={0: 'Total_Departures'})
		
		## Append the LATE departure Stats
		total_flights = pd.concat([total_flights, late_dep.groupby('Reporting_Airline').count()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Late_Departures'})
		
		total_flights = pd.concat([total_flights, late_dep.groupby('Reporting_Airline').mean()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Avg_Delay'})
		
		# Append the EARLY departure stats
		total_flights = pd.concat([total_flights, early_dep.groupby('Reporting_Airline').count()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Early_Departures'})
		
		total_flights = pd.concat([total_flights, early_dep.groupby('Reporting_Airline').mean()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Avg_Early_Minutes_SVD'})
		
		# Append Misc stats
		total_flights['Port_Traffic_Share'] = 100 * total_flights['Total_Departures'] / airport_volume
		
		total_flights['Percent_Late_Departures'] = total_flights['Late_Departures'] / total_flights['Total_Departures']
		
		return total_flights.to_json()

"""

HANGER is a metaphorical construct. The place there airport objects are subclassed as
smaller set of fetures as trained on data... but not cross validated

forsee - airstrips takeoffs / landings as CV and charts?


For now, c/p my code from JN for tomorrow, will be classed


faa = Ohare()

ob_flights = faa.get_mini_ob_flights()

ob_flights = ob_flights.reset_index()

ob_flights = ob_flights.drop(labels='index', axis=1)

ob_flights_dum_al = ob_flights.merge(pd.get_dummies(ob_flights['Reporting_Airline']), left_index=True, right_index=True)

ob_flts_all_dms = ob_flights_dum_al.merge(pd.get_dummies(ob_flights_dum_al['Dest']), left_index=True, right_index=True)





ob_flts_all_dms = ob_flts_all_dms.dropna()
from sklearn.model_selection import train_test_split

y = ob_flts_all_dms['DepDelay']
X = ob_flts_all_dms.loc[:,'ArrDelay':]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .2, random_state=51)

average_delay_trn = np.mean(y_train)
np.mean(y_train)

for i in range (1, 8):
    print (f'The average delay for day of the week: {i}, is {np.mean(y_train[X_train.DayOfWeek == i])}.')


"""