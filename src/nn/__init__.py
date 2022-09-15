from numba import jit, cuda, njit, prange
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
    if activation == 'sigmoid':
        return sigmoid(x)
    elif activation == 'relu':
        return relu(x)
    elif activation == 'softmax':
        return softmax(x)
    else:
        return x


@cuda.jit(device=True)
def gpu_compute(inputs, weights, bias, activation):
    return do_activation(np.dot(weights, inputs) + bias, activation)


@jit(nopython=True)
def cpu_compute(inputs, weights, bias, activation):
    return do_activation(np.dot(weights, inputs) + bias, activation)


@cuda.jit(cache=True)
def gpu_compute_layers(layers, inputs):
    interm = None
    index = cuda.grid(1)
    if index < len(layers):
        layer = layers[index]
        if index == 0:
            interm = gpu_compute(layer.weights, inputs, layer.bias, layer.activation)
        else:
            interm = gpu_compute(layer.weights, interm, layer.bias, layer.activation)
    return interm


def cpu_compute_layers(layers, inputs):
    inputs /= np.linalg.norm(inputs)
    for index, layer in enumerate(layers):
        if index == 0:
            interm = cpu_compute(inputs, layer[0], layer[1], layer[2])
        else:
            interm = cpu_compute(interm, layer[0], layer[1], layer[2])
    return interm