class Snowflake {

    constructor(design) {
        let x = random(width);
        let y = random(-80, -30);
        this.img = design;
        this.pos = createVector(x, y);
        this.vel = createVector(0, 0);
        this.acc = createVector();
        this.radius = this.getRandomSize();
        this.angle = random(TWO_PI);
        this.dir = random(1) > 0.5 ? 1 : -1;
    }

    getRandomSize() {
        // Beta distribution with a = b = 0.5
        let seed = Math.random();
        let beta = Math.pow(sin(seed*PI/2), 2);
        // scale to the left
        let beta_left = (beta < 0.5) ? 2*beta : 2*(1-beta);
        // Make sure that min size of particle is 1px
        return map(beta_left*24, 0, 24, 3, 20);
    }

    applyForce(force) {
        // Parallax Effect 
        let apparentForce = force.copy();
        apparentForce.mult(this.radius);

        this.acc.add(force);
    }

    update() {
        this.vel.add(this.acc);
        // this.vel.limit(this.radius * 0.6);
        this.pos.add(this.vel);
        this.acc.mult(0);
        this.angle += (this.dir * this.vel.mag())/50;
    }

    offScreen() {
        return (this.pos.y > height + this.radius) || (this.pos.x > this.width + this.r) || (this.pos.x > -this.r);
    }

    render() {
        push();
        translate(this.pos.x, this.pos.y);
        rotate(this.angle);
        imageMode(CENTER);
        image(this.img, 0, 0, this.radius, this.radius);
        pop();
    }


}