from quads import QuadTree

class QuadTree():

    def __init__(self, x, y, width, height, max_objects=10, max_levels=5, level=0):
        self.max_objects = max_objects
        self.max_levels = max_levels
        self.level = level
        self.objects = []
        self.bounds = {'x': x, 'y': y, 'width': width, 'height': height}
        self.nodes = []
    
    def clear(self):
        self.objects = []
        for node in self.nodes:
            node.clear()
        self.nodes = []
    
    def split(self):
        sub_width = self.bounds['width'] / 2
        sub_height = self.bounds['height'] / 2
        x = self.bounds['x']
        y = self.bounds['y']
        self.nodes.append(QuadTree(x + sub_width, y, sub_width, sub_height, self.max_objects, self.max_levels, self.level + 1))
        self.nodes.append(QuadTree(x, y, sub_width, sub_height, self.max_objects, self.max_levels, self.level + 1))
        self.nodes.append(QuadTree(x, y + sub_height, sub_width, sub_height, self.max_objects, self.max_levels, self.level + 1))
        self.nodes.append(QuadTree(x + sub_width, y + sub_height, sub_width, sub_height, self.max_objects, self.max_levels, self.level + 1))
    
    def get_index(self, rect):
        index = -1
        vertical_midpoint = self.bounds['x'] + (self.bounds['width'] / 2)
        horizontal_midpoint = self.bounds['y'] + (self.bounds['height'] / 2)
        top_quadrant = (rect['y'] < horizontal_midpoint and rect['y'] + rect['height'] < horizontal_midpoint)
        bottom_quadrant = (rect['y'] > horizontal_midpoint)
        if rect['x'] < vertical_midpoint and rect['x'] + rect['width'] < vertical_midpoint:
            if top_quadrant:
                index = 1
            elif bottom_quadrant:
                index = 2
        elif rect['x'] > vertical_midpoint:
            if top_quadrant:
                index = 0
            elif bottom_quadrant:
                index = 3
        return index
    
    def insert(self, rect):
        if len(self.nodes) > 0:
            index = self.get_index(rect)
            if index != -1:
                self.nodes[index].insert(rect)
                return
        self.objects.append(rect)
        if len(self.objects) > self.max_objects and self.level < self.max_levels:
            if len(self.nodes) == 0:
                self.split()
            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i])
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1
    
    def retrieve(self, rect):
        index = self.get_index(rect)
        if index != -1 and len(self.nodes) > 0:
            return self.nodes[index].retrieve(rect)
        return self.objects