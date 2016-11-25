from src.descriptors.descriptors import *
from src.shared import *


class ImageComparator:
    def compare(self, image, z_collection):
        key = 'rgb_hist'
        description_data = z_collection.descriptors[key]
        return enhance_image(image, key, description_data)


def enhance_image(image, key, description_data):
    delta, image_description = compare_descriptor(image, key, description_data)
    # Delta is positive so we need the highest difference to see if it's worth checking this descriptor
    return key, description_data.descriptor * delta


def compare_descriptor(image, key, description_data):
    descriptor = description_data.descriptor
    delta = np.zeros(descriptor.shape)
    image_description = DESCRIPTORS[key].compute(image)

    less_than = descriptor >= 0
    delta[less_than] = np.maximum(0, description_data.quantiles[2] - image_description)[less_than]
    delta[~less_than] = np.maximum(0, image_description - description_data.quantiles[0])[~less_than]

    return delta, image_description
