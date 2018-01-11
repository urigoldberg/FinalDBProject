var photo;

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
    var finalTable = "<table class=\"table table-striped imagetable\">" +
        "<thead>" +
        "<tr><th>Artist</th>" +
        "<th>Song name</th>" +
        "<th>YouTube link</th></tr>" +
        "</thead>" +
        "<tbody>";
    for (i = 0; i < responseArr.Results.length; i++) {
        finalTable +=
            "<tr>" +
            "<th>" + responseArr.Results[i].song_name +
            "</th><th>" + responseArr.Results[i].artist_name + "</th>" +
            "<th>" + responseArr.Results[i].youtube_link + "</th>" +
            "</tr>";
    }
    finalTable += "</tbody></table>";
    return finalTable;
}

function fadeInTable(finalTable) {
    document.getElementById("imgTest").style.display = "none";
    document.getElementById("imgTest").innerHTML = finalTable;
    $("#imgTest").fadeIn(1500);
}

function fadeOutButtons() {
    console.log("before hiding buttons");
    document.getElementById("browsebutton").style.visibility = "hidden";
    document.getElementById("loadbutton").style.visibility = "hidden";
    document.getElementById("loadingsign").style.visibility = "hidden";
}

function loadDoc() {
    var xhttp = new XMLHttpRequest();
    document.getElementById("loadingsign").style.visibility="visible";
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            debugger;
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = createTableFromResponse(responseArr);
            fadeInTable(finalTable);
            document.getElementById("imageToTextHeader").innerText = "By extracting the keyword "+responseArr.keyword+" the Following songs were found:";
            fadeOutButtons();
        }
    };
    xhttp.open("POST", "pictureQuery", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (photo) {
        xhttp.send("photo="+encodeURIComponent(photo.substring(photo.indexOf(",")+1)));
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

