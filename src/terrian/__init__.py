import pygame
from pygame.sprite import Sprite, Group, Rect
import numpy as np

from spritesheet.image import load_image
from terrian.generator import TerrianGenerator
import constants

class Tile(Sprite):

    def __init__(self, x, y, size, image):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect.width = size
        self.rect.height = size


class Combined(Sprite):

    def __init__(self, sprites):
        Sprite.__init__(self)
    
        self.rect = sprites[0].rect.copy()
        for sprite in sprites[1:]:
            self.rect.union_ip(sprite.rect)

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        for sprite in sprites:
            self.image.blit(sprite.image, (sprite.rect.x-self.rect.left, sprite.rect.y-self.rect.top))

        print(self.rect)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        pygame.gfxdraw.rectangle(screen, self.rect, (0, 255, 0))
        
        


class Terrian(Group):

    def __init__(
        self,
        generate_method='perlin',
        chunk_window_size=3,
    ):
        Group.__init__(self)
        self.generator = TerrianGenerator(
            generate_method=generate_method,
            chunk_window_size=chunk_window_size,
        )
        tile_dims = (constants.TILE_SIZE, constants.TILE_SIZE)
        self.water_tile = load_image("assets/nature_tileset/sprite_015.png", scale=tile_dims)
        self.grass_tile = load_image("assets/nature_tileset/sprite_019.png", scale=tile_dims)
        self.dirt_tile = load_image("assets/nature_tileset/sprite_021.png", scale=tile_dims)


    def generate_chunks(self, chunk_position: np.array):
        self.empty()

        chunks = self.generator.generate_chunks(chunk_position)

        def get_image(bin):
            if bin > 0.6:
                return self.water_tile
            elif bin > 0.3:
                return self.grass_tile
            else:
                return self.dirt_tile

        chunk_groups = []

        print(f'Generating {len(chunks)} chunks')
        total_tiles = 0

        for chunk in chunks:
            print(chunk)
            tiles = []
            for tile, tx, ty in chunk.iter_tiles():
                total_tiles += 1
                print(tile, tx, ty)
                tiles.append(Tile(tx, ty, constants.TILE_SIZE, get_image(tile)))
            chunk_groups.append(Combined(tiles))
            self.add(Combined(tiles))

        print(f'Generated {total_tiles} tiles')

        #self.add(Combined(chunk_groups))
        #for sprite in self.tiles:
        #   self.add(sprite)
    
    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)