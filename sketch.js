let [w, h] = [window.innerWidth, window.innerHeight];

let cities = [];
let distances = [];
let ants = [];

const ANIM_SPEED = 500;

function setup() {
  createCanvas(w, h);
  noLoop();

  background(0);
  restart();
  play();
}

function mouseClicked() {
  if (mouseX > 0 && mouseX < w && mouseY > 0 && mouseY < h) {
    addCity(mouseX, mouseY);
    numCities = cities.length;
  }
}

function keyPressed() {
  if (key === "r") {
    restart();
  }
}

function iteration() {
  background(0);
  drawAntPaths();
  drawCities();
  drawAnts();
  setTimeout(() => {
    drawAntsDesirability();
    drawAnts();
  }, ANIM_SPEED);
  setTimeout(() => {
    moveAnts();
    drawCities();
    drawAnts();
    drawAntPaths();
  }, ANIM_SPEED * 2);
}

function restart() {
  cities = [];
  ants = [];
  for (let i = 0; i < numCities; i++)
    addCity(Math.random() * w, Math.random() * h);

  spawnAnts(numAnts);
  // iteration();
}

function play() {
  for (let i = 0; i < numCities; i++) {
    setTimeout(iteration, i * ANIM_SPEED * 3);
  }
}
