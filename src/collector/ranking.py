from scipy.stats import rankdata

from src.config_paths import ranks_from_descriptor
from src.shared import *


def ranksum(descriptor_name, descriptions, positive_indices, negative_indices, local=False):
    """
    Calculates the ranksum for the whole descriptors matrix
    :param descriptor_name: The name of the descriptor in order to store the ranksum matrix
    :param descriptions: The matrix of all the image descriptors
    :param positive_indices: The indices of the positively tagged descriptors
    :param negative_indices: The indices of the negatively tagged descriptors
    :param local: Whether to calculate local or global z-values
    :return: A ranksum matrix for the given descriptor
    """
    if local:
        ranks = np.apply_along_axis(rankdata, 0, descriptions)
    else:
        ranks_path = ranks_from_descriptor(descriptor_name)
        if not ranks_path.exists():
            ranks = np.apply_along_axis(rankdata, 0, descriptions)
            ranks_path.parent.mkdir(exist_ok=True, parents=True)
            np.savez_compressed(str(ranks_path), ranks=ranks)
        else:
            npz_file = np.load(str(ranks_path))
            ranks = npz_file['ranks']

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
