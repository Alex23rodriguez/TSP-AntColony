function Ant(city_index) {
  this.city = city_index;
  this.path = [this.city];
  this.desirability = getDesirabilityFromCity(this.city, this.path);
  this.done = false;

  this.chooseNextCity = function () {
    if (this.done) {
      this.city = this.path[0];
      console.log("Path value:", evalPath(this.path));
      return;
    }

    let next = pick(this.desirability);
    // let old = this.city;
    this.city = next;
    this.path.push(next);
    this.updateDesirability();
    // return [old, next];
  };

  this.draw = function () {
    stroke(255, 0, 0);
    strokeWeight(10);
    point(cities[this.city].x, cities[this.city].y);
  };

  this.drawPath = function () {
    drawPath(this.path, 1, this.done && this.city == this.path[0], true);
  };

  this.updateDesirability = function () {
    this.desirability = getDesirabilityFromCity(this.city, this.path);
    if (this.desirability.includes(NaN)) {
      this.done = true;
      this.desirability = undefined;
    }
  };
}
