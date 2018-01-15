var match4AllCurrentFilterNum = 0;
var addedFilters = "";
var filterTypesChosen = new Array();
var filterWordsChosen = new Array();
var additionalFiltersSelected ="";



function createJSONStringforImage(flowname, encoding) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,"photo",encoding);
    jsonString += "]}";
    return jsonString;
}

function createTableFromResponse(responseArr) {
    if(responseArr.isError == "true"){
        return "<p>"+responseArr.errorMessage+"</p>"
    }
    var numofRows = responseArr.Results.length;
    var columnNames = [];
     // debugger;
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
    for (i = 0; i < numofRows; i++){
        finaltable+="<tr>";
        for(j=0;j<numofCols;j++){
            // debugger;
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

function loadDocSpecialQuery(postUrl, sentData) {
    var xhttp = new XMLHttpRequest();
    document.getElementById("loadingsign").style.visibility="visible";
    // debugger;
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            // debugger;
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr);
            fadeInTable(finalTable);
            // debugger;
            document.getElementById("imageToTextHeader").innerText = "By extracting the keyword "+responseArr.keyword+" the Following songs were found:";
            fadeOutButtons("browsebutton", "loadbutton", "loadingsign");
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (photo) {
        var sentData = createJSONStringforImage(postUrl,encodeURIComponent(photo.substring(photo.indexOf(",") + 1)));
        debugger;
        xhttp.send("data="+sentData);
    }
    else {
        alert("Please enter a photo!");
    }
}


function printArraysTillNow() {
    for (i = 0; i < match4AllCurrentFilterNum; i++) {
        console.log("type number " + i + " is: " + filterTypesChosen[i] + ", filter number " + i + " is: " + filterWordsChosen[i]);
    }
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

function createJSONString(flowname) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    for (i = 0; i < match4AllCurrentFilterNum; i++) {
        jsonString = addParamJSON(jsonString,filterTypesChosen[i],filterWordsChosen[i]);
        if (i < match4AllCurrentFilterNum - 1) {
            jsonString += ",";
        }
    }
    if(additionalFiltersSelected){//TODO: finish this
        jsonString+=",";
        jsonString = addParamJSON(jsonString,"additionalFilters",additionalFiltersSelected) //TODO: convert this to groupby what
    }
    jsonString += "]}";
    debugger;
    return jsonString;
}

function getJSONStringOfValues(){
    match4AllCurrentFilterNum++;
    savePreviousSelections();
    var jsonString = createJSONString("filterKeys");
    return jsonString;
}

function savePreviousSelections(){
    for(i=0; i<match4AllCurrentFilterNum; i++){
        var selId = "sel"+(i);
        var temp = document.getElementById(selId);
        var typeChosen = temp.options[temp.selectedIndex].value;
        filterTypesChosen[i]=(typeChosen);
        var keywordId = "keywordToSearch"+(i);
        temp = document.getElementById(keywordId);
        var filterChosen = temp.value;
        filterWordsChosen[i]=(filterChosen);
    }
}

function fillOldFilters(){
    console.log("at fill old filters");
    for(i=1; i<match4AllCurrentFilterNum; i++){
        var selId = "sel"+(i);
        document.getElementById(selId).value = filterTypesChosen[i];
        var keywordId = "keywordToSearch"+(i);
        document.getElementById(keywordId).value = filterWordsChosen[i];
    }
}

function disableSpecialFilters(notDisable){
    additionalFiltersSelected = notDisable;
    var specArr = document.getElementsByClassName("spec");
    debugger;
    for(i=0;i<specArr.length;i++){
        var spec = specArr[i];
        if(spec.id != notDisable){
            spec.disabled = "true";
        }
    }
}

