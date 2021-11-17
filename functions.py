import math

def sigmoid(x):
    return 1.0/(1.0+math.exp(-x))

def sigmoid_prime(x):
    return sigmoid(x)*(1.0-sigmoid(x))

def alpha_decay(x):
    return .99*x