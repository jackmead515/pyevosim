import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group
import pymunk

import spritesheet

class Player(Sprite):

    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)

        self.sprite_sheet = spritesheet.SpriteStripAnim(
            'assets/slime_small_blue.png',
            (32, 32),
            (4, 2),
            1,
            True,
            30/12
        )
    

    def update(self, delta):
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
        self.rect.center = self.position


    def draw(self, screen):
        image = self.sprite_sheet.next()
        screen.blit(image, self.rect)