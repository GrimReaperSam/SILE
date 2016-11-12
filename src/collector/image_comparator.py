import numpy as np

from ..shared import *


class ImageComparator:
    def __init__(self, z_collector):
        self.z_collector = z_collector

    def compare(self, image, keyword):
        z_collection = self.z_collector.collect(keyword)
        for key in z_collection.descriptors:
            description_data = z_collection.descriptors[key]
            if description_data.delta_z > Z_VALUE_THRESHOLD:
                delta, image_description = self._compare_descriptor(image, key, description_data)
                # Delta is positive so we need the highest difference to see if it's worth checking this descriptor
                if delta.max() > DELTA_THRESHOLD:
                    z_times_delta = description_data.descriptor * delta

                    # TODO below
                    #enhance_image(description_data, image_description, image)

    def _compare_descriptor(self, image, key, description_data):
        descriptor = description_data.descriptor
        delta = np.zeros(descriptor.shape)
        image_description = self.z_collector.descriptor_calculator.describe_image(image, key)

        less_than = descriptor >= 0
        delta[less_than] = np.maximum(np.zeros(descriptor.shape), description_data.quantiles[2] - image_description)[less_than]
        delta[~less_than] = np.maximum(np.zeros(descriptor.shape), image_description - description_data.quantiles[0])[~less_than]
        return delta
