import pymunk
import pyglet as pg
import numpy as np

import sprites
import constants
from textures import texture_manager

class Player:

    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

        self.chunk_position = np.array([
            int(self.position[0] // constants.CHUNK_TILE_SIZE),
            int(self.position[1] // constants.CHUNK_TILE_SIZE)
        ])
    
        self.speed = 500.0

        self.sprite = sprites.load_sprite(texture_manager.WATER_TILE, self.position[0], self.position[1])


    def on_key_press(self, symbol, modifiers):
        if symbol == pg.window.key.W:
            self.velocity[1] = self.speed
            print('accelerating up')
        elif symbol == pg.window.key.S:
            self.velocity[1] = -self.speed
        elif symbol == pg.window.key.A:
            self.velocity[0] = -self.speed
        elif symbol == pg.window.key.D:
            self.velocity[0] = self.speed


    def on_key_release(self, symbol, modifiers):
        if symbol == pg.window.key.W:
            self.velocity[1] = 0.0
        elif symbol == pg.window.key.S:
            self.velocity[1] = 0.0
        elif symbol == pg.window.key.A:
            self.velocity[0] = 0.0
        elif symbol == pg.window.key.D:
            self.velocity[0] = 0.0


    def update(self, delta):
        self.chunk_position = np.array([
            int(self.position[0] // constants.CHUNK_TILE_SIZE),
            int(self.position[1] // constants.CHUNK_TILE_SIZE)
        ])
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
        self.sprite.update(self.position[0], self.position[1])


    def draw(self):
        self.sprite.draw()