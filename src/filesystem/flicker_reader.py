from pathlib import Path
import os

import pandas as pd

from .config_paths import *


class FlickerDB:
    def __init__(self):
        self.images = None
        self.__read_images()

    def ids_by_tag(self, tag):
        return self.images[self.images.tags.map(lambda t: tag in t)].id

    def path_from_id(self, image_id):
        return Path(self.__get_prefix(image_id)) / ("%s.jpg" % image_id)

    def __read_images(self):
        flicker_db_pickle = Path(os.getcwd()) / FLICKER_PANDAS_STRUCTURE
        if flicker_db_pickle.exists():
            self.images = pd.read_pickle(str(flicker_db_pickle))
        else:
            self.images = pd.read_table(FLICKER_BASE_TXT, sep='\t', header=None, names=['id', 'tags'])
            self.images.tags = self.images.tags.map(lambda t: str(t).translate(str.maketrans("<>", "  ")).split())
            self.images.to_pickle(str(flicker_db_pickle))

    @staticmethod
    def __get_prefix(image_id):
        if image_id > 9:
            return str(image_id)[-2:]
        else:
            return "0%s" % str(image_id)[-1]