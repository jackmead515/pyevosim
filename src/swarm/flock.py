from re import M
from numba import jit, prange
import numpy as np

P_X = 0 # x position
P_Y = 1 # y position
P_VX = 2 # x velocity
P_VY = 3 # y velocity
P_AX = 4 # x acceleration
P_AY = 5 # y acceleration

@jit(nopython=True, fastmath=True)
def distance(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


@jit(nopython=True, fastmath=True)
def update_flock(
    particles,
    target,
    speed,
    max_speed,
    delta
):
    for i in prange(len(particles)):
        particle = particles[i]
        velocity = particle[P_VX:P_VY+1]
        position = particle[P_X:P_Y+1]

        alignment = np.zeros(2, dtype=np.float32)
        cohesion = np.zeros(2, dtype=np.float32)
        seperation = np.zeros(2, dtype=np.float32)

        for j in prange(len(particles)):
            if i == j:
                continue

            other = particles[j]
            alignment += other[P_VX:P_VY+1]
            cohesion += other[P_X:P_Y+1]

            dist = distance(position, other[P_X:P_Y+1])
            diff = position - other[P_X:P_Y+1]
            diff /= dist**2

            seperation += diff

        alignment /= len(particles) - 1
        alignment = alignment * speed / np.linalg.norm(alignment)
        #alignment *= speed
        alignment -= velocity

        cohesion /= len(particles) - 1
        cohesion = cohesion - position
        cohesion = cohesion * speed / np.linalg.norm(cohesion)
        #cohesion *= speed
        cohesion -= velocity

        seperation /= len(particles) - 1
        seperation = seperation * speed / np.linalg.norm(seperation)
        seperation -= velocity

        tforce = (target - position)
        tforce = tforce * speed / np.linalg.norm(tforce)

        rforce = (np.random.random(2) - 1)

        #tforce /= np.linalg.norm(tforce)
        # tforce *= speed
        #tforce *= 0.7

        #rforce = (np.random.random(2) - 1)

        particle[P_AX:P_AY+1] = (alignment + cohesion + seperation + tforce + rforce) * delta
        particle[P_VX:P_VY+1] += particle[P_AX:P_AY+1] * delta * speed
        particle[P_VX:P_VY+1] = np.clip(particle[P_VX:P_VY+1], -max_speed, max_speed)
        particle[P_X:P_Y+1] += particle[P_VX:P_VY+1] * delta

    return particles


