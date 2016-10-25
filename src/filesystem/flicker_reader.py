import os
import pandas as pd

from .config_paths import *


class FlickerDB:
    def __init__(self):
        self.images = None
        self.__read_images()

    def ids_by_tag(self, tag):
        tags_series = self.images.tags.map(lambda t: tag in t)
        return self.images[tags_series].id, self.images[~tags_series].id

    def __read_images(self):
        flicker_db_pickle = Path(os.getcwd()) / FLICKER_PANDAS_STRUCTURE
        if flicker_db_pickle.exists():
            self.images = pd.read_pickle(str(flicker_db_pickle))
        else:
            self.images = pd.read_table(FLICKER_BASE_TXT, sep='\t', header=None, names=['id', 'tags'])
            self.images.tags = self.images.tags.map(lambda t: str(t).translate(str.maketrans("<>", "  ")).split())
            self.images.to_pickle(str(flicker_db_pickle))
