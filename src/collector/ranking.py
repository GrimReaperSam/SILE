import math
import numpy as np
from scipy.stats import rankdata

from src.shared import *


def ranksum(descriptions, positive_indices, negative_indices):
    ranks = np.apply_along_axis(rankdata, 0, descriptions)
    ranksum_array = ranks[positive_indices].sum(axis=0)

    positive_count = positive_indices.size
    positive_ref = REFERENCE_SAMPLE_SIZE
    negative_count = negative_indices.size
    negative_ref = (positive_count + negative_count) - positive_ref

    expected_mean = positive_count * (positive_count + negative_count + 1) / 2.0
    expected_variance = positive_count * negative_count * (positive_count + negative_count + 1) / 12.0
    z = (ranksum_array - expected_mean) / np.sqrt(expected_variance)
    z_star_coefficient = np.sqrt((negative_count * positive_ref)/(positive_count * negative_ref))
    return z_star_coefficient * z


def delta_z(z_matrix):
    return z_matrix.max() - z_matrix.min()
