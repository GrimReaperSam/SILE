from .descriptors import *


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
            'gabor_hist': GaborHistogram(),
            'gabor_layout': GaborLayout(),
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
            characteristics[image_index] = descriptor.compute(image)
        return characteristics
