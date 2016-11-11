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
            'lightness_layout': LightnessLayout(),
            'chroma_layout': ChromaLayout(),
            'hue_layout': HueLayout(),
            'details_hist': DetailsHistogram(),
            'frequency_hist' : LightnessFourier(),
            #'gabor_hist': GaborHistogram(),
            #'gabor_layout': GaborLayout(),
            #'lbp_hist': LinearBinaryPatternHistogram()
        }
        self.descriptor_provider = descriptor_provider

    def describe_image(self, image, descriptor_name):
        descriptor = self.descriptors[descriptor_name]
        return descriptor.compute(image)

    def describe_job(self, image, descriptor_name, descriptors_matrix, image_index):
        try:
            description = self.descriptor_provider.provide(image, descriptor_name)
            if description is None or np.all(np.isnan(description)):
                description = self.describe_image(image, descriptor_name)
            descriptors_matrix[image_index] = description
            logging.info('Processed image: %s' % image_index)
        except Exception:
            logging.info('Image %s could not be processed.' % image_index)
            descriptors_matrix.flush()

    def describe_set(self, images, descriptor_name):
        descriptor = self.descriptors[descriptor_name]
        descriptor_path = collections_from_descriptor(descriptor_name)
        if not descriptor_path.exists():
            descriptor_path.parent.mkdir(exist_ok=True, parents=True)
            descriptors_matrix = np.memmap(str(descriptor_path), dtype='float32', mode='w+', shape=(len(images), *descriptor.shape))
            descriptors_matrix.fill(np.nan)
            indices = np.array(range(len(images)))
        else:
            descriptors_matrix = np.memmap(str(descriptor_path), dtype='float32', mode='r+',
                                           shape=(len(images), *descriptor.shape))
            axes = tuple([x for x in range(1, descriptors_matrix.ndim)])
            zero_entries = np.all(np.isnan(descriptors_matrix), axis=axes)
            indices = zero_entries.nonzero()[0]
        with ft.ThreadPoolExecutor(max_workers=8) as executor:
            try:
                for image_index in indices:
                    image = images[image_index]
                    executor.submit(self.describe_job, image, descriptor_name, descriptors_matrix, image_index)
            except Exception:
                logging.exception('Not able to describe image %s' % image)
        descriptors_matrix.flush()
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