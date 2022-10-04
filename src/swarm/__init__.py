import random
from re import L

import pyglet as pg

import numpy as np

from swarm.util import update_swarm, get_fitness_values
from swarm.util import P_X, P_Y

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Swarm():

    def __init__(self, x, y, num_particles):
        self.num_particles = num_particles
        self.global_best_position = np.array([x, y], dtype=np.float32)
        self.global_best_value = float('inf')
        self.iterator = 0
        self.target = np.array([x, y], dtype=np.float32)
        self.particles = []
        self.batch = pg.graphics.Batch()
        self.speed = 20
        self.max_speed = 100
        self.spread = 200

        self.particles = []
        self.particle_sprites = []

        for _ in range(num_particles):
            x = float(np.random.uniform(x-20.0, x+20.0))
            y = float(np.random.uniform(y-20.0, y+20.0))
            c = pg.shapes.BorderedRectangle(
                x, y, 4, 4,
                border_color=(0, 0, 0),
                color=(142, 127, 99),
                batch=self.batch
            )
            c.anchor_x = 2
            c.anchor_y = 2

            # x, y, vx, vy, best_x, best_y, best_value
            self.particles.append([x, y, 0.0, 0.0, x, y, 0.0])
            self.particle_sprites.append(c)
        
        self.particles = np.array(self.particles, dtype=np.float32)
        
        self.target_sprite = pg.shapes.Circle(
            x, y, 4, batch=self.batch, color=(255, 0, 0)
        )


    def set_best_values(self):
        particles, best_value, best_position = get_fitness_values(self.particles, self.global_best_value, self.global_best_position)
        self.particles = particles
        self.global_best_value = best_value
        self.global_best_position = best_position


    def update(self, delta):
        self.set_best_values()
    
        self.iterator += 0.1 * delta

        self.target[0] = (2 + np.cos(2 * self.iterator)) * np.cos(3 * self.iterator) * self.spread
        self.target[1] = (2 + np.sin(2 * self.iterator)) * np.sin(3 * self.iterator) * self.spread
        self.target_sprite.x = self.target[0]
        self.target_sprite.y = self.target[1]

        self.particles = update_swarm(
            self.particles,
            self.target,
            self.global_best_position,
            self.speed,
            self.max_speed,
            delta
        )

        for i, particle in enumerate(self.particles):
            sprite = self.particle_sprites[i]
            sprite.x = particle[P_X]
            sprite.y = particle[P_Y]
            sprite.rotation += 10.0


    def draw(self):
        self.batch.draw()