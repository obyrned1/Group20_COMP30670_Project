# dummmyapp/app/views.py

from flask import render_template
from app import app
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import mysqldb

@app.route('/')
def index():
        returnDict = {}
        returnDict['Title'] = 'Dublin Bike Planner'
        return render_template("index.html", **returnDict)

def connectDB():
    ''' Create a connection to our AWS DB '''
    
    try:
        # http://docs.sqlalchemy.org/en/latest/core/engines.html
        engine = create_engine("mysql+mysqldb://ScrumMasterG20:Toxicbuzz18@dublin-bikes-data.csu7egshtvlv.us-west-2.rds.amazonaws.com:3306/DublinBikesData", echo = True)
        return engine

    except Exception as e:
        print("Error:", type(e))
        print(e)

#StaticData

        
if __name__ == '__main__':
    engine = connectDB()