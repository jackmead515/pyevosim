import numpy as np
import numba as nb

@nb.jit(nopython=True, fastmath=True)
def rp_contains(rect: np.array, point: np.array) -> bool:
    """
    Check if a point is inside a rectangle.
    point = [x, y]
    rect = [x, y, w, h]
    """
    return (rect[0] <= point[0] <= rect[0] + rect[2]) and (rect[1] <= point[1] <= rect[1] + rect[3])


@nb.jit(nopython=True, fastmath=True)
def cp_contains(circle: np.array, point: np.array) -> bool:
    """
    Check if a point is inside a circle.
    point = [x, y]
    circle = [x, y, r]
    """
    return np.linalg.norm(circle[:2] - point) <= circle[2]


@nb.jit(nopython=True, fastmath=True)
def rr_intersects(rect1: np.array, rect2: np.array) -> bool:
    """
    Check if two rectangles intersect.
    rect1 = [x, y, w, h]
    rect2 = [x, y, w, h]
    """
    return (rect1[0] <= rect2[0] + rect2[2] and rect1[0] + rect1[2] >= rect2[0] and rect1[1] <= rect2[1] + rect2[3] and rect1[1] + rect1[3] >= rect2[1])


@nb.jit(nopython=True, fastmath=True)
def cr_intersects(circle: np.array, rect: np.array) -> bool:
    """
    Check if a circle intersects a rectangle.
    circle = [x, y, r]
    rect = [x, y, w, h]
    """
    x = max(rect[0], min(circle[0], rect[0] + rect[2]))
    y = max(rect[1], min(circle[1], rect[1] + rect[3]))
    dx = x - circle[0]
    dy = y - circle[1]
    return (dx * dx + dy * dy) < (circle[2] * circle[2])


class QTree:

    def __init__(self, x, y, w, h, level=0, capacity=4):
        self.boundary = np.array([x, y, w, h], dtype=np.float32)
        self.capacity = capacity
        self.level = level
        self.divided = False
        self.quads = []
        self.points = []


    def subdivide(self):
        x, y, w, h = self.boundary
        level = self.level + 1

        hw = w / 2
        hh = h / 2

        self.quads = [
            QTree(x, y + hh, hw, hh, level, self.capacity), # north west
            QTree(x, y, hw, hh, level, self.capacity), # south west
            QTree(x + hw, y + hh, hw, hh, level, self.capacity), # north east
            QTree(x + hw, y, hw, hh, level, self.capacity) # south east
        ]

        self.divided = True
    

    def insert(self, point: np.array):
        if not rp_contains(self.boundary, point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True

        if not self.divided:
            self.subdivide()

        for quad in self.quads:
            if quad.insert(point):
                return True
        
        return False


    def query_rect(self, rect: np.array):
        if not rr_intersects(rect, self.boundary):
            return []

        points = []
        for point in self.points:
            if rp_contains(rect, point):
                points.append(point)

        if self.divided:
            for quad in self.quads:
                points += quad.query_rect(rect)
        
        return points
    

    def query_circle(self, circle: np.array):
        if not cr_intersects(circle, self.boundary):
            return []

        points = []
        for point in self.points:
            if cp_contains(circle, point):
                points.append(point)

        if self.divided:
            for quad in self.quads:
                points += quad.query_circle(circle)
        
        return points


def draw_tree(plot, tree, circle):
    x, y, w, h = tree.boundary
    plot.plot([x, x + w, x + w, x, x], [y, y, y + h, y + h, y], 'k-')

    for point in tree.points:
        if cp_contains(circle, point):
            plot.plot(point[0], point[1], 'r.')
        #plot.plot(point[0], point[1], 'ro')

    if tree.divided:
        for quad in tree.quads:
            draw_tree(plot, quad, circle)


if __name__ == "__main__":

    tree = QTree(0.0, 0.0, 100.0, 100.0)

    print(tree)

    for i in range(300):
        p = np.array(np.random.rand(2) * 99, dtype=np.float32)
        tree.insert(p)

    #rect = np.array([0.0, 0.0, 100.0, 100.0], dtype=np.float32)

    import matplotlib.pyplot as plot
    draw_tree(plot, tree, np.array([50, 50, 25], dtype=np.float32))

    # draw a circle
    circle = plot.Circle((50, 50), 25, color='r', fill=False)

    plot.gca().add_patch(circle)

    plot.show()


