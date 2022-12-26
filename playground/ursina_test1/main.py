from ursina import *
import pymunk as pm

from player import Player
from test_block import TestBlock
from plant import create_random_plant
from swarm import Swarm


"""
################################
Create the game
################################
"""

space = pm.Space(threaded=True)   
space.gravity = 0,0
space.threads = 4
space.iterations = 1
space.damping = 0.5

app = Ursina()

# add a plane to render the background
plane = Entity(model='quad', color=color.gray, scale=(64,64,1), z=1)

# create blocks of size two next to the player
blocks = []
for i in range(-5, 5):
    b = TestBlock(position=(i*2,4))
    space.add(b.body, b.shape)
    blocks.append(b)

# create and plant some random plants
plants = []
for i in range(20):
    p = create_random_plant()
    p.position = (random.uniform(-10,10), random.uniform(-10,10))
    plants.append(p)

# add a chest
chest = Entity(model='quad', texture='chest', scale=(0.5,0.5,1), position=(0,0), collider='box')

# add a swarm
swarm = Swarm()

player = Player(position=(0,0))
space.add(player.body, player.shape)

def update():
    space.step(time.dt)
    swarm.update()

def input(key):
    pass

camera.orthographic = True
camera.fov = 15
camera.position = (16,18)
camera.add_script(SmoothFollow(target=player, offset=[0,0,-30], speed=4))

window.fps_counter.enabled = True
window.exit_button.visible = True
window.borderless = True
window.fullscreen = False
#window.render_mode = 'wireframe'

app.run()