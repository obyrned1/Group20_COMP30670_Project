
 
function insertAddInfo(currentStation){
        chosenStation = currentStation;
        document.getElementById('infoTitle').innerHTML = '<h2> Information for:' + currentStation + '</h2>';
        //document.getElementById('additionalInfo').style.display = 'block';
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
//function stationsDropdown(){   
    var stations = [];
    var listItem = '';
    {% for Station in Static %}
    //var stationAddress = '{{ Station.address}}';
    stations.push({
        key: '{{ Station.address }}',
        value: {{ Station.number }}});
        {% endfor %}
    //stations.sort(function(a,b) {return (a.key > b.key) ? 1 : ((b.key > a.key) ? -1 : 0);} );
    //stations.sort(key);
    for(i=0; i < stations.length; i++){
        listItem += '<option value='+ stations[i].value+'>' + stations[i].key + '</option>';
    }
    document.getElementById('myDropdown').innerHTML = listItem;

    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js">
    
//}

function drawWeeklyChart(data) {
    var data = google.visualization.arrayToDataTable([
      ['Day', 'Number of Bikes Available'],
      ['Monday', data[0]["ROUND(AVG(available_bikes))"]],
      ['Tuesday',  data[1]["ROUND(AVG(available_bikes))"]],
      ['Wednesday',   data[2]["ROUND(AVG(available_bikes))"]],
      ['Thursday',  data[3]["ROUND(AVG(available_bikes))"]],
      ['Friday',  data[4]["ROUND(AVG(available_bikes))"]],
      ['Saturday',  data[5]["ROUND(AVG(available_bikes))"]],
      ['Sunday',  data[6]["ROUND(AVG(available_bikes))"]]
    ]);

    var options = {
      title: 'Daily Avg. Bike Availability',
      vAxis: {minValue: 0},
      height:300,
      width: 400,
      legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('chart'));

    chart.draw(data, options);
}
 
function insertAddHourlyInfo(day){
    //getElementById('infoTitle').innerHTML = '<h2> Information for:' + selected + '</h2>';
    //document.getElementById('additionalInfo').style.display = 'block';

    createHourlyChart(chosenStation,day);
}
         
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
         ['12am', data[0]["ROUND(AVG(available_bikes))"]],
         ['1am', data[1]["ROUND(AVG(available_bikes))"]],
         ['2am', data[2]["ROUND(AVG(available_bikes))"]],
         ['3am', data[3]["ROUND(AVG(available_bikes))"]],
         ['4am', data[4]["ROUND(AVG(available_bikes))"]],
         ['5am', data[5]["ROUND(AVG(available_bikes))"]],
         ['6am', data[6]["ROUND(AVG(available_bikes))"]],
         ['7am', data[7]["ROUND(AVG(available_bikes))"]],
         ['8am', data[8]["ROUND(AVG(available_bikes))"]],
         ['9am', data[9]["ROUND(AVG(available_bikes))"]],
         ['10am', data[10]["ROUND(AVG(available_bikes))"]],
         ['11am', data[11]["ROUND(AVG(available_bikes))"]],
         ['12pm', data[12]["ROUND(AVG(available_bikes))"]],
         ['1pm', data[13]["ROUND(AVG(available_bikes))"]],
         ['2pm', data[14]["ROUND(AVG(available_bikes))"]],
         ['3pm', data[15]["ROUND(AVG(available_bikes))"]],
         ['4pm',data[16]["ROUND(AVG(available_bikes))"]],
         ['5pm', data[17]["ROUND(AVG(available_bikes))"]],
         ['6pm', data[18]["ROUND(AVG(available_bikes))"]],
         ['7pm', data[19]["ROUND(AVG(available_bikes))"]],
         ['8pm', data[20]["ROUND(AVG(available_bikes))"]],
         ['9pm', data[21]["ROUND(AVG(available_bikes))"]],
         ['10pm', data[22]["ROUND(AVG(available_bikes))"]],
         ['11pm', data[23]["ROUND(AVG(available_bikes))"]]
    ]);

    var options = {
      title: 'Hourly Avg. Bike Availability',
      vAxis: {minValue: 0,
             gridlines: {count:7}},
      height:300,
      width: 400,
      legend: { position: 'bottom' }
    };

    var chart = new google.visualization.LineChart(document.getElementById('hourlyChart'));
    chart.draw(data, options);
}