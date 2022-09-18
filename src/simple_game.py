from typing import Tuple


import pygame
import pygame.gfxdraw
import pygame_gui
import pymunk
import pymunk.pygame_util
import numpy as np

from swarm import Swarm
from player import Player
from tiles.tile import TileMap
from camera import Camera2D
from terrian import Terrian
import constants

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
        self.background = pygame.Surface((constants.WORLD_CHUNK_SIZE, constants.WORLD_CHUNK_SIZE))
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

        self.swarm = Swarm(1000)
        
        self.terrian = Terrian(generate_method='perlin')

        #self.tile_map = TileMap(self.display_size[0], self.display_size[1], 16)

        self.player = Player(self.display_size[0]/2, self.display_size[1]/2)
        self.camera = Camera2D(0.0, 0.0)

        # self.gl_context = mgl.create_context(standalone=True)
        # self.gl_context.enable(mgl.BLEND)
        # ModernGLGroup.gl_context = self.gl_context

        # self.gl_group = ModernGLGroup([Particle(100.0, 100.0, 50.0, 50.0, (255, 0, 0))])

    
    def init(self):
        print('init')
        self.terrian.generate_chunks(np.array([1, 1]))
        #self.tile_map.random()
        print('init complete')


    def loop(self):
        self.input()
        self.update()
        self.draw()


    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                pass
        
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.camera.velocity[1] = 5.0
                    self.player.velocity[1] = -5.0
                elif event.key == pygame.K_s:
                    self.camera.velocity[1] = -5.0
                    self.player.velocity[1] = 5.0
                elif event.key == pygame.K_a:
                    self.camera.velocity[0] = 5.0
                    self.player.velocity[0] = -5.0
                elif event.key == pygame.K_d:
                    self.camera.velocity[0] = -5.0
                    self.player.velocity[0] = 5.0
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.camera.velocity[1] = 0.0
                    self.player.velocity[1] = 0.0
                elif event.key == pygame.K_s:
                    self.camera.velocity[1] = 0.0
                    self.player.velocity[1] = 0.0
                elif event.key == pygame.K_a:
                    self.camera.velocity[0] = 0.0
                    self.player.velocity[0] = 0.0
                elif event.key == pygame.K_d:
                    self.camera.velocity[0] = 0.0
                    self.player.velocity[0] = 0.0
    
            self.ui_manager.process_events(event)


    def update(self) -> None:
        self.current_fps = self.clock.tick(self.target_fps)
        self.delta = 1 - (self.current_fps / 1000.0)
        #self.space.step(self.delta)
        #self.ui_manager.update(self.delta)
        #self.swarm.update(self.delta)
        self.player.update(self.delta)
        #self.tile_map.update(self.delta)
        self.camera.update(self.delta)

        if self.player.changed_chunk():
            self.player.previous_chunk_position = self.player.chunk_position
            self.terrian.generate_chunks(self.player.chunk_position)


    def draw(self) -> None:
        self.screen.fill((0, 0, 0))
        #self.background.fill((0, 0, 0))

        self.terrian.draw(self.background)
        #self.tile_map.draw(self.background)
        #grid.draw_grid(self.screen, self.display_size[0], self.display_size[1], 16, (0, 0, 255))
        #self.ui_manager.draw_ui(self.background)
        #self.space.debug_draw(self.space_draw_options)
        #self.swarm.draw(self.background)
        self.player.draw(self.background)

        self.screen.blit(self.background, (self.camera.position[0], self.camera.position[1]))

        text = self.font.render(f'FPS: {self.current_fps}', True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        text = self.font.render(f'Chunk: {self.player.chunk_position}', True, (255, 255, 255))
        self.screen.blit(text, (10, 20))

        pygame.display.flip()

