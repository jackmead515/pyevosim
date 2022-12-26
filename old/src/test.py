import numpy as np
from plant.network import PlantNetwork

if __name__ == "__main__":

    import matplotlib.pyplot as plot

    plant_network = PlantNetwork(-1000, -1000, 1000, 1000)

    _id = plant_network.add_node(np.array([0, 0]), 'tree')

    for _ in range(100):
        _id = plant_network.germinate(_id)
        #_id = plant_network.germinate(_id)

    #print(f'neighbors', plant_network.neighbors(1, level=2))

    for n in plant_network.graph.nodes:
        node = plant_network.get_node(n)
        pos = node['position']
        plot.scatter(pos[0], pos[1], marker='o', color='green')
        plot.annotate(n, (pos[0], pos[1]))
    plot.show()

    # plant_network.add(1, np.array([0, 0]), 'tree')
    # plant_network.add(2, np.array([1, 1]), 'tree')
    # plant_network.add(3, np.array([-1, -1]), 'flower')
    # plant_network.add(4, np.array([-1, 0]), 'flower')

    # plant_network.graph.add_edge(1, 2)
    # plant_network.graph.add_edge(1, 3)
    # plant_network.graph.add_edge(3, 4)

    # for n in plant_network.neighbors(1):
    #     print(plant_network.get_node(n))

   #nx.draw(plant_network.graph, with_labels=True)
    #plot.show()

    print(plant_network.graph)


    # pygame.init()
    # pygame.display.set_caption("TileMap")
    # screen = pygame.display.set_mode((400, 300))
    # clock = pygame.time.Clock()

    # background = pygame.Surface((400, 300))
    # background.fill(pygame.Color('#000000'))

    # tile_map = TileMap(400, 300, 16)
    # tile_map.generate()

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             exit()

    #     screen.blit(background, (0, 0))
    #     tile_map.draw(screen)
    #     pygame.display.update()
    #     clock.tick(30)
