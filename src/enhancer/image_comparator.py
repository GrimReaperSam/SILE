from src.descriptors.descriptors import *


class ComparisonItem:
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
    def compare(self, image, z_collection, mask=None):
        delta_list = []
        for descriptor in z_collection.reject('lightness_layout', 'chroma_layout', 'hue_layout', 'details_hist',
                                              'frequency_hist').top(6):
            delta_list.append(ComparisonItem(image, descriptor[0], descriptor[1], mask))
        return sorted(delta_list, key=lambda ci: np.linalg.norm(ci.delta_z), reverse=True)

