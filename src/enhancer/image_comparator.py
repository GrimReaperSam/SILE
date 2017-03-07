from src.descriptors.descriptors import *


class ComparisonItem:
    """
        Contains the result of a comparison between an image and a z-value
        :key is the name of the descriptor used for comparing
        :description_data is the loaded data containing the z-values as well as some statistics of
        the images tagged with `key`
        :mask is a comparison mask that can be used to do local comparison
        :delta is the comparison result between the image's descriptors and all other images
        :delta_z is the product of delta and the z-values
    """
    def __init__(self, image, key, description_data, mask=None):
        self.key = key
        self.description_data = description_data
        self.mask = mask
        self.delta = None
        self.delta_z = None
        self.build(image)

    def build(self, image):
        descriptor = self.description_data.descriptor
        delta = np.zeros(descriptor.shape)
        image_description = DESCRIPTORS[self.key].compute(image, self.mask)

        pos = descriptor >= 0
        delta[pos] = np.maximum(0, self.description_data.quantiles[3] - image_description)[pos]
        delta[~pos] = np.maximum(0, image_description - self.description_data.quantiles[1])[~pos]

        self.delta = delta
        self.delta_z = descriptor * delta


class ImageComparator:
    """
        Utilities for comparing an image and a z-values collection (multiple descriptors)
    """
    def compare_single(self, image, z_collection, key, mask=None):
        return ComparisonItem(image, key, z_collection.descriptors[key], mask)

    def compare(self, image, z_collection, mask=None):
        delta_list = []
        for descriptor in z_collection.reject('lightness_layout', 'chroma_layout', 'hue_layout', 'details_hist',
                                              'frequency_hist').top(6):
            delta_list.append(ComparisonItem(image, descriptor[0], descriptor[1], mask))
        return sorted(delta_list, key=lambda ci: np.linalg.norm(ci.delta_z), reverse=True)

