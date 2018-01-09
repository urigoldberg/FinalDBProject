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
        document.getElementById("loadbutton").style.visibility ="visible";
        document.getElementById("browsebutton").innerText = "Change picture";
    }
}

function loadDoc() {
    var xhttp = new XMLHttpRequest();
    document.getElementById("loadingsign").style.visibility="visible";
    xhttp.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            var responseArr = JSON.parse(this.responseText);
            console.log("initializing table head and opening body tag");
            var finalTable = "<table class=\"table table-striped imagetable\">" +
                "<thead>" +
                "<tr><th>Artist</th>" +
                "<th>Song name</th>" +
                "<th>YouTube link</th></tr>" +
                "</thead>" +
                "<tbody>";
            for(i=0;i<responseArr.rows.length;i++){
                finalTable+=
                    "<tr>" +
                    "<th>" + responseArr.rows[i].SongName +
                    "</th><th>"+responseArr.rows[i].Artist+"</th>" +
                    "<th>"+responseArr.rows[i].YoutubeLink+"</th>" +
                    "</tr>";
            }
            finalTable+= "</tbody></table>";
            document.getElementById("imgTest").innerHTML = finalTable;
            document.getElementById("imageToTextHeader").innerText = "The Following songs were found:";
            console.log("before hiding buttons");
            document.getElementById("browsebutton").style.visibility = "hidden";
            document.getElementById("loadbutton").style.visibility = "hidden";
            document.getElementById("loadingsign").style.visibility="hidden";

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

