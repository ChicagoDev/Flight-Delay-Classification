#!/usr/bin/env bash


# """Given a folder of monthly flight data, populate a postgresql database with its data."""

#Arguments
# $1 BTA File Path
# $2 DB Name
# $3 Table Name
# $4 Postgres User Name


data/zips/2017-2018_BTS_ON_TM
FILES=/Users/bjg/Metis/Projects/McNulty/FlightOnTime/data/zips/2017-2018_BTS_ON_TM/*
for month in $FILES
do
    echo "Processing $month file..."
    grep ORD $month > ord.tmp.txt
    sed s/\"\"//g ord.tmp.txt > tmp.txt
    psql -c "copy \"ORD_IB_OB\" from '/Users/bjg/Metis/Projects/McNulty/FlightOnTime/scripts/tmp.txt' delimiters ',' csv;" faa

done
