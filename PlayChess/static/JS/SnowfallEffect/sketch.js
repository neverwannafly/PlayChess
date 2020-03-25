let snow = [];
let gravity;
let wind;
let sinIndex = 0;
let maxSnowFlakes = 180;

let spriteSheet;
let textures = [];

function stop() {
    maxSnowFlakes = 0;
}

function start() {
    maxSnowFlakes = 180;
}

function preload() {
    spriteSheet = loadImage('static/Images/snowflakes/flakes32.png');
}

function setup() {
    createCanvas(windowWidth, windowHeight);
    gravity = createVector(0, 0.01);
    wind = createVector(0, 0);
    for (let x=0; x<spriteSheet.width; x+=32) {
        for (let y=0; y<spriteSheet.height; y+=32) {
            let img = spriteSheet.get(x, y, 32, 32);
            textures.push(img);
        }
    }
}

function draw() {
    background(29, 29, 29);

    let prob = Math.floor(Math.random()*10);
    if (snow.length < maxSnowFlakes && prob < 5) {
        let design = random(textures);
        snow.push(new Snowflake(design));
    }

    for (let flake of snow) {
        flake.applyForce(gravity);
        // flake.applyForce(wind);
        // wind.x = sin(sinIndex);
        // sinIndex += 0.01;
        flake.update();
        flake.render();
    }

    for (let i = snow.length-1; i>=0; i--) {
        if (snow[i].offScreen()) {
            snow.splice(i, 1);
        }
    }

}

// stop();