var message = {};

message = {
    messageType: "SETTING",
    options: {
        "width": 512, //Integer
        "height": 480 //Integer
    }
};
parent.postMessage(message,'*');


// Creating the canvas
var canvas = document.createElement("canvas");
var surface, currentScreen;
surface = canvas.getContext('2d');
canvas.width = 512;
canvas.height = 480;
document.body.appendChild(canvas);

// Variables
var screenNum = 0;
var max_score = 0;
canvas.style.backgroundColor = 'rgba(50, 167, 50, 0.5)';
var mouseJustClicked = false;

// Background image
var bgReady = false;
var bgImage = new Image();
bgImage.onload = function () {
    bgReady = true;
};
bgImage.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/bg.png?raw=true";

// Hero image
var heroReady = false;
var heroImage = new Image();
heroImage.onload = function () {
    heroReady = true;
};
heroImage.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/hero.png?raw=true";

// diamond image
var diamondReady = false;
var diamondImage = new Image();
diamondImage.onload = function () {
    diamondReady = true;
};
diamondImage.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/diamond.png?raw=true";

// ghost1
var ghost1Ready = false;
var ghostImage = new Image();
ghostImage.onload = function () {
    ghost1Ready = true;
};
ghostImage.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/ghost322.png?raw=true";

// ghost2
var ghost2Ready = false;
var ghost2Image = new Image();
ghost2Image.onload = function () {
    ghost2Ready = true;
};
ghost2Image.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/ghost322.png?raw=true";

// ghost3
var ghost3Ready = false;
var ghost3Image = new Image();
ghost3Image.onload = function () {
    ghost3Ready = true;
};
ghost3Image.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/ghost322.png?raw=true";

// ghost4
var ghost4Ready = false;
var ghost4Image = new Image();
ghost4Image.onload = function () {
    ghost4Ready = true;
};
ghost4Image.src = "https://github.com/pedram-ghazi/pedram-ghazi.github.io/blob/master/images/ghost322.png?raw=true";

// Game objects
var hero = {
    speed: 210, // movement in pixels per second
    x: canvas.width / 2,
    y: canvas.height / 2
};
var diamond = {
    x: 0,
    y: 0
};
var ghost1 = {
    speed: 60, // movement in pixels per second
    x: 0,
    y: 0
};
var ghost2 = {
    speed: 60, // movement in pixels per second
    x: canvas.width - 32,
    y: canvas.height - 32
};
var ghost3 = {
    speed: 60, // movement in pixels per second
    x: canvas.width - 32,
    y: 0
};
var ghost4 = {
    speed: 60, // movement in pixels per second
    x: 0,
    y: canvas.height - 32
};
var diamondsCollected = 0;

// Handle keyboard controls
var keysDown = {};

addEventListener("keydown", function (e) {
    keysDown[e.keyCode] = true;
}, false);

addEventListener("keyup", function (e) {
    delete keysDown[e.keyCode];
}, false);

// Add diamond to the game when the player collects a diamond
var add_diamond = function () {
    // Throw the diamond somewhere on the screenNum randomly
    diamond.x = 32 + (Math.random() * (canvas.width - 100));
    diamond.y = 32 + (Math.random() * (canvas.height - 100));
};

// reset the game when the ghost1 catches our hero
var reset = function () {
    add_diamond();

    ghost1.x = 0;
    ghost1.y = 0;

    ghost2.x = canvas.width - 32;
    ghost2.y = canvas.height - 32;

    ghost3.x = canvas.width - 32;
    ghost3.y = 0;

    ghost4.x = 0;
    ghost4.y = canvas.height - 32;

    hero.x = canvas.width / 2;
    hero.y = canvas.height / 2;
};

function beginLoop() {
    var frameId = 0;
    var lastFrame = Date.now();
    add_diamond();

    function loop() {
        var thisFrame = Date.now();

        var elapsed = thisFrame - lastFrame;

        frameId = window.requestAnimationFrame(loop);

        currentScreen.update(surface, elapsed / 1000);
        currentScreen.draw(surface, screenNum);

        lastFrame = thisFrame;
    }

    loop();
}

canvas.addEventListener('click', checkStart, false);

