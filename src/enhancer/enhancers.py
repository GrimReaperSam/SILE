import abc

import numpy as np

from scipy.interpolate import interp1d


class Enhancer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def enhance(self, image, z_delta, strength):
        """
        :param image: The image itself
        :param z_delta: Indication on how to enhance the image
        :param strength: The strength of the enhancement
        :return: The descriptor for this image
        """

    @abc.abstractmethod
    def init_transfer_function(self):
        """
        :return: The bin centers and x2 values to initialize the transfer interpolation
        """

    def make_transfer(self, z_delta, strength):
        s_max = 5
        bin_centers, x2 = self.init_transfer_function()
        # elif key == 'chroma_hist':
        #     bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        #     x2 = np.linspace(0, 1, 80)
        # elif key == 'hue_angle_hist':
        #     bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        #     x2 = np.linspace(0, 1, 360)
        # elif key == 'rgb_hist':
        #     bin_centers = np.linspace(1 / 16, 15 / 16, 8)
        #     x2 = np.linspace(0, 1, 255)

        f_derivative = interp1d(bin_centers, strength * z_delta, fill_value='extrapolate')

        slopes = f_derivative(x2)
        slopes[slopes >= 0] = 1 / (1 + strength * slopes[slopes >= 0])
        slopes[slopes < 0] = 1 + np.abs(slopes[slopes < 0])

        slopes[slopes > s_max] = s_max
        slopes[slopes < 1 / s_max] = 1 / s_max

        mmap = np.cumsum(slopes)
        mmap -= mmap.min()
        mmap = mmap / mmap.max()

        return x2, mmap
        # elif key == 'chroma_hist':
        #     return x2, mmap * 80
        # elif key == 'hue_angle_hist':
        #     return x2, mmap * 360
        # elif key == 'rgb_hist':
        #     return x2, mmap * 255


class GLHEnhancer(Enhancer):
    def enhance(self, image, z_delta, strength):
        x2, mmap = self.make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 255, fill_value='extrapolate')
        return transfer_function(image / 255).astype(np.uint8)

    def init_transfer_function(self):
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 255)
        return bin_centers, x2

ENHANCERS = {
    'gray_hist': GLHEnhancer(),
    # 'chroma_hist': ChromaHistogram(),
    # 'hue_angle_hist': HueHistogram(),
    # 'rgb_hist': RGBHistogram(),
    # 'lab_hist': LABHistogram(),
    # 'lch_hist': LCHHistogram(),
    # 'lightness_layout': LightnessLayout(),
    # 'chroma_layout': ChromaLayout(),
    # 'hue_layout': HueLayout(),
    # 'details_hist': DetailsHistogram(),
    # 'frequency_hist': LightnessFourier(),
    #'gabor_hist': GaborHistogram(),
    #'gabor_layout': GaborLayout(),
    #'lbp_hist': LinearBinaryPatternHistogram()
}