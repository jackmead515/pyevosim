import random

import pygame
from pygame.sprite import Sprite, Group
import numpy as np
from tqdm import tqdm

from noise.perlin import PerlinNoiseFactory
from spritesheet.spritesheet import SpriteSheet


class Tile(Sprite):

    def __init__(self, x, y, image):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.position = np.array([x, y])

    def update(self, delta):
        self.rect.topleft = self.position


class TileMap(Group):

    def __init__(self, width, height, tile_size):
        Group.__init__(self)
        self.width = width
        self.height = height
        self.tile_size = tile_size

    def generate(self):

        gx = self.width
        gy = self.height

        pnf = PerlinNoiseFactory(2, octaves=4, tile=(gx, gy))
        noise = np.zeros((gx, gy))

        for x in tqdm(range(gx)):
            for y in range(gy):
                noise[x,y] = pnf(x/gx,y/gy)
        
        total_bins = 3
        minn = np.min(noise)
        maxn = np.max(noise)
        step = abs(maxn-minn) / total_bins
        fields = np.arange(minn, maxn, step)

        gxa = int(gx/self.tile_size)
        gya = int(gy/self.tile_size)
        tiles = np.zeros((gxa, gya))

        for x in range(gxa):
            for y in range(gya):
                x1 = x*self.tile_size
                x2 = x1+self.tile_size
                y1 = y*self.tile_size
                y2 = y1+self.tile_size
                mean = np.median(noise[x1:x2,y1:y2])
                tiles[x,y] = mean
        
        bins = np.digitize(tiles, fields)

        ss = SpriteSheet("assets/nature_tileset.png", (64, 64))

        pygame.transform.scale(ss.image_at((0, 3)), (16, 16))

        grass_tile = pygame.transform.scale(ss.image_at((0, 3)), (16, 16))
        water_tile = pygame.transform.scale(ss.image_at((1, 3)), (16, 16))


        def get_image(bin):
            if bin == 1:
                return water_tile
            elif bin == 2:
                return grass_tile
            elif bin == 3:
                return water_tile

        tiles = []
        for x in range(int(self.width/self.tile_size)):
            for y in range(int(self.height/self.tile_size)):
                tiles.append(Tile(
                    x*self.tile_size,
                    y*self.tile_size,
                    get_image(bins[x,y])
                ))

        for sprite in tiles:
            self.add(sprite)

