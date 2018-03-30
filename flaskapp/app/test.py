import urllib.request
import json
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
        
def getData():
    engine = connectDB()
    conn = engine.connect()
    rows = conn.execute("SELECT * FROM DynamicData WHERE number = 6 AND  last_update >= '2018-03-29 12:00:00' AND last_update <= '2018-03-29 12:30:00'")
    return rows

if __name__ == '__main__':
    getData()