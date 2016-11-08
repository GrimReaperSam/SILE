import abc
import logging

import numpy as np

from .ranking import ranksum, delta_z

from ..descriptors.descriptors_calculator import DescriptorsCalculator
from ..filesystem.flicker_reader import FlickerDB
from ..filesystem.config_paths import collections_from_descriptor


class ZCollector:
    def __init__(self, descriptor_provider, z_provider):
        self.flicker_db = FlickerDB()
        self.descriptor_calculator = DescriptorsCalculator(descriptor_provider)
        self.z_provider = z_provider

    def collect(self, keyword):
        logging.info('Start computing z-values for %s' % keyword)
        positives, negatives = self.flicker_db.ids_by_tag(keyword)
        z_collection = self.z_provider.provide(keyword)

        # Check if need to compute using all the descriptors
        if z_collection is None or z_collection.positive_count != len(positives) or z_collection.negative_count != len(negatives):
            z_collection = ZCollection(keyword)
            keys = self.descriptor_calculator.descriptors.keys()
        # Or maybe just a subset of descriptors because the others were computed already
        else:
            keys = [key for key in self.descriptor_calculator.descriptors.keys() if key not in z_collection.descriptors.keys()]

        # If no descriptors needed, skip the calculation
        if len(keys) != 0:
            for key in keys:
                logging.info('Start computing %s z-values for %s' % (key, keyword))
                descriptions = self.descriptor_calculator.describe_set(self.flicker_db.all_ids(), key)
                z_collection.descriptors[key] = DescriptorData(descriptions, positives - 1, negatives - 1)
                logging.info('End computing %s z-values for %s' % (key, keyword))
            z_collection.positive_count = len(positives)
            z_collection.negative_count = len(negatives)
            self.z_provider.save(keyword, z_collection)
        logging.info('End computing z-values for %s' % keyword)
        return z_collection


class ZCollection:
    def __init__(self, keyword):
        self.keyword = keyword
        self.descriptors = {}

        self.positive_count = 0
        self.negative_count = 0

    def __repr__(self):
        result = 'ZCollection for %s: \n' % self.keyword
        result += 'Positives %s, Negatives: %s\n' % (self.positive_count, self.negative_count)
        result += 'Descriptors: \n'
        for key in self.descriptors:
            result += 'Descriptor %s:\n' % key
            result += repr(self.descriptors[key])
        return result


class DescriptorData:
    def __init__(self, descriptions, positive_indices, negative_indices):
        self.descriptor = ranksum(descriptions, positive_indices, negative_indices)
        self.delta_z = delta_z(self.descriptor)

        self.mean = descriptions[positive_indices].mean(axis=0)
        self.std = descriptions[positive_indices].std(axis=0)
        self.quantiles = np.percentile(descriptions[positive_indices], [25, 50, 75], axis=0)
        self.q9 = np.percentile(descriptions[positive_indices], [10, 20, 30, 40, 50, 60, 70, 80, 90], axis=0)

    def __repr__(self):
        result = 'Z*-values: %s\n' % self.descriptor
        result += 'Delta Z*: %s\n' % self.delta_z
        return result


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