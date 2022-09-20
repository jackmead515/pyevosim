from dataclasses import dataclass

import pyglet as pg
from pyglet.image import TextureRegion, load as load_image

@dataclass
class TextureManager():

    WATER_TILE: TextureRegion
    GRASS_TILE: TextureRegion
    DIRT_TILE: TextureRegion

    def __init__(self):
        pass

    def load(self):
        self.WATER_TILE = load_image("assets/nature_tileset/sprite_015.png")
        self.GRASS_TILE = load_image("assets/nature_tileset/sprite_019.png")
        self.DIRT_TILE = load_image("assets/nature_tileset/sprite_021.png")

texture_manager = TextureManager()