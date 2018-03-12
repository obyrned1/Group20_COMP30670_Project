# dummmyapp/app/views.py

from flask import render_template
from app import app
from sysinfo import sysinfo

@app.route('/')
def index():
	returnDict = {}
	returnDict['user'] = 'clawlor90' 
	returnDict['Title'] = 'Home'
	returnDict['platform'] = sysinfo.main()
	return render_template("index.html", **returnDict)
