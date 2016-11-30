import abc

from scipy.interpolate import interp1d
from skimage.filters import gaussian

from src.color_helpers import *
from src.shared import *


class Enhancer(metaclass=abc.ABCMeta):
    def __init__(self):
        pass

    @abc.abstractmethod
    def enhance(self, image, z_delta, strength, mask=None):
        """
        :param image: The image itself
        :param z_delta: Indication on how to enhance the image
        :param strength: The strength of the enhancement
        :param mask: A mask to enhance on for local enhancement
        :return: The descriptor for this image
        """

    def compute_weight_map(self, image, z_descriptor):
        """
        :param image: The image itself
        :param z_descriptor: The z descriptor representing the aspect to be weighted
        :return: The weight map of this image
        """

    @abc.abstractmethod
    def init_transfer_function(self, **kwargs):
        """
        :param kwargs: channel='channel_name' to be used in some special cases
        :return: The bin centers and x2 values to initialize the transfer interpolation
        """

    def _get_mask(self, image, mask=None):
        if mask is None:
            h, w, _ = image.shape
            return np.ones((h, w), dtype=np.bool)
        return mask

    def _make_transfer(self, z_delta, strength, **kwargs):
        s_max = 5
        bin_centers, x2 = self.init_transfer_function(**kwargs)
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

    def _finalize_weight_map(self, my_map, h, w):
        my_map = my_map.reshape(h, w)

        # Blurring the weight map
        sigma = 0.02 * np.hypot(h, w)
        my_map = gaussian(my_map, sigma)

        # Clipping the weight map
        q = np.percentile(my_map, [5, 95])
        my_map = np.minimum(q[1], np.maximum(q[0], my_map))

        # Normalizing the weight map
        my_map -= q[0]
        my_map /= q[1] - q[0]
        return np.dstack(3 * (my_map,))


class GrayLevelHistogramEnhancer(Enhancer):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def enhance(self, image, z_delta, strength, mask=None):
        mask = self._get_mask(image, mask)

        x2, mmap = self._make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 255, fill_value='extrapolate')
        result = np.array(image)
        result[mask] = transfer_function(image[mask] / 255).astype(np.uint8)
        return result

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / (self.nbins * 2), 1 - 1 / (self.nbins * 2), self.nbins)
        x2 = np.linspace(0, 1, 255)
        return bin_centers, x2

    def compute_weight_map(self, image, z_descriptor):
        image_data = np.mean(image, 2)
        h, w = image_data.shape
        gray = image_data.reshape(h * w)
        bins = np.linspace(0, 256, self.nbins + 1, dtype=np.float32)

        indices = np.minimum(np.digitize(gray, bins) - 1, self.nbins - 1)
        my_map = z_descriptor[indices]
        return self._finalize_weight_map(my_map, h, w)


class ChromaHistogramEnhancer(Enhancer):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def enhance(self, image, z_delta, strength, mask=None):
        mask = self._get_mask(image, mask)

        x2, mmap = self._make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 80, fill_value='extrapolate')
        lch = lab_to_lch(rgb_to_lab(image))
        lch[..., 1][mask] = transfer_function(lch[..., 1][mask] / 80)
        return lab_to_rgb(lch_to_lab(lch))

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / (self.nbins * 2), 1 - 1 / (self.nbins * 2), self.nbins)
        x2 = np.linspace(0, 1, 80)
        return bin_centers, x2

    def compute_weight_map(self, image, z_descriptor):
        lch = lab_to_lch(rgb_to_lab(image))
        c_channel = lch[..., 1]
        h, w = c_channel.shape
        c_channel = c_channel.reshape(h * w)
        bins = np.linspace(0, 50, self.nbins + 1, dtype=np.float32)

        indices = np.minimum(np.digitize(c_channel, bins) - 1, self.nbins - 1)
        my_map = z_descriptor[indices]
        return self._finalize_weight_map(my_map, h, w)


