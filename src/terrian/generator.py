from typing import List
import random

import pygame
import numpy as np

from util.profile import profile
from terrian.chunk import Chunk
from noise.perlin import PerlinNoiseFactory
from constants import CHUNK_TILE_SIZE, WORLD_SIZE, WORLD_CHUNK_SIZE, TILE_SIZE, CHUNK_SIZE, CHUNK_TILE_SIZE


def create_multi_array(rows, cols, default_value=None):
    return [[default_value for _ in range(cols)] for _ in range(rows)]


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

        size = WORLD_CHUNK_SIZE*CHUNK_SIZE

        self.pnf = PerlinNoiseFactory(2, octaves=4, tile=(size, size))
        self.noise_map = np.zeros((WORLD_SIZE, WORLD_SIZE))

        self.chunk_map = create_multi_array(WORLD_CHUNK_SIZE, WORLD_CHUNK_SIZE)
        self.chunk_index = 1

        self.chunk_window = {}
        self.previous_chunk_window = {}


    @profile('generate_chunks')
    def generate_chunks(self, chunk_position: np.array) -> List:

        if self.generate_method == 'perlin':
            return self.generate_chunks_perlin(chunk_position)
        elif self.generate_method == 'random':
            return self.generate_chunks_random(chunk_position)


    def get_raw_chunk(self, x, y) -> Chunk:
        """
        Retrieve the raw chunk values from the world noise map
        """
        cx1 = x * CHUNK_TILE_SIZE
        cy1 = y * CHUNK_TILE_SIZE
        cx2 = cx1 + CHUNK_TILE_SIZE
        cy2 = cy1 + CHUNK_TILE_SIZE
        return self.noise_map[cx1:cx2, cy1:cy2]


    def get_chunk(self, x, y) -> Chunk:
        """
        Retrieve the chunk from the chunk map
        """
        return self.chunk_map[x][y]


    def set_chunk(self, x, y, chunk):
        self.chunk_map[x][y] = chunk


    def update_chunk_window(self, chunk_position):
        self.chunk_window = {}
        cwx, cwy, cwx2, cwy2 = self.get_chunk_window_coords(chunk_position)
        for cx in range(cwx, cwx2 + 1):
            for cy in range(cwy2, cwy + 1):
                self.chunk_window[f'{cx},{cy}'] = 1


    def get_chunk_window_coords(self, chunk_position):
        cpx, cpy = chunk_position[0], chunk_position[1]
        r = int((self.chunk_window_size - 1) / 2)

        # get the chunk window to loop over
        cwx, cwy = (cpx - r), (cpy + r)
        cwx2, cwy2 = (cpx + r), (cpy - r)

        return cwx, cwy, cwx2, cwy2

    
    def iter_chunks_to_generate(self):
        for k in self.chunk_window.keys():
            if k not in self.previous_chunk_window:
                x, y = k.split(',')
                yield int(x), int(y)


    def iter_chunk_window(self):
        for k in self.chunk_window.keys():
            x, y = k.split(',')
            yield int(x), int(y)

    
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

                    chx = (cx * CHUNK_SIZE * TILE_SIZE)
                    chy = (cy * CHUNK_SIZE * TILE_SIZE)
                    
                    # for each tile in the chunk, generate the tile
                    for tx in range(CHUNK_SIZE):
                        for ty in range(CHUNK_SIZE):
                            # world position
                            gx1 = chx + (tx * TILE_SIZE)
                            gy1 = chy + (ty * TILE_SIZE)
                        
                            self.noise_map[gx1, gy1] = np.random.uniform()
                            chunk.tiles[tx, ty] = rn

                    self.chunk_grid[cx, cy] = self.chunk_index
                    self.chunk_map[self.chunk_index] = chunk
                    self.chunk_index += 1
                    chunks.append(chunk)
                else:
                    chunks.append(self.chunk_map[chunk_id])

        return chunks


    def generate_chunks_perlin(self, chunk_position: np.array) -> List[Chunk]:
        print(f"generating chunks in window: {self.chunk_window}")

        chunks = []

        self.update_chunk_window(chunk_position)

        for cx, cy in self.iter_chunks_to_generate():

            chunk = self.get_chunk(cx, cy)

            # if the chunk is not generated, generate it
            if not chunk:
                chunk = Chunk(np.array([cx, cy]))

                print(f"generating {chunk}")

                chx = (cx * CHUNK_TILE_SIZE)
                chy = (cy * CHUNK_TILE_SIZE)

                # for each tile in the chunk, generate the tile
                for tx in range(CHUNK_SIZE):
                    for ty in range(CHUNK_SIZE):

                        # perlin position
                        px = cx * CHUNK_SIZE + tx
                        py = cy * CHUNK_SIZE + ty

                        # global position
                        gx1 = chx + (tx * TILE_SIZE)
                        gy1 = chy + (ty * TILE_SIZE)

                        # get the perlin noise value. fix the range to 0-1
                        rn = (self.pnf(px/CHUNK_SIZE, py/CHUNK_SIZE) + 1) / 2

                        self.noise_map[gx1, gy1] = rn
                        chunk.tiles[tx, ty] = rn

                self.set_chunk(cx, cy, chunk)
                self.chunk_index += 1

            chunks.append(chunk)

        print(f"generated {len(chunks)} chunks")

        self.previous_chunk_window = self.chunk_window

        return chunks