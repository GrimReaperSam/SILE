from src.descriptors.descriptors import *
from src.shared import *


class ImageComparator:
    def compare(self, image, z_collection):
        best_descriptor = None
        best_key = ''
        best_delta = None
        for descriptor in z_collection.top(5):
            delta = compare_descriptor(image, descriptor[0], descriptor[1])
            if best_descriptor is None or best_delta.max() - best_delta.min() < delta.max() - delta.min():
                best_key = descriptor[0]
                best_descriptor = descriptor[1]
                best_delta = delta
        return best_key, best_descriptor.descriptor * best_delta


def compare_descriptor(image, key, description_data):
    descriptor = description_data.descriptor
    delta = np.zeros(descriptor.shape)
    image_description = DESCRIPTORS[key].compute(image)

    less_than = descriptor >= 0
    delta[less_than] = np.maximum(0, description_data.quantiles[2] - image_description)[less_than]
    delta[~less_than] = np.maximum(0, image_description - description_data.quantiles[0])[~less_than]

    return delta
