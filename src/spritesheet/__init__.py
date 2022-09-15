import pygame

class SpriteSheet():

    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except Exception as e:
            print(f'Unable to load spritesheet image: {filename}')
            raise e


    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


    def load_strip(self, size, dimensions, colorkey = None):
        images = []
        for columns in range(dimensions[1]):
            for rows in range(dimensions[0]):
                rect = (columns * size[0], rows * size[1], size[0], size[1])
                print(rect)
                images.append(self.image_at(rect, colorkey))
        return images


class SpriteStripAnim():

    def __init__(self, filename, size, dimensions, colorkey=None, loop=False, frames=1):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        ss = SpriteSheet(filename)
        self.images = ss.load_strip(size, dimensions, colorkey)
        self.i = 0
        self.loop = loop
        self.frames = frames
        self.f = frames

    def iter(self):
        self.i = 0
        self.f = self.frames
        return self

    def next(self):
        if self.i >= len(self.images):
            if not self.loop:
                raise StopIteration
            else:
                self.i = 0
        image = self.images[self.i]
        self.f -= 1
        if self.f == 0:
            self.i += 1
            self.f = self.frames
        return image