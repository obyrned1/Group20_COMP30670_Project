'''
Created on 15 Mar 2018

@author: obyrned1, Emmet62, oleathlc
'''

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



@app.route('/')
def index():
    ''' index is used to send the returned data from the listed function, to the index.html that runs our application''' 
    
    returnDict = {}
    returnDict['Title'] = 'Dublin Bikes'
#   returnDict['Stations'] = getDynamicData()
    returnDict['Static'] = getStationData()
    return render_template("index.html", **returnDict)
    
    
# This function was retired as mentioned in the report    
#===============================================================================
# #@app.route('/stations')
# def getStationData():
#     ''' function returns all data from the static data database we have created'''
#     
#     # create a connection to our database
#     engine = connectDB()
#     conn = engine.connect()
#     
#     #create an empty array that will be populated by the data that is returned from the static data table
#     stations = []
#     rows = conn.execute("SELECT * FROM DublinBikesData.StaticData")
#     for row in rows:
#         # append each row in the static database, to the stations array
#         stations.append(dict(row))
#     return  stations#jsonify(stations=stations)
#===============================================================================



def getDynamicData():
    ''' Function returns dynamic data from the JCDecaux using our unique key '''
    
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    
    # we use json loads to return the data in a format which we can index into it
    standData = json.loads(str_file)
    if standData != None:
        return standData
    
    # The below else statement was our attempt to implement robustness if the API goes down
    # However, as mentioned in our report, our html file was not set up correctly to adapt to this scenario
    #===========================================================================
    # else:
    #     engine = connectDB()
    #     conn = engine.connect()
    #     stations = []
    #     rows = conn.execute("SELECT StaticData.number, StaticData.latitude, StaticData.longitude, DynamicData.available_bikes, DynamicData.available_bike_stands,DynamicData.last_update FROM DublinBikesData.StaticData INNER JOIN DublinBikesData.DynamicData ON StaticData.number=DynamicData.number")
    #     for row in rows:
    #         stations.append(dict(row))
    #     return stations
    #===========================================================================



@app.route("/available/<currentStation>")
def getDayData(currentStation):
    ''' Function returns data from the dynamic table, which will be used to create the daily charts on our app'''
    
    # create a connection to our database
    engine = connectDB()
    
    # create an empty array 
    dayData = []  
    
    # connect to our database
    conn = engine.connect()
    
    # for each day of the week...
    for i in range (0,7):
        
        # SQL query returns average available bikes for a given day and station number
        string = "SELECT AVG(available_bikes) FROM DynamicData WHERE number = {} AND WEEKDAY(last_update)= {};".format(currentStation,i)
        rows = conn.execute(string)
        
        # append the returned sql data into the dayData array as a dictionary
        for row in rows:
            dayData.append(dict(row))
    
    # jsonify the array 
    return jsonify(dayData)


@app.route("/hourly/<currentStation>/<day>")
def getHourlyData(currentStation, day):
    ''' Function returns data from the dynamic table, which will be used to create the hourly charts on our app'''

    # create a connection to our database
    engine = connectDB()
    
    # create an empty array
    hourlyData = []
    
    # connect to our database
    conn = engine.connect()
    
    # for every hour of the day between 5am and 11pm (thats when the stations are open)
    for i in range (5,24):
        
        # SQL query returns average available bikes for a given hour in a day and station number
        string = "SELECT AVG(available_bikes) FROM DynamicData WHERE number =  {} AND EXTRACT(HOUR FROM last_update) = {} AND WEEKDAY(last_update)= {};".format(currentStation,i,day)
        rows = conn.execute(string)
        
        # append the returned sql data into the hourlyData array as a dictionary
        for row in rows:
            hourlyData.append(dict(row))
    
    # jsonify the array       
    return jsonify(hourlyData)

