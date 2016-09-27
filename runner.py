from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt

from src.characteristics import gray_level, ranksum


light_1 = imread('resources/2452.jpeg')
grey = rgb2gray(light_1)
hist_light_1, centers = gray_level(grey)

light_2 = imread('resources/351519.jpeg')
grey = rgb2gray(light_2)
hist_light_2, centers = gray_level(grey)

dark_1 = imread('resources/5211.jpeg')
grey = rgb2gray(dark_1)
hist_dark_1, centers = gray_level(grey)

dark_2 = imread('resources/9716.jpeg')
grey = rgb2gray(dark_2)
hist_dark_2, centers = gray_level(grey)

z = []
for i in range(16):
    light_pos = np.array([hist_light_1[i], hist_light_2[i]])
    light_neg = np.array([hist_dark_1[i], hist_dark_2[i]])

    a = ranksum(light_pos, light_neg)
    print(a)
    z.append(a[3])

print(z)
