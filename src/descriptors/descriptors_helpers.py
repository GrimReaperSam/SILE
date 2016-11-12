import numpy as np
from skimage.filters import gaussian


def sample8x8(image):
    n = 8
    h, w = image.shape
    output = np.zeros((n, n))

    rows = np.linspace(1, h + 1, n + 1, dtype=np.int16)
    columns = np.linspace(1, w + 1, n + 1, dtype=np.int16)

    for i in range(n):
        for j in range(n):
            output[i, j] = np.mean(image[rows[i]:rows[i+1], columns[j]:columns[j+1]])

    return output


def hue_sample8x8(image, mask):
    n = 8
    h, w, = image.shape
    output = np.zeros((n, n))

    rows = np.linspace(1, h + 1, n + 1, dtype=np.int16)
    columns = np.linspace(1, w + 1, n + 1, dtype=np.int16)

    image = image / 180 * np.pi
    image[~mask] = -1

    for i in range(n):
        for j in range(n):
            patch = image[rows[i]:rows[i+1], columns[j]:columns[j+1]]
            positive = patch[patch >= 0]
            x = np.cos(positive).sum()
            y = np.sin(positive).sum()
            alpha = 180 / np.pi * np.arctan2(y, x)
            if alpha < 0:
                alpha += 360
            output[i, j] = alpha

    return output


def compute_lightness_blur(image, ss):
    h, w = image.shape
    ss = ss / 100 * np.sqrt(h**2 + w**2)
    ss = np.rint(3 * ss).astype(np.int8)
    return gaussian(image, ss), ss


def compute_gabor_kernel(size, frequency, theta):
    gy, gx = np.mgrid[-size:size+1, -size:size+1]
    rot = np.exp(2j*np.pi*frequency*(gx*np.cos(-theta) + gy*np.sin(-theta)))
    g = np.multiply(np.exp(-2*(gx**2 + gy**2)/size**2), rot)
    g = np.real(g)
    return g / np.sum(g)
