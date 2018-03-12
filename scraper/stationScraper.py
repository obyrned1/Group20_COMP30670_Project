'''
Created on 12 Mar 2018

@author: obyrned1
'''
import urllib.request
import json
import datetime
import csv


def getData():
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    standData = json.load(file)
    #print(standData)
    #there are 100 stations as given by JCDecaux json
    for i in range(0,100,1):
        standNum = standData[i]['number']
        #print(standNum)
        standName = standData[i]['name']
        #print(standName)
        standAddress = standData[i]['address']
        #print(standAddress)
        standLat = standData[i]['position']['lat']
        #print(standLat)
        standLng = standData[i]['position']['lng']
        #print(standLng)
        standStatus = standData[i]['status']
        #print(standStatus)
        standAvailableBikes = standData[i]['available_bikes']
        #print(standAvailableBikes)
        standAvailableSpaces = standData[i]['available_bike_stands']
        #print(standAvailableSpaces)
        dateTime = (standData[i]['last_update'] / 1000 )
        #divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        #print(standLastUpdate)
        array = [standNum, standName, standAddress, standLat, standLng, standStatus, standAvailableBikes, standAvailableSpaces, standLastUpdate]
        #print(array)
        #https://gis.stackexchange.com/questions/72458/export-list-of-values-into-csv-or-txt-file
        csvfile = "/home/obyrned1/compsci/comp30670/project/testData.csv"
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator=',')
            for val in array:
                writer.writerow([val])  
            output.write("\n")
        
getData()
