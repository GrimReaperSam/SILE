from pathlib import Path
import os

import pandas as pd

from .config_paths import *


class FlickerDB:
    def __init__(self):
        self.images = None
        self.read_images()

    def read_images(self):
        flicker_db_pickle = Path(os.getcwd()) / FLICKER_PANDAS_STRUCTURE
        if flicker_db_pickle.exists():
            self.images = pd.read_pickle(str(flicker_db_pickle))
        else:
            self.images = pd.read_table(FLICKER_BASE_TXT, sep='\t', header=None, names=['id', 'tags'])
            self.images.tags = self.images.tags.str.translate(str.maketrans("<>", "  ")).str.split()
            self.images.to_pickle(str(flicker_db_pickle))

