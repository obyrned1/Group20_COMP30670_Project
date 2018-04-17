function populateStationBox(bikes, stands) {
        var boxInfo = '<p> No. of Available Bikes : ' + bikes + '</p>' + '<p> No. of Available Stands : ' + stands + '</p>' +'<p> Credit Card Terminal : Yes</p>' + '<p> Leap Card Accepted : Yes';
        document.getElementById('stationInfoBox').innerHTML = boxInfo;
}
    
function drawWeeklyChart(data) {
        var data = google.visualization.arrayToDataTable([
          ['Day', 'Number of Bikes Available'],
          ['Monday', data[1]["ROUND(AVG(available_bikes))"]],
          ['Tuesday',  data[2]["ROUND(AVG(available_bikes))"]],
          ['Wednesday',   data[3]["ROUND(AVG(available_bikes))"]],
          ['Thursday',  data[4]["ROUND(AVG(available_bikes))"]],
          ['Friday',  data[5]["ROUND(AVG(available_bikes))"]],
          ['Saturday',  data[6]["ROUND(AVG(available_bikes))"]],
          ['Sunday',  data[0]["ROUND(AVG(available_bikes))"]]
        ]);

        var options = {
          title: 'Daily Avg. Bike Availability',
          vAxis: {minValue: 0},
          legend: { position: 'bottom' }
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
        var data = google.visualization.arrayToDataTable([
             ['Time', 'Number of Bikes Available'],
             ['5am', data[0]["ROUND(AVG(available_bikes))"]],
             ['6am', data[1]["ROUND(AVG(available_bikes))"]],
             ['7am', data[2]["ROUND(AVG(availabsle_bikes))"]],
             ['8am', data[3]["ROUND(AVG(available_bikes))"]],
             ['9am', data[4]["ROUND(AVG(available_bikes))"]],
             ['10am', data[5]["ROUND(AVG(available_bikes))"]],
             ['11am', data[6]["ROUND(AVG(available_bikes))"]],
             ['12pm', data[7]["ROUND(AVG(available_bikes))"]],
             ['1pm', data[8]["ROUND(AVG(available_bikes))"]],
             ['2pm', data[9]["ROUND(AVG(available_bikes))"]],
             ['3am', data[10]["ROUND(AVG(available_bikes))"]],
             ['4m', data[11]["ROUND(AVG(available_bikes))"]],
             ['5pm', data[12]["ROUND(AVG(available_bikes))"]],
             ['6pm', data[13]["ROUND(AVG(available_bikes))"]],
             ['7pm', data[14]["ROUND(AVG(available_bikes))"]],
             ['8pm', data[15]["ROUND(AVG(available_bikes))"]],
             ['9pm',data[16]["ROUND(AVG(available_bikes))"]],
             ['10pm', data[17]["ROUND(AVG(available_bikes))"]],
             ['11pm', data[18]["ROUND(AVG(available_bikes))"]]
        ]);

        var options = {
          title: 'Hourly Avg. Bike Availability',
          vAxis: {minValue: 0,
                 gridlines: {count:7}},
                 legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('hourlyChart'));
        chart.draw(data, options);
      }

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