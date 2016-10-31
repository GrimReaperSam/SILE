import abc
import logging
import pickle

import numpy as np

from .ranking import ranksum, delta_z

from ..descriptors.descriptors_calculator import DescriptorsCalculator


class ZCollector:
    def __init__(self, descriptor_provider, image_provider, z_provider):
        self.image_provider = image_provider
        self.z_provider = z_provider
        self.descriptor_calculator = DescriptorsCalculator(descriptor_provider)

    def collect(self, keyword):
        logging.info('Start computing z-values for %s' % keyword)
        positives, negatives = self.image_provider.provide(keyword)
        z_collection = self.z_provider.provide(keyword)

        # Check if need to compute using all the descriptors
        if z_collection is None or z_collection.positive_count != len(positives) or z_collection.negative_count != len(negatives):
            z_collection = ZCollection()
            keys = self.descriptor_calculator.descriptors.keys()
        # Or maybe just a subset of descriptors because the others were computed already
        else:
            keys = [key for key in self.descriptor_calculator.descriptors.keys() if key not in z_collection.descriptors.keys()]

        # If no descriptors needed, skip the calculation
        if len(keys) != 0:
            for key in keys:
                logging.info('Start computing %s z-values for %s' % (key, keyword))
                positive_values = self.descriptor_calculator.describe_set(positives, key)
                negative_values = self.descriptor_calculator.describe_set(negatives, key)
                z_collection.descriptors[key] = DescriptorData(positive_values, negative_values)
                logging.info('End computing %s z-values for %s' % (key, keyword))
            z_collection.positive_count = len(positives)
            z_collection.negative_count = len(negatives)
            self.z_provider.save(keyword, z_collection)
        logging.info('End computing z-values for %s' % keyword)
        return z_collection


class ZCollection:
    def __init__(self):
        self.descriptors = {}

        self.positive_count = 0
        self.negative_count = 0


class DescriptorData:
    def __init__(self, positive_values, negative_values):
        pickle.dump(positive_values, open('positives.pkl', 'wb'))
        pickle.dump(negative_values, open('negatives.pkl', 'wb'))

        rank = ranksum(positive_values, negative_values)
        self.descriptor = rank
        self.delta_z = delta_z(rank)
        self.mean = positive_values.mean(axis=0)
        self.std = positive_values.std(axis=0)
        self.quantiles = np.percentile(positive_values, [25, 50, 75], axis=0)
        self.q9 = np.percentile(positive_values, [10, 20, 30, 40, 50, 60, 70, 80, 90], axis=0)


class ImageProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def provide(self, keyword):
        """
        :param keyword: The tag of the images
        :return: An iterator over the images that have this tag and another
                 over the ones that don't.
        """


class ZProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def provide(self, keyword):
        """
        :param keyword: The tag of the images
        :return: A ZCollection of Z value for different descriptors
        """

    @abc.abstractmethod
    def save(self, keyword, z_collection):
        """

        :param keyword: The tag of the images
        :param z_collection: A ZCollection of Z value for difference descriptors
        :return:
        """