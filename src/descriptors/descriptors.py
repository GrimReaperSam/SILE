import abc

from skimage import exposure, img_as_float
from skimage.color import rgb2lab, lab2lch, gray2rgb
from skimage.io import imread
from scipy import ndimage as ndi

from .helpers import *

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
        :param image: GrayLevel or RGB image matrix
        :return: The descriptor for this image
        """

    def _get_image(self, image):
        try:
            image_data = imread(rgb_from_id(image))
        except Exception:
            missing_data_image = ndi.imread(rgb_from_id(image))
            image_data = np.array(missing_data_image.item())
        return image_data

    def _get_lab(self, image):
        lab_path = lab_from_id(image)
        if lab_path.exists():
            return np.load(str(lab_path))
        else:
            image_data = self._get_image(image)
            image_data = gray2rgb(image_data)
            lab_data = rgb2lab(image_data)
            lab_path.parent.mkdir(exist_ok=True, parents=True)
            lab_data.dump(str(lab_path))
            return lab_data


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
        return hist / np.sum(hist)


class LABHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_3D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, self.nbins, self.nbins

    def compute(self, image):
        image_data = self._get_image(image)
        image_data = gray2rgb(image_data)
        lab = rgb2lab(image_data)
        h, w, d = lab.shape
        lab_ = img_as_float(lab.reshape((h * w, d)))
        lab_hist = np.histogramdd(lab_, bins=self.nbins)[0]
        return lab_hist / np.sum(lab_hist)


class ABHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, self.nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        h, w, d = lab.shape
        ab_ = lab[:, :, 1:3].reshape((h * w, d - 1))
        ab_hist = np.histogramdd(ab_, bins=self.nbins)[0]
        return ab_hist / np.sum(ab_hist)


class LCHHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_3D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, self.nbins, self.nbins

    def compute(self, image):
        image = gray2rgb(image)
        h, w, d = image.shape
        lab = rgb2lab(image)
        lch = img_as_float(lab2lch(lab)).reshape(h * w, d)
        lch_hist = np.histogramdd(lch, bins=self.nbins)[0]
        return lch_hist / np.sum(lch_hist)


class CHHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins, self.nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = img_as_float(lab2lch(lab))
        h, w, d = lch.shape
        ch_ = lch[:, :, 1:3].reshape(h * w, 2)
        ch_hist = np.histogramdd(ch_, bins=self.nbins)[0]
        return ch_hist / np.sum(ch_hist)


class LightnessHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_hist = exposure.histogram(l_, nbins=self.nbins)[0]
        return l_hist / np.sum(l_hist)


class ChromaHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        lab = self._get_lab(image)
        lch = lab2lch(lab)
        c_ = lch[..., 1]
        c_hist = np.histogram(c_, range=(0, 50), bins=self.nbins)[0]
        return c_hist / np.sum(c_hist)


class HueHistogram(Descriptor):
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    @property
    def shape(self):
        return self.nbins,

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        h_ = img_as_float(lch[:, :, 2])
        h_hist = exposure.histogram(h_, nbins=self.nbins)[0]
        return h_hist / np.sum(h_hist)


class RGBHistogram(Descriptor):
    def __init__(self):
        self.nbins = 8

    @property
    def shape(self):
        return self.nbins, self.nbins, self.nbins

    def compute(self, image):
        image = gray2rgb(image)
        h, w, d = image.shape
        rgb = img_as_float(image.reshape((h * w, d)))
        rgb_hist = np.histogramdd(rgb, bins=self.nbins)[0]
        return rgb_hist / np.sum(rgb_hist)


class LightnessLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_layout = sample8x8(l_)
        l_layout -= np.min(l_layout)
        return l_layout / np.max(l_layout)


class ChromaLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        c_layout = sample8x8(c_)
        c_layout -= np.min(c_layout)
        return c_layout / np.max(c_layout)


class HueLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        mask = c_ <= 1
        h_ = img_as_float(lch[:, :, 2])
        h_layout = hue_sample8x8(h_, mask)
        return h_layout


class LightnessHighLayout(Descriptor):
    def __init__(self, blur_factor=0.1):
        self.blur_factor = blur_factor

    @property
    def shape(self):
        return 8, 8

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
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
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_blur, ss = compute_lightness_blur(l_, 0.1)

        l_high = np.abs(l_[ss:-ss, ss:-ss] - l_blur[ss:-ss, ss:-ss])
        lab_l_crop = l_[ss:-ss, ss:-ss]

        details_hist = np.zeros((16, 3))

        positives = lab_l_crop <= 100 / 3
        if np.count_nonzero(positives) > lab_l_crop.size / 100:
            details_hist[:, 0] = exposure.histogram(l_high[positives], nbins=self.nbins)[0]

        positives = np.logical_and(lab_l_crop > 100 / 3, lab_l_crop <= 200 / 3)
        if np.count_nonzero(positives) > lab_l_crop.size / 100:
            details_hist[:, 1] = exposure.histogram(l_high[positives], nbins=self.nbins)[0]

        positives = lab_l_crop > 200 / 3
        if np.count_nonzero(positives) > lab_l_crop.size / 100:
            details_hist[:, 2] = exposure.histogram(l_high[positives], nbins=self.nbins)[0]

        return details_hist


class DetailsLayout(Descriptor):
    @property
    def shape(self):
        return 8, 8, 3

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
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
        image = gray2rgb(image)
        lab = rgb2lab(image)
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
        image = gray2rgb(image)
        # TODO save lab images if possible
        lab = rgb2lab(image)
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
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        fourier = np.absolute(np.fft.fft2(l_))
        resized = np.resize(fourier, (21, 21))
        return resized / np.max(resized)


class ChromaFourier(Descriptor):
    @property
    def shape(self):
        return 21, 21

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        l_ = img_as_float(lch[:, :, 1])
        fourier = np.absolute(np.fft.fft2(l_))
        resized = np.resize(fourier, (21, 21))
        return resized / np.max(resized)


class HueFourier(Descriptor):
    @property
    def shape(self):
        return 21, 21

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        l_ = img_as_float(lch[:, :, 2])
        fourier = np.absolute(np.fft.fft2(l_))
        resized = np.resize(fourier, (21, 21))
        return resized / np.max(resized)
