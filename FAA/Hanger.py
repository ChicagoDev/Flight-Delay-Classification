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
	def get_airline_departures(outbound_flights_df, return_type='json'):
		
		airport_volume = len(outbound_flights_df)
		
		late_dep = outbound_flights_df[outbound_flights_df.DepDelay > 0]  #O(n)
		early_dep = outbound_flights_df[outbound_flights_df.DepDelay <= 0] #O(n) ... could combine these into an if
		
		total_flights = outbound_flights_df.groupby('Reporting_Airline')
		
		total_flights = total_flights.size() #I only need to do the
		# groupby once, and then reference it again...
		
		total_flights = total_flights.rename(columns={0: 'Total_Departures'})
		
		
		
		## Append the LATE departure Stats
		late_departures = late_dep.groupby('Reporting_Airline')
		
		total_flights = pd.concat([total_flights, late_departures.count()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Late_Departures'})
		
		total_flights = pd.concat([total_flights, late_departures.mean()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Avg_Delay'})
		
		total_flights = total_flights.rename(columns={0: 'Total_Departures'})
		
		# Append the EARLY departure stats
		early_departures = early_dep.groupby('Reporting_Airline')
		
		total_flights = pd.concat([total_flights, early_departures.count()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Early_Departures'})
		
		total_flights = pd.concat([total_flights, early_departures.mean()[['DepDelay']]], axis=1)
		total_flights = total_flights.rename(columns={'DepDelay': 'Avg_Early_Minutes_SVD'})
		
		# Append Misc stats
		total_flights['Port_Traffic_Share'] = 100 * total_flights['Total_Departures'] / airport_volume
		
		total_flights['Percent_Late_Departures'] = total_flights['Late_Departures'] / total_flights['Total_Departures']
		
		if return_type == 'json':
			return total_flights.to_json()
		else:
			return total_flights
		
	@staticmethod
	def flights_per_day(flight_bts_df):
		fpd = flight_bts_df.groupby(flight_bts_df['DayOfWeek']).count()[['Year']]
		days = pd.DataFrame(['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'], index=[1, 2, 3, 4, 5, 6, 7])
		days_flights = pd.concat([days, fpd], axis=1)
		return days_flights.rename(columns={'Year': 'Flights', 0: 'Day'})
	
	@staticmethod
	def daily_delays(flight_bts_df):
		"""By day of week, return DF with number of flights and number of delays"""
		fly_by_day = Hanger.flights_per_day(flight_bts_df)
		
		delays = flight_bts_df.groupby(flight_bts_df['DayOfWeek']).sum()[['DepDel15']].DepDel15
		
		return pd.concat([fly_by_day, delays], axis=1)

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