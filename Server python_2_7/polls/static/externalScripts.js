//var photo;

function encodeImageFileAsURL1() {
    var filesSelected = document.getElementById("inputFileToLoad").files;
    if (filesSelected.length > 0) {
        var fileToLoad = filesSelected[0];
        var fileReader = new FileReader();
        fileReader.onload = function(fileLoadedEvent) {
            var srcData = fileLoadedEvent.target.result; // <--- data: base64
            var newImage = document.createElement('img');
            newImage.src = srcData;
            photo = srcData;
            //debugger;
            //document.getElementById("imgTest").innerHTML = newImage.outerHTML;
            document.getElementById("change").src = newImage.src;
            //alert("Converted Base64 version is " + document.getElementById("imgTest").innerHTML);
            //console.log("Converted Base64 version is " + document.getElementById("imgTest").innerHTML);
            console.log("Converted Base64 length is: " + document.getElementById("imgTest").innerHTML.length);
        };
        fileReader.readAsDataURL(fileToLoad);
    }
}

function loadDoc1() {
    var xhttp = new XMLHttpRequest(),
        responseType = "json",
        onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                alert(this.response);
                document.getElementById("demo").innerHTML = this.responseText;
                var responseArr = JSON.parse(this.response);
                //initializing table head and opening body tag
                var finalTable = "<table class=\"table table-striped\"><thead><tr><th>Artist</th><th>Song name</th></tr></thead><tbody>";
                for(i=0;i<responseArr.length;i++){
                        finalTable+="<tr><th>" + responseArr.first +"</th><th>"+responseArr.second+"</th></tr>";
                }
                finalTable+= "</tbody></table>";
                //alert(responseArr.size);
                console.log("grasssss tasts bad!!");
                document.getElementById("imgTest").innerHTML = finalTable;
                document.getElementById("browsebutton").hidden = true;
                document.getElementById("loadbutton").hidden = true;
            }
        };
    xhttp.open("POST", "polls/pictureQuery", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (photo) {
        xhttp.send("photo="+encodeURIComponent(photo.substring(22)));
    }
    else {
        alert("enter a photo");
    }
}

var photo;
function encodeImageFileAsURL() {
    alert("hi!");
    var filesSelected = document.getElementById("inputFileToLoad").files;
    if (filesSelected.length > 0) {
        var fileToLoad = filesSelected[0];
        var fileReader = new FileReader();
        fileReader.onload = function(fileLoadedEvent) {
            var srcData = fileLoadedEvent.target.result; // <--- data: base64
            var newImage = document.createElement('img');
            newImage.src = srcData;
            photo = srcData;
            //debugger;
            //document.getElementById("imgTest").innerHTML = newImage.outerHTML;
            document.getElementById("change").src = newImage.src;
            //alert("Converted Base64 version is " + document.getElementById("imgTest").innerHTML);
            //console.log("Converted Base64 version is " + document.getElementById("imgTest").innerHTML);
        };
        fileReader.readAsDataURL(fileToLoad);
    }
}

function loadDoc() {
    alert("fdsfdsfsdf");
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        alert(this.readyState);
        if (this.readyState === 4 && this.status === 200) {
            //document.getElementById("demo").innerHTML = "the xml from Vision Api is:" + this.responseText;
            alert(this.responseText);
        }
    };
    xhttp.open("POST", "polls/pictureQuery", true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    if (photo) {

        xhttp.send("photo="+encodeURIComponent(photo.substring(photo.indexOf(",")+1)));
    }
    else {
        alert("enter a photo");
    }
}
