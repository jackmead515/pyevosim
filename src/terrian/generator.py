from typing import List
import random

import pygame
import numpy as np

from terrian.chunk import Chunk
from noise.perlin import PerlinNoiseFactory
import constants

class TerrianGenerator:
    """
    Controls the generation of chunks based on
    the give tile position.
    """

    def __init__(
        self,
        generate_method='perlin',
        chunk_window_size=3,
    ):
        self.generate_method = generate_method
        self.chunk_window_size = chunk_window_size

        self.chunk_window = np.zeros((chunk_window_size, chunk_window_size), dtype=np.int8)
        self.pnf = PerlinNoiseFactory(
            2,
            octaves=4,
            tile=(constants.WORLD_CHUNK_SIZE*constants.CHUNK_SIZE, constants.WORLD_CHUNK_SIZE*constants.CHUNK_SIZE)
        )
        self.noise_map = np.zeros((constants.WORLD_SIZE, constants.WORLD_SIZE))
        self.chunk_grid = np.zeros((constants.WORLD_CHUNK_SIZE, constants.WORLD_CHUNK_SIZE))
        self.chunk_index = 1
        self.chunk_map = {}


    def generate_chunks(self, chunk_position: np.array) -> List:

        if self.generate_method == 'perlin':
            return self.generate_chunks_perlin(chunk_position)
        elif self.generate_method == 'random':
            return self.generate_chunks_random(chunk_position)

    
    def generate_chunks_random(self, chunk_position: np.array) -> List[Chunk]:
        cpx, cpy = chunk_position[0], chunk_position[1]
        r = int((self.chunk_window_size - 1) / 2)

        # get the chunk window to loop over
        cwx, cwy = (cpx - r), (cpy + r)
        cwx2, cwy2 = (cpx + r), (cpy - r)

        print(f"generating chunks from ({cwx},{cwy}) to ({cwx2},{cwy2})")

        chunks = []

        # loop over the chunk window
        for cx in range(cwx, cwx2 + 1):
            for cy in range(cwy2, cwy + 1):
                chunk_id = self.chunk_grid[cx, cy]

                # if the chunk is not generated, generate it
                if chunk_id == 0:
                    chunk = Chunk(np.array([cx, cy]))

                    chx = (cx * constants.CHUNK_SIZE * constants.TILE_SIZE)
                    chy = (cy * constants.CHUNK_SIZE * constants.TILE_SIZE)
                    
                    # for each tile in the chunk, generate the tile
                    for tx in range(constants.CHUNK_SIZE):
                        for ty in range(constants.CHUNK_SIZE):
                            # world position
                            gx1 = chx + (tx * constants.TILE_SIZE)
                            gy1 = chy + (ty * constants.TILE_SIZE)
                        
                            rn = random.random()
                            self.noise_map[gx1, gy1] = rn
                            chunk.tiles[tx, ty] = rn

                    self.chunk_grid[cx, cy] = self.chunk_index
                    self.chunk_map[self.chunk_index] = chunk
                    self.chunk_index += 1
                    chunks.append(chunk)
                else:
                    chunks.append(self.chunk_map[chunk_id])

        return chunks


    def generate_chunks_perlin(self, chunk_position: np.array) -> List[Chunk]:
        cpx, cpy = chunk_position[0], chunk_position[1]
        r = int((self.chunk_window_size - 1) / 2)

        # get the chunk window to loop over
        cwx, cwy = (cpx - r), (cpy + r)
        cwx2, cwy2 = (cpx + r), (cpy - r)

        print(f"generating chunks from ({cwx},{cwy}) to ({cwx2},{cwy2})")

        chunks = []

        # loop over the chunk window
        for cx in range(cwx, cwx2 + 1):
            for cy in range(cwy2, cwy + 1):
                chunk_id = self.chunk_grid[cx, cy]

                # if the chunk is not generated, generate it
                if chunk_id == 0:
                    chunk = Chunk(np.array([cx, cy]))

                    chx = (cx * constants.CHUNK_SIZE * constants.TILE_SIZE)
                    chy = (cy * constants.CHUNK_SIZE * constants.TILE_SIZE)
                    
                    # for each tile in the chunk, generate the tile
                    for tx in range(constants.CHUNK_SIZE):
                        for ty in range(constants.CHUNK_SIZE):
                            
                            # perlin position
                            px = cx * constants.CHUNK_SIZE + tx
                            py = cy * constants.CHUNK_SIZE + ty

                            # global position
                            gx1 = chx + (tx * constants.TILE_SIZE)
                            gy1 = chy + (ty * constants.TILE_SIZE)

                            # get the perlin noise value. fix the range to 0-1
                            rn = (self.pnf(px/constants.CHUNK_SIZE, py/constants.CHUNK_SIZE) + 1) / 2

                            self.noise_map[gx1, gy1] = rn
                            chunk.tiles[tx, ty] = rn

                    self.chunk_grid[cx, cy] = self.chunk_index
                    self.chunk_map[self.chunk_index] = chunk
                    self.chunk_index += 1
                    chunks.append(chunk)
                else:
                    chunks.append(self.chunk_map[chunk_id])

        return chunks