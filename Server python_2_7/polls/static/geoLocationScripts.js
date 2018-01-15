var geoCircle;
var userLat = 32.114314;
var userLong =  34.799579;
	
	function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setPosition);
    } else { 
        
    }
}

function setPosition(position) {
    userLat =  position.coords.latitude; 
    userLong = position.coords.longitude;
}

function initialize() {
	getLocation();
    var myLatLng = new google.maps.LatLng(userLat,userLong);
    var mapOptions = {
        zoom: 10,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.RoadMap
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
    // var triangleCoords = [
    //     new google.maps.LatLng(35.897814, 35.759400),
    //     new google.maps.LatLng(29.107839, 31.649001),
    //     new google.maps.LatLng(27.475650, 39.708607)
    // ];

    // Construct the polygon
    geoCircle = new google.maps.Circle({
        //paths: triangleCoords,
        center: myLatLng,
		radius: 10000,
		draggable: true,
        editable: true,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35
    });
	
    geoCircle.setMap(map);
    //google.maps.event.addListener(geoCircle, "dragend", getPolygonCoords);
    //google.maps.event.addListener(geoCircle.getPath(), "insert_at", getPolygonCoords);
    //google.maps.event.addListener(geoCircle.getPath(), "remove_at", getPolygonCoords);
    //google.maps.event.addListener(geoCircle.getPath(), "set_at", getPolygonCoords);
}

function getPolygonCoords() {
    var len = geoCircle.getPath().getLength();
    var htmlStr = "";
    for (var i = 0; i < len; i++) {
        htmlStr += geoCircle.getPath().getAt(i).toUrlValue(5) + "<br>";
    }
    document.getElementById('info').innerHTML = htmlStr;
}

function getParams() {
	var s = "{ 'lat':'"+geoCircle.center.lat()+"' ,'lan':"+geoCircle.center.lng() + "','radius': '"+ geoCircle.radius + "'}";
	console.log(s);
	return s;
}

function getCountry(latLng) {
    geocoder.geocode( {'latLng': latLng},
        function(results, status) {
            if(status == google.maps.GeocoderStatus.OK) {
                if(results[0]) {
                    for(var i = 0; i < results[0].address_components.length; i++) {
                        if(results[0].address_components[i].types[0] == "country") {
                            alert(results[0].address_components[i].long_name);
                        }
                    }
                }
                else {
                    alert("No results");
                }
            }
            else {
                alert("Status: " + status);
            }
        }
    );
}