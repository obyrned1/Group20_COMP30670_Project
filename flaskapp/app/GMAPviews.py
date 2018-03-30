#dummmyapp/app/views.py
 
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb
from flask import render_template
from app import app
from flask import jsonify
import time
import urllib.request
import json
import datetime
import csv
import time



#===============================================================================
# def connectDB():
#     try:
#         # http://docs.sqlalchemy.org/en/latest/core/engines.html
#         engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dublinbikes.cvzzy1efxyiq.us-east-2.rds.amazonaws.com:3306/DublinBikesData", echo = False)
#         return engine
#  
#     except Exception as e:
#         print("Error:", type(e))
#         print(e)
#===============================================================================
  

def connectDB():
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dbikes.cvzzy1efxyiq.us-east-2.rds.amazonaws.com:3306/DublinBikesData", echo = False)
        return engine

    except Exception as e:
        print("Error:", type(e))
        print(e)


@app.route('/')
def index():
    returnDict = {}
    returnDict['Title'] = 'Dublin Bike Planner'
    returnDict['Stations'] = getDynamicData()
    return render_template("index.html", **returnDict)
      
#===============================================================================
# #@app.route('/stations')
# def getStationData():
#     engine = connectDB()
#     conn = engine.connect()
#     stations = []
#     rows = conn.execute("SELECT * FROM DublinBikesData.StaticData")
#     for row in rows:
#         stations.append(dict(row))
#     return  stations#jsonify(stations=stations)
#===============================================================================

@app.route('/dydata')
def getDynamicData():
    
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    standData = json.loads(str_file)
    #print(standData)
    dydata = {}
    for i in range(0,100,1):
    #there are 100 stations as given by JCDecaux json
        standNum = standData[i]['number']
        standAddress = standData[i]['address']
        standBikes = standData[i]['bike_stands']
        standStatus = standData[i]['status']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        dydata[standNum] =  standAddress, standStatus, standBikes, standAvailableBikes, standAvailableSpaces,  standLastUpdate
    return dydata