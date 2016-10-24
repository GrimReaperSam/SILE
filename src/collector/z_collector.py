import abc
import time

from ..characteristics.descriptors_calculator import DescriptorsCalculator
from ..characteristics.ranking import ranksum, delta_z


class ZCollector:
    def __init__(self, image_provider, z_provider):
        self.image_provider = image_provider
        self.z_provider = z_provider
        self.descriptor_calculator = DescriptorsCalculator()

    def collect(self, keyword):
        if self.z_provider.exists(keyword):
            z_values = self.z_provider.provide(keyword)
        else:
            z_values = {}
            for key in self.descriptor_calculator.descriptors:
                positives, negatives = self.image_provider.provide(keyword)
                positive_values = self.descriptor_calculator.describe_set(positives, key)
                negative_values = self.descriptor_calculator.describe_set(negatives, key)
                rank = ranksum(positive_values, negative_values)
                delta = delta_z(rank)
                z_values[key] = {
                    'values': ranksum(positive_values, negative_values),
                    'delta_z': delta
                }
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
    def exists(self, keyword):
        """
        :param keyword: The tag of the images
        :return: True if the z_values for this keyword are stored and can be recovered
        """
