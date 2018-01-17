var photo;
var match4AllCurrentFilterNum = 0;
var addedFilters = "";
var filterTypesChosen = [];
var filterWordsChosen = [];
var additionalFiltersSelected ="";

//for updateyoutube link
var link_you =""
var song_name="";
var song_artist="";

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
        document.getElementById("browsebutton").innerHTML = "Change picture <input id=\"inputFileToLoad\" type=\"file\" style=\"display: none;\" onclick=\"encodeImageFileAsURL();\" onchange=\"encodeImageFileAsURL();\">";
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

function createTableFromResponse(responseArr,isSongTable) {
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


function likerowImageToMusic(rowNumber){
    var t = document.getElementsByClassName("imagetable");
    var htmlTable = t[0];
    var rows = htmlTable.rows;
    var specificRow=rows[rowNumber];
    var rowCells = specificRow.cells;
    song_name = rowCells[0].innerText;
    song_artist = rowCells[1].innerText;
    user_name = getCookieImageToMusic("user");
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

function getCookieImageToMusic(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
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

function insertButtonInTable(rowNumber){
    return "<button class='btn btn-default' onclick='fillUpdateRow("+rowNumber+")'>insert a youtube link</button>";
}

function fillUpdateRow(rowNumber){
    var t = document.getElementsByClassName("imagetable");
    var htmlTable = t[0];
    var rows = htmlTable.rows;
    var specificRow=rows[rowNumber];
    var rowCells = specificRow.cells;
    var specificcell = rowCells[3];
    document.getElementById("keyword").value = rowCells[0].innerText;
    document.getElementById("songname").value = rowCells[1].innerText;
    song_name = rowCells[1].innerText;
    document.getElementById("artist").value = rowCells[2].innerText;
    song_artist = rowCells[2].innerText;
    document.getElementById("youtubelink").value = "Please insert a link to update";
    document.getElementById("updaterow").style.visibility ="visible";
}

function updateYouTubeLinkTable(){
    link_you = document.getElementById("youtubelink").value;
    loadDocSpecialQueryimagetotext("updateyoutubelink");
}

function loadDocSpecialQueryimagetotext(flowname) {
    var sentData= createJSONStringforUpdate(flowname, "link", "song_name","song_artist");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            if(this.responseText === "None"){
                alert("Couldn't add youtube link! please try entering a valid link")
            }else{
                alert("successfully added youtube link! please query image again to see results");
            }
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send("data="+sentData);
}

function createJSONStringforUpdate(flowname,key1,key2,key3) {
    var jsonString = "{";
    jsonString = addFlowNameJSON(jsonString,flowname);
    jsonString = addparamsKeyforJSON(jsonString);
    jsonString = addParamJSON(jsonString,key1,link_you);
    jsonString+=",";
    jsonString = addParamJSON(jsonString,key2,song_name);
    jsonString+=",";
    jsonString = addParamJSON(jsonString,key3,song_artist);
    jsonString += "]}";
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
    return jsonString;
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

function loadDataForImageToMusic(postUrl) {
    var xhttp = new XMLHttpRequest();
    document.getElementById("loadingsign").style.visibility="visible";
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr,"1");
            fadeInTable(finalTable);
            document.getElementById("imageToTextHeader").innerText = "By extracting the keyword "+responseArr.keyword+" the Following songs were found:";
            fadeOutButtons("browsebutton", "loadbutton", "loadingsign");
        }
    };
    xhttp.open("POST", "Generic", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (photo) {
        var sentData = createJSONStringforImage(postUrl,encodeURIComponent(photo.substring(photo.indexOf(",") + 1)));
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
    if (event.target === loginModel ) {
        loginModel.style.display = "none";
    }
    if (event.target === signInModel ) {
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
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr);
            fadeInTable(finalTable);
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
    return jsonString;
}

function converNumToGroupBy(num){
    switch(num){
        case "spec0":
            return "GroupbyArtist";
        case "spec1":
            return "Groupbysongname";
        case "spec2":
            return "OrderbyArtist";
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
    for(var i=0;i<specArr.length;i++){
        var spec = specArr[i];
        if(spec.id !== filterNotToDisable){
            spec.disabled = "true";
        }
    }
}

