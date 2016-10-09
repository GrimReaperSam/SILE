from skimage.io import imread
import matplotlib.pyplot as plt
import os

from src.characteristics.histograms import *
from src.characteristics import ranksum

gray_hist = GrayLevelHistogram()

dark_hists = []
for i in os.listdir('DB/dark'):
    dark = imread('DB/dark/' + i)
    dark_hists.append(gray_hist.compute(dark))

light_hists = []
for i in os.listdir('DB/white'):
    light = imread('DB/white/' + i)
    light_hists.append(gray_hist.compute(light))

plt.plot(ranksum(dark_hists, light_hists))
plt.show()
