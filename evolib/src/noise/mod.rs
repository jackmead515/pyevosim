use pyo3::prelude::*;
use noise::{self, Turbulence, Perlin};
use noise::NoiseFn;

#[pyclass]
pub struct TerrianNoise {
    noise: Turbulence<Perlin, Perlin>,
    chunk_buffer: Vec<Vec<f64>>,
    seed: u32,
    frequency: f64,
    power: f64,
    roughness: u32,
    chunk_size: u32,
    world_size: u32,
}

impl TerrianNoise {
    fn recreate_chunk_buffer(&self) -> Vec<Vec<f64>> {
        let mut chunk_buffer = Vec::with_capacity(self.chunk_size as usize);
        for i in 0..self.chunk_size {
            let mut row: Vec<f64> = Vec::with_capacity(self.chunk_size as usize);
            for j in 0..self.chunk_size {
                row.push(0.0);
            }
            chunk_buffer.push(row);
        }
        return chunk_buffer;
    }


    /// Recreate the noise function with the current settings
    /// This is needed when changing the settings because the noise function
    /// is immutable (behind a reference and doesnt implement the Copy trait)
    fn recreate_noise(&self) -> Turbulence<Perlin, Perlin> {
        let perlin = Perlin::new(self.seed);
        let turbulence: Turbulence<Perlin, Perlin> = Turbulence::new(perlin)
            .set_frequency(self.frequency)
            .set_power(self.power)
            .set_roughness(self.roughness as usize);
        return turbulence;
    }
}

#[pymethods]
impl TerrianNoise {

    #[new]
    fn new(
        seed: u32,
        frequency: f64,
        power: f64,
        roughness: u32,
        chunk_size: u32,
        world_size: u32,
    ) -> Self {

        // Create the noise function
        let perlin = Perlin::new(seed);
        let noise: Turbulence<Perlin, Perlin> = Turbulence::new(perlin)
            .set_frequency(frequency)
            .set_power(power)
            .set_roughness(roughness as usize);

        // Create the chunk buffer
        let mut chunk_buffer = Vec::with_capacity(chunk_size as usize);
        for _i in 0..chunk_size {
            let mut row: Vec<f64> = Vec::with_capacity(chunk_size as usize);
            for _j in 0..chunk_size {
                row.push(0.0);
            }
            chunk_buffer.push(row);
        }

        return TerrianNoise {
            noise,
            chunk_buffer,
            seed,
            frequency,
            power,
            roughness,
            chunk_size,
            world_size
        }
    }

    #[setter]
    fn set_frequency(&mut self, f: f64) -> PyResult<()> {
        self.frequency = f;
        self.noise = self.recreate_noise();
        return Ok(());
    }

    #[setter]
    fn set_power(&mut self, p: f64) -> PyResult<()> {
        self.power = p;
        self.noise = self.recreate_noise();
        return Ok(());
    }

    #[setter]
    fn set_roughness(&mut self, r: u32) -> PyResult<()> {
        self.roughness = r;
        self.noise = self.recreate_noise();
        return Ok(());
    }

    #[pyo3(text_signature = "($self, x=10, y=10)")]
    fn noise(
        &self,
        x: f64,
        y: f64
    ) -> f64 {
        let x = x / self.world_size as f64;
        let y = y / self.world_size as f64;
        return self.noise.get([x, y]);
    }

    #[pyo3(text_signature = "($self, x=10, y=10)")]
    fn noise_chunk(
        &mut self,
        cx: f64,
        cy: f64
    ) -> Vec<Vec<f64>> {
        let x = cx * self.chunk_size as f64;
        let y = cy * self.chunk_size as f64;
        for i in 0..self.chunk_size {
            for j in 0..self.chunk_size {
                let x = (x + i as f64) / self.world_size as f64;
                let y = (y + j as f64) / self.world_size as f64;
                self.chunk_buffer[i as usize][j as usize] = self.noise.get([x, y]);
            }
        }
        return self.chunk_buffer.clone();
    }

}

