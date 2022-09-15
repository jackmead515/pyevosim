import pygame
from pygame import Vector2
from pygame.sprite import Sprite, Group
import pymunk


class BoxSprite(Sprite):

    def __init__(self, space, x, y, width, height, color):
        Sprite.__init__(self)
        self.space = space
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.position = Vector2(x, y)

        self.body = pymunk.Body(1,1666)
        self.body.position = self.position[0], self.position[1]
        self.poly = pymunk.Poly.create_box(self.body)
        self.space.add(self.body, self.poly)

    def update(self, delta):
        self.position = self.body.position
        self.rect.center = self.position


class Boxy(Group):
    
    def __init__(self, space):
        Group.__init__(self)

        sprites = []
        sprites.append(BoxSprite(space, 100, 100, 50, 50, (255, 0, 0)))
        sprites.append(BoxSprite(space, 150, 150, 20, 20, (0, 255, 0)))
        sprites.append(BoxSprite(space, 100, 150, 20, 20, (0, 0, 255)))
        
        for sprite in sprites:
            self.add(sprite)