import pyglet as pg
from pyglet.sprite import Sprite

from terrian import Terrian
from sprites import load_sprite
from player import Player
from camera import Camera
from swarm import Swarm

class Game:

    def __init__(self) -> None:
        self.window = pg.window.Window(1280, 720)

        self.terrian = Terrian(
            generate_method='perlin',
            chunk_window_size=3
        )
        self.player = Player(100.0, 100.0)
        self.swarm = Swarm(1000)
        self.camera = Camera(self.window, min_zoom=1, max_zoom=4)


    def init(self):
        self.window.activate()
        self.terrian.chunk_position = self.player.chunk_position
        self.terrian.generate_chunks(self.player.chunk_position)


    def on_key_press(self, key, modifiers):
        self.player.on_key_press(key, modifiers)


    def on_key_release(self, key, modifiers):
        self.player.on_key_release(key, modifiers)

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        self.camera.set_zoom(scroll_y)


    def on_mouse_press(self, x, y, button, modifiers):
        pass


    def update(self, delta):
        self.player.update(delta)
        self.swarm.update(delta)
        self.camera.update(self.player.position)
        self.terrian.update(self.player.chunk_position)


    def draw(self):
        self.window.clear()

        with self.camera:
            self.terrian.draw()
            self.player.draw()
            self.swarm.draw()