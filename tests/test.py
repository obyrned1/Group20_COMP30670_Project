
"""We had an issue with our test file. Whenever we tried to import the functions from GMAPviews reason we kept getting an 
error saying 'no module named app'. We spoke to Karl and another TA during the practicals but they weren't able to work it
out either. The format and structure we used was the same as for the LED Grid assignment and we had no issues there so not
sure what caused this problem. After a few hours of trying to work it out we decided to just copy some of the functions 
into the test file as we couldn't import them. We were able to import the functions within the scraper package so could
test them normally"""


from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb
from flask import render_template
import simplejson
from flask import jsonify
import time
import urllib.request
import json
import datetime
import csv
import time
from scraper import *


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
    return dayData


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
    return hourlyData


def test_connectDB():
    '''Test that we can successfully connect to the DB'''
    engine = connectDB()
    conn = engine.connect()
    assert conn != None

def test_getDynamicData():
    '''Test that we can retrieve dynamic bike data from the API
    Check that the dynamic data has been returned by checkin if the first station number is 42'''
    testDynamicData = getDynamicData()
    assert testDynamicData[0]['number'] == 42

def test_getDayData():
    ''' Test that we can retrieve daily information for the chosen station. In our actual applications this data is returned in json format but we have changed
    it to just return as a dictionary for the purpose of testing'''
    testDayData = getDayData(10)
    assert testDayData != None

def test_getHourlyData():
    ''' Test that we can retrieve hourly information for the chosen station and day. In our actual applications this data is returned in json format but we 
    have changed it to just return as a dictionary for the purpose of testing'''
    testHourlyData = getHourlyData(20, 3)
    assert testHourlyData != None
