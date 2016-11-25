import abc

from scipy.interpolate import interp1d

from ..descriptors.color_helpers import *


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
    def init_transfer_function(self, **kwargs):
        """
        :param kwargs: channel='channel_name' to be used in some special cases
        :return: The bin centers and x2 values to initialize the transfer interpolation
        """

    def make_transfer(self, z_delta, strength, **kwargs):
        s_max = 5
        bin_centers, x2 = self.init_transfer_function(kwargs)
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


class GrayLevelHistogramEnhancer(Enhancer):
    def enhance(self, image, z_delta, strength):
        x2, mmap = self.make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 255, fill_value='extrapolate')
        return transfer_function(image / 255).astype(np.uint8)

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 255)
        return bin_centers, x2


class ChromaHistogramEnhancer(Enhancer):
    def enhance(self, image, z_delta, strength):
        x2, mmap = self.make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 80, fill_value='extrapolate')
        lch = lab_to_lch(rgb_to_lab(image))
        lch[..., 1] = transfer_function(lch[..., 1] / 80)
        return lab_to_rgb(lch_to_lab(lch))

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 80)
        return bin_centers, x2


class HueHistogramEnhancer(Enhancer):
    def enhance(self, image, z_delta, strength):
        x2, mmap = self.make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 360, fill_value='extrapolate')
        lch = lab_to_lch(rgb_to_lab(image))
        lch[..., 2] = transfer_function(lch[..., 2] / 360)
        return lab_to_rgb(lch_to_lab(lch))

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / 32, 31 / 32, 16)
        x2 = np.linspace(0, 1, 360)
        return bin_centers, x2


class RGBHistogramEnhancer(Enhancer):
    def enhance(self, image, z_delta, strength):
        rgb = np.empty(image.shape)
        # Red
        zr = z_delta.sum(axis=(1, 2))
        x2, mmap = self.make_transfer(zr, strength)
        f = interp1d(x2, mmap * 255, fill_value='extrapolate')
        rgb[..., 0] = f(image[..., 0] / 255)

        # Green
        zg = z_delta.sum(axis=(0, 2))
        x2, mmap = self.make_transfer(zg, strength)
        f = interp1d(x2, mmap * 255, fill_value='extrapolate')
        rgb[..., 1] = f(image[..., 1] / 255)

        # Blue
        zb = z_delta.sum(axis=(0, 1))
        x2, mmap = self.make_transfer(zb, strength)
        f = interp1d(x2, mmap * 255, fill_value='extrapolate')
        rgb[..., 2] = f(image[..., 2] / 255)

        return rgb.astype(np.uint8)

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / 16, 15 / 16, 8)
        x2 = np.linspace(0, 1, 255)
        return bin_centers, x2


class LABHistogramEnhancer(Enhancer):
    def enhance(self, image, z_delta, strength):
        lab = rgb_to_lab(image)
        result = np.empty(lab.shape)
        # L-channel
        l_channel = z_delta.sum(axis=(1, 2))
        x2, mmap = self.make_transfer(l_channel, strength, channel='L')
        f = interp1d(x2, mmap * 100, fill_value='extrapolate')
        result[..., 0] = f(lab[..., 0] / 100)

        # A-channel
        a_channel = z_delta.sum(axis=(0, 2))
        x2, mmap = self.make_transfer(a_channel, strength, channel='AB')
        f = interp1d(x2, mmap * 80, fill_value='extrapolate')
        result[..., 1] = f(lab[..., 1] / 80)

        # B-channel
        b_channel = z_delta.sum(axis=(0, 1))
        x2, mmap = self.make_transfer(b_channel, strength, channel='AB')
        f = interp1d(x2, mmap * 80, fill_value='extrapolate')
        result[..., 2] = f(lab[..., 2] / 80)

        return lab_to_rgb(result)

    def init_transfer_function(self, **kwargs):
        channel = kwargs['channel']
        if channel == 'L':
            bin_centers = np.linspace(1 / 16, 15 / 16, 8)
            x2 = np.linspace(0, 1, 100)
        else:
            bin_centers = np.linspace(-15 / 16, 15 / 16, 8)
            x2 = np.linspace(-1, 1, 160)
        return bin_centers, x2


ENHANCERS = {
    'gray_hist': GrayLevelHistogramEnhancer(),
    'chroma_hist': ChromaHistogramEnhancer(),
    'hue_angle_hist': HueHistogramEnhancer(),
    'rgb_hist': RGBHistogramEnhancer(),
    'lab_hist': LABHistogramEnhancer(),
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