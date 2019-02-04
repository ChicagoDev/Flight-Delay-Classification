#!/usr/bin/env bash

faa_db_scripts/create_db_headers.py

psql -f update_faa_schema.sql FLIGHT_TEST

faa_db_scripts/create_db.sh


