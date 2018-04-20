'''
Created on 12 Mar 2018

@author: obyrned1, Emmet62, oleathlc
'''

import urllib.request
import json
import csv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb



def getJsonData():
    ''' This function returns data from the JCDecaux API, using a unique key. 
    It uses json loads to return it in a readable fashion that we can index into '''
    
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    standData = json.loads(str_file)
    return standData



def connectDB():
    ''' Create a connection to our AWS database '''
    
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dbikes.cvzzy1efxyiq.us-east-2.rds.amazonaws.com:3306/DublinBikesData", echo = False)
        return engine

    except Exception as e:
        # if there is an error in carrying out the above, print the error
        print("Error:", type(e))
        print(e)



def createDynamicTable():
    ''' Using SQL, create a table which will store the dynamic data for each Dublin Bikes station.
    The dynamic data is station number, status, available bikes, available stands, and last update '''
    
    # https://www.pythonsheets.com/notes/python-sqlalchemy.html
    # https://stackoverflow.com/questions/19479853/why-do-we-need-to-use-3-quotes-while-executing-sql-query-from-python-cursor
    sqlcreate = "CREATE TABLE DynamicData (number INTEGER NOT NULL, status VARCHAR (128), available_bikes INTEGER, available_bike_stands INTEGER, last_update TIMESTAMP)"
    
    try:
        engine.execute(sqlcreate)
        
    except Exception as e:
        # if there is an error in carrying out the above, print the error
        print("Error2:", type(e))
        print(e)
        
        

def populateDynamicTable(standData):
    ''' Populate the dynamic table with information for each bike station. '''
    
    # first, create a connection with the database we have created
    engine = connectDB()
    
    # There are 104 stations. For each station, we want to pull out the required information to populate the dynamic table
    for i in range(0,104,1):
        standNum = standData[i]['number']
        standStatus = standData[i]['status']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        #divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        
        # use the info above to populate the dynamic data table
        sqlpopulate = "INSERT INTO DynamicData VALUES ('" + str(standNum) + "','" + str(standStatus) + "','" + str(standAvailableBikes) + "','" + str(standAvailableSpaces) + "','" + str(standLastUpdate) + "');"
    
        try:
            engine.execute(sqlpopulate)

        except Exception as e:
            # if there is an error in carrying out the above, print the error
            print("Error3:", type(e))
            print(e)
        
        
        
def backupDataCsv(standData):
    ''' Populate the a CSV file as backup for the database, with information for each bike station. '''
    
    #there are 104 stations as given by JCDecaux json
    for i in range(0,104,1):
    
        standNum = standData[i]['number']
        standStatus = standData[i]['status']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        # divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        
        # put the information into an array
        array = [standNum, standStatus, standAvailableBikes, standAvailableSpaces, standLastUpdate]
        
        #https://gis.stackexchange.com/questions/72458/export-list-of-values-into-csv-or-txt-file
        csvfile = "/home/ec2-user/Group20_COMP30670_Project/testData.csv"
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator=',')
            # for each value in the array, populate a line in the CSV with it 
            for val in array:
                writer.writerow([val])  
            output.write("\n")
            
            
            
if __name__ == '__main__':
    
    engine = connectDB()
    
    # we only want create the dynamic table once. We ran it the first time then have it commented out since.
    #createDynamicTable()
   
    starttime=time.time()        
    
    while True:
        
        standData = getJsonData()
        populateDynamicTable(standData)
        backupDataCsv(standData)
        
        # when the above three operations are complete, wait 300 seconds (5 minutes), and re-run the above. 
        # This timer is set up as JCDecaux only provide info every 5 mins, so it is not necessary to have it continuously running
        time.sleep(300.0 - ((time.time() - starttime) % 300.0))