from numba import jit
import numpy as np


@jit(nopython=True, fastmath=True)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


@jit(nopython=True, fastmath=True)
def relu(x):
    return np.maximum(0, x)


@jit(nopython=True, fastmath=True)
def softmax(x):
    expo = np.exp(x)
    return expo / np.sum(expo)


@jit(nopython=True)
def do_activation(x, activation):
    if activation == 1:
        return sigmoid(x)
    elif activation == 2:
        return relu(x)
    elif activation == 3:
        return softmax(x)
    else:
        return x


@jit(nopython=True)
def compute(inputs, weights, bias, activation):
    return do_activation(np.dot(inputs, weights) + bias, activation)


def compute_layers(layers, inputs):
    inputs /= np.linalg.norm(inputs)
    interm = None
    for index, layer in enumerate(layers):
        if index == 0:
            interm = compute(inputs, layer[0], layer[1], layer[2])
        else:
            interm = compute(interm, layer[0], layer[1], layer[2])
    return interm