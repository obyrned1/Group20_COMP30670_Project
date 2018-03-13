import urllib.request
import json
import datetime
import csv
import time

def getJsonData():
    apiKey = "c9ec7733fec3fc712434d79c0484b74847a1a37b"
    file = urllib.request.urlopen("https://api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey=" + apiKey)
    # https://stackoverflow.com/questions/2835559/parsing-values-from-a-json-file
    str_file = file.read().decode('utf-8')
    standData = json.loads(str_file)
    return standData
    
def standDataCsv(standData):
    for i in range(0,100,1):
    #there are 100 stations as given by JCDecaux json
        standNum = standData[i]['number']
        standStatus = standData[i]['status']
        standAvailableBikes = standData[i]['available_bikes']
        standAvailableSpaces = standData[i]['available_bike_stands']
        dateTime = (standData[i]['last_update'] / 1000 )
        #divide by 1000 as the timestamp is in milliseconds
        # http://www.timestampconvert.com/?go2=true&offset=0&timestamp=1520870710000&Submit=++++++Convert+to+Date++++++
        # https://stackoverflow.com/questions/3682748/converting-unix-timestamp-string-to-readable-date-in-python
        standLastUpdate = datetime.datetime.fromtimestamp(dateTime).strftime('%Y-%m-%d %H:%M:%S')
        
        array = [standNum, standStatus, standAvailableBikes, standAvailableSpaces, standLastUpdate]
        
        #https://gis.stackexchange.com/questions/72458/export-list-of-values-into-csv-or-txt-file
        csvfile = "/home/obyrned1/compsci/comp30670/testData.csv"
        with open(csvfile, "a") as output:
            writer = csv.writer(output, lineterminator=',')
            for val in array:
                writer.writerow([val])  
            output.write("\n")
            
if __name__ == '__main__':
    starttime=time.time()        
    while True:
        data = getJsonData()
        standDataCsv(data)
        time.sleep(300.0 - ((time.time() - starttime) % 300.0))