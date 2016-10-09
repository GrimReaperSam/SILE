from skimage import exposure, img_as_float
from skimage.color import rgb2gray, rgb2lab, lab2lch, gray2rgb

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
        if len(image.shape) == 2:
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
        if len(image.shape) == 2:
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
        if len(image.shape) == 2:
            image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = img_as_float(lab2lch(lab))
        lch_hist = np.histogramdd(lch, bins=self.nbins)[0]
        return lch_hist / np.sum(lch_hist)


class CHHistogram:
    def __init__(self, nbins=DEFAULT_2D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        if len(image.shape) == 2:
            image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = img_as_float(lab2lch(lab))
        ch_ = lch[:, :, 1:3]
        ch_hist = np.histogramdd(ch_, bins=self.nbins)[0]
        return ch_hist / np.sum(ch_hist)


class LightnessHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        if len(image.shape) == 2:
            image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_hist = exposure.histogram(l_, nbins=self.nbins)[0]
        return l_hist / np.sum(l_hist)


class ChromaHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        if len(image.shape) == 2:
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
        if len(image.shape) == 2:
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
        h, w, d = image.shape
        rgb = img_as_float(image.reshape((h*w, d)))
        rgb_hist = np.histogramdd(rgb, bins=self.nbins)[0]
        return rgb_hist / np.sum(rgb_hist)


class LightnessLayout:
    def compute(self, image):
        if len(image.shape) == 2:
            image = gray2rgb(image)
        lab = rgb2lab(image)
        l_ = img_as_float(lab[:, :, 0])
        l_layout = sample8x8(l_)
        l_layout -= np.min(l_layout)
        return l_layout / np.max(l_layout)


class ChromaLayout:
    def compute(self, image):
        if len(image.shape) == 2:
            image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        c_layout = sample8x8(c_)
        c_layout -= np.min(c_layout)
        return c_layout / np.max(c_layout)


class HueLayout:
    def compute(self, image):
        if len(image.shape) == 2:
            image = gray2rgb(image)
        lab = rgb2lab(image)
        lch = lab2lch(lab)
        c_ = img_as_float(lch[:, :, 1])
        mask = c_ <= 1
        h_ = img_as_float(lch[:, :, 2])
        h_layout = hue_sample8x8(h_, mask)
        return h_layout
