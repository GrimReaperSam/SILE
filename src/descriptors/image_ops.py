import numpy as np


def rgb_to_lab(rgb_image):
    xyz_transformation_matrix = np.array([[0.412453, 0.357580, 0.180423],
                                          [0.212671, 0.715160, 0.072169],
                                          [0.019334, 0.119193, 0.950227]])
    threshold = 0.008856
    if rgb_image.max() > 1.0:
        divided = rgb_image / 255.0

    (w, h, d) = rgb_image.shape
    rgb = np.rollaxis(divided, 2).reshape(d, h * w)

    xyz = np.dot(xyz_transformation_matrix, rgb)
    # Normalizing for D65 white point
    xyz = xyz / np.array([[0.950456], [1.0], [1.088754]])

    xyz_threshold = xyz > threshold
    f_xyz = xyz_threshold * xyz ** (1 / 3) + ~xyz_threshold * (7.787 * xyz + 16 / 116)

    l = xyz_threshold[1] * (116 * xyz[1] ** (1 / 3) - 16) + ~xyz_threshold[1] * (903.3 * xyz[1])
    l = l.reshape(w, h, 1)
    a = 500 * (f_xyz[0] - f_xyz[1]).reshape(w, h, 1)
    b = 200 * (f_xyz[1] - f_xyz[2]).reshape(w, h, 1)

    return np.concatenate([l, a, b], axis=2)