class HueHistogramEnhancer(Enhancer):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def enhance(self, image, z_delta, strength, mask=None):
        mask = self._get_mask(image, mask)

        x2, mmap = self._make_transfer(z_delta, strength)
        transfer_function = interp1d(x2, mmap * 360, fill_value='extrapolate')
        lch = lab_to_lch(rgb_to_lab(image))
        lch[..., 2][mask] = transfer_function(lch[..., 2][mask] / 360)
        return lab_to_rgb(lch_to_lab(lch))

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / (self.nbins * 2), 1 - 1 / (self.nbins * 2), self.nbins)
        x2 = np.linspace(0, 1, 360)
        return bin_centers, x2

    def compute_weight_map(self, image, z_descriptor):
        lch = lab_to_lch(rgb_to_lab(image))
        h_channel = lch[..., 2]
        h, w = h_channel.shape
        h_channel = h_channel.reshape(h * w)
        bins = np.linspace(0, 360, self.nbins + 1, dtype=np.float32)

        indices = np.minimum(np.digitize(h_channel, bins) - 1, self.nbins - 1)
        my_map = z_descriptor[indices]
        return self._finalize_weight_map(my_map, h, w)


class RGBHistogramEnhancer(Enhancer):
    def __init__(self):
        self.nbins = 8

    def enhance(self, image, z_delta, strength, mask=None):
        mask = self._get_mask(image, mask)

        rgb = np.array(image)
        # Red
        zr = z_delta.sum(axis=(1, 2))
        x2, mmap = self._make_transfer(zr, strength)
        f = interp1d(x2, mmap * 255, fill_value='extrapolate')
        rgb[..., 0][mask] = f(image[..., 0][mask] / 255)

        # Green
        zg = z_delta.sum(axis=(0, 2))
        x2, mmap = self._make_transfer(zg, strength)
        f = interp1d(x2, mmap * 255, fill_value='extrapolate')
        rgb[..., 1][mask] = f(image[..., 1][mask] / 255)

        # Blue
        zb = z_delta.sum(axis=(0, 1))
        x2, mmap = self._make_transfer(zb, strength)
        f = interp1d(x2, mmap * 255, fill_value='extrapolate')
        rgb[..., 2][mask] = f(image[..., 2][mask] / 255)

        return rgb.astype(np.uint8)

    def init_transfer_function(self, **kwargs):
        bin_centers = np.linspace(1 / (self.nbins * 2), 1 - 1 / (self.nbins * 2), self.nbins)
        x2 = np.linspace(0, 1, 255)
        return bin_centers, x2

    def compute_weight_map(self, image, z_descriptor):
        h, w, d = image.shape
        rgb = image.reshape(h * w, d)
        bins = np.linspace(0, 256, self.nbins + 1, dtype=np.float32)

        indices = np.minimum(np.digitize(rgb, bins) - 1, self.nbins - 1)
        my_map = z_descriptor[np.hsplit(indices, 3)].reshape(h, w)
        return self._finalize_weight_map(my_map, h, w)


class LABHistogramEnhancer(Enhancer):
    def __init__(self):
        self.nbins = 8

    def enhance(self, image, z_delta, strength, mask=None):
        mask = self._get_mask(image, mask)

        lab = rgb_to_lab(image)
        result = np.array(lab)
        # L-channel
        l_channel = z_delta.sum(axis=(1, 2))
        x2, mmap = self._make_transfer(l_channel, strength, channel='L')
        f = interp1d(x2, mmap * 100, fill_value='extrapolate')
        result[..., 0][mask] = f(lab[..., 0][mask] / 100)

        # A-channel
        a_channel = z_delta.sum(axis=(0, 2))
        x2, mmap = self._make_transfer(a_channel, strength, channel='AB')
        f = interp1d(x2, mmap * 160 - 80, fill_value='extrapolate')
        result[..., 1][mask] = f(lab[..., 1][mask] / 80)

        # B-channel
        b_channel = z_delta.sum(axis=(0, 1))
        x2, mmap = self._make_transfer(b_channel, strength, channel='AB')
        f = interp1d(x2, mmap * 160 - 80, fill_value='extrapolate')
        result[..., 2][mask] = f(lab[..., 2][mask] / 80)

        return lab_to_rgb(result)

    def init_transfer_function(self, **kwargs):
        channel = kwargs['channel']
        if channel == 'L':
            bin_centers = np.linspace(1 / (self.nbins * 2), 1 - 1 / (self.nbins * 2), self.nbins)
            x2 = np.linspace(0, 1, 100)
        else:
            max_range = (self.nbins - 1) / (self.nbins * 2)
            bin_centers = np.linspace(-max_range, max_range, self.nbins)
            x2 = np.linspace(-0.5, 0.5, 160)
        return bin_centers, x2

    def compute_weight_map(self, image, z_descriptor):
        lab = rgb_to_lab(image)
        h, w, d = lab.shape
        lab = lab.reshape(h * w, d)
        l_bins = np.linspace(0, 100, self.nbins + 1, dtype=np.float32)
        ab_bins = np.linspace(-80, 80, self.nbins + 1, dtype=np.float32)

        l_indices = np.minimum(np.digitize(lab[..., 0], l_bins) - 1, self.nbins - 1)
        a_indices = np.minimum(np.digitize(lab[..., 1], ab_bins) - 1, self.nbins - 1)
        b_indices = np.minimum(np.digitize(lab[..., 2], ab_bins) - 1, self.nbins - 1)
        my_map = z_descriptor[[l_indices, a_indices, b_indices]].reshape(h, w)
        return self._finalize_weight_map(my_map, h, w)


