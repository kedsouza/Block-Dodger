// The canvas
var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

// Rectangle Variables
var rectangleX = canvas.width/2 - 15;
var rectangleY = canvas.height-30;
var rightPressed = false;
var leftPressed = false;

// Border Variables
var borderRectX = 5;
var borderRectY = 20;
var borderDY = 2;
var borderLeftPosY = 0;
var borderRightPosY = 0;
var borderLeftPosX = 0;
var borderRightPosX = canvas.width-borderRectX;
var borderDY = 0

// Obstacle Variables
var obstacleLength = 7;
var obstacleHeight = 7;
var obstacleList = [];

// Game Variables
var gameOver = false;
var score = 0;
var intervalTime = 1000;
var myInterval = null;

// Create an obstacles.
function createObstacle() {
    obstacleY = 0;
    obstacleX = Math.floor((Math.random() * (canvas.width - (obstacleLength + borderRectX)) + 1));
    obstacleX +=borderRectX;
    ctx.beginPath();
    ctx.rect(obstacleX, obstacleY, obstacleLength, obstacleHeight);
    ctx.fillStyle = "#8b0000";
    ctx.fill();
    ctx.closePath();
    // Addes the obstacle's cordinates to a list.
    obstacleList.push([obstacleX, obstacleY]);
}

// Moves a specific Obstacle
function moveObstacle (pos) {
    // Gets the obstacles cordinates from the list.
    x = obstacleList [pos][0];
    y = obstacleList [pos][1];
    y+=7;
    ctx.beginPath();
    ctx.rect(x, y, obstacleLength, obstacleHeight);
    ctx.fillStyle = "#8b0000";
    ctx.fill();
    ctx.closePath(); 
    // Updates the obstacles position.
    obstacleList[pos] = [x,y];
    // Checks if the user has hit the obstacle.
    if (y >= rectangleY && ((x >= rectangleX && x + obstacleLength <= rectangleX + 30))){
            gameOver = true;
    if (username != null){
        loadXMLDoc_PUSHTOHIGHSCOREDATABASE(username, score);
        //loadxmldoc_DELETECURRENTUSER(username);
    }
            //document.location.reload();
            window.location.replace("game-over.html?username=" + username + "&score="+score);

            return;
    }
    // If the obstacle has moven of screen delete it from the list.    
    if (y > canvas.height + obstacleHeight){
       obstacleList.splice(pos, 1);
    }
}

// Creates moving Borders.
function createBorders () {
    // Left Borders
    for (var i = 0; i < 25; i++){
            ctx.beginPath();
            ctx.rect(borderLeftPosX, borderLeftPosY + borderDY, borderRectX, borderRectY);
            ctx.fillStyle = "#0024DD";
            ctx.fill();
            ctx.closePath();
            borderLeftPosY += 24
     }
     // Right Borders
     for (var i = 0; i < 25; i++){
            ctx.beginPath();
            ctx.rect(borderRightPosX, borderRightPosY + borderDY, borderRectX, borderRectY);
            ctx.fillStyle = "#0024DD";
            ctx.fill();
            ctx.closePath();
            borderRightPosY += 24
     }
    
    // Sets the Borders y cordinate to 0. 
    borderLeftPosY = 0;
    borderRightPosY = 0;
    if (borderDY >= 20){
            borderDY = 0;
    }
 
}

// Draws the rectangle that the player can move
function drawRectangle() {
    ctx.clearRect(rectangleX, rectangleY, rectangleX + 30, rectangleY + 30);
    ctx.beginPath();
    ctx.rect (rectangleX, rectangleY, 30, 30);
    ctx.fillStyle = "#0095DD";
    ctx.fill();
    ctx.closePath();
}

// Draws all the elements.
function draw() {
    // Updates the score in the html.
    document.getElementById("scoreWindow").innerHTML =  "Score: "  + window.score;
    // Check if the game is not over and draws all the elements.
    if (gameOver== false){
        ctx.clearRect(0,0,canvas.width, canvas.height);
        drawRectangle();
        createBorders();
        // Moves the Obstacles in the obstacle list.
        for (i = 0; i < obstacleList.length; i++){
            moveObstacle (i);
        }
        
        // Moves the rectangle left or right depending on which button is pressed.
        if(rightPressed && rectangleX < (canvas.width - borderRectX) - 30) {
            rectangleX += 7;
        }
        else if(leftPressed && rectangleX > borderRectX) {
            rectangleX -= 7;
        }
        // Increments the borderMovement position.
        borderDY += 5;        
        // Add to the score.
        score +=1;
        // Increases the difficulty by making the obstacles appear quicker
        if (score % 500 == 0){
            intervalTime = intervalTime / 1.1;
            clearInterval (myInterval);
        }
    }
}
// Handles Key Down Events
function keyDownHandler(e) {
    if(e.keyCode == 39) {
        rightPressed = true;
    }
    else if(e.keyCode == 37) {
        leftPressed = true;
    }
}
// Handles Key Up Events
function keyUpHandler(e) {
    if(e.keyCode == 39) {
        rightPressed = false;
    }
    else if(e.keyCode == 37) {
        leftPressed = false;
    }
    
}

// Creates the obstacles. 
function createObstacles (){
    myInterval = setInterval (createObstacle, intervalTime);
}
// Creates the intial obstacles.
createObstacles ();
// Creates more obstacles every 5 seconds.
setInterval (createObstacles, 5000)

// Adds Key up and down intervals.
document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);
// Refreshes and draws the game.
setInterval (draw, 20);