import random

import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group
import pymunk

import numpy as np

WEIGHT = 0.5
C1 = 0.8
C2 = 0.9

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
        self.position += self.velocity
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
                1, 1, random_color()
            ))
        
        for sprite in self.particles:
            self.add(sprite)


    def fitness(self, particle):
        return particle.position[0] ** 2 + particle.position[1] ** 2 + 1


    def set_best_values(self):
        for particle in self.particles:
            fitness = self.fitness(particle)
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
            r1 = random.random()
            r2 = random.random()
            swarm_force = WEIGHT * particle.velocity + \
                C1 * r1 * (particle.best_position - particle.position) + \
                C2 * r2 * (self.global_best_position - particle.position)
            swarm_force /= np.linalg.norm(swarm_force)
            swarm_force *= 0.1
    
            target_force = np.subtract(self.target, particle.position)
            target_force /= np.linalg.norm(target_force)
            target_force *= 0.5

            random_force = np.array([r1*0.3, r2*0.3])

            particle.velocity += target_force
            particle.velocity += swarm_force
            particle.velocity += random_force

            particle.velocity /= np.linalg.norm(particle.velocity)
            particle.velocity *= 4

            particle.update(delta)
    
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.target, 5)
        super().draw(screen)
        #for particle in self.particles:
        #    particle.draw(screen)