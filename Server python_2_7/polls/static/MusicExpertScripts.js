var DEADButton = 1;
var mostViewedButton = 1;
var youTubeLinkButton = 1;
var albumWithSalesButton = 1;
var personalizeButton = 1;
var songsILikedButton = 1;

//for like song
var song_name;
var song_artist;
var user_name;


function createTableFromResponse(responseArr,isSongTable) {
    var urlcolumnNum;
    if(responseArr.isError == "true"){
        return "<p>"+responseArr.errorMessage+"</p>"
    }
    var numofRows = responseArr.Results.length;
    var columnNames = [];
    var tempUrlColumnNum = 0;
    for (var colName in responseArr.Results[0]) {
        if (colName) {
            columnNames.push(colName);
            if(colName === "URL"||colName ==="Youtube Link"  ||colName === "media_url"){
                urlcolumnNum = tempUrlColumnNum;
            }
            tempUrlColumnNum++;
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
    for (var i = 0; i < numofRows; i++){
        finaltable+="<tr>";
        for(var j=0;j<numofCols;j++){
            var val = responseArr.Results[i][columnNames[j]];
            if( j === urlcolumnNum && val !== "" && val!== "None"){
                finaltable+= "<th>"+linkToYouTube(val)+"</th>";
            }else{
                finaltable+="<th>"+val+"</th>";
            }
        }
        if(isSongTable === "1"){
            finaltable+="<th><button class='btn btn-default' onclick='likerow("+i+1+")'>Like song!</button></th>"
        }
        finaltable+="</tr>";
    }
    finaltable += "</tbody></table>";
    return finaltable;
}

function linkToYouTube(link){
    return "<a href="+link+" target=\"_blank\">Open YouTube Video</a>" ;
}

function likerow(rowNumber){
    var t = document.getElementsByClassName("imagetable");
    var htmlTable = t[0];
    var rows = htmlTable.rows;
    var specificRow=rows[rowNumber];
    var rowCells = specificRow.cells;
    song_name = rowCells[0].innerText;
    song_artist = rowCells[1].innerText;
    user_name = getCookie("user");
    var sentData = createJSONStringforLike("add_liked_song","song_name","song_artist","user_name");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            if(responseArr.isError === "true"){
                alert("Error liking this song! " + responseArr.errorMessage);
            }
            else{
                if(responseArr.Result === "false"){
                    alert("already liked this song");
                }else{
                    alert("successfully liked this song!");
                }
            }
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+sentData);
}

function fadeInTable(finalTable, elementIDToReplaceByTable) {
    elementIDToReplaceByTable = elementIDToReplaceByTable || "imgTest";
    document.getElementById(elementIDToReplaceByTable).style.display = "none";
    document.getElementById(elementIDToReplaceByTable).innerHTML = finalTable;
    $("#"+elementIDToReplaceByTable).fadeIn(1500);
}

function fadeOutButtons(elementId, elementId2, elementId3) {
    console.log("before hiding buttons");
    if(elementId){
        document.getElementById(elementId).style.visibility = "hidden";
    }
    if(elementId2){
        document.getElementById(elementId2).style.visibility = "hidden";
    }
    if(elementId3){
        document.getElementById(elementId3).style.visibility = "hidden";
    }
}

function hideDisplayofClass(classNames) {
    var fadeArr = document.getElementsByClassName(classNames);
    for (var i = 0; i < fadeArr.length; i++) {
        fadeArr[i].style.display = "none";
    }
}

function loadDocSpecialQuery(flowname, elementToReplaceByTable, replayText) {
    replayText = replayText || "the Following year was found:";
    var sentData;
    var isSongTable = "0";
    if(flowname === "columnname"){
        sentData = createJSONStringforDistinctColumnName(flowname, "genre", "Song");
    }else if(flowname === "year"){
        sentData = createJSONString(flowname, "num", "genre","dead");
    }
    else if(flowname === "youTubeLink"){
        sentData = createJSONString(flowname, "artistname", "operation");
        isSongTable = "1";
    }
    else if(flowname === "SucAlbums"){
        sentData = createJSONString(flowname, "genre", "numOfSales");
    }
    else{
        sentData = createJSONString(flowname, "location", "genre");
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr,isSongTable);
            fadeInTable(finalTable,elementToReplaceByTable);
            if(flowname === "year"){
                document.getElementById("responseheader").innerText = replayText;
            }
            hideDisplayofClass("tofade");
            hideDisplayofClass("querybutton");
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+sentData);
}

