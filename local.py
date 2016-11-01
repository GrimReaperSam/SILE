# from skimage.io import imread
# import os
# from src.descriptors.descriptors import *
# from src.collector import ranksum, delta_z
# import numpy as np
#
# gray_hist = GrayLevelHistogram()
#
# darks = os.listdir('DB/dark')[:4]
# print(darks)
# dark_hists = np.zeros((len(darks), *gray_hist.shape))
# for index, image in enumerate(darks):
#     dark = imread('DB/dark/' + image)
#     dark_hists[index] = gray_hist.compute(dark)
# print(dark_hists)
#
# lights = os.listdir('DB/white')[:4]
# print(lights)
# light_hists = np.zeros((len(lights), *gray_hist.shape))
# for index, image in enumerate(lights):
#     light = imread('DB/white/' + image)
#     light_hists[index] = gray_hist.compute(light)
# print(light_hists)
# rsum = ranksum(dark_hists, light_hists)
# print()
# print(rsum)
# print(delta_z(rsum))


# if len(rsum.shape) == 1:
#     plt.plot(ranksum(dark_hists, light_hists))
# elif len(rsum.shape) == 2:
#     plt.imshow(rsum, cmap='gray')
# plt.show()
#
#
# import logging
# logging.getLogger().setLevel(logging.INFO)
#
# from src.collector import *
# from src.descriptors.descriptors_calculator import DescriptorProvider
#
# class MyImageProvider(ImageProvider):
#     def provide(self, keyword):
#         return None, None
#
#
# class MyDescriptorProvider(DescriptorProvider):
#     def provide(self, image_id, descriptor_name):
#         return None
#
#     def save(self, image_id, descriptor_name, description):
#         return None
#
#
# class MyZProvider(ZProvider):
#     def provide(self, keyword):
#         return None
#
#     def save(self, keyword, z_values_map):
#         return None
#
# a = ZCollector(MyDescriptorProvider(), MyImageProvider(), MyZProvider())
#
# hist = a.collect('a')
# print(hist)


from skimage.io import imread
from src.descriptors.descriptors import GrayLevelHistogram
import numpy as np

glh = GrayLevelHistogram()
image = imread('DB/59898.jpg')
np.set_printoptions(suppress=True)
print(glh.compute(image))
