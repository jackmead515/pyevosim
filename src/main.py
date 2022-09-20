# from ast import Sub
# from dataclasses import dataclass
# from typing import List, Tuple
# import time

# import pygame
# import pygame.gfxdraw
# import pygame_gui
# import pymunk
# import pymunk.pygame_util
# import numpy as np

# from simple_game import SimpleGame


# def user_input(state: GameState):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             break

#         if event.type == pygame_gui.UI_BUTTON_PRESSED:
#             pass
            
#         state.ui_manager.process_events(event)


# def update_game(delta, state: GameState):
#     state.ui_manager.update(delta)
#     state.space.step(delta)

#     for i, creature in enumerate(state.creatures):
#         x, y = creature.head.body.position
#         vx, vy = creature.head.body.velocity
#         inputs = np.array([x, y, vx, vy])

#         # b = pymunk.Body()
#         # b.position = creature.head.body.position
#         # s = pymunk.Circle(b, radius=50)
#         # for result in state.space.shape_query(s):
#         #     if hasattr(result.shape.body, 'creature_id'):
#         #        if result.shape.body.creature_id != creature.id:
#         #            pass
#         #        print(result.shape.body.position)
        
#         creature.decide(inputs)


# def draw_game(state: GameState):
#     state.screen.blit(state.background, (0, 0))
#     state.ui_manager.draw_ui(state.screen)
#     state.space.debug_draw(state.space_draw_options)
#     pygame.display.update()


# if __name__ == "__main__":

#     pygame.init()
#     pygame.font.init()

#     game = SimpleGame()
#     game.init()

#     while 1:
#         game.loop()

#     pygame.quit()


# self.gui_batch = pg.graphics.Batch()

# depressed = pg.resource.image('assets/nature_tileset/sprite_000.png')
# pressed = pg.resource.image('assets/nature_tileset/sprite_001.png')

# self.button = pg.gui.ToggleButton(100, 400, pressed=pressed, depressed=depressed, batch=self.gui_batch)

# self.frame = pg.gui.Frame(self.window, order=4)
# self.frame.add_widget(self.button)

# img = pg.resource.image('assets/nature_tileset/sprite_005.png')
#         img.anchor_x = img.width // 2
#         img.anchor_y = img.height // 2
#         self.sprite = Sprite(img, x=32, y=32)

import pyglet as pg

from textures import texture_manager
from game import Game

if __name__ == "__main__":

    texture_manager.load()

    game = Game()

    game.init()

    @game.window.event
    def on_draw():
        game.draw()

    @game.window.event
    def on_key_press(symbol, modifiers):
        game.on_key_press(symbol, modifiers)

    @game.window.event
    def on_key_release(symbol, modifiers):
        game.on_key_release(symbol, modifiers)
    
    @game.window.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        print(x, y, scroll_x, scroll_y)
        game.on_mouse_scroll(x, y, scroll_x, scroll_y)

    pg.clock.schedule_interval(game.update, 1 / 30.0)
    pg.app.run()

