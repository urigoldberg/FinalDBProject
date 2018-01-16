var DEADButton = 1;
var q2Button = 1;
var q3Button = 1;


function createTableFromResponse(responseArr) {
    if(responseArr.isError == "true"){
        return "<p>"+responseArr.errorMessage+"</p>"
    }
    var numofRows = responseArr.Results.length;
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
    //filling table rows
    finaltable+="</tr></thead></tbody>";
    for (var i = 0; i < numofRows; i++){
        finaltable+="<tr>";
        for(var j=0;j<numofCols;j++){
            var val = responseArr.Results[i][columnNames[j]];
            finaltable+="<th>"+val+"</th>";
        }
        finaltable+="</tr>";
    }
    finaltable += "</tbody></table>";
    return finaltable;
}

function fadeInTable(finalTable, elementToReplaceByTable) {
    elementToReplaceByTable = elementToReplaceByTable || "imgTest";
    document.getElementById(elementToReplaceByTable).style.display = "none";
    document.getElementById(elementToReplaceByTable).innerHTML = finalTable;
    $("#"+elementToReplaceByTable).fadeIn(1500);
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

function loadDocSpecialQuery(flowname, elementToReplaceByTable) {
    var sentData;
    if(flowname === "columnname"){
        sentData = createJSONStringforDistinctColumnName(flowname, "genre", "Song");
    }else if(flowname === "year"){
        sentData = createJSONString(flowname, "num", "genre","dead");
    }
    else if(flowname === "youTubeLink"){
        sentData = createJSONString(flowname, "artistname", "operation");
    }
    else{
        sentData = createJSONString(flowname, "location", "genre");
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr);
            // debugger;
            fadeInTable(finalTable,elementToReplaceByTable);
            document.getElementById("responseheader").innerText = "the Following year was found:";
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
        jsonString = addParamJSON(jsonString,elementId,num);
        jsonString+=",";
    }
    if(elementId2){
        console.log(elementId2);
        var genre = document.getElementById(elementId2).value;
        jsonString = addParamJSON(jsonString,elementId2,genre);
    }
    if(keyString){
        jsonString+=",";
        x = document.getElementById("sel0").value === "Died" ? "1" : "0";
        jsonString = addParamJSON(jsonString,keyString,x);
    }
    jsonString += "]}";
    debugger;
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
            "                    <span class=\"form-group tofade\" >\n" +
            "                    <input type=\"text\" class=\"form-control\" value=\"hip-hop\" id=\"genre\">\n" +
            "                    </span>\n" +
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
            "                    <button id=\"getSongsButton\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('year','big')\">Query</button>\n"+
        "<button id=\"changeDEAD\" class =\"btn btn-default tofade\" onclick=\"switchDEAD()\">close Death / Birth query</button>";
        DEADButton = 0;
    }
    else{
        document.getElementById("DEAD").innerHTML = "<button id=\"changeDEAD\" class =\"btn btn-default\" onclick=\"switchDEAD()\">open Death / Birth query</button>";
        DEADButton=1;
    }
}

function switchMostViewed() {
    if(q2Button === 1){
        document.getElementById("q2").innerHTML = "<p>Most viewed artists on YouTube with Genre:</p>\n" +
            "                    <form id=\"q2form\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"genre\"></select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "                    <p>From location:</p>\n" +
            "                    <span class=\"form-group tofade\" >\n" +
            "                    <input type=\"text\" class=\"form-control\" value=\"usa\" id=\"location\">\n" +
            "                    </span>\n"+
            "<button id=\"getmostviewed\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('mostviewedartist','q2')\">Query</button>\n"+
            "<button id=\"changeq2\" class =\"btn btn-default\" onclick=\"switchMostViewed()\">Close most viewed query</button>";
        console.log("Setting q2Button to 0");
        loadDistinctDropdown("columnname", "genre", "genre", "Song");
        q2Button = 0;
    }
    else{
        document.getElementById("q2").innerHTML = "<button id=\"changeq2\" class =\"btn btn-default\" onclick=\"switchMostViewed()\">Open most viewed query</button>";
        console.log("Setting q2Button to 1");
        q2Button=1;
    }
}

function switchYouTubeLink() {
    if(q3Button === 1){
        document.getElementById("q3").innerHTML = "<p>Longest/shortest song on youtube of one of the following artists:</p>\n" +
            "                    <form id=\"q3form\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"artistname\"></select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "                    <form class=\"tofade\">\n" +
            "                        <div class=\"form-group\">\n" +
            "                            <select class=\"form-control\" id=\"operation\">\n" +
            "                                <option>max</option>\n" +
            "                                <option>min</option>\n" +
            "                            </select>\n" +
            "                        </div>\n" +
            "                    </form>\n" +
            "<button id=\"getmostviewed\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('youTubeLink','q3')\">Query</button>\n"+
            "<button id=\"changeq3\" class =\"btn btn-default\" onclick=\"switchYouTubeLink()\">Close YouTube link query</button>";
        console.log("Setting q3Button to 0");
        loadDistinctDropdown("columnname", "artistname", "name", "artists");
        q3Button = 0;
    }
    else{
        document.getElementById("q3").innerHTML = "<button id=\"changeq3\" class =\"btn btn-default\" onclick=\"switchYouTubeLink()\">open YouTube link query</button>";
        console.log("Setting q3Button to 1");
        q3Button=1;
    }
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
    var x;
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

function fillDropdownFromResponse(responseArr,columnName) {
    if(responseArr.isError == "true"){
        return "<p>"+responseArr.errorMessage+"</p>"
    }
    var numofRows = responseArr.Results.length;
    var finalDropDownOptions ="";
    // debugger;
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

