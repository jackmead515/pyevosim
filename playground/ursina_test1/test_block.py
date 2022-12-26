from ursina import *
import pymunk as pm

class TestBlock(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='quad',
            scale=(2,2,1),
            texture='white_cube',
             **kwargs
        )
        self.body = pm.Body()
        self.body.position = kwargs.get('position')
        self.body.velocity = (0,0)
        self.body.body_type = pm.Body.DYNAMIC

        self.shape = pm.Poly.create_box(self.body, size=(2,2))
        self.shape.mass = 2000
        self.shape.friction = 1
        self.shape.elasticity = 0

    def update(self):
        self.x = self.body.position[0]
        self.y = self.body.position[1]