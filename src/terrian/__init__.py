import random
from collections import deque

import pyglet as pg
import numpy as np

from sprites import load_sprite
from terrian.chunk import Chunk
from terrian.generator import TerrianGenerator
from textures import texture_manager
import constants


class Terrian():

    def __init__(
        self,
        generate_method='perlin',
        chunk_window_size=3,
    ):
        super().__init__()
        self.generator = TerrianGenerator(
            generate_method=generate_method,
            chunk_window_size=chunk_window_size,
        )
        self.batch = pg.graphics.Batch()

        self.sprite_iterator = deque()
        self.sprites = deque()
        self.init_tiles = False
        self.tile_gen_rate = 100

        self.chunk_position = np.array([0, 0])
        self.previous_chunk_position = self.chunk_position

    
    def initalize(self, chunk_position: np.array):
        self.chunk_position = chunk_position

        # update the previous chunk window in the generator with
        # some random chunk position such that the first time it
        # runs it will generate the chunks
        cwx, cwy, cwx2, cwy2 = self.generator.get_chunk_window_coords(chunk_position - 100)
        for cx in range(cwx, cwx2 + 1):
            for cy in range(cwy2, cwy + 1):
                self.generator.previous_chunk_window[f'{cx},{cy}'] = 1

        self.generate_chunks(self.chunk_position)


    def generate_chunks(self, chunk_position: np.array):
        """
        Generate chunks around the player chunk_position! Does not
        track if chunks have already been generated. All the current
        textures should be dropped from the batch and then re-added

        - Should be optimized to only generate chunks that need to 
          be generated based on the current chunk position and the
          chunk window size

        - Should be optimized to progressively generate tiles over time
          instead of all at once to prevent garbage collection
        """

        chunks = self.generator.generate_chunks(chunk_position)

        for chunk in chunks:
            for tile, tx, ty in chunk.iter_tiles():
                tile = self.generate_tile(chunk, tile, tx, ty)
                self.sprite_iterator.appendleft((tile, tx, ty, self.batch))

            # cp = chunk.get_world_position()
            # c = pg.shapes.Circle(cp[0], cp[1], 2, color=(255, 0, 0), batch=self.batch)
            # c.anchor_x = c.radius // 2
            # c.anchor_y = c.radius // 2

        if not self.init_tiles:
            self.init_tiles = True

            while len(self.sprite_iterator):
                args = self.sprite_iterator.pop()
                self.sprites.append(load_sprite(*args))


    def generate_tile(self, chunk: Chunk, tile: float, tx: int, ty: int):
        # minn = np.min(noise)
        # maxn = np.max(noise)
        # step = abs(maxn-minn) / total_bins
        # fields = np.arange(minn, maxn, step)
        # bins = np.digitize(tiles, fields)

        grass_tiles = [
            texture_manager.grass_1,
            texture_manager.grass_2,
            texture_manager.grass_3,
            texture_manager.grass_4,
        ]

        if tile > 0.3:
            num = np.random.binomial(3, 0.05, 1)[0]
            return grass_tiles[num]
            #return texture_manager.water_1
        elif tile > 0.4:
            num = np.random.binomial(3, 0.05, 1)[0]
            return grass_tiles[num]
            #return texture_manager.GRASS_TILE
        else:
            return texture_manager.dirt_1


    def update_tiles(self):
        for _ in range(self.tile_gen_rate):
            if not len(self.sprite_iterator):
                break
            args = self.sprite_iterator.pop()
            self.sprites.append(load_sprite(*args))


    def update(self, delta: float, chunk_position: np.array):
        self.chunk_position = chunk_position

        self.update_tiles()

        if not np.array_equal(self.chunk_position, self.previous_chunk_position):
            self.generate_chunks(self.chunk_position)
            self.previous_chunk_position = self.chunk_position


    def draw(self):
        self.batch.draw()