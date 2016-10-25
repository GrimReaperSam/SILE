import abc

from skimage.io import imread

from .descriptors import *
from ..filesystem.config_paths import *

class DescriptorsCalculator:
    def __init__(self):
        self.descriptors = {
            'gray_hist': GrayLevelHistogram(),
            'chroma_hist': ChromaHistogram(),
            'hue_angle_hist': HueHistogram(),
            'rgb_hist': RGBHistogram(),
            'lab_hist': LABHistogram(),
            'lch_hist': LCHHistogram(),
            'lightness_layout': LightnessLayout(),
            'chroma_layout': ChromaLayout(),
            'hue_layout': HueLayout(),
            'details_hist': DetailsHistogram(),
            #'gabor_hist': GaborHistogram(),
            #'gabor_layout': GaborLayout(),
            'lightness_fourier': LightnessFourier()
            #'lbp_hist': LinearBinaryPatternHistogram()
        }

    def describe_image(self, image):
        descriptors = {}
        for (k, v) in self.descriptors.items():
            descriptors[k] = v.compute(image)
        return descriptors

    def describe_set(self, images, descriptor_name):
        descriptor = self.descriptors[descriptor_name]
        characteristics = np.zeros((len(images), *descriptor.shape))
        for image_index, image in enumerate(images):
            characteristics[image_index] = descriptor.compute(imread(rgb_from_id(image)))
        return characteristics


class DescriptorProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def provide(self, keyword):
        """
        :param keyword: The tag of the images
        :return: An iterator over the images that have this tag and another
                 over the ones that don't.
        """
