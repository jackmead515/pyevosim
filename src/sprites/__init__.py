import pyglet as pg
import numpy as np
import pymunk as pm


def load_sprite(texture, x, y, batch=None, group=None) -> pg.sprite.Sprite:
    return pg.sprite.Sprite(texture, x, y, batch=batch, group=group)


class PhysicsEntity:


    def __init__(self, x, y, mass=0.1, moment=0, friction=1, elasticity=0.5, body_type=pm.Body.DYNAMIC):
        self.body = pm.Body(mass, moment, body_type)
        self.body.position = x, y
        self.shape = pm.Circle(self.body, 10)
        self.shape.mass = mass
        self.shape.friction = friction
        self.shape.elasticity = elasticity


    def update(self, delta):
        self.position = self.body.position
        self.velocity = self.body.velocity
        self.acceleration = self.body.force / self.body.mass

    def draw(self):
        pass


class Entity:

    def __init__(self, x, y) -> None:
        self.position = np.array([x, y], dtype=np.float32)
        self.velocity = np.array([0, 0], dtype=np.float32)
        self.acceleration = np.array([0, 0], dtype=np.float32)

    def update(self, delta):
        pass

    def draw(self):
        pass

    def delete(self):
        pass

