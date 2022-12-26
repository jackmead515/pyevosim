import random
from turtle import st

import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group
import pymunk

import numpy as np

class Particle(Sprite):

    def __init__(self, x, y, width, height, color):
        Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.position = np.array([x, y])
        self.velocity = np.array([0.0, 0.0])

    def update(self, delta):
        self.position += self.velocity
        self.rect.center = self.position

class Seekers(Group):

    def __init__(self, num_particles):
        Group.__init__(self)

        self.num_particles = num_particles
        self.target = np.array([random.random()*50, random.random()*50])
        self.iterator = 0

        self.particles = []
        for i in range(num_particles):
            self.particles.append(Particle(
                np.random.randint(500, 800)*1.0,
                np.random.randint(500, 600)*1.0,
                2, 2, (255, 0, 0)
            ))
        
        for sprite in self.particles:
            self.add(sprite)

    def update(self, delta):

        if self.iterator % 1000 == 0:
            self.target = np.array([np.random.randint(100, 1000), np.random.randint(100, 700)])

        self.iterator += 1

        
        for particle in self.particles:
            total_force = np.array([0.0, 0.0])
            count = 0

            for other in self.particles:
                distance = np.linalg.norm(particle.position - other.position)

                if distance > 0 and distance < 10:
                    diff = np.subtract(particle.position, other.position)
                    diff /= np.linalg.norm(diff)
                    diff /= distance
                    total_force += diff
                    count += 1

            if count > 0:
                total_force /= count
                total_force /= np.linalg.norm(total_force)
                total_force *= 10
                steer_force = np.subtract(total_force, particle.velocity)
                steer_force /= np.linalg.norm(steer_force)
                steer_force *= 0.1
                particle.velocity += steer_force

        for particle in self.particles:
            desired = np.subtract(self.target, particle.position)
            desired /= np.linalg.norm(desired)
            desired *= 10
            steer_force = np.subtract(desired, particle.velocity)
            steer_force /= np.linalg.norm(steer_force)
            steer_force *= 0.1
            particle.velocity += steer_force
            particle.update(delta)
        

