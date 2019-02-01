#!/usr/bin/env python
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import pandas as pd
from sqlalchemy import create_engine

"""Create a table with the defaul headers for the BTS on-time records. Arg 1 = username, Arg 2= table-name"""

username = sys.argv[1]

params = { 'host': 'localhost',
           'port': 5432
}
connection_string = f'postgres://{username}:{params["host"]}@{params["host"]}:{params["port"]}/faa'

engine = create_engine(connection_string)

schema = pd.read_csv('../data/ohare/column_definitions.csv')

schema.to_sql(sys.argv[2], engine, index=False)


