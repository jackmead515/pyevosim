import uuid

import numpy as np
import pyglet as pg

from sprites import load_sprite
from nn.brain import random_brain

class Creature():


    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

        self.brain = random_brain(5, 5)

        self.max_energy = 100.0
        self.energy = self.max_energy
        self.energy_regen = 0.1
        self.energy_loss = 1

        self.speed = 50.0

        self.animation = pg.resource.animation('assets/creatures/slime_small_red.gif')
        self.sprite = load_sprite(self.animation, self.position[0], self.position[1])

        self.id = str(uuid.uuid4())

        self.inputs = np.zeros(5, dtype=np.float32)


    def __str__(self):
        return f"Creature: {self.id}, Energy: {self.energy}, Position: {self.position}, Velocity: {self.velocity}"


    def update(self, delta):

        # get the surrounding tiles
        # get the surrounding creatures
        # get the surrounding food
        # raycat out in front of the creature
        # and detect the closest food, creature, and tiles

        self.inputs[0] = self.energy
        self.inputs[1] = self.position[0]
        self.inputs[2] = self.position[1]
        self.inputs[3] = self.velocity[0]
        self.inputs[4] = self.velocity[1]

        decision = np.argmax(self.brain.compute(self.inputs))

        energy_factor = self.energy / self.max_energy

        if decision == 0:
            self.velocity[0] = self.speed * energy_factor
            self.energy -= self.energy_loss
        elif decision == 1:
            self.velocity[0] = -self.speed * energy_factor
            self.energy -= self.energy_loss
        elif decision == 2:
            self.velocity[1] = self.speed * energy_factor
            self.energy -= self.energy_loss
        elif decision == 3:
            self.velocity[1] = -self.speed * energy_factor
            self.energy -= self.energy_loss
        elif decision == 4:
            self.velocity[0] = 0.0
            self.velocity[1] = 0.0

        self.energy = max(0, min(self.energy + self.energy_regen, self.max_energy))
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
        self.sprite.update(self.position[0], self.position[1])


    def draw(self):
        self.sprite.draw()