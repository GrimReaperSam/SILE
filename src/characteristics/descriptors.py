from skimage import exposure, img_as_float
from skimage.color import rgb2gray, rgb2lab, lab2lch, gray2rgb

from scipy import ndimage as ndi

from .helpers import *
from ..shared import *


class GrayLevelHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        grey = img_as_float(rgb2gray(image))
        hist = exposure.histogram(grey, nbins=self.nbins)[0]
        return hist / np.sum(hist)


class LABHistogram:
    def __init__(self, nbins=DEFAULT_3D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        h, w, d = lab.shape
        lab_ = img_as_float(lab.reshape((h*w, d)))
        lab_hist = np.histogramdd(lab_, bins=self.nbins)[0]
        return lab_hist / np.sum(lab_hist)


class ABHistogram:
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        h, w, d = lab.shape
        ab_ = lab[:, :, 1:3].reshape((h * w, d - 1))
        ab_hist = np.histogramdd(ab_, bins=self.nbins)[0]
        return ab_hist / np.sum(ab_hist)


class LCHHistogram:
    def __init__(self, nbins=DEFAULT_3D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        h, w, d = image.shape
        lab = rgb2lab(image)
        lch = img_as_float(lab2lch(lab)).reshape(h*w, d)
        lch_hist = np.histogramdd(lch, bins=self.nbins)[0]
        return lch_hist / np.sum(lch_hist)


class CHHistogram:
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = img_as_float(lab2lch(lab))
        h, w, d = lch.shape
        ch_ = lch[:, :, 1:3].reshape(h*w, 2)
        ch_hist = np.histogramdd(ch_, bins=self.nbins)[0]
        return ch_hist / np.sum(ch_hist)


class LightnessHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_hist = exposure.histogram(l_, nbins=self.nbins)[0]
        return l_hist / np.sum(l_hist)


class ChromaHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        c_hist = exposure.histogram(c_, nbins=self.nbins)[0]
        return c_hist / np.sum(c_hist)


class HueHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        h_ = img_as_float(lch[:, :, 2])
        h_hist = exposure.histogram(h_, nbins=self.nbins)[0]
        return h_hist / np.sum(h_hist)


class RGBHistogram:
    def __init__(self):
        self.nbins = 8

    def compute(self, image):
        image = gray2rgb(image)
        h, w, d = image.shape
        rgb = img_as_float(image.reshape((h*w, d)))
        rgb_hist = np.histogramdd(rgb, bins=self.nbins)[0]
        return rgb_hist / np.sum(rgb_hist)


class LightnessLayout:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_layout = sample8x8(l_)
        l_layout -= np.min(l_layout)
        return l_layout / np.max(l_layout)


class ChromaLayout:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        c_layout = sample8x8(c_)
        c_layout -= np.min(c_layout)
        return c_layout / np.max(c_layout)


class HueLayout:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        mask = c_ <= 1
        h_ = img_as_float(lch[:, :, 2])
        h_layout = hue_sample8x8(h_, mask)
        return h_layout


class LightnessHighLayout:
    def __init__(self, blur_factor=0.1):
        self.blur_factor = blur_factor

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_blur, ss = compute_lightness_blur(l_, self.blur_factor)

        l_high = np.abs(l_[ss:-ss, ss:-ss] - l_blur[ss:-ss, ss:-ss])

        l_high_layout = sample8x8(l_high)
        l_high_layout -= np.min(l_high_layout)
        return l_high_layout / np.max(l_high_layout)


class DetailsHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

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


class DetailsLayout:
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


class GaborHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])

        thetas = np.pi * np.array([0, 1/4, 1/2, 3/4])
        sizes = np.array([10, 20])
        histograms = np.zeros((sizes.size, thetas.size, self.nbins))

        for s_i, s in enumerate(sizes):
            for t_i, t in enumerate(thetas):
                kernel = compute_gabor_kernel(s, 1/s, t)
                gabor_real = ndi.convolve(l_, kernel)
                histograms[s_i, t_i, :] = exposure.histogram(gabor_real, nbins=self.nbins)[0]

        return histograms


class GaborLayout:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])

        thetas = np.pi * np.array([0, 1/4, 1/2, 3/4])
        sizes = np.array([10, 20])
        layouts = np.zeros((sizes.size, thetas.size, 8, 8))

        for s_i, s in enumerate(sizes):
            for t_i, t in enumerate(thetas):
                kernel = compute_gabor_kernel(s, 1 / s, t)
                gabor_real = ndi.convolve(l_, kernel)
                layout = sample8x8(gabor_real)
                layout -= np.min(layout)
                layouts[s_i, t_i, :, :] = layout / np.max(layout)

        return layouts


class LightnessFourier:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        fourier = np.absolute(np.fft.fft2(l_))
        resized = np.resize(fourier, (21, 21))
        return resized / np.max(resized)


class ChromaFourier:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        l_ = img_as_float(lch[:, :, 1])
        fourier = np.absolute(np.fft.fft2(l_))
        resized = np.resize(fourier, (21, 21))
        return resized / np.max(resized)


class HueFourier:
    def compute(self, image):
        image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        l_ = img_as_float(lch[:, :, 2])
        fourier = np.absolute(np.fft.fft2(l_))
        resized = np.resize(fourier, (21, 21))
        return resized / np.max(resized)
