import abc

class ZCollector:
    def __init__(self, image_provider, z_provider):
        self.image_provider = image_provider
        self.z_provider = z_provider

    def collect(self, keyword):
        if self.z_provider.exists(keyword):
            z_values = self.z_provider.provide(keyword)
        else:
            z_values = self.image_provider.provide(keyword)

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
