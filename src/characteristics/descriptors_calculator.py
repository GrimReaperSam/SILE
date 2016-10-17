from .descriptors import *


class DescriptorsCalculator:
    def __init__(self):
        self.characteristics = {
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

    def describe(self, image):
        descriptors = {}
        for (k, v) in self.characteristics.items():
            descriptors[k] = v.compute(image)
        return descriptors
