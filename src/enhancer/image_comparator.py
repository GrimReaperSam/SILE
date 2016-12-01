from src.descriptors.descriptors import *


class ImageComparator:
    def compare(self, image, z_collection, mask=None):
        best_descriptor = None
        best_key = ''
        best_delta = None
        best_delta_z = None
        for descriptor in z_collection.reject('lightness_layout', 'chroma_layout', 'hue_layout', 'details_hist',
                                              'frequency_hist').top(3):
            delta = self.compare_descriptor(image, descriptor[0], descriptor[1], mask)
            delta_z = descriptor[1].descriptor * delta
            if best_descriptor is None or np.linalg.norm(best_delta_z) < np.linalg.norm(delta_z):
                best_key = descriptor[0]
                best_descriptor = descriptor[1]
                best_delta = delta
                best_delta_z = delta_z
        return best_key, best_descriptor.descriptor * best_delta

    def compare_descriptor(self, image, key, description_data, mask=None):
        descriptor = description_data.descriptor
        delta = np.zeros(descriptor.shape)
        image_description = DESCRIPTORS[key].compute(image, mask)

        less_than = descriptor >= 0
        delta[less_than] = np.maximum(0, description_data.quantiles[2] - image_description)[less_than]
        delta[~less_than] = np.maximum(0, image_description - description_data.quantiles[0])[~less_than]

        return delta
