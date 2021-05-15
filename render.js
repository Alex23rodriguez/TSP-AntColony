function drawCities() {
  stroke(255);
  strokeWeight(15);
  for (let c of cities) {
    point(c.x, c.y);
  }
}

function drawPath(path, intensity = 1, closed = true, red = false) {
  if (red) {
    stroke(255, 0, 0, intensity * 255);
  } else {
    stroke(255, intensity * 255);
  }
  strokeWeight(1);
  for (let i = 1; i < path.length; i++) {
    line(
      cities[path[i]].x,
      cities[path[i]].y,
      cities[path[i - 1]].x,
      cities[path[i - 1]].y
    );
  }
  if (closed) {
    let c = cities[path[path.length - 1]];
    line(cities[path[0]].x, cities[path[0]].y, c.x, c.y);
  }
}

function drawDesirability(city_index, desirability) {
  if (desirability === undefined) return;
  let city = cities[city_index];
  let mx = Math.max(...desirability);
  let intensity = desirability.map((d) => (d / mx) * 255);
  strokeWeight(2);
  for (let i in cities) {
    stroke(255, intensity[i]);
    line(cities[i].x, cities[i].y, city.x, city.y);
  }
}

function drawAnts() {
  for (a of ants) a.draw();
}

function drawAntsDesirability() {
  for (a of ants) drawDesirability(a.city, a.desirability);
}

function drawAntPaths() {
  for (a of ants) a.drawPath();
}

function onlyDrawIthPath(i) {
  background(0);
  drawCities();
  drawPath(ants[i].path, 1, true);
}
