import pyglet as pg
import numpy as np


class Camera:
    """ A simple 2D camera that contains the speed and offset."""

    def __init__(self, window: pg.window.Window, min_zoom=1, max_zoom=3):
        assert min_zoom <= max_zoom, "Minimum zoom must not be greater than maximum zoom"
        self._window = window
        self.max_zoom = max_zoom
        self.min_zoom = min_zoom
        self.scroll_speed = 0.1
        self.position = np.array([0.0, 0.0])
        self._zoom = max(min(1, self.max_zoom), self.min_zoom)


    def set_zoom(self, value):
        """ Here we set zoom, clamp value to minimum of min_zoom and max of max_zoom."""
        zoom = self._zoom + value * self.scroll_speed
        self._zoom = max(min(zoom, self.max_zoom), self.min_zoom)


    def update(self, player_position):
        self.position[0] = player_position[0] - (self._window.width / 2)
        self.position[1] = player_position[1] - (self._window.height / 2)


    def begin(self):

        x = (self.position[0] / self._zoom) + self._zoom
        y = (self.position[1] / self._zoom) + self._zoom

        #x = self.position[0] * self._zoom
        #y = self.position[1] * self._zoom

        view_matrix = self._window.view.translate((-x, -y, 0))

        view_matrix = view_matrix.scale((self._zoom, self._zoom, 1))

        self._window.view = view_matrix


    def end(self):

        x = (self.position[0] / self._zoom) + self._zoom
        y = (self.position[1] / self._zoom) + self._zoom

        # x = self.position[0] * self._zoom
        # y = self.position[1] * self._zoom

        view_matrix = self._window.view.scale((1 / self._zoom, 1 / self._zoom, 1))

        view_matrix = view_matrix.translate((x, y, 0))

        self._window.view = view_matrix


    def __enter__(self):
        self.begin()


    def __exit__(self, exception_type, exception_value, traceback):
        self.end()


class CenteredCamera(Camera):
    """A simple 2D camera class. 0, 0 will be the center of the screen, as opposed to the bottom left."""

    def begin(self):
        x = -self._window.width // 2 / self._zoom + self.offset_x
        y = -self._window.height // 2 / self._zoom + self.offset_y

        view_matrix = self._window.view.translate((-x * self._zoom, -y * self._zoom, 0))
        view_matrix = view_matrix.scale((self._zoom, self._zoom, 1))
        self._window.view = view_matrix

    def end(self):
        x = -self._window.width // 2 / self._zoom + self.offset_x
        y = -self._window.height // 2 / self._zoom + self.offset_y

        view_matrix = self._window.view.scale((1 / self._zoom, 1 / self._zoom, 1))
        view_matrix = view_matrix.translate((x * self._zoom, y * self._zoom, 0))
        self._window.view = view_matrix