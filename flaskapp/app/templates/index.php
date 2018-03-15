<?php
    $host = 'dublin-bikes-data.csu7egshtvlv.us-west-2.rds.amazonaws.com';
    $dbname = 'DublinBikesData';
    $username = 'ScrumMasterG20';
    $password = 'Toxicbuzz18';

    try {
        $conn = new PDO("mysql:host=$host;dbname=$dbname; port=3306; charset=utf8", $username, $password);
    $sql = 'SELECT *
            FROM StaticData
            ORDER BY number';
    $q = $conn->query($sql);
    
    $q->setFetchMode(PDO::FETCH_ASSOC);
 
    } 
    catch (PDOException $pe) {
        die("Ooops! Something went wrong! Could not connect to the database $dbname :" . $pe->getMessage());
    }
?>
       
<!-- dummyapp/app/templates/index.html -->
<html>
<head>
<title>{{ title }}</title>
</head>
<body>
<h1>DUBLIN BIKES</h1>
<div id="map" style="width:100%;height:600px;">
<script>
    function initMap() {
        var dublin = {lat: 53.3454403, lng: -6.2714263,};
        var myLatLng = {lat: 53.344407, lng: -6.257285,};
        var map = new  google.maps.Map(document.getElementById('map'), {
          zoom: 14,
          center: dublin
        });
        var contentString = '<div id="content">'+
            '<div id="siteNotice">'+
            '</div>'+
            '<h1 id="firstHeading" class="firstHeading">Trinity College Dublin</h1>'+
            '<div id="bodyContent">'+
            '<p><b>TRINITY</b> A great bunch of lads.</p>'+
            '</div>'+
            '</div>';
        var infowindow = new google.maps.InfoWindow({
          content: contentString
        });
        var marker = new google.maps.Marker({
          position: myLatLng,
          draggable: false,
          animation: google.maps.Animation.DROP,
          map: map,
          title: "Trinity"
          });
        marker.addListener('click', function() {
            infowindow.open(map, marker);
        });    
    }
    
        function setMarkers(map) {
            <?php while ($r = $q->fetch()): ?>
            { 
            $lat = array($r['lat']);
            $long = arrray($r['lng']);
            $name = array($r['name']);
            $number = array($r['number']);
            }
                
            
            for (var i = 0; i < 100; i++){
                var marker2 = new google.maps.Marker({
                    position: {lat: ($lat[i]), lng: ($long[i]) },
                    map: map,
                    title: ($name[i]),
                    zIndex: ($number[i])
                  });
            }
                
            <?php endwhile; ?>
            
        }
            
    
</script>
<script async defer
    src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBRUrdJ4Tz9rLrHrOkwJWpA9QSYNJbWQ0Q&callback=initMap">
</script>
</div>
<div>
<table>
                 <thead>
                     <tr>
                         <th>Number</th>
                         <th>Name</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($r = $q->fetch()): ?>
                    <tr><?php 
                            $text = "<tr> Number :<td> " . addslashes($r['number']) . "</td><td> Name : " . addslashes($r['name']) . "</tr>";?>
                        <td><?php echo htmlspecialchars($r['number'])?></td>
                        <td><?php echo htmlspecialchars($r['name'])?></td>
                    </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
    <table ><tr id='details'></tr></table>
</div>
</body>
</html>