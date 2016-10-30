import numpy as np


class ImageComparator:
    def __init__(self, z_collector):
        self.z_collector = z_collector

    def compare(self, image, keyword):
        z_collection = self.z_collector.collect(keyword)
        for key in z_collection.descriptors:
            delta = self.compare_descriptor(image, key, z_collection[key])
            print(delta)

    def compare_descriptor(self, image, key, description):
        delta = np.zeros(description.shape)
        image_description = self.z_collector.descriptor_calculator.describe_image(image, key)

        less_than = description >= 0
        delta[less_than] = np.max(np.zeros(description.shape), description.quantiles[2] - image_description)
        delta[~less_than] = np.max(np.zeros(description.shape), image_description - description.quantiles[0])
        return delta
