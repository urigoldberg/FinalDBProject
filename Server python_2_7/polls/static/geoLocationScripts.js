var geoCircle;
var user_Lat = 32.114314;
var user_Long =  34.799579;
	
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(setPosition);
    }else {
        alert("please enable browser to use your position!")
    }
}

function getSongsForGeoLocation(){
    var sentData = createJSONStringforGeo("geoService","latitude","longitude","radius");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            var responseTable = responseArr = createTableFromResponseGeo(responseArr,"0");
            fadeInTableGeo(responseTable,"geoTable");
            document.getElementById("returnpar").innerHTML= "The following artists were found";
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+sentData);
}

function fadeInTableGeo(finalTable, elementToReplaceByTable) {
    document.getElementById(elementToReplaceByTable).style.display = "none";
    document.getElementById(elementToReplaceByTable).innerHTML = finalTable;
    $("#"+elementToReplaceByTable).fadeIn(1500);
}


function createTableFromResponseGeo(responseArr,isSongTable) {
    if(responseArr.isError === "true"){
        return "<p>"+responseArr.errorMessage+"</p>"
    }
    var numOfRows = responseArr.Results.length;
    var columnNames = [];
    for (var colName in responseArr.Results[0]) {
        if (colName) {
            columnNames.push(colName);
        }
    }
    var numofCols = columnNames.length;
    var finaltable = "<table class=\"table table-striped imagetable\"><thead><tr>";
    //insert column names in table
    for(var col in columnNames){
        finaltable += "<th>"+columnNames[col]+"</th>"
    }
    if(isSongTable === "1"){
        finaltable+="<th>Like this song</th>"
    }
    //filling table rows
    finaltable+="</tr></thead></tbody>";

    for (var i = 0; i < numOfRows; i++){
        finaltable+="<tr>";
        for(var j=0;j<numofCols;j++){
            var val = responseArr.Results[i][columnNames[j]];
            if(val === "None"){
                finaltable+="<th>"+insertButtonInTable(i+1)+"</th>";
            }else{
                finaltable+="<th>"+val+"</th>";
            }
        }
        if(isSongTable === "1"){
            finaltable+="<th><button class='btn btn-default' onclick='likerowImageToMusic("+(i+1)+")'>Like song!</button></th>";
        }
        finaltable+="</tr>";
    }
    finaltable += "</tbody></table>";
    return finaltable;
}

function setPosition(position) {
    user_Lat =  position.coords.latitude;
    user_Long = position.coords.longitude;
}

function createJSONStringforGeo(flowname, elementId, elementId2, elementId3) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,elementId,geoCircle.center.lat());
    jsonString+=",";
    jsonString = addParamJSON(jsonString,elementId2,geoCircle.center.lng());
    jsonString+=",";
    jsonString = addParamJSON(jsonString,elementId3,geoCircle.radius);
    jsonString += "]}";
    return jsonString;
}

function initialize() {
	//insert current location into user_lat / user_long
	getLocation();
	//move map to current position and initialize map location
    var myLatLng = new google.maps.LatLng(user_Lat,user_Long);
    var mapOptions = {
        zoom: 10,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.RoadMap
    };
    var map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);

    // Construct the polygon
    geoCircle = new google.maps.Circle({
        center: myLatLng,
		radius: 10000,
		draggable: true,
        editable: true,
        strokeColor: '#53d795',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#53d795',
        fillOpacity: 0.35
    });
	
    geoCircle.setMap(map);
}

// function getPolygonCoords() {
//     var len = geoCircle.getPath().getLength();
//     var htmlStr = "";
//     for (var i = 0; i < len; i++) {
//         htmlStr += geoCircle.getPath().getAt(i).toUrlValue(5) + "<br>";
//     }
//     document.getElementById('info').innerHTML = htmlStr;
// }
//
// function getParams() {
// 	var s = "{ 'lat':'"+geoCircle.center.lat()+"' ,'lan':"+geoCircle.center.lng() + "','radius': '"+ geoCircle.radius + "'}";
// 	console.log(s);
// 	// alert(s);
// 	return s;
// }
//
// function getCountry(latLng) {
//     geocoder.geocode( {'latLng': latLng},
//         function(results, status) {
//             if(status === google.maps.GeocoderStatus.OK) {
//                 if(results[0]) {
//                     for(var i = 0; i < results[0].address_components.length; i++) {
//                         if(results[0].address_components[i].types[0] === "country") {
//                             alert(results[0].address_components[i].long_name);
//                         }
//                     }
//                 }
//                 else {
//                     alert("No results");
//                 }
//             }
//             else {
//                 alert("Status: " + status);
//             }
//         }
//     );
// }