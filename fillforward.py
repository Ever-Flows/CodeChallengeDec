
# Import all modules including SQLAlchemy to develop general set up
import sqlalchemy as db
# Import credentials from local file - not to be passed to github
from config import dbuser, dbpasswd, dburi, dbport, dbname
import pymysql
pymysql.install_as_MySQLdb()
import pandas as pd

# Create Engine
try: 
    engine = db.create_engine(f"mysql://{dbuser}:{dbpasswd}@{dburi}:{dbport}/{dbname}")
    print("New table uploaded after forward fill")

except:
    print("Error: Creating Engine")

# Create connection to database
#engine = db.create_engine('sqlite:///census.sqlite')
connection = engine.connect()
metadata = db.MetaData()

# Set up the query to retrieve table
pcyear = db.Table('planforcalendaryear', metadata, autoload=True, autoload_with=engine)

query = db.select([pcyear])

# Execute the query
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()

# Query and load results into a dataframe
df=pd.read_sql_query(query,engine)

# Forward fill the dataframe
df = df.fillna(method='ffill')

# write the dataframe to a new table
try:
    df.to_sql('planforcalendaryear1', con=engine, if_exists='replace',index_label='id')
except: 
    print("Error writing the fill forward dataframe to the database")