import pyglet as pg
import numpy as np
import time

from sprites.image import load_image
from sprites import load_sprite
from terrian.generator import TerrianGenerator
from textures import texture_manager
import constants

# class Tile(Sprite):

#     def __init__(self, x, y, size, image):
#         Sprite.__init__(self)
#         self.image = image
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.rect.width = size
#         self.rect.height = size


# class Combined(Sprite):

#     def __init__(self, sprites):
#         Sprite.__init__(self)
    
#         self.rect = sprites[0].rect.copy()
#         for sprite in sprites[1:]:
#             self.rect.union_ip(sprite.rect)

#         self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

#         for sprite in sprites:
#             self.image.blit(sprite.image, (sprite.rect.x-self.rect.left, sprite.rect.y-self.rect.top))

#         print(self.rect)

#     def draw(self, screen):
#         screen.blit(self.image, self.rect)
#    
# 
#     pygame.gfxdraw.rectangle(screen, self.rect, (0, 255, 0))

def profile_time(func):
    def wrapper(*args, **kwargs):
        
        return result
    return wrapper

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
        self.sprites = []

        self.chunk_position = np.array([0, 0])
        self.previous_chunk_position = self.chunk_position


    def generate_chunks(self, chunk_position: np.array):
        """
        Generate chunks around the player chunk_position! Does not
        track if chunks have already been generated. All the current
        textures should be dropped from the batch and then re-added
        """
        self.batch = pg.graphics.Batch()
        self.sprites = []
        
        chunks = self.generator.generate_chunks(chunk_position)

        def get_image(bin):
            if bin > 0.6:
                return texture_manager.WATER_TILE
            elif bin > 0.3:
                return texture_manager.GRASS_TILE
            else:
                return texture_manager.DIRT_TILE

        for chunk in chunks:
            
            for tile, tx, ty in chunk.iter_tiles():
                self.sprites.append(load_sprite(get_image(tile), tx, ty, batch=self.batch))

            cp = chunk.get_world_position()
            c = pg.shapes.Circle(cp[0], cp[1], 2, color=(255, 0, 0), batch=self.batch)
            c.anchor_x = c.radius // 2
            c.anchor_y = c.radius // 2
            self.sprites.append(c)


    def update(self, chunk_position: np.array):
        self.chunk_position = chunk_position
        if not np.array_equal(self.chunk_position, self.previous_chunk_position):
            self.generate_chunks(self.chunk_position)
            self.previous_chunk_position = self.chunk_position


    def draw(self):
        self.batch.draw()