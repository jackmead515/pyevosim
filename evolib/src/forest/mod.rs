use pyo3::prelude::*;
use noise::{self, NoiseFn, Turbulence, Perlin};
use nalgebra::Vector2;

const NEIGHBORS: [[i32; 2]; 8] = [
    [1, 0],
    [1, 1],
    [0, 1],
    [-1, 1],
    [-1, 0],
    [-1, -1],
    [0, -1],
    [1, -1]
];

fn between(value: f32, min: f32, max: f32) -> bool {
    return value >= min && value <= max;
}

fn get_direction(degrees: f32) -> [i32; 2] {
    // default to tangent
    let mut direction = [1, 0];

    return match degrees {
        // 0 degrees
        d if between(d, 0.0, 22.5) => {
            direction = [1, 0];
            direction
        },
        d if between(d, 22.5, 67.5) => {
            direction = [1, 1];
            direction
        },
        d if between(d, 67.5, 112.5) => {
            direction = [0, 1];
            direction
        },
        d if between(d, 112.5, 157.5) => {
            direction = [-1, 1];
            direction
        },
        d if between(d, 157.5, 202.5) => {
            direction = [-1, 0];
            direction
        },
        d if between(d, 202.5, 247.5) => {
            direction = [-1, -1];
            direction
        },
        d if between(d, 247.5, 292.5) => {
            direction = [0, -1];
            direction
        },
        d if between(d, 292.5, 337.5) => {
            direction = [1, -1];
            direction
        },
        d if between(d, 337.5, 360.0) => {
            direction = [1, 0];
            direction
        },
        _ => {
            direction
        }
    }
}

#[pyclass]
pub struct Forest {
    plants: Vec<[u32; 2]>,
    plant_grid: Vec<Vec<u8>>,
    max_plants: u32,
    noise: Turbulence<Perlin, Perlin>,
    iterator: usize,
}

#[pymethods]
impl Forest {

    #[new]
    fn new(
        seed: u32,
        frequency: f64,
        power: f64,
        roughness: u32,
        max_plants: u32,
        start_position: [u32; 2],
    ) -> Self {

        // Create the noise function
        let perlin = Perlin::new(seed);
        let noise: Turbulence<Perlin, Perlin> = Turbulence::new(perlin)
            .set_frequency(frequency)
            .set_power(power)
            .set_roughness(roughness as usize);

        // initial grid
        let mut plant_grid = Vec::new();
        for _ in 0..max_plants*2 {
            let mut row = Vec::new();
            for _ in 0..max_plants*2 {
                row.push(0);
            }
            plant_grid.push(row);
        }

        let mut plants: Vec<[u32; 2]> = Vec::with_capacity(max_plants as usize);
        plants.push(start_position);

        Forest {
            plants,
            plant_grid,
            noise,
            max_plants,
            iterator: 0,
        }

    }

    fn noise(
        &self,
        x: f64,
        y: f64
    ) -> f64 {
        let x = x / self.max_plants as f64;
        let y = y / self.max_plants as f64;
        return self.noise.get([x, y]);
    }

    fn update(&mut self, delta: f32, wind: [f32; 2]) -> Option<[u32; 2]> {

        // increment the iterator
        self.iterator += 1;
        if self.iterator >= self.plants.len() {
            self.iterator = 0;
        }

        let plant = self.plants[self.iterator];

        // noise direction and scale from -1 to 1 to 0 to 6.283185
        let mut noise_angle = self.noise(plant[0] as f64, plant[1] as f64);
        noise_angle = (noise_angle + 1.0) * 3.141592;

        // wind direction and get the radian angle
        let wind_angle = Vector2::new(wind[0], wind[1]).angle(&Vector2::new(1.0, 0.0)) as f64;

        // add wind and noise and convert to degrees
        let mut angle = noise_angle + wind_angle;
        angle = angle * 180.0 / 3.141592;

        // get the direction from the angle
        let direction = get_direction(angle as f32);

        println!("px: {}, py: {}", plant[0], plant[1]);
        println!("dx: {}, dy: {}", direction[0], direction[1]);

        let next_plant = [
            (plant[0] as i32 + direction[0]) as u32,
            (plant[1] as i32 + direction[1]) as u32
        ];

        // get the neighbors
        let neighbors = NEIGHBORS.iter().map(|n| {
            let x = (plant[0] as i32 + n[0]) as u32;
            let y = (plant[1] as i32 + n[1]) as u32;
            return [x, y];
        }).filter(|n| {
            let x = n[0] as usize;
            let y = n[1] as usize;
            return self.plant_grid[x][y] == 1;
        }).filter(|n| {
            return n[0] == next_plant[0] && n[1] == next_plant[1];
        }).collect::<Vec<[u32; 2]>>();

        // if there are no neighbors, add the plant
        if neighbors.len() == 0 {
            self.plants.push(next_plant);
            self.plant_grid[next_plant[0] as usize][next_plant[1] as usize] = 1;
            return Some(next_plant);
        }

        return None;
    }

    fn get_plants(&self) -> Vec<[u32; 2]> {
        return self.plants.clone();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_forest() {
        let mut forest = Forest::new(
            12342214, 
            0.8, 
            3.0, 
            10, 
            1000, 
            [1280 / 2, 720 / 2]
        );

        let plant = forest.update(0.0, [1.0, -1.0]);

        assert_eq!(forest.get_plants().len(), 2);
    }

}