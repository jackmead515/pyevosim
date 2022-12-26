from numba import jit, prange
import numpy as np

# A = 20
# B = 0.2
# C = 2*np.pi

WEIGHT = 0.5
COGNITIVE_FACTOR = 0.8
SOCIAL_FACTOR = 0.9
SWARM_GROUP_FACTOR = 0.2
SWARM_TARGET_FACTOR = 0.7
SWARM_RANDOM_FACTOR = 0.1

P_X = 0 # x position
P_Y = 1 # y position
P_VX = 2 # x velocity
P_VY = 3 # y velocity
P_BX = 4 # x best position
P_BY = 5 # y best position
P_BV = 6 # best value

# @jit(nopython=True, fastmath=True)
# def auckley_fitness(vec):
#     d = vec.shape[-1]
#     sum_sq_term = -A * np.exp(-B * np.sqrt(np.sum(vec * vec, axis=-1) / d))
#     cos_term = -np.exp(np.sum(np.cos(C * vec) / d, axis=-1))
#     return A + np.exp(1) + sum_sq_term + cos_term


@jit(nopython=True, fastmath=True)
def figure_eight_func(index, spread):
    return np.array([
        (2 + np.cos(2 * index)) * np.cos(3 * index) * spread,
        (2 + np.sin(2 * index)) * np.sin(3 * index) * spread
    ], dtype=np.float32)


@jit(nopython=True, fastmath=True)
def standard_fitness(vec):
    return vec[0] ** 2 + vec[1] ** 2 + 1


@jit(nopython=True, fastmath=True)
def get_fitness_values(
    particles,
    best_value,
    best_position,
):
    for i in prange(len(particles)):
        particle = particles[i]
        fitness = standard_fitness(particle[P_X:P_Y+1])
        if particle[P_BV] < fitness:
            particle[P_BV] = fitness
            particle[P_BX:P_BY] = particle[P_X:P_Y]
            if particle[P_BV] < best_value:
                best_value = fitness
                best_position = particle[P_BX:P_BY]

    return particles, best_value, best_position


@jit(nopython=True, fastmath=True)
def get_swarm_force(
    particle,
    global_best_position,
    target_position,
    speed,
):
    velocity = particle[P_VX:P_VY+1]
    position = particle[P_X:P_Y+1]
    best_position = particle[P_BX:P_BY+1]

    inertia = WEIGHT * velocity
    cognitive = COGNITIVE_FACTOR * np.random.random() * (best_position - position)
    social = SOCIAL_FACTOR * np.random.random() * (global_best_position - position)

    swarm_force = (inertia + cognitive + social) * SWARM_GROUP_FACTOR
    swarm_force /= np.linalg.norm(swarm_force)

    target_force = (target_position - position) * SWARM_TARGET_FACTOR
    target_force /= np.linalg.norm(target_force)

    #random_force = (np.random.random(2) - 1) * SWARM_RANDOM_FACTOR

    total_force = (target_force + swarm_force)
    return total_force * speed / np.linalg.norm(total_force)


@jit(nopython=True, fastmath=True, parallel=True)
def update_swarm(
    particles,
    target,
    global_best_position,
    speed,
    max_speed,
    delta,
):
    # x, y, vx, vy, best_x, best_y, best_value

    for i in prange(len(particles)):
        particle = particles[i]
        velocity = get_swarm_force(
            particle,
            global_best_position,
            target,
            speed,
        )

        new_velocity = (velocity * delta) + particle[P_VX:P_VY+1]
        new_velocity = np.clip(new_velocity, -max_speed, max_speed)
        particle[P_VX:P_VY+1] = new_velocity
        particle[P_X:P_Y+1] += new_velocity * delta
    
    return particles