'''
Created on 12 Mar 2018

@author: obyrned1
'''
import urllib.request
import json
import datetime
import csv
import time
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb


def getJsonData():
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    standData = json.loads(str_file)
    return standData
    
def standDataCsv(standData):
    for i in range(0,100,1):
    #there are 100 stations as given by JCDecaux json
        standNum = standData[i]['number']
        standName = standData[i]['name']
        standAddress = standData[i]['address']
        standLat = standData[i]['position']['lat']
        standLng = standData[i]['position']['lng']
        standStatus = standData[i]['status']
        standTotalStands = standData[i]['bike_stands']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        #divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        
        array = [standNum, standName, standAddress, standLat, standLng, standStatus, standTotalStands, standAvailableBikes, standAvailableSpaces, standLastUpdate]
        
        #https://gis.stackexchange.com/questions/72458/export-list-of-values-into-csv-or-txt-file
        csvfile = "/home/obyrned1/compsci/comp30670/testData.csv"
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator=',')
            for val in array:
                writer.writerow([val])  
            output.write("\n")
        
def connectDB():
    ''' Create a connection to our AWS DB'''
    
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    engine = create_engine("mysql+mysqldb://'ScrumMasterG20':'ToxicBuzz18'@'dublin-bikes-data.csu7egshtvlv.us-west-2.rds.amazonaws.com':'3306'/'dublin-bikes-data'")
    return engine

def createStaticTable(engine):
    ''' Create a table to store the static data for each Dublin Bikes station'''
    
    # https://www.pythonsheets.com/notes/python-sqlalchemy.html
    engine.execute('CREATE TABLE IF NOT EXISTS "StaticData" ('
                   'number INTEGER NOT NULL,'
                   'name VARCHAR,'
                   'address VARCHAR,'
                   'latitude REAL,'
                   'longitude REAL,'
                   'stands Integer, '
                   'PRIMARY KEY (number));')

if __name__ == '__main__':
    starttime=time.time()        
    while True:
        data = getJsonData()
        standDataCsv(data)
        #time.sleep(300.0 - ((time.time() - starttime) % 300.0))
