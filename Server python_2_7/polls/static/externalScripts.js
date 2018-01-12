var photo;

var match4allfilternum = 1;

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

function createTableFromResponse(responseArr) {
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

function fadeInTable(finalTable) {
    document.getElementById("imgTest").style.display = "none";
    document.getElementById("imgTest").innerHTML = finalTable;
    $("#imgTest").fadeIn(1500);
}

function fadeOutButtons(elementId, elementId2, elementId3) {
    elementId3 = elementId3 || "loadingsign";
    elementId2 = elementId2 || "loadbutton";
    elementId = elementId || "browsebutton";
    console.log("before hiding buttons");
    document.getElementById(elementId).style.visibility = "hidden";
    document.getElementById(elementId2).style.visibility = "hidden";
    document.getElementById(elementId3).style.visibility = "hidden";
}

function loadDoc(postUrl, sentData) {
    sentData = sentData || "photo=" + encodeURIComponent(photo.substring(photo.indexOf(",") + 1));
    postUrl = postUrl || "pictureQuery";
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
    xhttp.open("POST", postUrl, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (photo) {
        xhttp.send(sentData);
    }
    else {
        alert("Please enter a photo!");
    }
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    var loginmodal = document.getElementById('Login');
    var signinmodel = document.getElementById('SignIn');
    if (event.target == loginmodal ) {
        loginmodal.style.display = "none";
    }
    if (event.target == signinmodel ) {
        signinmodel.style.display = "none";
    }
}

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

function addFilterNum(addedFilters,i) {
    addedFilters += "<form>\n" +
        "                    <div class=\"form-group\">\n" +
        "                        <label for=\"sel"+ i +"\">Select list (select one):</label>\n" +
        "                        <select class=\"form-control\" id=\"sel\"+ i +\"\">\n" +
        "                            <option>Artist</option>\n" +
        "                            <option>Song name</option>\n" +
        "                            <option>Genere</option>\n" +
        "                        </select>\n" +
        "                    </div>\n" +
        "                </form>\n" +
        "\n" +
        "                <div class=\"form-group\">\n" +
        "                    <input id=\"keywordToSearch\"+ i +\"\" type=\"text\" class=\"form-control\" value=\"write keyword here\">\n" +
        "                </div>"
    return addedFilters;
}

function addfilter(){
    match4allfilternum+=1;
    var addedFilters;
    for(i=0;i<match4allfilternum-1;i++){
        addedFilters = addFilterNum(addedFilters,i+1);
    }
    document.getElementById("big").innerHTML = addedFilters;

}

