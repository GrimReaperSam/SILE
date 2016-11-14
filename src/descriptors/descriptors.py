import abc
import logging

from skimage import exposure, img_as_float
from skimage.color import gray2rgb
from skimage.io import imread

from scipy import ndimage as ndi
from scipy.io import loadmat, savemat

from .descriptors_helpers import *
from .color_helpers import *
from .matlab import imresize

from ..filesystem.config_paths import *
from ..shared import *


class Descriptor(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def shape(self):
        """
        :return: The shape of the descriptor
        """

    @abc.abstractmethod
    def compute(self, image):
        """
        :param image: Either Path or an image ID in the DB
        :return: The descriptor for this image
        """

    def _get_image(self, image):
        # Check if image is of type Path
        if isinstance(image, np.ndarray):
            return image
        image_path = image if isinstance(image, Path) else rgb_from_id(image)
        try:
            image_data = imread(image_path)
        except Exception:
            missing_data_image = ndi.imread(image_path)
            image_data = np.array(missing_data_image.item())
        return image_data

    def _get_lab(self, image):
        if isinstance(image, np.ndarray):
            image_data = gray2rgb(image)
            return rgb_to_lab(image_data)
        if not isinstance(image, Path):
            lab_path = lab_from_id(image)
            if lab_path.exists():
                try:
                    return loadmat(str(lab_path))['data']
                except Exception:
                    logging.info('Could not load lab data for %s' % image)
        return rgb_to_lab(gray2rgb(self._get_image(image)))


class GrayLevelHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        image_data = self._get_image(image)
        if image_data.ndim == 3:
            image_data = np.mean(image_data, 2)
        hist = np.histogram(image_data, range=(0, 256), bins=self.nbins)[0]
        hist_sum = hist.sum()
        return hist / hist_sum if hist_sum != 0 else hist


class LABHistogram(Descriptor):
    def __init__(self):
        self.nbins = 8

    @property
    def shape(self):
        return self.nbins, self.nbins, self.nbins

    def compute(self, image):
        lab = self._get_lab(image)
        h, w, d = lab.shape
        lab_ = lab.reshape(h * w, d)
        lab_hist = np.histogramdd(lab_, range=[(0, 100), (-80, 80), (-80, 80)], bins=self.nbins)[0]
        lab_hist_sum = lab_hist.sum()
        return lab_hist / lab_hist_sum if lab_hist_sum != 0 else lab_hist


class ABHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, self.nbins

    def compute(self, image):
        lab = self._get_lab(image)
        h, w, d = lab.shape
        ab_ = lab[:, :, 1:3].reshape((h * w, d - 1))
        ab_hist = np.histogramdd(ab_, bins=self.nbins)[0]
        ab_hist_sum = ab_hist.sum()
        return ab_hist / ab_hist_sum if ab_hist_sum != 0 else ab_hist


class LCHHistogram(Descriptor):
    def __init__(self):
        self.nbins = 8

    @property
    def shape(self):
        return self.nbins, self.nbins, self.nbins

    def compute(self, image):
        lab = self._get_lab(image)
        h, w, d = lab.shape
        lch = lab_to_lch(lab).reshape(h * w, d)
        lch_hist = np.histogramdd(lch, range=[(0, 100), (0, 80), (0, 360)], bins=self.nbins)[0]
        lch_hist_sum = lch_hist.sum()
        return lch_hist / lch_hist_sum if lch_hist_sum != 0 else lch_hist


class CHHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, self.nbins

    def compute(self, image):
        lab = self._get_lab(image)
        lch = img_as_float(lab_to_lch(lab))
        h, w, d = lch.shape
        ch_ = lch[:, :, 1:3].reshape(h * w, 2)
        ch_hist = np.histogramdd(ch_, bins=self.nbins)[0]
        ch_hist_sum = ch_hist.sum()
        return ch_hist / ch_hist_sum if ch_hist_sum != 0 else ch_hist


class LightnessHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_hist = exposure.histogram(l_, nbins=self.nbins)[0]
        l_hist_sum = l_hist.sum()
        return l_hist / l_hist_sum if l_hist_sum != 0 else l_hist


class ChromaHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        lab = self._get_lab(image)
        c_ = np.sqrt(lab[..., 1] ** 2 + lab[..., 2] ** 2)
        c_hist = np.histogram(c_, range=(0, 50), bins=16)[0]
        c_hist_sum = c_hist.sum()
        return c_hist / c_hist_sum if c_hist_sum != 0 else c_hist


class HueHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        lab = self._get_lab(image)
        lab_c = np.sqrt(lab[..., 1] ** 2 + lab[..., 2] ** 2)
        lab_h = 180 / np.pi * np.arctan2(lab[..., 2], lab[..., 1])
        neg = lab_h < 0
        lab_h[neg] += 360
        mask = lab_c > 1
        if mask.sum() > 16:
            h_hist = np.histogram(lab_h, range=(0, 360), bins=16)[0]
        else:
            h_hist = np.zeros(16)
        h_hist_sum = h_hist.sum()
        return h_hist / h_hist_sum if h_hist_sum != 0 else h_hist


class RGBHistogram(Descriptor):
    def __init__(self):
        self.nbins = 8

    @property
    def shape(self):
        return self.nbins, self.nbins, self.nbins

    def compute(self, image):
        image_data = self._get_image(image)
        image_data = gray2rgb(image_data)
        h, w, d = image_data.shape
        rgb = image_data.reshape(h * w, d)
        rgb_hist = np.histogramdd(rgb, bins=self.nbins)[0]
        rgb_hist_sum = rgb_hist.sum()
        return rgb_hist / rgb_hist_sum if rgb_hist_sum != 0 else rgb_hist


class LightnessLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        lab = self._get_lab(image)
        l_layout = sample8x8(lab[..., 0])
        l_layout -= l_layout.min()
        return l_layout / l_layout.max()


class ChromaLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        lab = self._get_lab(image)
        c_ = np.sqrt(lab[..., 1] ** 2 + lab[..., 2] ** 2)
        c_layout = sample8x8(c_)
        c_layout -= c_layout.min()
        return c_layout / c_layout.max()


class HueLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        lab = self._get_lab(image)
        lab_c = np.sqrt(lab[..., 1] ** 2 + lab[..., 2] ** 2)
        lab_h = 180 / np.pi * np.arctan2(lab[..., 2], lab[..., 1])
        neg = lab_h < 0
        lab_h[neg] += 360
        mask = lab_c > 1
        return hue_sample8x8(lab_h, mask)


class LightnessHighLayout(Descriptor):
    def __init__(self, blur_factor=0.1):
        self.blur_factor = blur_factor

    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_blur, ss = compute_lightness_blur(l_, self.blur_factor)

        l_high = np.abs(l_[ss:-ss, ss:-ss] - l_blur[ss:-ss, ss:-ss])

        l_high_layout = sample8x8(l_high)
        l_high_layout -= np.min(l_high_layout)
        return l_high_layout / np.max(l_high_layout)


class DetailsHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, 3

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_blur, ss = compute_lightness_blur(l_, 0.1)

        l_high = np.abs(l_[ss-1:-ss, ss-1:-ss] - l_blur[ss-1:-ss, ss-1:-ss])
        lab_l_crop = l_[ss-1:-ss, ss-1:-ss]

        details_hist = np.zeros((16, 3))

        positives = lab_l_crop <= 100 / 3
        if positives.sum() > lab_l_crop.size / 100:
            details_hist[:, 0] = np.histogram(l_high[positives], range=(0, 40), bins=self.nbins)[0]
            if details_hist[:, 0].sum() > 0:
                details_hist[:, 0] /= details_hist[:, 0].sum()

        positives = (lab_l_crop > 100 / 3) & (lab_l_crop <= 200 / 3)
        if positives.sum() > lab_l_crop.size / 100:
            details_hist[:, 1] = np.histogram(l_high[positives], range=(0, 40), bins=self.nbins)[0]
            if details_hist[:, 1].sum() > 0:
                details_hist[:, 1] /= details_hist[:, 1].sum()

        positives = lab_l_crop > 200 / 3
        if positives.sum() > lab_l_crop.size / 100:
            details_hist[:, 2] = np.histogram(l_high[positives], range=(0, 40), bins=self.nbins)[0]
            if details_hist[:, 2].sum() > 0:
                details_hist[:, 2] /= details_hist[:, 2].sum()

        return details_hist


class DetailsLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8, 3

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_blur, ss = compute_lightness_blur(l_, 0.1)

        l_high = np.abs(l_[ss:-ss, ss:-ss] - l_blur[ss:-ss, ss:-ss])
        lab_l_crop = l_[ss:-ss, ss:-ss]

        details = np.zeros(l_high.shape)
        details_layout = np.zeros((8, 8, 3))

        positives = lab_l_crop <= 100 / 3
        if np.count_nonzero(positives) > lab_l_crop.size / 100:
            details[positives] = l_high[positives]
            details_layout[:, :, 0] = sample8x8(details)
            details_layout[:, :, 0] -= np.min(details_layout[:, :, 0])
            details_layout[:, :, 0] /= np.max(details_layout[:, :, 0])

        positives = np.logical_and(lab_l_crop > 100 / 3, lab_l_crop <= 200 / 3)
        if np.count_nonzero(positives) > lab_l_crop.size / 100:
            details[positives] = l_high[positives]
            details_layout[:, :, 1] = sample8x8(details)
            details_layout[:, :, 1] -= np.min(details_layout[:, :, 1])
            details_layout[:, :, 1] /= np.max(details_layout[:, :, 1])

        positives = lab_l_crop > 200 / 3
        if np.count_nonzero(positives) > lab_l_crop.size / 100:
            details[positives] = l_high[positives]
            details_layout[:, :, 2] = sample8x8(details)
            details_layout[:, :, 2] -= np.min(details_layout[:, :, 2])
            details_layout[:, :, 2] /= np.max(details_layout[:, :, 2])

        return details_layout


class GaborBanks:
    def __init__(self):
        self.thetas = np.pi * np.array([0, 1 / 4, 1 / 2, 3 / 4])
        self.sizes = np.array([10, 20])
        self.kernels = [[None] * self.thetas.size] * self.sizes.size
        for s_i, s in enumerate(self.sizes):
            for t_i, t in enumerate(self.thetas):
                self.kernels[s_i][t_i] = compute_gabor_kernel(s, 1 / s, t)


gb = GaborBanks()


class GaborHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return gb.sizes.size, gb.thetas.size, self.nbins

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = img_as_float(lab[:, :, 0])

        histograms = np.zeros((gb.sizes.size, gb.thetas.size, self.nbins))

        for s_i, s in enumerate(gb.sizes):
            for t_i, t in enumerate(gb.thetas):
                kernel = gb.kernels[s_i][t_i]
                gabor_real = ndi.convolve(l_, kernel)
                histograms[s_i, t_i, :] = exposure.histogram(gabor_real, nbins=self.nbins)[0]

        return histograms


class GaborLayout(Descriptor):
    @property
    def shape(self):
        return gb.sizes.size, gb.thetas.size, 8, 8

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = img_as_float(lab[:, :, 0])

        layouts = np.zeros((gb.sizes.size, gb.thetas.size, 8, 8))

        for s_i, s in enumerate(gb.sizes):
            for t_i, t in enumerate(gb.thetas):
                kernel = gb.kernels[s_i][t_i]
                gabor_real = ndi.convolve(l_, kernel)
                layout = sample8x8(gabor_real)
                layout -= np.min(layout)
                layouts[s_i, t_i, :, :] = layout / np.max(layout)

        return layouts


class LightnessFourier(Descriptor):
    @property
    def shape(self):
        return 21, 21

    def compute(self, image):
        lab = self._get_lab(image)
        l_ = lab[..., 0]
        fourier = np.fft.fft2(l_)
        shifted = np.fft.fftshift(fourier)
        return imresize(np.abs(shifted), 21, 21)


DESCRIPTORS = {
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
    'frequency_hist': LightnessFourier(),
    #'gabor_hist': GaborHistogram(),
    #'gabor_layout': GaborLayout(),
    #'lbp_hist': LinearBinaryPatternHistogram()
}