class LCHHistogramEnhancer(Enhancer):
    def __init__(self):
        self.nbins = 8

    def enhance(self, image, z_delta, strength, mask=None):
        mask = self._get_mask(image, mask)

        lch = lab_to_lch(rgb_to_lab(image))
        result = np.array(lch)
        # L-channel
        l_channel = z_delta.sum(axis=(1, 2))
        x2, mmap = self._make_transfer(l_channel, strength, channel='L')
        f = interp1d(x2, mmap * 100, fill_value='extrapolate')
        result[..., 0][mask] = f(lch[..., 0][mask] / 100)

        # C-channel
        c_channel = z_delta.sum(axis=(0, 2))
        x2, mmap = self._make_transfer(c_channel, strength, channel='C')
        f = interp1d(x2, mmap * 80, fill_value='extrapolate')
        result[..., 1][mask] = f(lch[..., 1][mask] / 80)

        # H-channel
        h_channel = z_delta.sum(axis=(0, 1))
        x2, mmap = self._make_transfer(h_channel, strength, channel='H')
        f = interp1d(x2, mmap * 360, fill_value='extrapolate')
        result[..., 2][mask] = f(lch[..., 2][mask] / 360)

        return lab_to_rgb(lch_to_lab(result))

    def init_transfer_function(self, **kwargs):
        channel = kwargs['channel']
        bin_centers = np.linspace(1 / (self.nbins * 2), 1 - 1 / (self.nbins * 2), self.nbins)
        if channel == 'L':
            x2 = np.linspace(0, 1, 100)
        elif channel == 'C':
            x2 = np.linspace(0, 1, 80)
        else:
            x2 = np.linspace(0, 1, 360)
        return bin_centers, x2

    def compute_weight_map(self, image, z_descriptor):
        lch = lab_to_lch(rgb_to_lab(image))
        h, w, d = lch.shape
        lch = lch.reshape(h * w, d)

        l_bins = np.linspace(0, 100, self.nbins + 1, dtype=np.float32)
        c_bins = np.linspace(0, 50, self.nbins + 1, dtype=np.float32)
        h_bins = np.linspace(0, 360, self.nbins + 1, dtype=np.float32)

        l_indices = np.minimum(np.digitize(lch[..., 0], l_bins) - 1, self.nbins - 1)
        c_indices = np.minimum(np.digitize(lch[..., 1], c_bins) - 1, self.nbins - 1)
        h_indices = np.minimum(np.digitize(lch[..., 2], h_bins) - 1, self.nbins - 1)
        my_map = z_descriptor[[l_indices, c_indices, h_indices]].reshape(h, w)
        return self._finalize_weight_map(my_map, h, w)


ENHANCERS = {
    'gray_hist': GrayLevelHistogramEnhancer(),
    'chroma_hist': ChromaHistogramEnhancer(),
    'hue_angle_hist': HueHistogramEnhancer(),
    'rgb_hist': RGBHistogramEnhancer(),
    'lab_hist': LABHistogramEnhancer(),
    'lch_hist': LCHHistogramEnhancer(),
    # 'lightness_layout': LightnessLayout(),
    # 'chroma_layout': ChromaLayout(),
    # 'hue_layout': HueLayout(),
    # 'details_hist': DetailsHistogram(),
    # 'frequency_hist': LightnessFourier(),
    #'gabor_hist': GaborHistogram(),
    #'gabor_layout': GaborLayout(),
    #'lbp_hist': LinearBinaryPatternHistogram()
}