function updateDists() {
  // recalculates array distances from scratch
  let n = cities.length;

  distances = Array.from(Array(n), () => Array(n));
  for (let i = 0; i < n; i++) {
    distances[i][i] = 0;
    for (let j = i + 1; j < n; j++) {
      let d = getDist(cities[i], cities[j]);
      distances[i][j] = d;
      distances[j][i] = d;
    }
  }
}

function getDesirabilityOfDist(dst) {
  return Math.pow(1 / dst, dstPower);
}

function getDesirabilityFromCity(city_index, visited = []) {
  let desirability = Array.from(cities, (_, i) => {
    if (visited.includes(i)) return 0;
    return getDesirabilityOfDist(distances[i][city_index]);
  });
  normalizeArray(desirability);
  return desirability;
}

function spawnAnts(n) {
  for (let i = 0; i < n; i++) {
    ants.push(new Ant(randint(numCities)));
  }
  numAnts = ants.length;
  drawAnts();
}

function updateAntsDesirability() {
  for (a of ants) a.updateDesirability();
}

function addCity(x, y) {
  let c = { x, y };
  cities.push(c);
  updateDists();

  updateAntsDesirability();
  stroke(255);
  strokeWeight(15);
  point(c.x, c.y);
}

function evalPath(path) {
  s = distances[path[0]][path[path.length - 1]];
  for (let i = 0; i < path.length - 1; i++) {
    s += distances[path[i]][path[i + 1]];
  }
  return s;
}

function moveAnts() {
  for (a of ants) a.chooseNextCity();
}

function findBestPath(draw = false) {
  // compute the best path by checking every permutation
  // warning: veeery slow if numCities is high
  let bestpath = [];
  let perms = permuteWrapper(Array.from(Array(numCities - 1), (_, i) => i + 1));
  let best = Infinity;

  for (p of perms) {
    let val = evalPath([0].concat(p));
    if (val < best) {
      best = val;
      bestpath = [0].concat(p);
    }
  }

  console.log(evalPath(bestpath));
  if (draw) {
    background(0);
    drawPath(bestpath);
  }
  return bestpath;
}
