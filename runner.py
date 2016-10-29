# from skimage.io import imread
# import os
#
# from src.characteristics.descriptors import *
# from src.characteristics import ranksum, delta_z
# import numpy as np
#
# gray_hist = GrayLevelHistogram()
#
# darks = os.listdir('DB/dark')
# dark_hists = np.zeros((len(darks), *gray_hist.shape))
# for index, image in enumerate(darks):
#     dark = imread('DB/dark/' + image)
#     dark_hists[index] = gray_hist.compute(dark)
#
# lights = os.listdir('DB/white')
# light_hists = np.zeros((len(lights), *gray_hist.shape))
# for index, image in enumerate(lights):
#     light = imread('DB/white/' + image)
#     light_hists[index] = gray_hist.compute(light)
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

# i = imread('DB/dark/8.jpg')
# dh = LightnessFourier()
# a = dh.compute(i)
# plt.imshow(a, cmap='gray')
# plt.show()


# import logging
# logging.getLogger().setLevel(logging.INFO)
#
# from src.collector import *
# from src.characteristics.descriptors_calculator import DescriptorProvider
#
# from pathlib import Path
# import os
# import pandas as pd
#
#
# class MyImageProvider(ImageProvider):
#     def provide(self, keyword):
#         i = os.listdir('DB/dark')[:10]
#         pos = ['DB/dark/' + n for n in i]
#         i = os.listdir('DB/white')[:10]
#         neg = ['DB/white/' + n for n in i]
#         return pos, neg
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
#         z_value_path = Path('a.h5')
#         if z_value_path.exists():
#             store = pd.HDFStore(str(z_value_path))
#             z_values = {}
#             for key in store.keys():
#                 z_values[key] = store[key].as_matrix()
#             store.close()
#             return z_values
#         else:
#             return None
#
#     def save(self, keyword, z_values_map):
#         z_value_path = 'a.h5'
#         store = pd.HDFStore(str(z_value_path))
#         for key, z_value_matrix in z_values_map.items():
#             if z_value_matrix.ndim == 1:
#                 store.put(key, pd.Series(z_value_matrix))
#             elif z_value_matrix.ndim == 2:
#                 store.put(key, pd.DataFrame(z_value_matrix))
#             elif z_value_matrix.ndim == 3:
#                 store.put(key, pd.Panel(z_value_matrix))
#             else:
#                 store.put(key, pd.Panel4D(z_value_matrix), format='table')
#         store.close()
#
# a = ZCollector(MyDescriptorProvider(), MyImageProvider(), MyZProvider())
#
# hist = a.collect('a')
# print(hist)

import logging
from src.filesystem.providers import *
from src.collector import *

logging.getLogger().setLevel(logging.INFO)

a = ZCollector(MyDescriptorProvider(), MyImageProvider(), MyZProvider())
hist = a.collect('bw')
print(hist)


# from src.characteristics.descriptors import GrayLevelHistogram
# from skimage.io import imread
# glh = GrayLevelHistogram()
# a = glh.compute(imread('DB/dark/17.jpg'))
# print(a)
