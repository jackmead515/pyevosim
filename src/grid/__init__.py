import pygame

def draw_grid(screen, width, height, tile_size, color):
    for x in range(0, width, tile_size):
        pygame.draw.line(screen, color, (x, 0), (x, height))
    for y in range(0, height, tile_size):
        pygame.draw.line(screen, color, (0, y), (width, y))