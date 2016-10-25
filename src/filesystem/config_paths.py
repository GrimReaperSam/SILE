from pathlib import Path

# BASE PATH
BASE_PATH = Path('/datafast/alindner/mirflickr/')
DB_PATH = Path('DB/')

# MIR FLICKER BASE FILE
FLICKER_BASE_TXT = BASE_PATH / 'id_kw_mirflickr.txt'
FLICKER_PANDAS_STRUCTURE = 'mirflickr_pd.pkl'

# DB PATHES
RGB_IMAGES = BASE_PATH / DB_PATH / 'photos/1024'
LAB_IMAGES = BASE_PATH / DB_PATH / 'photos/cielab'


def path_from_id(self, image_id):
    return Path(self.__get_prefix(image_id)) / ("%s.jpg" % image_id)


def rgb_from_id(self, image_id):
    return Path(RGB_IMAGES) / self.path_from_id(image_id)


def lab_from_id(self, image_id):
    return Path(LAB_IMAGES) / self.path_from_id(image_id)


def __get_prefix(image_id):
    if image_id > 9:
        return str(image_id)[-2:]
    else:
        return "0%s" % str(image_id)[-1]