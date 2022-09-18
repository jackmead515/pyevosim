import pygame
import numpy as np
from tiles.tile import TileMap

from terrian.generator import TerrianGenerator

if __name__ == "__main__":

    tg = TerrianGenerator(generate_method='random')

    chunks = tg.generate_chunks(np.array([5, 5]))

    from matplotlib import pyplot as plt

    plt.imshow(chunks[0])
    plt.show()


    # pygame.init()
    # pygame.display.set_caption("TileMap")
    # screen = pygame.display.set_mode((400, 300))
    # clock = pygame.time.Clock()

    # background = pygame.Surface((400, 300))
    # background.fill(pygame.Color('#000000'))

    # tile_map = TileMap(400, 300, 16)
    # tile_map.generate()

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()

    #     screen.blit(background, (0, 0))
    #     tile_map.draw(screen)
    #     pygame.display.update()
    #     clock.tick(30)
