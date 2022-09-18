from ast import Sub
from dataclasses import dataclass
from typing import List, Tuple
import time

import pygame
import pygame.gfxdraw
import pygame_gui
import pymunk
import pymunk.pygame_util
import numpy as np

from simple_game import SimpleGame


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


if __name__ == "__main__":

    pygame.init()
    pygame.font.init()

    game = SimpleGame()
    game.init()

    while 1:
        game.loop()

    pygame.quit()
    

