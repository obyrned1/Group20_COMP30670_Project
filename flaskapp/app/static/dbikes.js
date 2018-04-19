
// Function to populate the area below the dropdowns, with station information
function populateStationBox(bikes, stands) {
        
    //Inserts station info into the information box underneath the dropdowns
        var boxInfo = '<p> No. of Available Bikes : ' + bikes + '</p>' + '<p> No. of Available Stands : ' + stands + '</p>' +   
        '<div class="container" ><img class="image" style="width:100%;height:60px;" src="../static/leap_card.png">' + 
            '<div class="middle"><div class="text">Leap Card Compatible</div></div>';
        document.getElementById('stationInfoBox').innerHTML = boxInfo;
}



// Function to create a chart based on the average daily bikes for each day for a selected station   
function drawWeeklyChart(data) {
        
    // Call the div that the charts are going to populate, and fill it with a gif as the chart loads
        var loading = ("<img src='../static/bike.gif' style='height:300px;width:100%;'>");
        document.getElementById('chart').innerHTML = loading;
    
    // Creates the weekly charts with a blue line for average and a red for average when its raining
        var data = google.visualization.arrayToDataTable([
          ['Day', 'No. of Bikes', 'No. of Bikes (Raining)'],
          ['Monday', Math.round(data[1]["AVG(available_bikes)"]), Math.ceil(data[1]["AVG(available_bikes)"]*1.04)],
          ['Tuesday',  Math.round(data[2]["AVG(available_bikes)"]), Math.ceil(data[2]["AVG(available_bikes)"]*1.04)],
          ['Wednesday',   Math.round(data[3]["AVG(available_bikes)"]), Math.ceil(data[3]["AVG(available_bikes)"]*1.04)],
          ['Thursday',  Math.round(data[4]["AVG(available_bikes)"]), Math.ceil(data[4]["AVG(available_bikes)"]*1.04)],
          ['Friday',  Math.round(data[5]["AVG(available_bikes)"]), Math.ceil(data[5]["AVG(available_bikes)"]*1.04)],
          ['Saturday',  Math.round(data[6]["AVG(available_bikes)"]), Math.ceil(data[6]["AVG(available_bikes)"]*1.04)],
          ['Sunday',  Math.round(data[0]["AVG(available_bikes)"]), Math.ceil(data[0]["AVG(available_bikes)"]*1.04)]
        ]);

        var options = {
          title: 'Daily Avg. Bike Availability',
          vAxis: {minValue: 0},
          backgroundColor:{  
                fill: 'lightgrey',
                stroke: '#000',
                strokeWidth: 3
            },
          legend: { position: 'bottom' },
          animation: {
                duration: 750,
                startup: true 
            }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart'));
        chart.draw(data, options);
}


//Resets the station in the dropdown to match the station selected on the map
function resetStation(station){
        document.getElementById("myDropdown").value=document.getElementById(station).value;
}
// some parts adapted from: https://stackoverflow.com/questions/30012913/google-map-api-v3-add-multiple-infowindows   
   

//Calls the createChart method based on the station selected
function insertAddInfo(currentStation){
        chosenStation = currentStation;
        createChart(currentStation);
}    
        

//Pulls in data from the database relating to the station selected and calls the drawWeekly function to draw a chart with that information
function createChart(currentStation){
        
        var xmlhttp = new XMLHttpRequest();
        var url = "/available/" + currentStation;
        
        google.charts.load('current', {packages: ['corechart']});
        google.charts.setOnLoadCallback(drawWeeklyChart);
        console.log(url);
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var data = JSON.parse(xmlhttp.response);
                console.log('data', data);
                drawWeeklyChart(data);
                }
            };
        xmlhttp.open("GET",url, true);
        xmlhttp.send();
}


//Resets the dropdown for day of week to the current day and loads an hourly chart for that day for the selected station
function resetDropdown() {
        var d = new Date();
        var n = d.getDay();
        document.getElementById("dayOfWeek").value=n;
        createHourlyChart(chosenStation, n);
}   


//Calls the createHourlyChart based on the day of the week selected
function insertAddHourlyInfo(day){
        createHourlyChart(chosenStation,day);
}; 


//Pulls in data from the database relating to the station and day selected and calls the drawHourly function to draw a chart with that information
function createHourlyChart(currentStation,day){
    
        var xmlhttp = new XMLHttpRequest();
        var url = "/hourly/" + currentStation + "/" + day;
        
        google.charts.load('current', {packages: ['corechart']});
        google.charts.setOnLoadCallback(drawHourlyChart);
        console.log(url);
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                var data = JSON.parse(xmlhttp.response);
                console.log('data', data);
                drawHourlyChart(data);
                }
            };
        xmlhttp.open("GET",url, true);
        xmlhttp.send();
};


