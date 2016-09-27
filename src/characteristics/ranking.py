import numpy as np


def ranksum(c_pos, c_neg):
    concatenated_characteristics = np.concatenate((c_pos, c_neg))
    sorted_characteristics = np.sort(concatenated_characteristics)

    positive_indices, = np.where(np.in1d(sorted_characteristics, c_pos))
    ranksum_t = np.sum(positive_indices)

    positive_count = len(c_pos)
    negative_count = len(c_neg)
    expected_mean = positive_count * (positive_count + negative_count + 1) / 2
    expected_variance = positive_count * negative_count * (positive_count + negative_count + 1) / 12

    z = (ranksum_t - expected_mean) / expected_variance

    return ranksum_t, expected_mean, expected_variance, z