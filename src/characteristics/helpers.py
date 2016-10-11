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

    rows = np.round(np.linspace(1, h + 1, n + 1))
    columns = np.round(np.linspace(1, w + 1, n + 1))

    image[mask] = -1

    for i in range(n):
        for j in range(n):
            patch = image[rows[i]:rows[i+1], columns[j]:columns[j+1]]
            positive = patch[patch >= 0]
            x = np.sum(np.cos(positive))
            y = np.sum(np.sin(positive))
            alpha = np.arctan2(y, x)
            if alpha < 0:
                alpha += 2 * np.pi
                output[i, j] = alpha

    return output


def compute_lightness_blur(image, ss):
    h, w = image.shape
    ss = ss / 100 * np.sqrt(h**2 + w**2)
    ss = np.round(3 * ss)
    return gaussian(image, ss), ss