function checkStart(e) {
    var p = getMousePos(e);
    if (screenNum == 0) {
        if (p.y >= canvas.height * 0.5) {
            console.log('Load Game');
            message = {
                messageType: "LOAD_REQUEST",
            };
            parent.postMessage(message,'*');
            // Listen incoming messages, and load the game
            window.addEventListener("message", function(evt) {
                if(evt.data.messageType == "LOAD") {
                    loadGame(evt.data.gameState);
                } else if (evt.data.messageType == "ERROR") {
                    alert(evt.data.text);
                }
            });
            // mouseJustClicked = true;
        } else {
            console.log('New Game');
            mouseJustClicked = true;
        }
    } else if(screenNum == 1) {
        console.log('Game saved');
        message =  {
            messageType: "SAVE",
            gameState: {
                playerPos: {
                    "x": hero.x,
                    "y": hero.y
                },
                ghost1: {
                    "x": ghost1.x,
                    "y": ghost1.y
                },
                ghost2: {
                    "x": ghost2.x,
                    "y": ghost2.y
                },
                ghost3: {
                    "x": ghost3.x,
                    "y": ghost3.y
                },
                ghost4: {
                    "x": ghost4.x,
                    "y": ghost4.y
                },
                diamond: {
                    "x": diamond.x,
                    "y": diamond.y
                },
                score: diamondsCollected
            },
        };
        parent.postMessage(message,'*');
        mouseJustClicked = true;
    }
}

function loadGame(data){
    hero.x = data.playerPos.x;
    hero.y = data.playerPos.y;
    ghost1.x = data.ghost1.x;
    ghost1.y = data.ghost1.y;
    ghost2.x = data.ghost2.x;
    ghost2.y = data.ghost2.y;
    ghost3.x = data.ghost3.x;
    ghost3.y = data.ghost3.y;
    ghost4.x = data.ghost4.x;
    ghost4.y = data.ghost4.y;
    diamond.x = data.diamond.x;
    diamond.y = data.diamond.y;
    diamondsCollected = data.score;

    mouseJustClicked = true;
}

function getMousePos(e) {
    var r = canvas.getBoundingClientRect();
    return {
        x: e.clientX - r.left,
        y: e.clientY - r.top
    };
}

