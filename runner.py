# from skimage.io import imread
# import matplotlib.pyplot as plt
# import os

# from src.characteristics.descriptors import *
# from src.characteristics import ranksum, delta_z

# gray_hist = LightnessFourier()

# dark_hists = []
# for i in os.listdir('DB/dark'):
#     dark = imread('DB/dark/' + i)
#     dark_hists.append(gray_hist.compute(dark))
#
# light_hists = []
# for i in os.listdir('DB/white'):
#     light = imread('DB/white/' + i)
#     light_hists.append(gray_hist.compute(light))
#
# rsum = ranksum(dark_hists, light_hists)
# print(delta_z(rsum))
#
# if len(rsum.shape) == 1:
#     plt.plot(ranksum(dark_hists, light_hists))
# elif len(rsum.shape) == 2:
#     plt.imshow(rsum, cmap='gray')
# plt.show()
#


# from src.characteristics.descriptors_calculator import DescriptorsCalculator
#
# dc = DescriptorsCalculator()
#
# i = os.listdir('DB/dark')
# images = list(map(lambda n: imread('DB/dark/' + n), i))
# chars = dc.describe_set(images, 'lightness_layout')
# print(chars.shape)
# print(chars[0:5])


# from src.collector import *
#
#
# class MyImageProvider(ImageProvider):
#     def provide(self, keyword):
#         i = os.listdir('DB/dark')[:5]
#         pos = [imread('DB/dark/' + n) for n in i]
#         i = os.listdir('DB/white')[:5]
#         neg = [imread('DB/white/' + n) for n in i]
#         return pos, neg
#
#
# class MyZProvider(ZProvider):
#     def exists(self, keyword):
#         return False
#
#     def provide(self, keyword):
#         return keyword * 3, keyword
#
# a = ZCollector(MyImageProvider(), MyZProvider())
#
# hist = a.collect('a')
# print(hist)

from src.filesystem.providers import *
from src.collector import *
a = ZCollector(MyDescriptorProvider(), MyImageProvider(), MyZProvider())
hist = a.collect('bw')
print(hist)
