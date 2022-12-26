from typing import List

import numpy as np
import pyglet as pg

from terrian.chunk import Chunk
from textures import texture_manager

class Biome:

    def __init__(self):
        pass


    def get_tile_values(self, tiles: np.array) -> np.array:
        """
        Override per biome implementation to generate
        a unique tile from the base tileset in a biome.

        For plain, that's water, grass, and dirt.
        For forest, that's trees, grass, and dirt.
        For desert, that's sand, grass, and dirt.
        etc....
        """
        pass


    def apply_biome_rules(self, chunk: Chunk, tiles: np.array) -> np.array:
        """
        Apply biome rules to the given tile chunk
        """
        pass


    def generate(self, chunk: Chunk) -> np.array:
        """
        Generates tiles based on the given biome and rule
        set that is applyed to the given tiles
        """
        tiles = self.get_tile_values(chunk.tiles)
        tile_textures = np.zeros(tiles.shape, dtype=np.int8)

        for tx in range(tiles.shape[0]):
            for ty in range(tiles.shape[1]):
                top, right, bottom, left = chunk.neighbors(tx, ty)
        tiles = self.apply_biome_rules(chunk, tiles)
        return tiles

            