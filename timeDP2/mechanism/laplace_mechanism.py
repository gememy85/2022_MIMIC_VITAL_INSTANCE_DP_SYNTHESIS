import numpy as np

def laplace_mechanism(value : float, sensitivity: float, epsilon:float):
    scale = sensitivity/epsilon
    noise = np.random.laplace(0, size=1, scale=scale)
    return value + noise.item()
