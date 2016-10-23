import pandas as pd


def read(flicker_file):
    images = pd.read_table(flicker_file, sep='\t', header=None, names=['id', 'tags'])
    images.tags = images.tags.str.translate(str.maketrans("<>", "  ")).str.split()
    return images
