import random

import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group
import pymunk

import numpy as np

from swarm.util import get_swarm_force, standard_fitness

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class Particle(Sprite):

    def __init__(self, x, y, width, height, color):
        Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.position = np.array([x, y])
        self.best_position = self.position
        self.best_value = float('inf')
        self.velocity = np.array([0.0, 0.0])

    def update(self, delta):
        self.position += self.velocity*delta
        self.rect.center = self.position


class Swarm(Group):

    def __init__(self, num_particles):
        Group.__init__(self)

        self.num_particles = num_particles
        self.global_best_position = np.array([random.random()*50, random.random()*50])
        self.global_best_value = float('inf')
        self.iterator = 0

        self.target = np.array([500, 300])

        self.particles = []
        for i in range(num_particles):
            self.particles.append(Particle(
                np.random.randint(500, 800)*1.0,
                np.random.randint(500, 600)*1.0,
                2, 2, random_color()
            ))
        
        for sprite in self.particles:
            self.add(sprite)


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
            particle.velocity *= 5

            particle.update(delta)
    
    # def draw(self, screen):
    #     #pygame.draw.circle(screen, (0, 255, 0), self.target, 5)
    #     super().draw(screen)