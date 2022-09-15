from dataclasses import dataclass
import time
import random
from multiprocessing import Pool
from concurrent.futures import ThreadPoolExecutor

from nn import gpu_compute_layers, cpu_compute_layers

import numpy as np

class Brain:

    def __init__(self, architecture):
        self.layers = []
        for inputs, outputs, activation in architecture:
            self.layers.append([
                np.random.rand(outputs, inputs), #weights
                np.random.rand(outputs, 1), #bias
                activation #activation
            ])


    def compute(self, inputs):
        # threads = 32
        # nblocks = (len(self.layers) // threads) + 1
        # config = (nblocks), (threads)
        # return gpu_compute_layers[config](self.layers, inputs)

        return cpu_compute_layers(self.layers, inputs)


    def evolve(self):
        for x, layer in enumerate(self.layers):
            # shift from 0,1 to 0,2 then to -1,1, then to -.5,.5
            nudge = ((np.random.rand(*layer[0].shape)*2) - 1) / 2
            layer[0] += nudge
            layer[0] = np.clip(layer[0], 0, 1)
            self.layers[x] = layer


    def code(self):
        codes = []
        for layer in self.layers:
            ws = layer[0].shape
            bs = layer[1].shape

            a = np.average(layer[0])
            s = layer[0].sum()
            b = layer[1].sum()
            sd = np.std(layer[0])

            m = ws[0]*ws[1] + bs[0]*bs[1] + 1 + 1
            t = s + b + sd + a

            codes.append(round(((t / m) * (90 - 65)) + 65))
        return codes


if __name__ == "__main__":


    inputs = np.zeros((100, 1))

    brain = Brain([
        (100, 50, 'relu'),
        (50, 25, 'sigmoid'),
        (25, 5, 'softmax')
    ])

    for i in range(100):
        choices = brain.compute(inputs)
        select = np.argmax(choices)
        print(choices, select)
        brain.evolve()
    exit()

    brains = []
    for i in range(100):
        brain = Brain([
            (100, 50, 'relu'),
            (50, 25, 'sigmoid'),
            (25, 5, 'softmax')
        ])
        brains.append(brain)

    averages = np.zeros(1000)
    start_time = time.time()
    for i in range(1000):
       start = time.time()
       for brain in brains:
           select = np.argmax(brain.compute(inputs))
       averages[i] = time.time() - start

    print('total', time.time() - start_time)
    print('avg', np.average(averages))

    for i in range(10000):
       print([chr(c) for c in brains[0].code()])
       brains[0].evolve()