function addFlowNameJSON(jsonString, flowname) {
    jsonString += "\"flowname\":" + "\"" + flowname + "\",";
    return jsonString;
}

function addparamsKeyforJSON(jsonString) {
    jsonString += "\"params\":[";
    return jsonString;
}

function addParamJSON(jsonString, keyString, valueString) {
    jsonString += "{\"" + keyString + "\"" + ":" + "\"" + valueString + "\"}";
    return jsonString;
}

function createJSONString(flowname, elementId, elementId2, keyString) {
    var x;
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    if(elementId){
        var num = document.getElementById(elementId).value;
        num = num.replace("&","_AND_");
        jsonString = addParamJSON(jsonString,elementId,num);
        jsonString+=",";
    }
    if(elementId2){
        console.log(elementId2);
        var genre = document.getElementById(elementId2).value;
        genre = genre.replace("&","_AND_");
        jsonString = addParamJSON(jsonString,elementId2,genre);
    }
    if(keyString){
        jsonString+=",";
        x = document.getElementById("sel0").value === "Died" ? "1" : "0";
        jsonString = addParamJSON(jsonString,keyString,x);
    }
    jsonString += "]}";
    return jsonString;
}

function createJSONStringforLike(flowname, elementId, elementId2, elementId3) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,elementId,song_name);
    jsonString+=",";
    jsonString = addParamJSON(jsonString,elementId2,song_artist);
    jsonString+=",";
    jsonString = addParamJSON(jsonString,elementId3,user_name);
    jsonString += "]}";
    return jsonString;
}

function switchDEAD(){
    if(DEADButton === 1){
        document.getElementById("DEAD").innerHTML = "<div id=\"responseheader\"></div>\n" +
            "                    <h4 class=\"tofade\">Death / Birth query:</h4>\n" +
            "                    <span class=\"tofade\">the year that at least </span>\n" +
            "                    <span class=\"form-group tofade\" >\n" +
            "                    <input type=\"text\" class=\"form-control\" value=\"2\" id=\"num\">\n" +
            "                    </span>\n" +
            "                    <span class=\"tofade\">artists of genre </span>\n" +
            "                    <form id=\"q2form\" class='tofade'>\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control tofade\" id=\"genre\"></select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "                    <span class=\"tofade\"> have </span>\n" +
            "                    <form id=\"Died\" class=\"tofade\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"sel0\">\n" +
            "                                <option>Died</option>\n" +
            "                                <option>Born</option>\n" +
            "                            </select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "\n" +
            "                    <!--added forms will be here-->\n" +
            "                    <div id=\"big\"></div>\n" +
            "\n" +
            "                    <button id=\"getSongsButton\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('year','big','the Following year was found:')\">Query</button>\n"+
        "<button id=\"changeDEAD\" class =\"btn btn-default tofade\" onclick=\"switchDEAD()\">Close Death / Birth query</button>";
        loadDistinctDropdown("columnname", "genre", "genre", "Song");
        DEADButton = 0;
    }
    else{
        document.getElementById("DEAD").innerHTML = "<button id=\"changeDEAD\" class =\"btn btn-default\" onclick=\"switchDEAD()\">Open Death / Birth query</button>";
        DEADButton=1;
    }
}

