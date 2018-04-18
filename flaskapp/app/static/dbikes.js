function populateStationBox(bikes, stands) {
        var boxInfo = '<p> No. of Available Bikes : ' + bikes + '</p>' + '<p> No. of Available Stands : ' + stands + '</p>' +'<p> Credit Card Terminal : Yes</p>' + '<p> Leap Card Accepted : Yes';
        document.getElementById('stationInfoBox').innerHTML = boxInfo;
}
    
function drawWeeklyChart(data) {
        var loading = ("<img src='../static/BikeBreaking.gif' style='height:300px;width:100%;'>");
        document.getElementById('chart').innerHTML = loading;
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
          legend: { position: 'bottom' },
          animation: {
                duration: 750,
                startup: true //This is the new option
            }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart'));

        chart.draw(data, options);
      }


function resetStation(station){
        document.getElementById("myDropdown").value=document.getElementById(station).value;
    }
    // some parts adapted from: https://stackoverflow.com/questions/30012913/google-map-api-v3-add-multiple-infowindows   
   
function insertAddInfo(currentStation){
        chosenStation = currentStation;
        createChart(currentStation);
    }    
        
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
function resetDropdown() {
            var d = new Date();
            var n = d.getDay();
        document.getElementById("dayOfWeek").value=n;
        createHourlyChart(chosenStation, n);
        }   
        function insertAddHourlyInfo(day){
        
        createHourlyChart(chosenStation,day);
        };    
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
        }
      function drawHourlyChart(data) {
        var loading2 = ("<img src='../static/BikeBreaking.gif' style='height:300px;width:100%;'>");
        document.getElementById('hourlyChart').innerHTML = loading2;
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
          vAxis: {minValue: 0,
                 gridlines: {count:7}},
          legend: { position: 'bottom' },
          animation: {
                duration: 750,
                startup: true //This is the new option
            }                
        };

        var chart = new google.visualization.LineChart(document.getElementById('hourlyChart'));
        chart.draw(data, options);
      }

/*
function getWeather(){
//call weather API from openweathermap
    var weatherdata;
    $.getJSON("http://api.openweathermap.org/data/2.5/weather?q=Dublin&id=7778677&APPID=2abe029b7b8d40e80d1ed447f4522f0d",function(data){
    var currentWeather = data.weather[0].description;
    var current_temp=data.main.temp;
    var wind_speed=data.wind.speed;
    var icon = data.weather[0].icon;
    var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");
    
    $('h3#weather').html("Current Weather in Dublin");
    $('p#temp').html("Temperature: " + parseInt( + current_temp - 273.15) + " °C");
    $('p#humidity').html("Wind Speed: " + wind_speed + " m/s");
    $('p#wind').html(iconUrl);
    
})
}
*/

function getWeather() {

    //call weather API from openweathermap
    var weatherdata;
    $.getJSON("http://api.openweathermap.org/data/2.5/forecast?q=Dublin&id=7778677&APPID=2abe029b7b8d40e80d1ed447f4522f0d",function(data){

    var dailydesc = "Daily Weather Forecast";
    var breakdown = "";
    
//code for this 'for' loop was adapted from practical 5, exercise 5//
    for (i = 0; i <= 32 ; i+= 8) {
        
        var date = new Date(data.list[i].dt*1000);
        var timeStampCon = date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear();
        var weatherdesc = data.list[i].weather[0].description;
        var icon = data.list[i].weather[0].icon;
        var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");

        
//code for the below table formation adapted from practical 6, exercise 4//
        
        breakdown += "<table id = 'dailytable'><tr><td>" + timeStampCon +"</tr></td><tr><td>" + iconUrl + "</tr></td><tr><td class = 'capitalisedesc'>" + weatherdesc + "</tr></td>";
        
        breakdown += "</table>"
          
    }
    
        document.getElementById("dailyfore").innerHTML = breakdown;
    
        document.getElementById("daydesc").innerHTML = dailydesc;
    
    })
              }