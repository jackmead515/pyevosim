
import numpy as np

import constants

class Chunk:
    """
    Represents a chunk of terrian where the tiles
    represent the class of tile and the coords is the
    space where the chunk is located in the world.

    coords are np.array[] of 3 variables, x, y, and z

    tiles are a 2d np.array[] representing the grid space
    """

    def __init__(self, position: np.array) -> None:
        self.chunk_position = position
        self.tiles = np.zeros((constants.CHUNK_SIZE, constants.CHUNK_SIZE))


    def get_chunk_position(self) -> np.array:
        return self.chunk_position

    def get_world_position(self) -> np.array:
        return self.chunk_position * constants.CHUNK_SIZE * constants.TILE_SIZE

    def iter_tiles(self):
        """
        Iterates over the tiles in the chunk and returns
        a tuple for the tile number, and the global tile position
        """
        cpx, cpy = self.chunk_position[0]*constants.CHUNK_SIZE*constants.TILE_SIZE, self.chunk_position[1]*constants.CHUNK_SIZE*constants.TILE_SIZE

        for tx in range(self.tiles.shape[0]):
            for ty in range(self.tiles.shape[1]):
                gx1, gy1 = tx*constants.TILE_SIZE + cpx, ty*constants.TILE_SIZE + cpy
                yield self.tiles[tx, ty], gx1, gy1


    def __str__(self) -> str:
        return f"chunk ({self.chunk_position})"