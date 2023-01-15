from ursina import Sprite

import random

def create_random_plant():
    r = random.randint(84, 87)
    return Plant(r)

class Plant(Sprite):
    def __init__(self, num, **kwargs):
        super().__init__(
            texture=f'assets1/sprite_0{num}.png',
            scale=(4,4,1),
             **kwargs
        )

        self.shadow = Sprite(
            parent=self,
            texture=f'assets1_shadows/sprite_0{num}.png',
            **kwargs
        )
            
