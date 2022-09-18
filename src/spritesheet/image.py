import pygame

def load_image(file_path, scale=None):
    image = pygame.image.load(file_path).convert()
    if scale:
        image = pygame.transform.scale(image, scale)
    
    return image
