const FLASK_API = "localhost:5000"

function loadXMLDoc_GETHIGHSCORE(){
    var xmlHttp = new XMLHttpRequest ();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200){
            var responseText =  xmlHttp.responseText;
            objs = JSON.parse(responseText)
            populateHighScoreData(objs);
        }
    };
    xmlHttp.open ( "GET", "http://" + FLASK_API + "/HighScores/GetTopTen", true);
    xmlHttp.setRequestHeader('Content-Type', 'application/json');
    xmlHttp.send();
}

function loadXMLDoc_GETHIGHSCOREPOSITION (username, currentScore){
    socket.emit("requestScorePosition", {username, currentScore})
    // var xmlHttp = new XMLHttpRequest ();

    // var data = JSON.stringify({"score": currentScore});
    // xmlHttp.onreadystatechange = function () {
    //     if (this.readyState == 4 && this.status == 200){
    //         document.getElementById("highScorePosition").innerHTML =  xmlHttp.responseText + 'st'
    //     }
    // }
    // xmlHttp.open ( "POST", "http://" + FLASK_API + "/HighScores/GetPosition", true);
    // xmlHttp.setRequestHeader('Content-Type', 'application/json');
    // xmlHttp.send(data);
}	

function loadXMLDoc_PUSHTOHIGHSCOREDATABASE(username, score){
var data = JSON.stringify({"username": username, "score": score});
    var xmlhttp = new XMLHttpRequest ();
    
    xmlhttp.open ( "POST", "http://" + FLASK_API + "/HighScores/Add", false);
        xmlhttp.setRequestHeader('content-type', 'application/json');
        xmlhttp.send(data);
    return xmlhttp.responsetext;
}