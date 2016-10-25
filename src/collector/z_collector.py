import abc
import logging

from ..characteristics.descriptors_calculator import DescriptorsCalculator
from ..characteristics.ranking import ranksum, delta_z


class ZCollector:
    def __init__(self, descriptor_provider, image_provider, z_provider):
        self.image_provider = image_provider
        self.z_provider = z_provider
        self.descriptor_calculator = DescriptorsCalculator(descriptor_provider)

    def collect(self, keyword):
        logging.info('Start computing z-values for %s' % keyword)
        z_values = self.z_provider.provide(keyword)
        if z_values is None:
            z_values = {}
            for key in self.descriptor_calculator.descriptors:
                logging.info('Start computing %s z-values for %s' % (key, keyword))
                positives, negatives = self.image_provider.provide(keyword)
                positive_values = self.descriptor_calculator.describe_set(positives, key)
                negative_values = self.descriptor_calculator.describe_set(negatives, key)
                rank = ranksum(positive_values, negative_values)
                delta = delta_z(rank)
                z_values[key] = {
                    'values': ranksum(positive_values, negative_values),
                    'delta_z': delta
                }
                logging.info('End computing %s z-values for %s' % (key, keyword))
            self.z_provider.save(keyword, z_values)
        logging.info('End computing z-values for %s' % keyword)
        return z_values


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
        :return: A data structure representing the z_values for different characteristics
        """

    @abc.abstractmethod
    def save(self, keyword, z_values_map):
        """

        :param keyword: The tag of the images
        :param z_values_map: A map of descriptor and z_values
        :return:
        """