//Function to create a chart based on the average hourly bikes for each hour for a selected station on the selected day
function drawHourlyChart(data) {
        
    // Call the div that the charts are going to populate, and fill it with a gif as the chart loads
        var loading2 = ("<img src='../static/bike.gif' style='height:300px;width:100%;'>");
        document.getElementById('hourlyChart').innerHTML = loading2;
    
    // Creates the weekly charts with a blue line for average and a red for average when its raining
        var data = google.visualization.arrayToDataTable([
             ['Day', 'No. of Bikes', 'No. of Bikes (Raining)'],
             ['5am', Math.round(data[0]["AVG(available_bikes)"]), Math.ceil(data[0]["AVG(available_bikes)"] * 1.04)],
             ['6am', Math.round(data[1]["AVG(available_bikes)"]), Math.ceil(data[1]["AVG(available_bikes)"] * 1.04)],
             ['7am', Math.round(data[2]["AVG(available_bikes)"]), Math.ceil(data[2]["AVG(available_bikes)"] * 1.04)],
             ['8am', Math.round(data[3]["AVG(available_bikes)"]), Math.ceil(data[3]["AVG(available_bikes)"] * 1.04)],
             ['9am', Math.round(data[4]["AVG(available_bikes)"]), Math.ceil(data[4]["AVG(available_bikes)"] * 1.04)],
             ['10am', Math.round(data[5]["AVG(available_bikes)"]), Math.ceil(data[5]["AVG(available_bikes)"] * 1.04)],
             ['11am', Math.round(data[6]["AVG(available_bikes)"]), Math.ceil(data[6]["AVG(available_bikes)"] * 1.04)],
             ['12pm', Math.round(data[7]["AVG(available_bikes)"]), Math.ceil(data[7]["AVG(available_bikes)"] * 1.04)],
             ['1pm', Math.round(data[8]["AVG(available_bikes)"]), Math.ceil(data[8]["AVG(available_bikes)"] * 1.04)],
             ['2pm', Math.round(data[9]["AVG(available_bikes)"]), Math.ceil(data[9]["AVG(available_bikes)"] * 1.04)],
             ['3am', Math.round(data[10]["AVG(available_bikes)"]), Math.ceil(data[10]["AVG(available_bikes)"] * 1.04)],
             ['4m', Math.round(data[11]["AVG(available_bikes)"]), Math.ceil(data[11]["AVG(available_bikes)"] * 1.04)],
             ['5pm', Math.round(data[12]["AVG(available_bikes)"]), Math.ceil(data[12]["AVG(available_bikes)"] * 1.04)],
             ['6pm', Math.round(data[13]["AVG(available_bikes)"]), Math.ceil(data[13]["AVG(available_bikes)"] * 1.04)],
             ['7pm', Math.round(data[14]["AVG(available_bikes)"]), Math.ceil(data[14]["AVG(available_bikes)"] * 1.04)],
             ['8pm', Math.round(data[15]["AVG(available_bikes)"]), Math.ceil(data[15]["AVG(available_bikes)"] * 1.04)],
             ['9pm', Math.round(data[16]["AVG(available_bikes)"]), Math.ceil(data[16]["AVG(available_bikes)"] * 1.04)],
             ['10pm', Math.round(data[17]["AVG(available_bikes)"]), Math.ceil(data[17]["AVG(available_bikes)"] * 1.04)],
             ['11pm', Math.round(data[18]["AVG(available_bikes)"]), Math.ceil(data[18]["AVG(available_bikes)"] * 1.04)]
        ]);

        var options = {
          title: 'Hourly Avg. Bike Availability',
            backgroundColor:{  
                fill: 'lightgrey',
                stroke: '#000',
                strokeWidth: 3
            },
          vAxis: {minValue: 0,
                 gridlines: {count:7}},
          legend: { position: 'bottom' },
          animation: {
                duration: 750,
                startup: true 
            }                
        };

        var chart = new google.visualization.LineChart(document.getElementById('hourlyChart'));
        chart.draw(data, options);
}


//call weather API from openweathermap
function getWeather() {
    var weatherdata;
    $.getJSON("http://api.openweathermap.org/data/2.5/forecast?q=Dublin&id=7778677&APPID=2abe029b7b8d40e80d1ed447f4522f0d",function(data){

    var dailydesc = "Daily Weather Forecast";
    var breakdown = "";
    
    for (i = 0; i <= 32 ; i+= 8) {
        var date = new Date(data.list[i].dt*1000);
        var timeStampCon = date.getDate() + '/' + (date.getMonth() + 1);
        var weatherdesc = data.list[i].weather[0].description;
        var icon = data.list[i].weather[0].icon;
        var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");
        
    // Puts the 5 day-forecast in a table
        breakdown += "<table id = 'dailytable'><tr><td>" + timeStampCon +"</tr></td><tr><td>" + iconUrl + "</tr></td><tr><td class = 'capitalisedesc'>" + weatherdesc + "</tr></td>";
        breakdown += "</table>"
          
    }
    document.getElementById("dailyfore").innerHTML = breakdown;
    document.getElementById("daydesc").innerHTML = dailydesc;
    })
}