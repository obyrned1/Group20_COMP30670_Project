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
    returnDict['Title'] = 'Dublin Bikes'
    returnDict['Stations'] = getDynamicData()
    returnDict['Static'] = getStationData()
    return render_template("index.html", **returnDict)
    
#@app.route('/stations')
def getStationData():
    engine = connectDB()
    conn = engine.connect()
    stations = []
    rows = conn.execute("SELECT * FROM DublinBikesData.StaticData")
    for row in rows:
        stations.append(dict(row))
    return  stations#jsonify(stations=stations)


def getDynamicData():
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    standData = json.loads(str_file)
    if standData != None:
        return standData
    else:
        engine = connectDB()
        conn = engine.connect()
        stations = []
        rows = conn.execute("SELECT StaticData.number, StaticData.latitude, StaticData.longitude, DynamicData.available_bikes, DynamicData.available_bike_stands,DynamicData.last_update FROM DublinBikesData.StaticData INNER JOIN DublinBikesData.DynamicData ON StaticData.number=DynamicData.number")
        for row in rows:
            stations.append(dict(row))
        return stations

@app.route("/available/<currentStation>")
def getDayData(currentStation):
    engine = connectDB()
    dayData = []  
    conn = engine.connect()
    for i in range (0,7):
        string = "SELECT AVG(available_bikes) FROM DynamicData WHERE number = {} AND WEEKDAY(last_update)= {};".format(currentStation,i)
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
        string = "SELECT AVG(available_bikes) FROM DynamicData WHERE number =  {} AND EXTRACT(HOUR FROM last_update) = {} AND WEEKDAY(last_update)= {};".format(currentStation,i,day)
        rows = conn.execute(string)
        for row in rows:
            hourlyData.append(dict(row))
    return jsonify(hourlyData)

