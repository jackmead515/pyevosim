from typing import Tuple

import pygame
import pygame.gfxdraw
import pygame_gui
import pymunk
import pymunk.pygame_util

from swarm import Swarm
from player import Player
from swarm.util import B
from tiles.tile import TileMap
import grid

class SimpleGame:

    screen: pygame.Surface
    ui_manager: pygame_gui.UIManager
    space: pymunk.Space
    space_draw_options: pymunk.pygame_util.DrawOptions
    background: pygame.Surface
    display_size: Tuple
    clock: pygame.time.Clock

    def __init__(self) -> None:

        self.clock = pygame.time.Clock()
        self.display_size = (1280, 720)
        self.background = pygame.Surface(self.display_size)
        self.background.fill(pygame.Color('#000000'))

        pygame.display.set_caption('Evo Simulator')
        
        self.ui_manager = pygame_gui.UIManager(self.display_size)
        self.screen = pygame.display.set_mode(self.display_size, pygame.DOUBLEBUF)

        self.space_draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.space_draw_options.collision_point_color = (0, 255, 0, 255)
        self.space_draw_options.flags = self.space_draw_options.DRAW_COLLISION_POINTS 
        self.space_draw_options.flags |= self.space_draw_options.DRAW_SHAPES
        
        pymunk.pygame_util.positive_y_is_up = True

        self.space = pymunk.Space(threaded=True)
        self.space.threads = 4
        self.space.iterations = 2
        self.space.gravity = (0.0, 0.0)

        self.font = pygame.font.SysFont(None, 12)

        self.target_fps = 30.0
        self.current_fps = 0.0
        self.delta = 0.0

        self.swarm = Swarm(100)
        self.player = Player(100, 100)
        self.tile_map = TileMap(self.display_size[0], self.display_size[1], 16)

        # self.gl_context = mgl.create_context(standalone=True)
        # self.gl_context.enable(mgl.BLEND)
        # ModernGLGroup.gl_context = self.gl_context

        # self.gl_group = ModernGLGroup([Particle(100.0, 100.0, 50.0, 50.0, (255, 0, 0))])

    
    def init(self):
        print('init')
        self.tile_map.generate()
        print('init complete')


    def loop(self):
        self.input()
        self.update()
        self.draw()


    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                pass
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.player.velocity.y = -5
                elif event.key == pygame.K_s:
                    self.player.velocity.y = 5
                elif event.key == pygame.K_a:
                    self.player.velocity.x = -5
                elif event.key == pygame.K_d:
                    self.player.velocity.x = 5
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.velocity.y = 0
                elif event.key == pygame.K_s:
                    self.player.velocity.y = 0
                elif event.key == pygame.K_a:
                    self.player.velocity.x = 0
                elif event.key == pygame.K_d:
                    self.player.velocity.x = 0
    
            self.ui_manager.process_events(event)


    def update(self) -> None:
        self.current_fps = self.clock.tick(self.target_fps)
        self.delta = 1 - (self.current_fps / 1000.0)
        self.space.step(self.delta)
        self.ui_manager.update(self.delta)
        self.swarm.update(self.delta)
        self.player.update(self.delta)
        self.tile_map.update(self.delta)


    def draw(self) -> None:
        self.screen.blit(self.background, (0, 0))
        self.tile_map.draw(self.screen)
        #grid.draw_grid(self.screen, self.display_size[0], self.display_size[1], 16, (0, 0, 255))
        self.ui_manager.draw_ui(self.screen)
        #self.space.debug_draw(self.space_draw_options)
        self.swarm.draw(self.screen)
        self.player.draw(self.screen)

        text = self.font.render(f'FPS: {self.current_fps:.2f}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        pygame.display.update()

