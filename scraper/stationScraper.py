'''
Created on 12 Mar 2018

@author: obyrned1, Emmet62, oleathlc
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
    ''' This function returns data from the JCDecaux API, using a unique key. 
    It uses json loads to return it in a readable fashion that we can index into '''
    
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
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dbikes.cvzzy1efxyiq.us-east-2.rds.amazonaws.com:3306/DublinBikesData", echo = False)
        return engine

    except Exception as e:
        # if there is an error in carrying out the above, print the error
        print("Connection Error:", type(e))
        print(e)
        
        

def createStaticTable():
    ''' Using SQL, create a table which will store the static data for each Dublin Bikes station.
    The static data is station number, name, address, latitude, longitude and stands '''
    
    # https://www.pythonsheets.com/notes/python-sqlalchemy.html
    # https://stackoverflow.com/questions/19479853/why-do-we-need-to-use-3-quotes-while-executing-sql-query-from-python-cursor
    sqlcreate = "CREATE TABLE StaticData (number INTEGER NOT NULL, name VARCHAR (128), address VARCHAR (128), latitude DOUBLE, longitude DOUBLE, stands INTEGER, PRIMARY KEY (number))"
    
    try:
        engine.execute(sqlcreate)
        
    except Exception as e:
        # if there is an error in carrying out the above, print the error
        print("Static Table Creation Error:", type(e))
        print(e)



def populateStaticTable(standData):
    ''' Populate the static table with information for each bike station. '''

    # There are 104 stations. For each station, we want to pull out the required information to populate the dynamic table
    for i in range(0,104,1):
    
        standNum = standData[i]['number']
        standName = standData[i]['name']
        standName = standName.replace("'","")
        standAddress = standData[i]['address']
        standAddress = standAddress.replace("'","")
        standLat = standData[i]['position']['lat']
        standLng = standData[i]['position']['lng']
        standTotalStands = standData[i]['bike_stands']
        
        sqlpopulate = "INSERT INTO StaticData VALUES ('" + str(standNum) + "','" + str(standName) + "','" + str(standAddress) + "','" + str(standLat) + "','" + str(standLng) + "','" + str(standTotalStands) + "');"
    
        try:
            engine.execute(sqlpopulate)

        except Exception as e:
            # if there is an error in carrying out the above, print the error
            print("Populate Static Table Error:", type(e))
            print(e)
    
    
if __name__ == '__main__':
    engine = connectDB()
    createStaticTable() 
    standData = getJsonData()
    populateStaticTable(standData)
