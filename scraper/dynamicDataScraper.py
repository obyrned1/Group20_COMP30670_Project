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

def connectDB():
    ''' Create a connection to our AWS DB '''
    
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dublinbikes.cvzzy1efxyiq.us-east-2.rds.amazonaws.com:3306/DublinBikesData", echo = True)
        return engine

    except Exception as e:
        print("Error:", type(e))
        print(e)

def createDynamicTable():
    ''' Create a table to store the static data for each Dublin Bikes station '''
    
    # https://www.pythonsheets.com/notes/python-sqlalchemy.html
    # https://stackoverflow.com/questions/19479853/why-do-we-need-to-use-3-quotes-while-executing-sql-query-from-python-cursor
    sqlcreate = "CREATE TABLE DynamicData (number INTEGER NOT NULL, status VARCHAR (128), available_bikes INTEGER, available_bike_stands INTEGER, last_update TIMESTAMP)"
    
    try:
        engine.execute(sqlcreate)
        
    except Exception as e:
        print("Error2:", type(e))
        print(e)

def populateDynamicTable(standData):
    ''' Populate the static table with static information for each bike station '''
    ''' We will probably want to pass in the information for each station one at a time. '''

    for i in range(0,100,1):
    #there are 100 stations as given by JCDecaux json
        standNum = standData[i]['number']
        standStatus = standData[i]['status']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        #divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        
        sqlpopulate = "INSERT INTO DynamicData VALUES ('" + str(standNum) + "','" + str(standStatus) + "','" + str(standAvailableBikes) + "','" + str(standAvailableSpaces) + "','" + str(standLastUpdate) + "');"
    
        try:
            engine.execute(sqlpopulate)

        except Exception as e:
            print("Error3:", type(e))
            print(e)
        
def backupDataCsv(standData):
    for i in range(0,100,1):
    #there are 100 stations as given by JCDecaux json
        standNum = standData[i]['number']
        standStatus = standData[i]['status']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        #divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        
        array = [standNum, standStatus, standAvailableBikes, standAvailableSpaces, standLastUpdate]
        
        #https://gis.stackexchange.com/questions/72458/export-list-of-values-into-csv-or-txt-file
        csvfile = "/home/ec2-user/Group20_COMP30670_Project/testData.csv"
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator=',')
            for val in array:
                writer.writerow([val])  
            output.write("\n")
            
if __name__ == '__main__':
    engine = connectDB()
    #createDynamicTable()
    starttime=time.time()        
    while True:
        standData = getJsonData()
        populateDynamicTable(standData)
        backupDataCsv(standData)
        time.sleep(300.0 - ((time.time() - starttime) % 300.0))