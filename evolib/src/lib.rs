use pyo3::prelude::*;

pub mod noise;
pub mod swarm;
pub mod forest;

#[pymodule]
fn evolib(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<noise::TerrianNoise>()?;
    m.add_class::<swarm::Swarm>()?;
    m.add_class::<forest::Forest>()?;
    Ok(())
}