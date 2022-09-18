import pygame

class SpriteSheet():

    def __init__(self, file_path, dims=()):
        self.sheet = pygame.image.load(file_path).convert()
        self.dims = dims

    def image_at(self, coords=()):
        rect = pygame.Rect((0,0,0,0))
        rect.x = coords[0]*self.dims[0]
        rect.y = coords[1]*self.dims[1]
        rect.width = self.dims[0]
        rect.height = self.dims[1]
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image