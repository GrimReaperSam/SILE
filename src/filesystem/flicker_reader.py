import logging
import os

import pandas as pd

from src.config_paths import *


class FlickerDB:
    """
    This class is responsible for reading the FLICKR DB and processing it.
    It exposes methods to search for images by tag
    """
    def __init__(self):
        self.images = None
        self.__read_images()

    def ids_by_tag(self, tag):
        """
        :param tag:
        :return: A tuple (positive, negative) splitting the db into images having and not having the given tag
        """
        tags_series = self.images.tags.map(lambda t: tag in t)
        return self.images[tags_series].id.values, self.images[~tags_series].id.values

    def all_ids(self):
        """
        :return: All the id values in a list
        """
        return self.images.id.values

    def __read_images(self):
        """
        Initializes the flickr db from the file, and saves the processed format into a pickle for faster loading
        :return: Nothing
        """
        logging.info('Start reading pickle db')
        flicker_db_pickle = Path(os.getcwd()) / FLICKER_PANDAS_STRUCTURE
        if flicker_db_pickle.exists():
            self.images = pd.read_pickle(str(flicker_db_pickle))
        else:
            self.images = pd.read_table(FLICKER_BASE_TXT, sep='\t', header=None, names=['id', 'tags'])
            self.images.tags = self.images.tags.map(lambda t: str(t).translate(str.maketrans("<>", "  ")).split())
            self.images.to_pickle(str(flicker_db_pickle))
        logging.info('End reading pickle db')
