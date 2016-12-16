import abc
import logging
from copy import deepcopy

import numpy as np

from src.collector.ranking import ranksum, delta_z
from src.descriptors.descriptors import DESCRIPTORS
from src.descriptors.descriptors_calculator import DescriptorsCalculator
from src.filesystem.flicker_reader import FlickerDB


class ZCollector:
    def __init__(self, descriptor_provider, z_provider):
        self.flicker_db = FlickerDB()
        self.descriptor_calculator = DescriptorsCalculator(descriptor_provider)
        self.z_provider = z_provider

    def collect(self, keyword, local=False):
        logging.info('Start computing z-values for %s' % keyword)
        positives, negatives = self.flicker_db.ids_by_tag(keyword)
        z_collection = self.z_provider.provide(keyword, local)

        # Check if need to compute using all the descriptors
        if z_collection is None or z_collection.positive_count != len(positives) or z_collection.negative_count != len(negatives):
            z_collection = ZCollection(keyword)
            keys = DESCRIPTORS.keys()
        # Or maybe just a subset of descriptors because the others were computed already
        else:
            keys = [key for key in DESCRIPTORS.keys() if key not in z_collection.descriptors.keys()]

        # If no descriptors needed, skip the calculation
        if len(keys) != 0:
            for key in keys:
                logging.info('Start computing %s z-values for %s' % (key, keyword))
                descriptions = self.descriptor_calculator.describe_set(self.flicker_db.all_ids(), key)
                z_collection.descriptors[key] = DescriptorData(key, descriptions, positives - 1, negatives - 1)
                logging.info('End computing %s z-values for %s' % (key, keyword))
            z_collection.positive_count = len(positives)
            z_collection.negative_count = len(negatives)
            self.z_provider.save(keyword, z_collection, local)
        logging.info('End computing z-values for %s' % keyword)
        return z_collection


class ZCollection:
    def __init__(self, keyword):
        self.keyword = keyword
        self.descriptors = {}

        self.positive_count = 0
        self.negative_count = 0

    def allow(self, *args):
        """
        :param args: The keywords to allow
        :return: A ZCollection with only the allowed keys
        """
        new_z_col = deepcopy(self)
        new_z_col.descriptors = {}
        for key in args:
            new_z_col.descriptors[key] = deepcopy(self.descriptors[key])
        return new_z_col

    def reject(self, *args):
        """
        :param args: The keywords to reject
        :return: A ZCollection without the keys provided
        """
        new_z_col = deepcopy(self)
        for key in args:
            new_z_col.descriptors.pop(key, None)
        return new_z_col

    def top(self, n):
        """
        :param n the number of top descriptors ranked by z-values
        :return The top n descriptors in this keyword's z_collection
        """
        sorted_descriptors = sorted(self.descriptors.items(), key=lambda item: item[1].delta_z, reverse=True)
        return sorted_descriptors[:n]

    def __repr__(self):
        result = 'ZCollection for %s: \n' % self.keyword
        result += 'Positives %s, Negatives: %s\n' % (self.positive_count, self.negative_count)
        result += 'Descriptors: \n'
        for key in self.descriptors:
            result += 'Descriptor %s:\n' % key
            result += repr(self.descriptors[key])
        return result


class DescriptorData:
    def __init__(self, key, descriptions, positive_indices, negative_indices):
        self.descriptor = ranksum(key, descriptions, positive_indices, negative_indices)
        self.delta_z = delta_z(self.descriptor)

        self.mean = descriptions[positive_indices].mean(axis=0)
        self.std = descriptions[positive_indices].std(axis=0)
        self.quantiles = np.percentile(descriptions[positive_indices], [0, 25, 50, 75, 100], axis=0)
        self.q9 = np.percentile(descriptions[positive_indices], [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], axis=0)

    def __repr__(self):
        return 'Delta Z*: %s\n' % self.delta_z


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
    def provide(self, keyword, local=False):
        """
        :param keyword: The tag of the images
        :param local: Whether the z-values are calculated locally or globally
        :return: A ZCollection of Z value for different descriptors
        """

    @abc.abstractmethod
    def save(self, keyword, z_collection, local=False):
        """

        :param keyword: The tag of the images
        :param z_collection: A ZCollection of Z value for difference descriptors
        :param local: Whether the z-values are calculated locally or globally
        :return:
        """