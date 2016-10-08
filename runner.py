from skimage.io import imread
import matplotlib.pyplot as plt
import os

from src.characteristics import HistogramCharacteristic, ranksum

dark_hists = []
for i in os.listdir('DB/dark'):
    dark = imread('DB/dark/' + i)
    dark_hists.append(HistogramCharacteristic(dark).gray_level()[0])

light_hists = []
for i in os.listdir('DB/white'):
    light = imread('DB/white/' + i)
    light_hists.append(HistogramCharacteristic(light).gray_level()[0])

plt.plot(ranksum(light_hists, dark_hists))
plt.show()
