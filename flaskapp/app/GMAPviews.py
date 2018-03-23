# dummmyapp/app/views.py

from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb
from flask import render_template
from app import app
from flask import jsonify


def connectDB():
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dublin-bikes-data.csu7egshtvlv.us-west-2.rds.amazonaws.com:3306/DublinBikesData", echo = False)
        return engine

    except Exception as e:
        print("Error:", type(e))
        print(e)

@app.route('/')
def index():
    returnDict = {}
    returnDict['Title'] = 'Dublin Bike Planner'
    returnDict['Stations'] = getStationData()
    return render_template("index.html", **returnDict)
    

@app.route('/stations')
def getStationData():
    engine = connectDB()
    conn = engine.connect()
    stations = []
    rows = conn.execute("SELECT * FROM DublinBikesData.StaticData")
    for row in rows:
        stations.append(dict(row))
    return  stations#jsonify(stations=stations)


