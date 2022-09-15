from dataclasses import dataclass
from typing import List, Tuple

import pygame
import pygame.gfxdraw
import pygame_gui
import pymunk
import pymunk.pygame_util
import numpy as np

from test.creature import Creature


def static_boundaries():
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    l1 = pymunk.Segment(body, (0,0), (1280,0), 2)
    l2 = pymunk.Segment(body, (1280,0), (1280,720), 2)
    l3 = pymunk.Segment(body, (1280,720), (0,720), 2)
    l4 = pymunk.Segment(body, (0,720), (0,0), 2)
    l1.friction = 1
    l2.friction = 1
    l3.friction = 1
    l4.friction = 1
    return body, l1, l2, l3, l4



@dataclass
class GameState:

    screen: pygame.Surface
    ui_manager: pygame_gui.UIManager
    space: pymunk.Space
    space_draw_options: pymunk.pygame_util.DrawOptions
    background: pygame.Surface
    display_size: Tuple
    clock: pygame.time.Clock

    creatures: List[Creature]

    def __init__(self) -> None:

        self.clock = pygame.time.Clock()
        self.display_size = (1280, 720)
        self.background = pygame.Surface(self.display_size)
        self.background.fill(pygame.Color('#000000'))

        pygame.display.set_caption('Evo Simulator')
        
        self.ui_manager = pygame_gui.UIManager(self.display_size)
        self.screen = pygame.display.set_mode(self.display_size)

        self.space_draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space_draw_options.collision_point_color = (0, 255, 0, 255)
        self.space_draw_options.flags = self.space_draw_options.DRAW_COLLISION_POINTS | self.space_draw_options.DRAW_SHAPES

        def draw_circle(pos, angle, radius, outline_color, fill_color):
            pygame.gfxdraw.aacircle(self.screen, int(pos[0]), int(pos[1]), int(radius), fill_color)

        self.space_draw_options.draw_circle = draw_circle

        self.space = pymunk.Space(threaded=True)
        self.space.threads = 4
        self.space.iterations = 2
        self.space.gravity = (0.0, 0.0)

        self.creatures = []
        for i in range(40):
            creature = Creature(i)
            creature.initalize(position=(500, (i+1)*20))
            self.creatures.append(creature)

        for creature in self.creatures:
            creature.add(self.space)

        self.space.add(*static_boundaries())

        hello_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text='Say Hello',
            manager=self.ui_manager
        )