from src.descriptors.descriptors import *


class ImageComparator:
    def compare(self, image, z_collection, mask=None):
        best_descriptor = None
        best_key = ''
        best_delta = None
        best_importance = 0
        for descriptor in z_collection.reject('lightness_layout', 'chroma_layout', 'hue_layout', 'details_hist',
                                              'frequency_hist').top(5):
            delta, importance = self.compare_descriptor(image, descriptor[0], descriptor[1], mask)

            if best_descriptor is None or importance > best_importance:
                best_key = descriptor[0]
                best_descriptor = descriptor[1]
                best_delta = delta
                best_importance = importance
        return best_key, best_descriptor.descriptor * best_delta

    def compare_descriptor(self, image, key, description_data, mask=None):
        descriptor = description_data.descriptor
        delta = np.zeros(descriptor.shape)
        importance = np.zeros(descriptor.shape)
        image_description = DESCRIPTORS[key].compute(image, mask)

        pos = descriptor >= 0
        delta[pos] = np.maximum(0, description_data.quantiles[3] - image_description)[pos]
        delta[~pos] = np.maximum(0, image_description - description_data.quantiles[1])[~pos]

        # Divide by either q[25%] - q[0%] or q[100%] - q[75%]
        importance[pos] = delta[pos] / (description_data.quantiles[4] - description_data.quantiles[3])[pos]
        importance[~pos] = delta[~pos] / (description_data.quantiles[1] - description_data.quantiles[0])[~pos]

        return delta, importance.sum() / importance.size