function switchMostViewed() {
    if(mostViewedButton === 1){
        document.getElementById("q2").innerHTML = "<div id=\"responseheader\"></div>\n" +
            "                    <h4 class=\"tofade\">Most viewed query:</h4>\n" +
            "                    <p>Most viewed artists on YouTube with Genre:</p>\n" +
            "                    <form id=\"q2form\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"genre\"></select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "                    <p>From location:</p>" +
            "                    <span class=\"form-group tofade\" >\n" +
            "                    <input type=\"text\" class=\"form-control\" value=\"usa\" id=\"location\">\n" +
            "                    </span>\n"+
            "<button id=\"getmostviewed\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('mostviewedartist','q2','the Following Artists were found:')\">Query</button>\n"+
            "<button id=\"changeq2\" class =\"btn btn-default\" onclick=\"switchMostViewed()\">Close most viewed query</button>";
        console.log("Setting mostViewedButton to 0");
        loadDistinctDropdown("columnname", "genre", "genre", "Song");
        mostViewedButton = 0;
    }
    else{
        document.getElementById("q2").innerHTML = "<button id=\"changeq2\" class =\"btn btn-default\" onclick=\"switchMostViewed()\">Open most viewed query</button>";
        console.log("Setting mostViewedButton to 1");
        mostViewedButton=1;
    }
}

function switchYouTubeLink() {
    if(youTubeLinkButton === 1){
        document.getElementById("q3").innerHTML = "<div id=\"responseheader\"></div>\n" +
            "                    <h4 class=\"tofade\">Youtube Link query:</h4>\n" +
            "                    <form class=\"tofade\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"operation\">\n" +
            "                                <option>max</option>\n" +
            "                                <option>min</option>\n" +
            "                            </select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "                    <p>length song on youtube of one of the following artists:</p>\n" +
            "                    <form id=\"q3form\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"artistname\"></select>\n" +
            "                        </div>\n" +
            "                    </form>" +
            "<button id=\"getmostviewed\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('youTubeLink','q3','the Following songs were found:')\">Query</button>\n"+
            "<button id=\"changeq3\" class =\"btn btn-default\" onclick=\"switchYouTubeLink()\">Close Longest/Shortest YouTube video query</button>";
        console.log("Setting youTubeLinkButton to 0");
        loadDistinctDropdown("columnname", "artistname", "name", "Artist");
        youTubeLinkButton = 0;
    }
    else{
        document.getElementById("q3").innerHTML = "<button id=\"changeq3\" class =\"btn btn-default\" onclick=\"switchYouTubeLink()\">Open Longest/Shortest YouTube video query</button>";
        console.log("Setting youTubeLinkButton to 1");
        youTubeLinkButton=1;
    }
}

function switchAlbumWithSales(){
    if(albumWithSalesButton === 1){
        document.getElementById("q4").innerHTML = "<div id=\"responseheader\"></div>\n" +
            "<h4 class=\"tofade\">Album with sales query:</h4>\n"+
            "<p>Albums of the genre:</p>\n" +
            "                    <form id=\"q4form\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"genre\"></select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "                    <p>with:</p>\n"+
            "                    <form class=\"tofade\">\n" +
            "                    <span class=\"form-group tofade\" >\n" +
            "                    <input type=\"text\" class=\"form-control\" value=\"2\" id=\"numOfSales\">\n" +
            "                    </span>\n"+
            "                    </form>\n" +
            "                    <p> sales</p>\n"+
            "<button id=\"getmostviewed\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('SucAlbums','q4','the Following albums were found:')\">Query</button>\n"+
            "<button id=\"changeq4\" class =\"btn btn-default\" onclick=\"switchAlbumWithSales()\">Close Album with sales query</button>";
        console.log("Setting albumWithSalesButton to 0");
        loadDistinctDropdown("columnname", "genre", "genre", "Song");
        albumWithSalesButton = 0;
    }
    else{
        document.getElementById("q4").innerHTML = "<button id=\"changeq4\" class =\"btn btn-default\" onclick=\"switchAlbumWithSales()\">Open Album with sales query</button>";
        console.log("Setting albumWithSalesButton to 1");
        albumWithSalesButton=1;
    }
}

