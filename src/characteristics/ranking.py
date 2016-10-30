import logging
import math
import numpy as np
from scipy.stats import rankdata

from ..shared import *


def delta_z(z_matrix):
    return z_matrix.max() - z_matrix.min()


def ranksum(positives, negatives):
    characteristic_shape = np.array(positives[0]).shape

    positive_matrix = np.stack(positives, axis=-1)
    negative_matrix = np.stack(negatives, axis=-1)
    z = np.zeros(characteristic_shape)
    for indices in np.ndindex(characteristic_shape):
        light_pos = positive_matrix[indices]
        light_neg = negative_matrix[indices]

        a = ranksum_characteristic(light_pos, light_neg)
        z[indices] = a[3]
    return z


def ranksum_characteristic(c_pos, c_neg):
    concatenated_characteristics = np.concatenate((c_pos, c_neg))
    ranks = rankdata(concatenated_characteristics)

    positive_count = len(c_pos)
    negative_count = len(c_neg)

    ranksum_t = ranks[:positive_count].sum()
    expected_mean = positive_count * (positive_count + negative_count + 1) / 2.0
    expected_variance = positive_count * negative_count * (positive_count + negative_count + 1) / 12.0
    z = (ranksum_t - expected_mean) / np.sqrt(expected_variance)

    adjusted_t = REFERENCE_SAMPLE_SIZE / positive_count * ranksum_t
    adjusted_mean = REFERENCE_SAMPLE_SIZE / positive_count * expected_mean
    adjusted_variance = REFERENCE_SAMPLE_SIZE ** 2 / (positive_count * negative_count) * expected_variance
    adjusted_z = math.sqrt((REFERENCE_SAMPLE_SIZE * negative_count) / (positive_count * REFERENCE_SAMPLE_SIZE)) * z

    logging.info("Computing ranksum, positives: %s, negatives: %s, ranksum: %s, z: %s" %
                 (positive_count, negative_count, ranksum_t, z))

    return adjusted_t, adjusted_mean, adjusted_variance, adjusted_z
