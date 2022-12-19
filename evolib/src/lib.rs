use pyo3::prelude::*;

pub mod noise;
pub mod swarm;

#[pymodule]
fn evolib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<noise::TerrianNoise>()?;
    m.add_class::<swarm::Swarm>()?;
    Ok(())
}