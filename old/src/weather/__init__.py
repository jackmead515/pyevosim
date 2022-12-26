import pyglet as pg

from sprites import load_sprite
from textures import texture_manager

class Weather():

    def __init__(self) -> None:
        pass


class Rain(Weather):

    def __init__(self) -> None:
        super().__init__()
        self.batch = pg.graphics.Batch()

        self.sprites = []
        for i in range(100):
            self.sprites.append(
                load_sprite(
                    pg.shapes.Circle()
                )
            )


    def update(self, dt: float) -> None:
        pass


    def draw(self) -> None:
        pass