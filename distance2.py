import pandas as  pd
import csv, sqlite3, sys
import datetime
 
 
def main(city,dist,dbname):
    conn = sqlite3.connect(dbname)
    query = "select x.*, y.* from city as x, city as y where x.data_load_date= y.data_load_date and x.City=\""+city+"\""
    df = pd.read_sql_query( query, conn)
    latitude = df['Latitude']
    longitude = df['Longitude']
    df['distance'] = 68.35*(((latitude.iloc[:,0]-latitude.iloc[:,1])**2 + (longitude.iloc[:,0]-longitude.iloc[:,1])**2)**0.5)
    city = df['City']
    df['Origin_City'] = city.iloc[:,0]
    state = df['State']
    df['Origin_State'] = state.iloc[:,0]
    high = df['temp']
    df['second_city_temp'] = high.iloc[:,1]
    low = df['humidity']
    df['second_city_humidity'] = low.iloc[:,1]
    mf = df[['Origin_City', 'Origin_State', 'City','second_city_temp', 'second_city_humidity','distance']]
    odf = mf[mf['distance'] < int(dist)].groupby('Origin_City').agg({'second_city_temp':['mean'],'second_city_humidity':['mean'],'distance':['count']})
    odf.columns=['mean_temp','mean_humidity','num_cities_in_radius']
    odf['given_radius_in_miles'] = dist
    odf = odf.reset_index()
    print(odf.iloc[0,:].to_dict())
    
# call main function    
if __name__ == '__main__':
    if(len(sys.argv)==4):
            main(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
            print("Error - usage python distance.py <City> <distance> <database>")