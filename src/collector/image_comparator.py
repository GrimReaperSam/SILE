from scipy.interpolate import interp1d

from ..descriptors.descriptors import *
from ..shared import *


class ImageComparator:
    def __init__(self, z_collection):
        self.z_collection = z_collection

    def compare(self, image, s):
        images = {}
        for key in ['gray_hist', 'chroma_hist', 'hue_angle_hist', 'rgb_hist']:
            description_data = self.z_collection.descriptors[key]
            if description_data.delta_z > Z_VALUE_THRESHOLD:
                images[key] = enhance_image(image, key, description_data, s)
            else:
                images[key] = image
        return images


def enhance_image(image, key, description_data, s):
    delta, image_description = compare_descriptor(image, key, description_data)
    # Delta is positive so we need the highest difference to see if it's worth checking this descriptor
    if delta.max() > DELTA_THRESHOLD:
        z_delta = description_data.descriptor * delta
        return transfer(image, key, z_delta, s)
    return image


def compare_descriptor(image, key, description_data):
    descriptor = description_data.descriptor
    delta = np.zeros(descriptor.shape)
    image_description = DESCRIPTORS[key].compute(image)

    less_than = descriptor >= 0
    delta[less_than] = np.maximum(0, description_data.quantiles[2] - image_description)[less_than]
    delta[~less_than] = np.maximum(0, image_description - description_data.quantiles[0])[~less_than]

    return delta, image_description


def transfer(image, key, z_delta, s):
    if key == 'gray_hist':
        transfer_function = interp1d(*make_transfer(key, s, z_delta), fill_value='extrapolate')
        return transfer_function(image / 255).astype(np.uint8)
    elif key == 'chroma_hist':
        transfer_function = interp1d(*make_transfer(key, s, z_delta), fill_value='extrapolate')
        lch = lab_to_lch(rgb_to_lab(image))
        lch[..., 1] = transfer_function(lch[..., 1] / 80)
        return lab_to_rgb(lch_to_lab(lch))
    elif key == 'hue_angle_hist':
        transfer_function = interp1d(*make_transfer(key, s, z_delta), fill_value='extrapolate')
        lch = lab_to_lch(rgb_to_lab(image))
        lch[..., 2] = transfer_function(lch[..., 2] / 360)
        return lab_to_rgb(lch_to_lab(lch))
    elif key == 'rgb_hist':
        rgb = np.empty(image.shape)
        # Red
        zr = z_delta.sum(axis=(1, 2))
        f = interp1d(*make_transfer(key, s, zr), fill_value='extrapolate')
        rgb[..., 0] = f(image[..., 0] / 255)
        # Green
        zg = z_delta.sum(axis=(0, 2))
        f = interp1d(*make_transfer(key, s, zg), fill_value='extrapolate')
        rgb[..., 1] = f(image[..., 1] / 255)
        # Blue
        zb = z_delta.sum(axis=(0, 1))
        f = interp1d(*make_transfer(key, s, zb), fill_value='extrapolate')
        rgb[..., 2] = f(image[..., 2] / 255)
        return rgb.astype(np.uint8)


def make_transfer(key, s, zd):
    s_max = 5

    if key == 'gray_hist':
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 255)
    elif key == 'chroma_hist':
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 80)
    elif key == 'hue_angle_hist':
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 360)
    elif key == 'rgb_hist':
        bin_centers = np.linspace(1 / 16, 15 / 16, 8)
        x2 = np.linspace(0, 1, 255)

    f_derivative = interp1d(bin_centers, s * zd, fill_value='extrapolate')

    slopes = f_derivative(x2)
    slopes[slopes >= 0] = 1 / (1 + s * slopes[slopes >= 0])
    slopes[slopes < 0] = 1 + np.abs(slopes[slopes < 0])

    slopes[slopes > s_max] = s_max
    slopes[slopes < 1 / s_max] = 1 / s_max

    mmap = np.cumsum(slopes)
    mmap -= mmap.min()
    mmap = mmap / mmap.max()

    if key == 'gray_hist':
        return x2, mmap * 255
    elif key == 'chroma_hist':
        return x2, mmap * 80
    elif key == 'hue_angle_hist':
        return x2, mmap * 360
    elif key == 'rgb_hist':
        return x2, mmap * 255
