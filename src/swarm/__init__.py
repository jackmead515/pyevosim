import random

import pyglet as pg

import numpy as np

from swarm.util import get_swarm_force, standard_fitness

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


class Particle():

    def __init__(self, sprite, x, y):
        self.sprite = sprite
        self.position = np.array([x, y])
        self.best_position = self.position
        self.best_value = float('inf')
        self.velocity = np.array([0.0, 0.0])

    def update(self, delta):
        self.position += self.velocity*delta
        self.sprite.x = self.position[0]
        self.sprite.y = self.position[1]


class Swarm():

    def __init__(self, num_particles):
        self.num_particles = num_particles
        self.global_best_position = np.array([random.random()*50, random.random()*50])
        self.global_best_value = float('inf')
        self.iterator = 0
        self.target = np.array([500, 300])
        self.particles = []
        self.batch = pg.graphics.Batch()
        self.speed = 10

        for _ in range(num_particles):
            c = pg.shapes.Circle(
                np.random.randint(500, 800)*1.0,
                np.random.randint(500, 600)*1.0,
                2,
                color=random_color(),
                batch=self.batch
            )

            self.particles.append(Particle(c, c.x, c.y))


    def set_best_values(self):
        for particle in self.particles:
            fitness = standard_fitness(particle.position)
            if particle.best_value < fitness:
                particle.best_value = fitness
                particle.best_position = particle.position
                if particle.best_value < self.global_best_value:
                    self.global_best_value = fitness
                    self.global_best_position = particle.best_position


    def update(self, delta):
        self.set_best_values()

        self.iterator += 2
        self.target[0] = np.sin(self.iterator/100) * 100 + 500
        self.target[1] = np.cos(self.iterator/100) * 100 + 500

        for particle in self.particles:

            force = get_swarm_force(
                particle.velocity,
                particle.position,
                particle.best_position,
                self.global_best_position,
                self.target,
                0.1,
                0.5,
                0.3
            )

            particle.velocity += force*delta
            particle.velocity /= np.linalg.norm(particle.velocity)
            particle.velocity *= self.speed

            particle.update(delta)
    
    def draw(self):
        self.batch.draw()