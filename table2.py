import urllib3, urllib, json, urllib.request
import pandas as  pd
import csv, sqlite3, sys
import datetime


def db_connect(dbfile):
    today = str(datetime.date.today())
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except:
        print("Error opening database file")
        sys.exit()

def main(file,dbname):
    today = str(datetime.date.today())
    avoutputfile = "av-"+today+".data"
    try:
        avfile = open(avoutputfile, "w")
    except:
        print("Error: Cannot open Output Average  file")
        sys.exit()

    try:
        df = pd.read_csv(file,header=None,delimiter=",", names = ['data_load_date' , 'City' , 'State' , 'Latitude' , 'Longitude', 'Forecast_date', 'Low', 'High','wind_speed', 'wind_chill', 'humidity'])
    except:
        print("Error: Cannot open input file for list of cities")
        sys.exit()
    for rows in range(0,df.shape[0]-5,10):
        #for columns in range(0,df.shape[1]-1):
            if(df.iloc[rows,1] == df.iloc[rows+5,1]):
                if(df.iloc[rows,0] == df.iloc[rows+5,0]):
                    sum_temp=0
                    for k in range(rows+1,rows+6):
                        #print(rows,":",k,":", df.iloc[rows,1],":",df.iloc[k,7])
                        sum_temp = sum_temp + df.iloc[k,7]
                    avfile.write("{0},{1},{2},{3},{4}\n".format(df.iloc[rows,0],df.iloc[rows,1],df.iloc[rows,2],sum_temp/5,df.iloc[rows,8]))
    
    avfile.close()
    conn = db_connect(dbname)
    curs = conn.cursor()
    # Create forecast5days table if not already created
    try: 
        curs.execute("CREATE TABLE if not exists forecast5days (id INTEGER PRIMARY KEY, data_load_date TEXT, City TEXT, State TEXT,  Av5High REAL,wind_speed REAL );")
    except:
        print("Error Creating forecast5days Table")

    #Store data in forecast5days table
    try: 
        readfile2 = csv.reader(open(avoutputfile, 'r'), delimiter=',')
    except:
        print("Error opening Av5days file for reading ")

    for i in readfile2:
        curs.execute("INSERT INTO forecast5days (data_load_date, City, State, Av5High, wind_speed) VALUES (?, ?, ?,?,?);",i)
    conn.commit()



# call main function    
if __name__ == '__main__':
    if(len(sys.argv)==3):
            main(sys.argv[1],sys.argv[2])
    else:
            print("Error - usage python table2.py <file with forecast date> <db file>")
