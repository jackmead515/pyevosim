from dataclasses import dataclass
from typing import List

import pyglet as pg
import numpy as np

from sprites import load_sprite

@dataclass
class PlantTraits:
    growth_rate: float
    growth_stages: List[int]
    max_offspring: int


plant_stages = [ "seed", "sprout", "vegetative", "flowering", "fruiting" ]
plant_sprites = [
    "assets/plant/sprite_0.png",
    "assets/plant/sprite_1.png",
    "assets/plant/sprite_2.png",
    "assets/plant/sprite_3.png",
    "assets/plant/sprite_4.png",
]


def next_stage(stage):
    return plant_stages[plant_stages.index(stage) + 1]


class Plant():

    def __init__(self, x, y):
        self.position = np.array([x, y])

        self.traits = PlantTraits(
            growth_rate=1,
            max_offspring=10,
            growth_stages=[5, 5, 5, 5, 5]
        )

        self.stage_index = 0
        self.stage = plant_stages[self.stage_index]
        self.age_next_stage = self.traits.growth_stages[self.stage_index]
        self.age_since_stage = 0
        self.age = 0
        self.seedling_radius_range = (10, 20)

        image = pg.image.load(plant_sprites[self.stage_index])
        self.sprite = load_sprite(image, self.position[0], self.position[1])


        # self.sprite = pg.text.Label(
        #     self.stage,
        #     x=self.position[0],
        #     y=self.position[1],
        #     anchor_x='center',
        #     anchor_y='center'
        # )


    def update(self, delta):
        growth = self.traits.growth_rate * delta
        self.age += growth
        self.age_since_stage += growth

        if self.stage_index >= len(self.traits.growth_stages)-1:
            return

        if self.age_since_stage >= self.age_next_stage:
            self.stage_index += 1
            self.age_since_stage = 0
            self.stage = plant_stages[self.stage_index]
            self.age_next_stage = self.traits.growth_stages[self.stage_index]
            self.sprite.text = self.stage

            image = pg.image.load(plant_sprites[self.stage_index])
            self.sprite = load_sprite(image, self.position[0], self.position[1])


    def draw(self):
        self.sprite.draw()


