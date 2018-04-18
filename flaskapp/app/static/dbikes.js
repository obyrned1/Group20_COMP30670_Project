function populateStationBox(bikes, stands) {
        var boxInfo = '<p> No. of Available Bikes : ' + bikes + '</p>' + '<p> No. of Available Stands : ' + stands + '</p>' +'<p> Credit Card Terminal : Yes</p>' + '<p> Leap Card Accepted : Yes';
        document.getElementById('stationInfoBox').innerHTML = boxInfo;
}
    
function drawWeeklyChart(data) {
        var loading = ("<img src='../static/BikeBreaking.gif' style='height:300px;width:100%;'>");
        document.getElementById('chart').innerHTML = loading;
        var data = google.visualization.arrayToDataTable([
          ['Day', 'No. of Bikes', 'No. of Bikes (Raining)'],
          ['Monday', data[1]["ROUND(AVG(available_bikes))"], (data[1]["ROUND(AVG(available_bikes))"]*1.15)],
          ['Tuesday',  data[2]["ROUND(AVG(available_bikes))"], (data[2]["ROUND(AVG(available_bikes))"]*1.15)],
          ['Wednesday',   data[3]["ROUND(AVG(available_bikes))"], (data[3]["ROUND(AVG(available_bikes))"]*1.15)],
          ['Thursday',  data[4]["ROUND(AVG(available_bikes))"], (data[4]["ROUND(AVG(available_bikes))"]*1.15)],
          ['Friday',  data[5]["ROUND(AVG(available_bikes))"], (data[5]["ROUND(AVG(available_bikes))"]*1.15)],
          ['Saturday',  data[6]["ROUND(AVG(available_bikes))"], (data[6]["ROUND(AVG(available_bikes))"]*1.15)],
          ['Sunday',  data[0]["ROUND(AVG(available_bikes))"], (data[0]["ROUND(AVG(available_bikes))"]*1.15)]
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
             ['5am', data[0]["ROUND(AVG(available_bikes))"], (data[0]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['6am', data[1]["ROUND(AVG(available_bikes))"], (data[1]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['7am', data[2]["ROUND(AVG(availabsle_bikes))"], (data[2]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['8am', data[3]["ROUND(AVG(available_bikes))"], (data[3]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['9am', data[4]["ROUND(AVG(available_bikes))"], (data[4]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['10am', data[5]["ROUND(AVG(available_bikes))"], (data[5]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['11am', data[6]["ROUND(AVG(available_bikes))"], (data[6]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['12pm', data[7]["ROUND(AVG(available_bikes))"], (data[7]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['1pm', data[8]["ROUND(AVG(available_bikes))"], (data[8]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['2pm', data[9]["ROUND(AVG(available_bikes))"] , (data[9]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['3am', data[10]["ROUND(AVG(available_bikes))"], (data[10]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['4m', data[11]["ROUND(AVG(available_bikes))"], (data[11]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['5pm', data[12]["ROUND(AVG(available_bikes))"], (data[12]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['6pm', data[13]["ROUND(AVG(available_bikes))"], (data[13]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['7pm', data[14]["ROUND(AVG(available_bikes))"], (data[14]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['8pm', data[15]["ROUND(AVG(available_bikes))"], (data[15]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['9pm',data[16]["ROUND(AVG(available_bikes))"], (data[16]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['10pm', data[17]["ROUND(AVG(available_bikes))"], (data[17]["ROUND(AVG(available_bikes))"] * 1.15)],
             ['11pm', data[18]["ROUND(AVG(available_bikes))"], (data[18]["ROUND(AVG(available_bikes))"] * 1.15)]
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
        
        var weathericon =data.list[i].weather[0].icon;
        var weatherdesc = data.list[i].weather[0].description;
        var icon = data.list[i].weather[0].icon;
        var iconUrl = ("<img src='http://openweathermap.org/img/w/" + icon + ".png'>");

        
//code for the below table formation adapted from practical 6, exercise 4//
        
        breakdown += "<table id = 'dailytable'><tr><td>" + iconUrl + "</tr></td><tr><td class = 'capitalisedesc'>" + weatherdesc + "</tr></td>";
        
        breakdown += "</table>"
          
    }
    
        document.getElementById("dailyfore").innerHTML = breakdown;
    
        document.getElementById("daydesc").innerHTML = dailydesc;
    
    })
              }