import numpy as np

class Camera2D:

    def __init__(self, x, y):
        self.position = np.array([x, y])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])

    def update(self, delta):
        self.velocity += self.acceleration * delta
        self.position += self.velocity * delta