function switchPerzonalize(){
    if(personalizeButton === 1){
        document.getElementById("q5").innerHTML = "<div id=\"responseheader\"></div>\n" +
            "<button id=\"person\" class =\"btn btn-default\" onclick=\"sendPerson()\">query</button>"+
            "<button id=\"changeq5\" class =\"btn btn-default\" onclick=\"switchPerzonalize()\">Close Song recommendations for you query</button>";
        console.log("Setting personalizeButton to 0");
        personalizeButton = 0;
    }
    else{
        document.getElementById("q5").innerHTML = "<button id=\"changeq4\" class =\"btn btn-default\" onclick=\"switchPerzonalize()\">Open Song recommendations for you query</button>";
        console.log("Setting personalizeButton to 1");
        personalizeButton=1;
    }
}

function switchSongsILiked(){
    if(songsILikedButton === 1){
        document.getElementById("q6").innerHTML = "<div id=\"responseheader\"></div>\n" +
            "<button id=\"person\" class =\"btn btn-default\" onclick=\"sendSongsILiked()\">query</button>"+
            "<button id=\"changeq6\" class =\"btn btn-default\" onclick=\"switchSongsILiked()\">Close Songs i liked query</button>";
        console.log("Setting songsILikedButton to 0");
        songsILikedButton = 0;
    }
    else{
        document.getElementById("q6").innerHTML = "<button id=\"changeq6\" class =\"btn btn-default\" onclick=\"switchSongsILiked()\">Open Songs i liked query</button>";
        console.log("Setting songsILikedButton to 1");
        songsILikedButton=1;
    }
}

function sendSongsILiked(){
    var xhttp = new XMLHttpRequest();
    var jsonSent = createJSONStringforLikedSongs("get_all_songs","user_name");
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr,"0");
            fadeInTable(finalTable,"q6");
            hideDisplayofClass("tofade");
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+jsonSent);
}

function createJSONStringforLikedSongs(flowname, elementId, elementId2, elementId3) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,elementId,getCookie("user"));
    jsonString += "]}";
    return jsonString;
}

function sendPerson(){
    var xhttp = new XMLHttpRequest();
    var x = getCookie("user");
    var y = getCookie("bs");
    var jsonSent = createJSONStringforPersonalization("personalization",x,y);
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr,"0");
            fadeInTable(finalTable,"q5");
            hideDisplayofClass("tofade");
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+jsonSent);
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

function loadDistinctDropdown(flowName, elementIdtoChange, columnName, tablename) {
    var sentData = createJSONStringforDistinctColumnName(flowName, columnName, tablename);
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = fillDropdownFromResponse(responseArr,columnName);
            document.getElementById(elementIdtoChange).style.visibility = "hidden";
            document.getElementById(elementIdtoChange).innerHTML = finalTable;
            document.getElementById(elementIdtoChange).style.visibility = "visible";
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+sentData);
}

function createJSONStringforDistinctColumnName(flowname, columnName, tablename) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,"column",columnName);
    jsonString+=",";
    jsonString = addParamJSON(jsonString,"tablename",tablename);
    jsonString += "]}";
    console.log(jsonString);
    return jsonString;
}

function createJSONStringforPersonalization(flowname, columnName, tablename) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,"user",columnName);
    jsonString+=",";
    jsonString = addParamJSON(jsonString,"bs",tablename);
    jsonString += "]}";
    console.log(jsonString);
    return jsonString;
}

function fillDropdownFromResponse(responseArr,columnName) {
    if(responseArr.isError === "true"){
        return "<p>"+responseArr.errorMessage+"</p>"
    }
    var numofRows = responseArr.Results.length;
    var finalDropDownOptions ="";
    for(var i=0;i<numofRows;i++){
        if(columnName === "genre"){
            finalDropDownOptions+="<option>"+responseArr.Results[i].genre+"</option>";
        }
        else{
            finalDropDownOptions+="<option>"+responseArr.Results[i].name+"</option>";
        }
    }
    return finalDropDownOptions;
}

