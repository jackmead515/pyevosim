
import sqlite3
import pyglet as pg
import pymunk as pm
import numpy as np

from terrian import Terrian
from player import Player
from camera import Camera

class Game:

    def __init__(self) -> None:
        self.window = pg.window.Window(1280, 720)
        self.camera = Camera(self.window, min_zoom=1, max_zoom=4)
        self.terrian = Terrian(
            generate_method='perlin',
            chunk_window_size=3
        )

        self.background = pg.shapes.Rectangle(0, 0, 1280, 720, color=(0,0,0))
        self.background.opacity = 64

        self.player = Player(100.0, 100.0)
        
        #pm.pygame_util.positive_y_is_up = True
        self.space = pm.Space(threaded=True)
        self.space.threads = 4
        self.space.iterations = 1
        self.space.gravity = (0.0, 0.0)


    def init(self):
        #self.window.set_fullscreen(True)
        self.window.activate()
        self.terrian.initalize(self.player.chunk_position)
        self.window.activate()


    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, modifiers)


    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)


    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.set_zoom(scroll_y)


    def on_mouse_motion(self, x, y, dx, dy):
        pass


    def on_mouse_press(self, x, y, button, modifiers):
        # global mouse position
        mx = self.player.position[0] + x - self.window.width // 2
        my = self.player.position[1] + y - self.window.height // 2


    def update(self, delta):
        self.space.step(delta)
        self.player.update(delta)
        self.camera.update(self.player.position)
        self.terrian.update(delta, self.player.chunk_position)


    def draw(self):
        self.window.clear()

        with self.camera:
            self.terrian.draw()
            self.player.draw()