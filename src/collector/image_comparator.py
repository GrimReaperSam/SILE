import numpy as np

from scipy.interpolate import interp1d

from ..descriptors.descriptors import *
from ..shared import *


class ImageComparator:
    def __init__(self, z_collection):
        self.z_collection = z_collection

    def compare(self, image, s):
        for key in ['gray_hist']:
            description_data = self.z_collection.descriptors[key]
            if description_data.delta_z > Z_VALUE_THRESHOLD:
                return enhance_image(image, key, description_data, s)
        return image


def enhance_image(image, key, description_data, s):
    delta, image_description = compare_descriptor(image, key, description_data)
    # Delta is positive so we need the highest difference to see if it's worth checking this descriptor
    if delta.max() > DELTA_THRESHOLD:
        z_delta = description_data.descriptor * delta
        return transfer(image, z_delta, s)
    return image


def compare_descriptor(image, key, description_data):
    descriptor = description_data.descriptor
    delta = np.zeros(descriptor.shape)
    image_description = DESCRIPTORS[key].compute(image)

    less_than = descriptor >= 0
    delta[less_than] = np.maximum(0, description_data.quantiles[2] - image_description)[less_than]
    delta[~less_than] = np.maximum(0, image_description - description_data.quantiles[0])[~less_than]

    return delta, image_description


def transfer(image, z_delta, s):
    transfer_function = interp1d(*make_transfer(s, z_delta), fill_value='extrapolate')
    return transfer_function(image / 255).astype(np.uint8)


def make_transfer(s, zd):
    s_max = 5

    f_derivative = interp1d(np.linspace(1 / 32, 31 / 32, 16), s * zd, fill_value='extrapolate')

    x2 = np.linspace(0, 1, 255)
    slopes = f_derivative(x2)
    slopes[slopes >= 0] = 1 / (1 + s * slopes[slopes >= 0])
    slopes[slopes < 0] = 1 + np.abs(slopes[slopes < 0])

    slopes[slopes > s_max] = s_max
    slopes[slopes < 1 / s_max] = 1 / s_max

    mmap = np.cumsum(slopes)
    mmap -= mmap.min()
    mmap = mmap / mmap.max() * 255
    return x2, mmap
