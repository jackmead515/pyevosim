import time

import numpy as np
import networkx as nx
import pyglet as pg

from quads.qtree import QTree
from sprites import load_sprite
from textures import texture_manager
import constants as c


class PlantNetwork():

    def __init__(self, x, y, w, h, max_plants) -> None:
        self.graph = nx.Graph()
        self.qtree = QTree(0, 0, w, h, capacity=4)
        self.node_id = 0
        self.max_plants = max_plants
        self.total_plants = 0

        self.batch = pg.graphics.Batch()
        self.plants = {}

        self.last_update = 0


    def init(self, x, y):
        _id = self.add_node(np.array([x, y]), 'tree')
        n = self.get_node(_id)
        pos = n['position']

        s = load_sprite(texture_manager.bush_1, pos[0], pos[1], batch=self.batch)
        self.plants[_id] = s


    def add_node(self, position: np.array, type: str):
        self.graph.add_node(self.node_id, position=position, type=type)
        self.qtree.insert(position)
        self.total_plants += 1
        tmp = self.node_id
        self.node_id += 1
        return tmp


    def add_edge(self, source, target):
        self.graph.add_edge(source, target)


    def get_node(self, id):
        return self.graph.nodes[id]


    def ancestors(self, id, level=1):
        ancestors = []

        for n in self.graph.neighbors(id):
            for level in range(level):
                for n in self.graph.neighbors(n):
                    if n == id:
                        continue
                    ancestors.append(n)

        return ancestors


    def neighbors(self, pos: np.array):
        c = np.array([pos[0], pos[1], 300], dtype=np.float32)
        neighbors = self.qtree.query_circle(c)
        return neighbors


    def germinate(self, id) -> int:
        node = self.get_node(id) 
        pos = node['position']

        # get the total vector of the family nodes
        vectors = []
        for npos in self.neighbors(pos):
            vec = pos - npos
            vectors.append(vec)
        
        # default to a random direction
        uvec = np.random.uniform(-1, 1, size=2)
        
        # if there are neighbors, get the unit vector
        if len(vectors) > 1:
            uvec = sum(vectors)
            uvec /= np.linalg.norm(uvec)

        # get a random unit vector
        rvec = np.random.uniform(-1, 1, size=2)

        # combine both vectors!
        vec = rvec + uvec
        vec /= np.linalg.norm(vec)
        new_pos = pos + (vec * np.random.uniform(50, 100))

        # restrict position to a tile space. makes it look prettier
        new_pos -= new_pos % c.TILE_SIZE

        _id = self.add_node(new_pos, node['type'])
        self.add_edge(id, _id)

        return _id


    def update(self, delta):

        now = time.time()
        elapsed = now - self.last_update
        
        if elapsed > 0.1 and self.total_plants < self.max_plants:
            self.last_update = now
            _id = self.germinate(self.node_id-1)
            n = self.get_node(_id)
            pos = n['position']

            s = load_sprite(texture_manager.bush_1, pos[0], pos[1], batch=self.batch)
            self.plants[_id] = s


    def draw(self):
        self.batch.draw()