import pyglet as pg
import time

width = 1280
height = 720

window = pg.window.Window(width, height)

batch = pg.graphics.Batch()

pressed = pg.image.load('../assets/ui/buttonSquare_brown_pressed.png')
hover = pg.image.load('../assets/ui/buttonSquare_brown.png')
depressed = pg.image.load('../assets/ui/arrowBlue_left.png') 

button = pg.gui.widgets.PushButton(100, 100, pressed, depressed, hover=hover, batch=batch)

def on_update(dt):
    pass

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    pass

pg.clock.schedule_interval(on_update, 1 / 30.0)

window.activate()

pg.app.run()