var bermudaTriangle;
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

    var map = new google.maps.Map(document.getElementById('map-canvas'),
                                  mapOptions);
								  


    var triangleCoords = [
        new google.maps.LatLng(35.897814, 35.759400),
        new google.maps.LatLng(29.107839, 31.649001),
        new google.maps.LatLng(27.475650, 39.708607)

    ];

    // Construct the polygon
    bermudaTriangle = new google.maps.Circle({
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
	
    bermudaTriangle.setMap(map);
    //google.maps.event.addListener(bermudaTriangle, "dragend", getPolygonCoords);
    //google.maps.event.addListener(bermudaTriangle.getPath(), "insert_at", getPolygonCoords);
    //google.maps.event.addListener(bermudaTriangle.getPath(), "remove_at", getPolygonCoords);
    //google.maps.event.addListener(bermudaTriangle.getPath(), "set_at", getPolygonCoords);
}

function getPolygonCoords() {
    var len = bermudaTriangle.getPath().getLength();
    var htmlStr = "";
    for (var i = 0; i < len; i++) {
        htmlStr += bermudaTriangle.getPath().getAt(i).toUrlValue(5) + "<br>";
    }
    document.getElementById('info').innerHTML = htmlStr;
}

function getParams() {
	var s = "{ 'lat':'"+bermudaTriangle.center.lat()+"' ,'lan':"+bermudaTriangle.center.lng() + "','radius': '"+ bermudaTriangle.radius + "'}";
	console.log(s);
	return s;
}