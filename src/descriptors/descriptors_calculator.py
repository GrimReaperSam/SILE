import logging
import concurrent.futures as ft

from .descriptors import *


class DescriptorsCalculator:
    def __init__(self, descriptor_provider):
        self.descriptors = {
            'gray_hist': GrayLevelHistogram(),
            'chroma_hist': ChromaHistogram(),
            'hue_angle_hist': HueHistogram(),
            'rgb_hist': RGBHistogram(),
            'lab_hist': LABHistogram(),
            'lch_hist': LCHHistogram(),
            # 'lightness_layout': LightnessLayout(),
            # 'chroma_layout': ChromaLayout(),
            # 'hue_layout': HueLayout(),
            # 'details_hist': DetailsHistogram(),
            #'gabor_hist': GaborHistogram(),
            #'gabor_layout': GaborLayout(),
            #'lightness_fourier': LightnessFourier()
            #'lbp_hist': LinearBinaryPatternHistogram()
        }
        self.descriptor_provider = descriptor_provider

    def describe_image(self, image, descriptor_name):
        descriptor = self.descriptors[descriptor_name]
        return descriptor.compute(image)

    def describe_job(self, image, descriptor_name, descriptors_matrix, image_index):
        description = self.descriptor_provider.provide(image, descriptor_name)
        if description is None or np.all(description == 0):
            description = self.describe_image(image, descriptor_name)
        descriptors_matrix[image_index] = description
        if image_index % 1000 == 0:
            descriptor_path = collections_from_descriptor(descriptor_name)
            descriptor_path.parent.mkdir(exist_ok=True, parents=True)
            descriptors_matrix.dump(str(descriptor_path))
            logging.info('Processed until: %s, Saved descriptors matrix at %s' % (image_index, str(descriptor_path)))

    def describe_set(self, images, descriptor_name, descriptors_matrix):
        descriptor = self.descriptors[descriptor_name]
        if descriptors_matrix is None:
            descriptors_matrix = np.zeros((len(images), *descriptor.shape))
            indices = np.array(range(len(images)))
        else:
            axes = tuple([x for x in range(1, descriptors_matrix.ndim)])
            zero_entries = np.all(descriptors_matrix == 0, axis=axes)
            indices = zero_entries.nonzero()[0]
        with ft.ThreadPoolExecutor(max_workers=8) as executor:
            try:
                for image_index in indices:
                    image = images[image_index]
                    executor.submit(self.describe_job, image, descriptor_name, descriptors_matrix, image_index)
            except Exception:
                logging.exception('Not able to describe image %s' % image)
        return descriptors_matrix


class DescriptorProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def provide(self, image_id, descriptor_name):
        """
        :param image_id: The id of the image
        :param descriptor_name: The name of the descriptor
        :return: An iterator over the images that have this tag and another
                 over the ones that don't.
        """

    @abc.abstractmethod
    def save(self, image_id, descriptor_name, description):
        """
        :param image_id: The id of the image
        :param descriptor_name: The name of the descriptor
        :param description: The value of the descriptor
        """