import pyglet as pg

def load_sprite(texture, x, y, batch=None, group=None) -> pg.sprite.Sprite:
    return pg.sprite.Sprite(texture, x, y, batch=batch, group=group)


def load_spritesheet():
    pass


def load_animation():
    pass