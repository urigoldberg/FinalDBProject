var photo;
var match4AllCurrentFilterNum = 0;
var addedFilters = "";
var filterTypesChosen = [];
var filterWordsChosen = [];
var additionalFiltersSelected ="";

function encodeImageFileAsURL() {
    var filesSelected = document.getElementById("inputFileToLoad").files;
    if (filesSelected.length > 0) {
        var fileToLoad = filesSelected[0];
        var fileReader = new FileReader();
        fileReader.onload = function(fileLoadedEvent) {
            var srcData = fileLoadedEvent.target.result; // <--- data: base64
            var newImage = document.createElement('img');
            newImage.src = srcData;
            photo = srcData;
            document.getElementById("change").src = newImage.src;
            console.log("Converted Base64 length is: " + document.getElementById("imgTest").innerHTML.length);
        };
        fileReader.readAsDataURL(fileToLoad);
        document.getElementById("browsebutton").innerText = "Change picture";
        $("#loadbutton").fadeIn(1500);
    }
}

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
    var numOfRows = responseArr.Results.length;
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
    for (var i = 0; i < numOfRows; i++){
        finaltable+="<tr>";
        for(var j=0;j<numofCols;j++){
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

function loadDoc(postUrl) {
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
        // debugger;
        xhttp.send("data="+sentData);
    }
    else {
        alert("Please enter a photo!");
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    var loginModel = document.getElementById('Login');
    var signInModel = document.getElementById('SignIn');
    if (event.target == loginModel ) {
        loginModel.style.display = "none";
    }
    if (event.target == signInModel ) {
        signInModel.style.display = "none";
    }
};

function usermessage(message,show){
    if(show){
        alert(message);
    }
}

function searchKeyword(keyword){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            // debugger;
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr);
            fadeInTable(finalTable);
            // debugger;
            document.getElementById("imageToTextHeader").innerText = "By extracting the keyword "+responseArr.keyword+" the Following songs were found:";
            fadeOutButtons("keywordToSearch","getSongsButton");
        }
    };
    xhttp.open("POST", "keywordQuery", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (keyword) {
        xhttp.send(keyword);
    }
    else {
        alert("Please enter a keyword!");
    }
}

function addFilterNum(i) {
    console.log("adding filter form with select "+i);
    addedFilters += "<form>\n" +
        "                    <div class=\"form-group\">\n" +
        "                        <label for=\"sel"+i+"\">Select filter type:</label>\n" +
        "                        <select class=\"form-control\" id=\"sel"+i+"\">\n" +
        "                            <option>Artist</option>\n" +
        "                            <option>Song name</option>\n" +
        "                            <option>Genre</option>\n" +
        "                        </select>\n" +
        "                    </div>\n" +
        "                </form>\n" +
        "\n" +
        "                <div class=\"form-group\">\n" +
        "                    <label for=\"keywordToSearch"+i+"\">Enter keyword for filter:</label>\n" +
        "                    <input id=\"keywordToSearch"+i+"\" type=\"text\" class=\"form-control\" value=\"write keyword here\">\n" +
        "                </div>";
    return addedFilters;
}

function printArraysTillNow() {
    for (var i = 0; i < match4AllCurrentFilterNum; i++) {
        console.log("type number " + i + " is: " + filterTypesChosen[i] + ", filter number " + i + " is: " + filterWordsChosen[i]);
    }
}

function addfilter(){
    match4AllCurrentFilterNum+=1;
    savePreviousSelections();
    addFilterNum(match4AllCurrentFilterNum);
    document.getElementById("big").innerHTML = addedFilters;
    printArraysTillNow();
    fillOldFilters();
}

function queryDBforFilters() {
    var sentData = getJSONStringOfValues();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            //create table from response
            var finalTable = createTableFromResponse(responseArr);
            fadeInTable(finalTable,"big");
            //remove all forms
            document.getElementById("initialinput").style.visibility = "hidden";
            document.getElementById("initialform").style.visibility = "hidden";
            document.getElementById("responseheader").innerHTML = "<h4>By extracting the keyword "+responseArr.keyword+" the Following songs were found:</h4>";
            fadeOutButtons("addAnotherButton", "getSongsButton");
        }
    };

    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    console.log("String for JSON is: "+ sentData);
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
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    for (var i = 0; i < match4AllCurrentFilterNum; i++) {
        jsonString = addParamJSON(jsonString,filterTypesChosen[i],filterWordsChosen[i]);
        if (i < match4AllCurrentFilterNum - 1) {
            jsonString += ",";
        }
    }
    if(additionalFiltersSelected !== ""){
        jsonString+=",";
        jsonString = addParamJSON(jsonString,"additionalFilters",converNumToGroupBy(additionalFiltersSelected));
    }
    jsonString += "]}";
    debugger;
    return jsonString;
}

function converNumToGroupBy(num){
    switch(num){
        case "spec0":
            return "GroupbyArtist";
        case "spec1":
            return "Groupbysongname";
        case "spec2":
            return "Orderbysongname";
        case "spec3":
            return "Orderbysongname";
    }
}

function getJSONStringOfValues(){
    match4AllCurrentFilterNum++;
    savePreviousSelections();
    return createJSONString("filterKeys");
}

function savePreviousSelections(){
    for(var i=0; i<match4AllCurrentFilterNum; i++){
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
    for(var i=1; i<match4AllCurrentFilterNum; i++){
        var selId = "sel"+(i);
        document.getElementById(selId).value = filterTypesChosen[i];
        var keywordId = "keywordToSearch"+(i);
        document.getElementById(keywordId).value = filterWordsChosen[i];
    }
}

function disableSpecialFilters(filterNotToDisable){
    additionalFiltersSelected = filterNotToDisable;
    var specArr = document.getElementsByClassName("spec");
    // debugger;
    for(var i=0;i<specArr.length;i++){
        var spec = specArr[i];
        if(spec.id !== filterNotToDisable){
            spec.disabled = "true";
        }
    }
}

