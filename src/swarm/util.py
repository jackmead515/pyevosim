from numba import jit, cuda, njit, prange

import numpy as np

A = 20
B = 0.2
C = 2*np.pi

WEIGHT = 0.5
C1 = 0.8
C2 = 0.4

@jit(nopython=True, fastmath=True)
def auckley_fitness(vec):
    d = vec.shape[-1]
    sum_sq_term = -A * np.exp(-B * np.sqrt(np.sum(vec * vec, axis=-1) / d))
    cos_term = -np.exp(np.sum(np.cos(C * vec) / d, axis=-1))
    return A + np.exp(1) + sum_sq_term + cos_term

@jit(nopython=True, fastmath=True)
def standard_fitness(vec):
    return vec[0] ** 2 + vec[1] ** 2 + 1

@jit(nopython=True, fastmath=True)
def get_swarm_force(
    velocity,
    position,
    local_best_position,
    global_best_position,
    target_position,
    swarm_weight_factor,
    target_weight_factor,
    random_weight_factor,
):
    inertia = WEIGHT * velocity
    cognitive = C1 * np.random.random() * (local_best_position - position)
    social = C2 * np.random.random() * (global_best_position - position)

    swarm_force = inertia + cognitive + social 
    swarm_force /= np.linalg.norm(swarm_force)
    swarm_force *= swarm_weight_factor

    target_force = target_position - position
    target_force /= np.linalg.norm(target_force)
    target_force *= target_weight_factor

    random_force = np.random.random(2) * random_weight_factor

    return target_force + swarm_force + random_force