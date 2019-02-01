#!/usr/bin/env bash


# """Given a folder of monthly flight data, populate a postgresql database with its data."""

#Arguments
# $1 BTA File Path
# $2 DB Name
# $3 Table Name
# $4 Postgres User Name



FILES=/Users/bjg/Metis/Projects/McNulty/FlightOnTime/data/bts_on_time_reports/*
for month in $FILES
do
    #echo "Processing $month file..."
    grep ORD $month > tmp.txt
    psql -c "copy \"HEAD_TST\" from '/Users/bjg/Metis/Projects/McNulty/FlightOnTime/scripts/tmp.txt' delimiters ',' csv;" faa

done
