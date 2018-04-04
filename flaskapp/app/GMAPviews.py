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
    #returnDict['DayData'] = getDayData(1)
    returnDict['HourlyData'] = getHourlyData(1, 3)
    return render_template("index.html", **returnDict)
    
# Will need to use the below to add robustness - if API goes down we will use this to place markers
#===============================================================================
# @app.route('/stations')
# def getStationData():
#     engine = connectDB()
#     conn = engine.connect()
#     stations = []
#     rows = conn.execute("SELECT * FROM DublinBikesData.StaticData")
#     for row in rows:
#         stations.append(dict(row))
#     return  stations#jsonify(stations=stations)
#===============================================================================

#===============================================================================
# @app.route("/available/<int:station_id>")
# def get_stations(station_id):
#     engine = connectDB()
#     data = []
#     rows = engine.execute("SELECT available_bikes from DynamicData where number = {};".format(station_id))
#     for row in rows:
#         data.append(dict(row))
# 
#     return jsonify(available=data) 
#===============================================================================

#@app.route('/dydata')
def getDynamicData():
    
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    standData = json.loads(str_file)
    return standData

@app.route("/available/<station_id>")
def getDayData(station_id):
    engine = connectDB()
    dayData = []
    conn = engine.connect()
    for i in range (0,7):
        string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number = "+ str(station_id)+" AND WEEKDAY(last_update) = " + str(i)
        rows = conn.execute(string)
        for row in rows:
            dayData.append(row)
    var_fixed = []
    for row in dayData:
        var_fixed.append(list(map(int,list(row))))
    return jsonify(data=var_fixed)

def getHourlyData(station, day):
    engine = connectDB()
    hourlyData = []
    conn = engine.connect()
    for i in range (0,24):
        string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number = " + str(station) + " AND EXTRACT(HOUR FROM last_update) =" + str(i) + " AND WEEKDAY(last_update)=" + str(day)
        rows = conn.execute(string)
        for row in rows:
            hourlyData.append(row)
    var_fixed1 = []
    for row in hourlyData:
        var_fixed1.append(list(map(int,list(row))))
    return var_fixed1
