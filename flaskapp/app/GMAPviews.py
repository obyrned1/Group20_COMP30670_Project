#dummmyapp/app/views.py
 
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb
from flask import render_template
import simplejson
from app import app
from flask import jsonify
import time
import urllib.request
import json
import datetime
import csv
import time
import pandas as pd


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
    returnDict['Static'] = getStationData()
    return render_template("index.html", **returnDict)
    
#Will need to use the below to add robustness - if API goes down we will use this to place markers
#@app.route('/stations')
def getStationData():
    engine = connectDB()
    conn = engine.connect()
    stations = []
    rows = conn.execute("SELECT * FROM DublinBikesData.StaticData")
    for row in rows:
        stations.append(dict(row))
    return  stations#jsonify(stations=stations)

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

#===============================================================================
# @app.route("/occupancy/<int:station_id>")
# def get_occupancy(station_id):
#     engine = connectDB()
#     df = pd.read_sql_query("select * from DynamicData where number = %(number)s", engine, params={"number": station_id}) 
#     #df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')
#     df.set_index('last_update', inplace=True)
#     res = df['available_bikes'].resample('1d').mean()
#     #res['dt'] = df.index
#     print(res)
#     return jsonify(data=json.dumps(list(zip(map(lambda x:x.isoformat(), res.index), res.values)))) 
#===============================================================================

@app.route("/available/<currentStation>")
def getDayData(currentStation):
    engine = connectDB()
    dayData = []  
    conn = engine.connect()
    for i in range (0,7):
        string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number = {} AND WEEKDAY(last_update)= {};".format(currentStation,i)
        rows = conn.execute(string)
        for row in rows:
            dayData.append(dict(row))
    return jsonify(dayData)

@app.route("/hourly/<currentStation>/<day>")
def getHourlyData(currentStation, day):
    engine = connectDB()
    hourlyData = []
    conn = engine.connect()
    for i in range (5,24):
        string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number =  {} AND EXTRACT(HOUR FROM last_update) = {} AND WEEKDAY(last_update)= {};".format(currentStation,i,day)
        rows = conn.execute(string)
        for row in rows:
            hourlyData.append(dict(row))
    return jsonify(hourlyData)

@app.route("/hourly/<currentStation>/<day>/<hour>")
def getPrediction(currentStation, day, hour):
    engine = connectDB()
    predictData = []
    conn = engine.connect()
    string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number =  {} AND EXTRACT(HOUR FROM last_update) = {} AND WEEKDAY(last_update)= {};".format(currentStation, hour ,day)
    rows = conn.execute(string)
    for row in rows:
        predictData.append(dict(row))
    return jsonify(predictData)

