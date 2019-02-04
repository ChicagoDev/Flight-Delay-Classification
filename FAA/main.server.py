#!/usr/bin/env python3
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from FAA import Ohare
from FAA import Hanger
import pickle

if sys.argv[1] == 'local':
	faa = Ohare.Ohare(sql=True, sql_user='bjg', db_name='FLIGHT_TEST')

else:
	faa = Ohare.Ohare(sql=True, sql_user='ubuntu', db_name='ORD_IB_OB')


#Airline Departure Stats
"""This snippet produces as dataframe that is indexed by Airline. The columns/stats are the total departures. Ontime
and late departure totals. The ratios of the late and early departures. Additionally, Shows how much of the airport's traffic is composed from each airline."""
airline_stats = Hanger.Hanger.get_airline_departures(faa.flights_from_ohare, return_type='not_json')
#############

# Get the cities with the largest outbound delays
city_ob_delays = faa.get_ob_delays()




###############

#What days of the week have the worst delays?
dow_delays = Hanger.Hanger.daily_delays(faa.flights_from_ohare)


###############

#Save the results

output = {
	'airline_delays': airline_stats,
	'city_ob_delays': city_ob_delays,
	'day_of_week_delays': dow_delays
}

with open('../data/server_runs/airport_stats.pkl', 'wb') as fl:
	pickle.dump(output, fl)
fl.close()