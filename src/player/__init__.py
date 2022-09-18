import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group
import pymunk
import numpy as np

import spritesheet
import constants

class Player(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()

        self.chunk_position = np.array([0, 0])
        self.previous_chunk_position = np.array([0, 0])

        self.position = np.array([x, y])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

        self.sprite_sheet = spritesheet.SpriteStripAnim(
            'assets/slime_small_blue.png',
            (32, 32),
            (4, 2),
            1,
            True,
            30/12
        )
    
    def changed_chunk(self):
        return not np.array_equal(self.chunk_position, self.previous_chunk_position)


    def update(self, delta):
        self.chunk_position = np.array([
            int(self.position[0] // constants.CHUNK_TILE_SIZE),
            int(self.position[1] // constants.CHUNK_TILE_SIZE)
        ])
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
        self.rect.center = (self.position[0], self.position[1])


    def draw(self, screen):
        image = self.sprite_sheet.next()
        screen.blit(image, self.rect)