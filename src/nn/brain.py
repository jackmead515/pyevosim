import random
import sys

sys.path.append('..')

from nn import compute_layers

import numpy as np

activations = [('relu', 1), ('sigmoid', 2), ('softmax', 3)]


def random_brain(inputs, outputs):
    architecture = []

    ra = random.choice(activations)
    hl1 = random.randint(inputs, 50)
    architecture.append((inputs, hl1, ra[1]))

    ra = random.choice(activations)
    hl2 =  random.randint(outputs, hl1)
    architecture.append((hl1, hl2, ra[1]))

    ra = random.choice(activations)
    architecture.append((hl2, outputs, ra[1]))

    return Brain(architecture)


class Brain:

    def __init__(self, architecture):
        """
        architecture: [
            (input_size, hidden_size, activation_function),
        ]
        """
        self.layers = []
        for inputs, outputs, activation in architecture:
            self.layers.append([
                np.array(np.random.rand(inputs, outputs), dtype=np.float32) - 0.5, #weights
                np.array(np.random.rand(1, outputs), dtype=np.float32) - 0.5, #bias
                activation #activation
            ])


    def compute(self, inputs):
        return compute_layers(self.layers, inputs)


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

    inputs = [np.random.random() for i in range(5)]

    print(inputs)

    brain = Brain([
        (5, 50, 'relu'),
        (50, 25, 'sigmoid'),
        (25, 5, 'sigmoid'),
    ])

    outputs = brain.compute(inputs)

    print(outputs)
