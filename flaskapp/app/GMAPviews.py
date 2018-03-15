# dummmyapp/app/views.py

from flask import render_template
from app import app

@app.route('/')
def index():
        returnDict = {}
        returnDict['Title'] = 'Dublin Bike Planner'
        return render_template("index.html", **returnDict)

