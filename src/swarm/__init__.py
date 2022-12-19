import random
from re import L

import pyglet as pg

import numpy as np

from swarm.swarm import update_swarm, get_fitness_values, figure_eight_func
from swarm.flock import update_flock
from swarm.swarm import P_X, P_Y

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
        self.speed = 100.0
        self.max_speed = 200.0
        self.spread = 200

        self.particles = []
        self.particle_sprites = []

        for _ in range(num_particles):
            px = float(np.random.uniform(x-20.0, x+20.0))
            py = float(np.random.uniform(y-20.0, y+20.0))
            c = pg.shapes.BorderedRectangle(
                x, y, 4, 4,
                border_color=(0, 0, 0),
                color=(142, 127, 99),
                batch=self.batch
            )
            c.anchor_x = 2
            c.anchor_y = 2

            # x, y, vx, vy, best_x, best_y, best_value
            vx = np.random.uniform(-1.0, 1.0) * self.speed
            vy = np.random.uniform(-1.0, 1.0) * self.speed
            self.particles.append([px, py, vx, vy, px, py, 0.0])
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
        self.target = figure_eight_func(self.iterator, self.spread)
        self.target_sprite.x = self.target[0]
        self.target_sprite.y = self.target[1]

        # self.particles = update_flock(
        #     self.particles,
        #     self.target,
        #     self.speed,
        #     self.max_speed,
        #     delta
        # )

        #print(self.particles)

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