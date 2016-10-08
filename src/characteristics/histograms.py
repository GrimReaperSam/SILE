from skimage import exposure, img_as_float
from skimage.color import rgb2gray, rgb2lab, lab2lch
from ..shared import *


class HistogramCharacteristic:
    def __init__(self, image, nbins=HISTOGRAM_CHARACTERISTIC_BIN_SIZE):
        self.image = image
        self.nbins = nbins

    def gray_level(self):
        grey = rgb2gray(self.image)
        grey = img_as_float(grey)
        return exposure.histogram(grey, nbins=self.nbins)

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