// define the start screen
currentScreen = (function () {

    var hue = 0;
    var direction = 1;
    var wasButtonDown = false;
    var title = 'Blood Diamond';

    function centerText(ctx, text, y) {
        var measurement = ctx.measureText(text);
        var x = (ctx.canvas.width - measurement.width) / 2;
        ctx.fillText(text, x, y);
    }

    function draw(ctx) {

        if (screenNum == 0) {
            var y = ctx.canvas.height / 2;
            var color = 'rgb(' + hue + ', 0, 0)';

            ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
            ctx.fillStyle = 'white';
            ctx.font = '48px monospace';
            centerText(ctx, title, y);

            ctx.fillStyle = color;
            ctx.font = '24px monospace';
            centerText(ctx, 'Start a new game', y*0.5);
            centerText(ctx, 'Load game', y*1.5);

            ctx.fillStyle = 'white';
            ctx.font = '14px monospace';
            centerText(ctx, '*TO SAVE THE GAME JUST CLICK ON SCREEN WHILE YOU ARE PLAYING', y*1.8);

        }
        else if (screenNum == 1) {
            if (bgReady) {
                ctx.drawImage(bgImage, 0, 0);
            }

            if (heroReady) {
                ctx.drawImage(heroImage, hero.x, hero.y);
            }

            if (diamondReady) {
                ctx.drawImage(diamondImage, diamond.x, diamond.y);
            }

            if (ghost1Ready) {
                ctx.drawImage(ghostImage, ghost1.x, ghost1.y);
            }

            if (ghost2Ready) {
                ctx.drawImage(ghost2Image, ghost2.x, ghost2.y);
            }

            if (ghost3Ready) {
                ctx.drawImage(ghost3Image, ghost3.x, ghost3.y);
            }

            if (ghost4Ready) {
                ctx.drawImage(ghost4Image, ghost4.x, ghost4.y);
            }
            // Score
            ctx.fillStyle = "rgb(256, 220, 220)";
            ctx.font = "17px Helvetica";
            ctx.textAlign = "left";
            ctx.textBaseline = "top";
            ctx.fillText("Score: " + diamondsCollected, 40, 5);
        }
    }

    function update(ctx, elapsed) {
        hue += 7 * direction;
        if (hue > 255) direction = -1;
        if (hue < 1) direction = 1;

        if (screenNum == 1) {
            if (ghost1.x >= hero.x) {
                ghost1.x -= ghost1.speed * elapsed;
            } else {
                ghost1.x += ghost1.speed * elapsed;
            }
            if (ghost1.y < hero.y) {
                ghost1.y += ghost1.speed * elapsed;
            } else {
                ghost1.y -= ghost1.speed * elapsed;
            }

            if (diamondsCollected > 5) {
                if (ghost2.x < hero.x && Math.abs(ghost2.x - ghost1.x) > 60) {
                    ghost2.x += ghost2.speed * elapsed;
                } else {
                    ghost2.x -= ghost2.speed * elapsed;
                }
                if (ghost2.y < hero.y && Math.abs(ghost2.y - ghost1.y) > 60) {
                    ghost2.y += ghost2.speed * elapsed;
                } else {
                    ghost2.y -= ghost2.speed * elapsed;
                }
            }
            if (diamondsCollected > 15) {
                if (ghost3.x < hero.x && Math.abs(ghost3.x - ghost2.x) > 60 && Math.abs(ghost3.x - ghost1.x) > 60) {
                    ghost3.x += ghost3.speed * elapsed;
                } else {
                    ghost3.x -= ghost3.speed * elapsed;
                }
                if (ghost3.y < hero.y && Math.abs(ghost3.y - ghost2.y) > 60 && Math.abs(ghost3.y - ghost1.y) > 60) {
                    ghost3.y += ghost3.speed * elapsed;
                } else {
                    ghost3.y -= ghost3.speed * elapsed;
                }
            }
            if (diamondsCollected > 25) {
                if (ghost4.x < hero.x && Math.abs(ghost4.x - ghost3.x) > 60 && Math.abs(ghost4.x - ghost2.x) > 60 && Math.abs(ghost4.x - ghost1.x) > 60) {
                    ghost4.x += ghost4.speed * elapsed;
                } else {
                    ghost4.x -= ghost4.speed * elapsed;
                }
                if (ghost4.y < hero.y && Math.abs(ghost4.y - ghost3.y) > 60 && Math.abs(ghost4.y - ghost2.y) > 60 && Math.abs(ghost4.y - ghost1.y) > 60) {
                    ghost4.y += ghost4.speed * elapsed;
                } else {
                    ghost4.y -= ghost4.speed * elapsed;
                }
            }

            if (38 in keysDown && hero.y > 32) { // Player holding up
                hero.y -= hero.speed * elapsed;
            }
            if (40 in keysDown && hero.y < canvas.height - 64) { // Player holding down
                hero.y += hero.speed * elapsed;
            }
            if (37 in keysDown && hero.x > 32) { // Player holding left
                hero.x -= hero.speed * elapsed;
            }
            if (39 in keysDown && hero.x < canvas.width - 64) { // Player holding right
                hero.x += hero.speed * elapsed;
            }

            // Are diamond and hero touching?
            if (hero.x <= (diamond.x + 24) && diamond.x <= (hero.x + 24) && hero.y <= (diamond.y + 24) && diamond.y <= (hero.y + 24)
            ) {
                ++diamondsCollected;
                add_diamond();
            }

            // Are ghost1 and hero touching?
            if (hero.x <= (ghost1.x + 24) && ghost1.x <= (hero.x + 24) && hero.y <= (ghost1.y + 24) && ghost1.y <= (hero.y + 24)
                || hero.x <= (ghost2.x + 24) && ghost2.x <= (hero.x + 24) && hero.y <= (ghost2.y + 24) && ghost2.y <= (hero.y + 24)
                || hero.x <= (ghost3.x + 24) && ghost3.x <= (hero.x + 24) && hero.y <= (ghost3.y + 24) && ghost3.y <= (hero.y + 24)
                || hero.x <= (ghost4.x + 24) && ghost4.x <= (hero.x + 24) && hero.y <= (ghost4.y + 24) && ghost4.y <= (hero.y + 24)
            ) {
                var message = {
                    messageType: "SCORE",
                    score: diamondsCollected
                };
                parent.postMessage(message,'*');
                max_score = diamondsCollected;
                diamondsCollected = 0;
                reset();
            }
        }

        if (mouseJustClicked) {
            screenNum = 1;
        }
    }


    return {
        draw: draw,
        update: update
    };
}());

beginLoop();