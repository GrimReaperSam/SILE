import math
import numpy as np

from ..shared import *


def ranksum(histograms_positive, histograms_negative):
    positive_matrix = np.vstack(histograms_positive)
    negative_matrix = np.vstack(histograms_negative)
    z = []
    for i in range(DEFAULT_1D_HISTOGRAM_NBINS):
        light_pos = positive_matrix[:, i]
        light_neg = negative_matrix[:, i]

        a = ranksum_characteristic(light_pos, light_neg)
        z.append(a[3])
    return z


def ranksum_characteristic(c_pos, c_neg):
    concatenated_characteristics = np.concatenate((c_pos, c_neg))
    sorted_characteristics = np.sort(concatenated_characteristics)

    positive_indices, = np.where(np.in1d(sorted_characteristics, c_pos))
    ranksum_t = np.sum(positive_indices) + np.size(positive_indices)  # Adding the size to account for +1 for each index

    positive_count = len(c_pos)
    negative_count = len(c_neg)
    expected_mean = positive_count * (positive_count + negative_count + 1) / 2
    expected_variance = positive_count * negative_count * (positive_count + negative_count + 1) / 12
    z = (ranksum_t - expected_mean) / np.sqrt(expected_variance)

    adjusted_t = REFERENCE_SAMPLE_SIZE / positive_count * ranksum_t
    adjusted_mean = REFERENCE_SAMPLE_SIZE / positive_count * expected_mean
    adjusted_variance = REFERENCE_SAMPLE_SIZE ** 2 / (positive_count * negative_count) * expected_variance
    adjusted_z = math.sqrt(REFERENCE_SAMPLE_SIZE ** 2 / (positive_count * negative_count)) * z

    return adjusted_t, adjusted_mean, adjusted_variance, adjusted_z
