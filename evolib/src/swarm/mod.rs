use pyo3::prelude::*;
use nalgebra::Vector2;
use rand;
use rayon::prelude::*;
use noise::{NoiseFn, Perlin};

use std::time::Instant;


#[pyclass]
pub struct Swarm {
    creatures: Vec<[f32; 7]>,
    target: [f32; 6],
    inertia_factor: f32,
    cognitive_factor: f32,
    social_factor: f32,
    swarm_group_factor: f32,
    swarm_target_factor: f32,
    swarm_random_factor: f32,
    speed: f32,
    max_speed: f32,
    best_value: f32,
    best_position: [f32; 2],
    now: Instant,
    noise: Perlin,
}

#[pymethods]
impl Swarm {
    #[new]
    fn new(
        target_x: f32,
        target_y: f32,
        inertia_factor: f32,
        cognitive_factor: f32,
        social_factor: f32,
        swarm_group_factor: f32,
        swarm_target_factor: f32,
        swarm_random_factor: f32,
        speed: f32,
        max_speed: f32,
    ) -> Self {
        let mut creatures = Vec::new();
        for _ in 0..100 {
            creatures.push([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]);
        }

        // x, y, vx, vy, ix, iy;
        let target = [target_x, target_y, 0.0, 0.0, target_x, target_y];

        Swarm {
            creatures,
            target,
            inertia_factor,
            cognitive_factor,
            social_factor,
            swarm_group_factor,
            swarm_target_factor,
            swarm_random_factor,
            speed,
            max_speed,
            best_value: 0.0,
            best_position: [0.0, 0.0],
            now: Instant::now(),
            noise: Perlin::new(1234),
        }
    }

    fn randomize(&mut self) {
        for creature in &mut self.creatures {
            creature[0] = self.target[0] + rand::random::<f32>() * 100.0 - 50.0;
            creature[1] = self.target[1] + rand::random::<f32>() * 100.0 - 50.0;
            creature[2] = rand::random::<f32>() * 2.0 - 1.0;
            creature[3] = rand::random::<f32>() * 2.0 - 1.0;
            creature[4] = 0.0;
            creature[5] = 0.0;
        }
    }

    fn update(&mut self, delta: f32) {
        self.update_target();
        self.update_best();
        self.update_creatures(delta);
    }

    /// Update the creatures of this swarm by calculating
    /// the nessesary forces from the swarm, target and random.
    fn update_creatures(&mut self, delta: f32) {
        self.creatures.par_iter_mut()
            .for_each(|creature| {
                let x = creature[0]; let y = creature[1];
                let vx = creature[2]; let vy = creature[3];
                let bx = creature[4]; let by = creature[5];

                let ix = self.inertia_factor * vx;
                let iy = self.inertia_factor * vy;

                let cx = self.cognitive_factor * rand::random::<f32>() * (bx - x);
                let cy = self.cognitive_factor * rand::random::<f32>() * (by - y);

                let sx = self.social_factor * rand::random::<f32>() * (self.best_position[0] - x);
                let sy = self.social_factor * rand::random::<f32>() * (self.best_position[1] - y);

                let mut acceleration = Vector2::new(0.0, 0.0);

                // add the swarm forces
                let swarm_force = Vector2::new(
                    ix + cx + sx,
                    iy + cy + sy
                ).normalize() * self.swarm_group_factor * self.speed;
                acceleration += swarm_force;

                // add the target steering force
                let target_force = Vector2::new(
                    self.target[0] - x,
                    self.target[1] - y
                ).normalize() * self.swarm_target_factor * self.speed;
                let steer_force = target_force - Vector2::new(vx, vy);
                acceleration += steer_force;

                // add the random steering force
                let random_force = Vector2::new(
                    rand::random::<f32>() * 2.0 - 1.0,
                    rand::random::<f32>() * 2.0 - 1.0
                ).normalize() * self.swarm_random_factor * self.speed;
                acceleration += random_force;

                // limit the acceleration
                if acceleration.magnitude() > self.max_speed {
                    acceleration = acceleration.normalize() * self.max_speed;
                }

                // update the velocity and position
                creature[2] += acceleration[0] * delta;
                creature[3] += acceleration[1] * delta;
                creature[0] += creature[2];
                creature[1] += creature[3];
            });
    }

    /// Update the position of the target that the swarm should follow
    fn update_target(&mut self) {
        let time = self.now.elapsed().as_secs_f32();
        let tx = (2.0 + (2.0 * time).cos()) * (3.0 * time).cos() * self.speed;
        let ty = (2.0 + (2.0 * time).sin()) * (3.0 * time).sin() * self.speed;
        self.target[0] = ty + self.target[4];
        self.target[1] = tx + self.target[5];
    }

    /// Update the fitness values of the creatures to simulate
    /// the flocking behaviour of the swarm.
    fn update_best(&mut self) {
        for creature in &mut self.creatures {
            let x = creature[0];
            let y = creature[1];
            let bv = creature[6];

            let fitness = x.powf(2.0) + y.powf(2.0) + 1.0;

            if fitness < bv {
                creature[4] = x;
                creature[5] = y;
                creature[6] = fitness;
                if fitness < self.best_value {
                    self.best_position[0] = x;
                    self.best_position[1] = y;
                    self.best_value = fitness;
                }
            }
        }
    }

    fn get_creatures(&self) -> Vec<[f32; 7]> {
        return self.creatures.clone();
    }

    fn get_target(&self) -> Vec<f32> {
        return self.target.to_vec();
    }
}