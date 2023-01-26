import numpy as np

def to_rad(degree):
    return degree * np.pi / 180

def to_degree(rad):
    return rad / np.pi * 180