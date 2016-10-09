from skimage import exposure, img_as_float
from skimage.color import rgb2gray, rgb2lab, lab2lch
import numpy as np

from ..shared import *


class GrayLevelHistogram:
    def __init__(self, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        grey = img_as_float(rgb2gray(image))
        hist = exposure.histogram(grey, nbins=self.nbins)[0]
        return hist / np.sum(hist)


class LabHistogram:
    def __init__(self, nbins=DEFAULT_3D_HISTOGRAM_NBINS):
        self.nbins = nbins

    def compute(self, image):
        lab = rgb2lab(image)
        h, w, d = lab.shape
        lab_ = img_as_float(lab.reshape((h*w, d)))
        lab_hist = np.histogramdd(lab_, bins=self.nbins)[0]
        return lab_hist / np.sum(lab_hist)


class HistogramCharacteristic:
    def __init__(self, image, nbins=DEFAULT_1D_HISTOGRAM_NBINS):
        self.image = image
        self.nbins = nbins

    def chroma_level(self):
        img_lab = rgb2lab(self.image)
        img_lch = lab2lch(img_lab)
        chroma = img_lch[:, :, 1]
        return exposure.histogram(chroma, nbins=self.nbins)

    def hue_angle_level(self):
        img_lab = rgb2lab(self.image)
        img_lch = lab2lch(img_lab)
        chroma = img_lch[:, :, 2]
        return exposure.histogram(chroma, nbins=self.nbins)
