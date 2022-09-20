import random

import pygame
from pygame.sprite import Sprite, Group
import numpy as np
from tqdm import tqdm

from noise.perlin import PerlinNoiseFactory
from sprites.spritesheet import SpriteSheet
from sprites.image import load_image


class Tile(Sprite):

    def __init__(self, x, y, image):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class TileMap(Group):

    def __init__(self, width, height, tile_size):
        Group.__init__(self)
        self.width = width
        self.height = height
        self.tile_size = tile_size

    def random(self):
        tile_dims = (self.tile_size, self.tile_size)

        water_tile = load_image("assets/nature_tileset/sprite_015.png", scale=tile_dims)
        grass_tile = load_image("assets/nature_tileset/sprite_019.png", scale=tile_dims)
        dirt_tile = load_image("assets/nature_tileset/sprite_021.png", scale=tile_dims)

        def get_image(bin):
            if bin == 1:
                return water_tile
            elif bin == 2:
                return grass_tile
            elif bin == 3:
                return dirt_tile

        tiles = []
        for x in range(int(self.width/self.tile_size)):
            for y in range(int(self.height/self.tile_size)):
                tiles.append(Tile(
                    x*self.tile_size,
                    y*self.tile_size,
                    get_image(random.randint(1, 3))
                ))

        for sprite in tiles:
            self.add(sprite)


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

        tile_dims = (self.tile_size, self.tile_size)

        water_tile = load_image("assets/nature_tileset/sprite_015.png", scale=tile_dims)
        grass_tile = load_image("assets/nature_tileset/sprite_019.png", scale=tile_dims)
        dirt_tile = load_image("assets/nature_tileset/sprite_021.png", scale=tile_dims)

        def get_image(bin):
            if bin == 1:
                return water_tile
            elif bin == 2:
                return grass_tile
            elif bin == 3:
                return dirt_tile

        tiles = []
        for x in range(int(gx/self.tile_size)):
            for y in range(int(gy/self.tile_size)):
                tiles.append(Tile(
                    x*self.tile_size,
                    y*self.tile_size,
                    get_image(bins[x, y])
                ))

        for sprite in tiles:
            self.add(sprite)
