from skimage.io import imread
from skimage.color import rgb2gray
import matplotlib.pyplot as plt

from src.characteristics import gray_level


image = imread('resources/351519.jpeg')
grey = rgb2gray(image)
hist, centers = gray_level(grey)
width = 0.7 * (centers[1] - centers[0])
print(hist)

plt.bar(centers, hist, align='center', width=width)
plt.show()
