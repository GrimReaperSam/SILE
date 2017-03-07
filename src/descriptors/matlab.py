import numpy as np

# Code reproduced from MATLAB imresize in order to accurately reproduce the results of Lindner
# The resize used by the python libraries doesn't produce similar values as they do different kind of interpolations

def reduce_along_dim(img, dim, weights, indices):
    """
    Perform bilinear interpolation given along the image dimension dim
    -weights are the kernel weights
    -indices are the corresponding indices location
    return img resize along dimension dim
    """
    other_dim = abs(dim - 1)
    if other_dim == 0:  # resizing image width
        weights = np.tile(weights[np.newaxis, :, :, np.newaxis], (img.shape[other_dim], 1, 1, 3))
        out_img = img[:, indices, :] * weights
        out_img = np.sum(out_img, axis=2)
    else:  # resize image height
        weights = np.tile(weights[:, :, np.newaxis, np.newaxis], (1, 1, img.shape[other_dim], 3))
        out_img = img[indices, :, :] * weights
        out_img = np.sum(out_img, axis=1)

    return out_img


def cubic_spline(x):
    """
    Compute the kernel weights
    See Keys, "Cubic Convolution Interpolation for Digital Image
    Processing," IEEE Transactions on Acoustics, Speech, and Signal
    Processing, Vol. ASSP-29, No. 6, December 1981, p. 1155.
    """
    absx = np.abs(x)
    absx2 = absx ** 2
    absx3 = absx ** 3
    kernel_weight = (1.5 * absx3 - 2.5 * absx2 + 1) * (absx <= 1) + (-0.5 * absx3 + 2.5 * absx2 - 4 * absx + 2) * (
        (1 < absx) & (absx <= 2))
    return kernel_weight


def contribution(in_dim_len, out_dim_len, scale):
    """
    Compute the weights and indices of the pixels involved in the cubic interpolation along each dimension.

    output:
    weights a list of size 2 (one set of weights for each dimension). Each item is of size OUT_DIM_LEN*Kernel_Width
    indices a list of size 2(one set of pixel indices for each dimension) Each item is of size OUT_DIM_LEN*kernel_width

    note that if the entire column weights is zero, it gets deleted since those pixels don't contribute to anything
    """
    kernel_width = 4
    if scale < 1:
        kernel_width = 4 / scale

    x_out = np.array(range(1, out_dim_len + 1))
    # project to the input space dimension
    u = x_out / scale + 0.5 * (1 - 1 / scale)

    # position of the left most pixel in each calculation
    l = np.floor(u - kernel_width / 2)

    # maxium number of pixels in each computation
    p = int(np.ceil(kernel_width) + 2)

    indices = np.zeros((l.shape[0], p), dtype=int)
    indices[:, 0] = l

    for i in range(1, p):
        indices[:, i] = indices[:, i - 1] + 1

    # compute the weights of the vectors
    u = u.reshape((u.shape[0], 1))
    u = np.repeat(u, p, axis=1)

    if scale < 1:
        weights = scale * cubic_spline(scale * (indices - u))
    else:
        weights = cubic_spline((indices - u))

    weights_sums = weights.sum(1)
    weights = weights / weights_sums[:, np.newaxis]

    indices -= 1
    indices[indices < 0] = 0
    indices[indices > in_dim_len - 1] = in_dim_len - 1  # clamping the indices at the ends

    valid_cols = ~np.all(weights == 0, axis=0) # find columns that are not all zeros

    indices = indices[:, valid_cols]
    weights = weights[:, valid_cols]

    return weights, indices


def imresize(img, cropped_width, cropped_height):
    """
    Function implementing matlab's imresize functionality default behaviour
    Cubic spline interpolation with Antialiasing correction when scaling down the image.
    """
    width_scale = float(cropped_width) / img.shape[1]
    height_scale = float(cropped_height) / img.shape[0]

    if len(img.shape) == 2:  # Gray Scale Case
        img = np.tile(img[:, :, np.newaxis], (1, 1, 3))  # Broadcast

    order = np.argsort([height_scale, width_scale])
    scale = [height_scale, width_scale]
    out_dim = [cropped_height, cropped_width]

    weights = [0, 0]
    indices = [0, 0]

    for i in range(0, 2):
        weights[i], indices[i] = contribution(img.shape[i], out_dim[i], scale[i])

    for i in range(0, len(order)):
        img = reduce_along_dim(img, order[i], weights[order[i]], indices[order[i]])

    return img.mean(axis=2)

