# CodeChallenge - Date 12/7/2018
This git is a repsonse to Code challenge received on 12/7/2018

# Requirements
The requirements of the code challenge are in the [pdf file](https://github.com/Ever-Flows/CodeChallengeDec/blob/master/Housecall%20Pro%20Data%20Solutions%20Architect%20Assessment.pdf) in this repository. 

# Setup
Assumption 
* **Anaconda is installed** - on MAC type - brew install conda

# Steps for setup
No new modules need to be installed
* **Create codech environment** type in terminal window: conda create -n codech python=3.6
* **Activate environment** type in terminal window: source activate codech
* **Check modules** - Compare with modules in [modules.txt](https://github.com/Ever-Flows/CodeChallengeDec/blob/master/modules.txt)

# Usage
* *python retrieve.py ci.csv weather-2018-12-08.sl3* runs the code and meets all requirements outlined Exercise 1.1 of  the requirements pdf files. It creates two tables in the output sqllite3 file. One for City data and the other for forecast as requested. The program frst retrives the data and stores in csv files and subsequently updartes the database.

* *python table2.py forecast-2018-12-08.data weather-2018-12-08.sl3* helps with requirement 1.2 and creates the table in the input sqllite2 database file. the table is names forecast5days

* *python distance2.py "Kansas City" 100 weather-2018-12-08.sl3* helps with requirement in Exercise 3. It outputs the json data as requested giving the count and mean temp/humidity for the cities in the provided radius.



# Other Files
* **.data files* as retrieved from the Yahoo API
* *error.log files* are for data retrieval errors
* **.sl3 files* are sqllite3 files
* **.sql files* are mysql scripts

# Test environment
* On Apple Mac

# Exercise 1

1. Two python scripts - retrieve.py - retreives data from API and stores in database provided 
2. python script - table2
3. Comments in file. To make the scripts more robust
*  update for environments
* shutdowns
* partial runs and 
* less than 10 days forecast
* also change database to hold more data if needed
4. For expectations 
* will make sure that the tables meet the requirements 
* and if forecast for next 10 days need to be stored for every pull
* Also look at data retention and adjust script accordingly
* Wind chill and Wind speed are not available as forecasts - so will confirm that - probably move to another API


# Exercise 2
* fill.sql script is attached. It is for mysql. It sis not complete and not tested. Requires more work but works out the design and is close to full implementation. The script is easier in [MS SQL] (https://koukia.ca/common-sql-problems-filling-null-values-with-preceding-non-null-values-ad538c9e62a6) but requires a lot more work on mysql.
* The problem is trivial if we use Python to forward fill the nulls as demonstrated in fillforward.py. The Python script assumes database and tables are set up using the fill2.sql script. This is tested and works as required.


# Exercise 3

1. code in distance2.py
2. to make script better
* adapt for environment, 
* address machine reboots
* multiple runs
* give a list of cities
* adapt to different ways of entering
* check for states too
3. For get http requests 
* not much change is needed 
* set up the api and make sure that the API gateway requests and have access to the database. 
* challenges - city names not match or found - may not be adapted the way it is requested
   assumptions - database is available on the server


# Misc 
All data files and database files are in the repo







