from skimage.io import imread
import matplotlib.pyplot as plt

from src.characteristics import HistogramCharacteristic, ranksum


light_1 = imread('resources/2452.jpeg')
hist_light_1, centers = HistogramCharacteristic(light_1).chroma_level()

light_2 = imread('resources/351519.jpeg')
hist_light_2, centers = HistogramCharacteristic(light_2).chroma_level()

light_3 = imread('resources/light1.jpg')
hist_light_3, centers = HistogramCharacteristic(light_3).chroma_level()

light_4 = imread('resources/light1.jpg')
hist_light_4, centers = HistogramCharacteristic(light_4).chroma_level()

light_5 = imread('resources/light1.jpg')
hist_light_5, centers = HistogramCharacteristic(light_5).chroma_level()

light_6 = imread('resources/5211.jpeg')
hist_light_6, centers = HistogramCharacteristic(light_6).chroma_level()

dark_1 = imread('resources/dark1.jpg')
hist_dark_1, centers = HistogramCharacteristic(dark_1).chroma_level()

dark_2 = imread('resources/9716.jpeg')
hist_dark_2, centers = HistogramCharacteristic(dark_2).chroma_level()

dark_3 = imread('resources/dark2.png')
hist_dark_3, centers = HistogramCharacteristic(dark_3).chroma_level()

pos = [hist_light_1, hist_light_2, hist_light_3, hist_light_4, hist_light_5, hist_light_6]
neg = [hist_dark_1, hist_dark_2, hist_dark_3]

plt.plot(ranksum(pos, neg))
plt.show()
