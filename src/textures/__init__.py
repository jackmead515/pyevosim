from dataclasses import dataclass
import yaml
import os

from tqdm import tqdm
import pyglet as pg
from pyglet.image import load as load_image

@dataclass
class TextureManager():

    def __init__(self):
        pass

    def load(self):
        texture_map = "assets/texture_map.yml"

        if not os.path.exists(texture_map):
            raise FileNotFoundError(f"Texture map not found: {texture_map}")
        
        with open(texture_map, "r") as f:
            texture_map = yaml.safe_load(f)

        for texture_name in tqdm(texture_map["textures"]):

            texture_path = os.path.join("assets", texture_map["textures"][texture_name])

            if not os.path.exists(texture_path):
                raise FileNotFoundError(f"Texture not found: {texture_path}")

            texture_image = load_image(texture_path)

            setattr(self, texture_name, texture_image)


texture_manager = TextureManager()