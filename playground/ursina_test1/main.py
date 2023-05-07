from ursina import *
from ursina.shaders import lit_with_shadows_shader
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
plane = Entity(
    model='quad',
    color=color.rgb(153, 102, 51),
    scale=(256,256,1),
    z=1,
    shader=lit_with_shadows_shader,
    collider='box'
)

# create blocks of size two next to the player
blocks = []
for i in range(-5, 5):
    b = TestBlock(position=(i*2,4))
    space.add(b.body, b.shape)
    blocks.append(b)

# create and plant some random plants
plants = []
for i in range(20):
    p = create_random_plant(shader=lit_with_shadows_shader)
    p.position = (random.uniform(-10,10), random.uniform(-10,10))
    plants.append(p)

# add a chest
chest = Entity(
    model='quad',
    texture='chest',
    scale=(0.5,0.5,1),
    position=(0,0),
    collider='box',
    shader=lit_with_shadows_shader,
)

# create random trees
trees = []
for i in range(1000):
    n = round(random.uniform(1, 7))
    x, y = random.uniform(-100,100), random.uniform(-100,100)
    #z = random.uniform(-1.01, -1.1)
    trees.append(Entity(
        model='quad',
        texture=f'tree{n}',
        position=(x, y),
        scale=(6, 6, 1),
        shader=lit_with_shadows_shader,
        #z=1,
    ))

# add a swarm
swarm = Swarm()

player = Player(
    position=(0,0),
    shader=lit_with_shadows_shader
)
space.add(player.body, player.shape)

#
light = PointLight(
    color=color.rgb(252, 239, 112),
    z=-30,
    y=100,
    x=100,
    shadows=True,
)
#light.look_at_2d(player)
light.animate_position((-100, -100, -5), duration=10, curve=curve.linear)
#light.animate_position((-100, -100, -1), duration=10, curve=curve.linear)


# add a spot light


# player_light = PointLight(
#     position=player.position,
#     color=color.rgb(252, 229, 112),
#     shadows=True,
# # )
# player_light.add_script(SmoothFollow(
#     target=player,
#     offset=[0,0,-2],
# ))


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