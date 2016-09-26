from skimage import exposure, img_as_float


def gray_level(image):
    image = img_as_float(image)
    (hist, centers) = exposure.histogram(image, nbins=16)
    return hist, centers