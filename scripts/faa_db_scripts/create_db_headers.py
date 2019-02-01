#!/usr/bin/env python

"""Prereq: First create the faa database in Postgres.
    This script creates the schema of the whole planes database, by outputting a pandas df
    to sql. The database is populated with one row. The row must be removed, and some columns
    need to be declared to accept text: which is done in update_schema.sql"""

import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
import pandas as pd
from sqlalchemy import create_engine
from FAA import Ohare

faa = Ohare.Ohare()

schema = faa.ord_flights.head(1)

username = 'bjg' # or 'ubuntu'
database_name = 'ORD_IB_OB'

params = { 'host': 'localhost',
           'port': 5432
}

connection_string = f'postgres://{username}:{params["host"]}@{params["host"]}:{params["port"]}/faa'

engine = create_engine(connection_string)

schema.to_sql(database_name, engine, index=False)


