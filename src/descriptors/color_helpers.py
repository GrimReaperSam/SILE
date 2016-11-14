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


def lab_to_rgb(lab):
    h, w, d = lab.shape
    lab = lab.reshape(h * w, d)

    l = lab[..., 0]
    a = lab[..., 1]
    b = lab[..., 2]

    # Thresholds
    threshold_y = 0.008856
    threshold_xz = 0.206893

    # Compute Y
    f_y = ((l + 16) / 116) ** 3
    y_greater = f_y > threshold_y
    f_y = (~y_greater) * (l / 903.3) + y_greater * f_y
    y = f_y

    # Alter f_y slightly for further calculations
    f_y = y_greater * (f_y ** (1 / 3)) + (~y_greater) * (7.787 * f_y + 16 / 116)
    # Compute X
    f_x = a / 500 + f_y
    x_greater = f_x > threshold_xz
    x = (x_greater * (f_x ** 3) + (~x_greater) * ((f_x - 16 / 116) / 7.787))
    # Compute Z
    f_z = f_y - b / 200
    z_greater = f_z > threshold_xz
    z = (z_greater * (f_z ** 3) + (~z_greater) * ((f_z - 16 / 116) / 7.787))

    # Normalizing for D65 white point
    x *= 0.950456
    z *= 1.088754

    # XYZ to RGB
    xyz_transformation_matrix = [[3.240479, -1.537150, -0.498535],
                                 [-0.969256, 1.875992, 0.041556],
                                 [0.055648, -0.204043, 1.057311]]

    xyz = np.vstack([x, y, z])
    rgb = np.maximum(np.minimum(np.dot(xyz_transformation_matrix, xyz), 1), 0) * 255
    return rgb.T.reshape(h, w, d).astype(np.uint8)


def lab_to_lch(lab):
    h, w, d = lab.shape

    l_ = lab[..., 0].reshape(h, w, 1)
    c_ = np.sqrt(lab[..., 1] ** 2 + lab[..., 2] ** 2).reshape(h, w, 1)
    h_ = 180 / np.pi * np.arctan2(lab[..., 2], lab[..., 1]).reshape(h, w, 1)
    neg = h_ < 0
    h_[neg] += 360

    return np.concatenate([l_, c_, h_], axis=2)


def lch_to_lab(lch):
    lab = np.asarray(lch)
    c, h = lch[..., 1], lch[..., 2] * np.pi / 180
    lab[..., 1], lab[..., 2] = c * np.cos(h), c * np.sin(h)
    return lab