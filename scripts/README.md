# Steps to create database

`./create_ohare_db.sh`


* Create a Database on the Postgres Instance called FAA
* Run create_db_headers.py
    * Check username and database name
* Run update_schema.sql
    * First sed replace the table-name in the update file.
    * Ex: sed s/"HEAD_TST"/ORD_IB_OB/g update_schema.sql > update_all_flts_schema.sql
* Populate Database with a directory of BTA Files.
    * Use create_db.sh
    * Check name of database and table