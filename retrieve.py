import urllib3, urllib, json, urllib.request
import pandas as  pd
import csv, sqlite3, sys
import datetime
import pytz

def db_connect(dbfile):
    today = str(datetime.date.today())
    try:
        conn = sqlite3.connect(dbfile)
        return conn
    except:
        print("Error opening database file")
        sys.exit()

def month_to_num(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return months.index(month) + 1

def main(param, dbfile):
    today = str(datetime.date.today())

    # 1. open all files for output
    try:
        df = pd.read_csv(param)
    except:
        print("Error: Cannot open input file for list of cities")
        sys.exit()

    errorlog = "error-"+today+".log"
    try:
        logf = open(errorlog, "w")
    except:
        print("Error: Cannot open Error Log file")
        sys.exit()

    outputcityfile = "op-"+today+".data"
    try:
        cityfile = open(outputcityfile, "w")
    except:
        print("Error: Cannot open Output City  file")
        sys.exit()

    outputforecastfile = "forecast-"+today+".data"

    try:
        forecastfile = open(outputforecastfile, "w")
    except:
        print("Error: Cannot open Output City  file")
        sys.exit()

    

    # the main loop to retrieve all data
    for index,row in df.iterrows():
        #2. set up the URL
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\"" +df.iloc[index,0]+ "," + df.iloc[index,1] + "\") "
        yql_url = baseurl + urllib.parse.urlencode({'q':yql_query}) + "&format=json"
        # 3. make the request
        try:
            result = urllib.request.urlopen(yql_url).read()
            data = json.loads(result)
            
            # 4. store city wide data in file
            
            cityfile.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11}\n".format(df.iloc[index,0],df.iloc[index,1], data['query']['created'].split("T")[0], data['query']['results']['channel']['location']['city'], data['query']['results']['channel']['location']['region'], data['query']['results']['channel']['item']['lat'], data['query']['results']['channel']['item']['long'],data['query']['results']['channel']['wind']['speed'],data['query']['results']['channel']['wind']['chill'],data['query']['results']['channel']['atmosphere']['humidity'],data['query']['results']['channel']['atmosphere']['pressure'],data['query']['results']['channel']['item']['condition']['temp']))

            # 5. store forecast data in forecast file
            for i in data['query']['results']['channel']['item']['forecast']:
                # look for debug option next iteraiton
                #print(data['query']['results']['channel']['item']['forecast'])
                date = i['date'].split()
                datewrite = date[2]+"-"+str(month_to_num(date[1]))+"-"+date[0]
                #print(datewrite)
                forecastfile.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(data['query']['created'].split("T")[0],data['query']['results']['channel']['location']['city'],data['query']['results']['channel']['location']['region'],data['query']['results']['channel']['item']['lat'], data['query']['results']['channel']['item']['long'],datewrite, i['low'], i['high'],data['query']['results']['channel']['wind']['speed'],data['query']['results']['channel']['wind']['chill'],data['query']['results']['channel']['atmosphere']['humidity']))
            
        except Exception as e: 
                    # print(e)
                    #print("Error for" + df.iloc[index,0]+ "," + df.iloc[index,1])
                    logf.write("Error for {0},{1}\n".format(str(df.iloc[index,0]), str(df.iloc[index,1])))

    #5b - Clean up close all files

    forecastfile.close()
    cityfile.close()
    logf.close()
    #6. Connect to the database file
    conn = db_connect(dbfile)
    curs = conn.cursor()
    #7. Create forecast table if not already created
    try: 
        curs.execute("CREATE TABLE if not exists forecast (id INTEGER PRIMARY KEY, data_load_date TEXT, City TEXT, State TEXT, Latitude REAL, Longitude REAL, Forecast_date TEXT, Low REAL, High REAL,wind_speed REAL, wind_chill REAL, humidity REAL );")
    except:
        print("Error Creating Forecast Table")

    #8. Store data in forecast table
    try: 
        readfile = csv.reader(open(outputforecastfile, 'r'), delimiter=',')
    except:
        print("Error opening forecast file for reading ")

    for i in readfile:
        curs.execute("INSERT INTO forecast (data_load_date, City, State, Latitude, Longitude, Forecast_date, Low, High,wind_speed, wind_chill,humidity) VALUES (?, ?, ?,?,?,?,?,?,?,?,?);",i)
    conn.commit()

    #9. Create city table if not already created
    try: 
        curs.execute("CREATE TABLE if not exists city (id INTEGER PRIMARY KEY, requested_city, requested_state, data_load_date TEXT, City TEXT, State TEXT, Latitude REAL, Longitude REAL, wind_speed REAL, wind_chill REAL, humidity REAL, pressure REAL, temp real );")
    except:
        print("Error Creating Forecast Table")

    #10. Store data in city table
    try: 
        readfile2 = csv.reader(open(outputcityfile, 'r'), delimiter=',')
    except:
        print("Error opening City file for reading ")

    for i in readfile2:
        curs.execute("INSERT INTO city (requested_city, requested_state,data_load_date, City, State, Latitude, Longitude, wind_speed,wind_chill, humidity,pressure,temp) VALUES (?, ?, ?,?,?,?,?,?,?,?,?,?);",i)
    conn.commit()





# call main function    
if __name__ == '__main__':
    if(len(sys.argv)==3):
            main(sys.argv[1],sys.argv[2])
    else:
            print("Error - usage python retrieve.py <file with list of cities> <db file>")
