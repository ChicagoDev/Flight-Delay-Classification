# FlightOnTime

## Project 3 at Metis
This project is a supervised machine learning program. The goal objective is to determine whether an outbound flight from O'Hare airport will or will not be delayed.

### Directory Structure

* FAA - Main Codebase
  * Ohare.py
    * Loads database
    * Creates DataFrame of outbound data
    * Calculated attributes 
    * Creates a modeling DataFrame
  * Hanger.py
    * Static miscellaneous methods. Creates charts and Data 'views'
  * model_airplanes.py
    * Helpers for creating training sets from airport data 
* data/ 
* docs/
* notebooks/ - EDA and Modeling
  * Modeling v2.ipynb 
* scripts/ - Unix and SQL scripts used for loading data 

[Blog Post](http://www.chicagoan.io/project-mcnulty/)

### Data Sources
[Bureau of Transportation](https://www.bts.gov/browse-statistical-products-and-data/bts-publications/airline-service-quality-performance-234-time)

[Weather.gov](weather.gov) 