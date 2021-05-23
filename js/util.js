function distSq(p1, p2) {
  let dx = p1.x - p2.x;
  let dy = p1.y - p2.y;
  return dx * dx + dy * dy;
}

function getDist(p1, p2) {
  let dx = p1.x - p2.x;
  let dy = p1.y - p2.y;
  return Math.sqrt(dx * dx + dy * dy);
}

function normalizeArray(arr) {
  // given an array of numbers, it scales the array in place so that the numbers now add up to one
  let s = arr.reduce((x, y) => x + y);
  for (let i in arr) arr[i] = arr[i] / s;
}

function pick(desirability) {
  // given an array of numbers that add up to one, randomly picks an index with weighted probability
  let r = Math.random();
  let s = 0;
  for (let i in desirability) {
    s += desirability[i];
    if (r < s) {
      return Number(i);
    }
  }
}

function randint(max) {
  // returns a random integer between zero and max, not including max
  return ~~(Math.random() * max);
}

// permutations func
// https://stackoverflow.com/questions/9960908/permutations-in-javascript

function permute(input) {
  var i, ch;
  for (i = 0; i < input.length; i++) {
    ch = input.splice(i, 1)[0];
    _usedChars.push(ch);
    if (input.length == 0) {
      _permArr.push(_usedChars.slice());
    }
    permute(input);
    input.splice(i, 0, ch);
    _usedChars.pop();
  }
  return _permArr;
}

function permuteWrapper(input) {
  _permArr = [];
  _usedChars = [];
  return permute(input);
}
