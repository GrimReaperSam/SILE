from pathlib import Path

# BASE PATH
BASE_PATH = Path('/datafast/alindner/mirflickr')
DB_PATH = Path('DB')
WORK_PATH = Path('/data/lahoud/DB')

# MIR FLICKER BASE FILE
FLICKER_BASE_TXT = BASE_PATH / 'id_kw_mirflickr.txt'
FLICKER_PANDAS_STRUCTURE = WORK_PATH / 'mirflickr_pd.pkl'

# DB PATHS
RGB_IMAGES = BASE_PATH / DB_PATH / 'photos/1024'
LAB_IMAGES = BASE_PATH / DB_PATH / 'photos/cielab'

# DESCRIPTOR PATHS
DESCRIPTOR_PATHS = WORK_PATH / 'descriptors'

# Z-VALUE PATHS
Z_VALUE_PATHS = WORK_PATH / 'z-values'


def path_from_id(image_id):
    return Path(__get_prefix(image_id)) / ('%s.jpg' % image_id)


def rgb_from_id(image_id):
    return RGB_IMAGES / path_from_id(image_id)


def lab_from_id(image_id):
    return LAB_IMAGES / path_from_id(image_id)


def descriptor_from_id(image_id, descriptor_name):
    return DESCRIPTOR_PATHS / __get_prefix(image_id) / str(image_id) / ('%s.pkl' % descriptor_name)


def z_value_from_keyword(keyword):
    return Z_VALUE_PATHS / ('%s.pkl' % keyword)


def __get_prefix(image_id):
    if image_id > 9:
        return str(image_id)[-2:]
    else:
        return "0%s" % str(image_id)[-1]