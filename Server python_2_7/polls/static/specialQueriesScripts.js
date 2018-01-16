var DEADButton = 1;

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

function hideDisplayofClass(classNames) {
    var fadeArr = document.getElementsByClassName(classNames);
    for (i = 0; i < fadeArr.length; i++) {
        fadeArr[i].style.display = "none";
    }
}

function loadDocSpecialQuery(postUrl) {
    var sentData = createJSONString(postUrl);
    var xhttp = new XMLHttpRequest();
    // debugger;
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            // debugger;
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr);
            fadeInTable(finalTable,"big");
            document.getElementById("responseheader").innerText = "the Following year was found:";
            // debugger;
            hideDisplayofClass("tofade");
            hideDisplayofClass("querybutton");
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    // debugger;
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

function createJSONString(flowname) {
    var x;
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    // debugger;
    var num = document.getElementById("num").value;
    jsonString = addParamJSON(jsonString,"num",num);
    jsonString+=",";
    var genre = document.getElementById("genre").value;
    jsonString = addParamJSON(jsonString,"genre",genre);
    jsonString+=",";
    x = document.getElementById("sel0").value == "Died" ? "1" : "0";
    jsonString = addParamJSON(jsonString,"dead",x);
    jsonString += "]}";
    // debugger;
    return jsonString;
}

function switchDEAD(){
    if(DEADButton == 1){
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
            "                    <button id=\"getSongsButton\" class =\"btn btn-default querybutton \" onclick=\"loadDocSpecialQuery('year')\" >Query</button>\n"+
        "<button id=\"changeDEAD\" class =\"btn btn-default tofade\" onclick=\"switchDEAD()\">close Death / Birth query</button>";
        DEADButton = 0;
    }
    else{
        document.getElementById("DEAD").innerHTML = "<button id=\"changeDEAD\" class =\"btn btn-default\" onclick=\"switchDEAD()\">open Death / Birth query</button>";
        DEADButton=1;
    }
}

