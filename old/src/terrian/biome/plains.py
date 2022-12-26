from typing import List

import numpy as np
import pyglet as pg

from terrian.chunk import Chunk
from textures import texture_manager
from biome import Biome


rule = {
    'rule': [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ],
    'result': [
        
    ]
}





class PlainBiome(Biome):


    def __init__(self):
        super().__init__()


    def get_tile_values(self, tiles: np.array) -> np.array:
        tile_values = np.zeros(tiles.shape, dtype=np.int8)

        for i, tile in enumerate(tiles):
            if tile > 0.6:
                tile_values[i] = 0 # water
            elif tile > 0.3:
                tile_values[i] = 1 # grass
            else:
                tile_values[i] = 2 # dirt

        return tile_values


    def apply_biome_rules(self, chunk: Chunk, tiles: np.array) -> np.array:
        tile_textures = np.zeros(tiles.shape, dtype=np.int8)