import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from FAA import Ohare
from FAA import Hanger
import pickle


#Airline Departure Stats
faa = Ohare.Ohare(sql=True)
al_dep = Hanger.Hanger.get_airline_departures(faa.flights_from_ohare)
with open('../data/server_runs/departure_by_airlines.json.pkl', 'w') as json_fl:
	pickle.dump(al_dep, json_fl)
json_fl.close()
#############