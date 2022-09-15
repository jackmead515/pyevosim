import pygame

class SpriteSheet():

    def __init__(self, file_path, dimensions=()):
        self.sheet = pygame.image.load(file_path).convert()
        self.dimensions = dimensions

    def image_at(self, coords=()):
        rect = (
            coords[0]*self.dimensions[0], 
            coords[1]*self.dimensions[1],
            coords[0],
            coords[1]
        )
        rect = pygame.Rect(rect)
        rect.x = coords[0]*self.dimensions[0]
        rect.y = coords[1]*self.dimensions[1]
        rect.width = self.dimensions[0]
        rect.height = self.dimensions[1]
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image