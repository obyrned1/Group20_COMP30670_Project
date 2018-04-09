import urllib.request
import json, decimal
from flask import jsonify
from decimal import Decimal
import datetime
import csv
import time
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb

def connectDB():
    ''' Create a connection to our AWS DB '''
    
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dbikes.cvzzy1efxyiq.us-east-2.rds.amazonaws.com:3306/DublinBikesData", echo = False)
        return engine

    except Exception as e:
        print("Error:", type(e))
        print(e)

def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def getDayData(station):
    engine = connectDB()
    dayData = []
    string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number = " + str(station) + " AND WEEKDAY(last_update)=" + str(0) + ';'
        
    conn = engine.connect()
    #===========================================================================
    # 
    # for i in range (0,7):
    #     string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number = " + str(station) + " AND WEEKDAY(last_update)=" + str(i) + ';'
    #===========================================================================
    rows = conn.execute(string)
    for row in rows:
        dayData.append((row))
    #===========================================================================
    # var_fixed = []
    # for row in dayData:
    #     var_fixed.append(list(map(int,list(row))))
    #===========================================================================
    return jsonify(dayData)


def getHourlyData(station, day):
    engine = connectDB()
    hourlyData = []
    conn = engine.connect()
    for i in range (0,24):
        string = "SELECT ROUND(AVG(available_bikes)) FROM DynamicData WHERE number = " + str(station) + " AND EXTRACT(HOUR FROM last_update) =" + str(i) + " AND WEEKDAY(last_update)=" + str(day)
        rows = conn.execute(string)
        for row in rows:
            hourlyData.append(row)
    #===========================================================================
    # var_fixed = []
    # for row in hourlyData:
    #     var_fixed.append(list(map(int,list(row))))
    # return var_fixed
    #===========================================================================
    return hourlyData

if __name__ == '__main__':
    print(getDayData(1))
    
    