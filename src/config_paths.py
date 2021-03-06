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

# MASKS PATHS
MASKS_PATH = WORK_PATH / 'masks'

# DESCRIPTOR PATHS
DESCRIPTOR_PATHS = WORK_PATH / 'descriptors'

# Z-VALUE PATHS
Z_VALUE_PATHS = WORK_PATH / 'z-values'

# COLLECTION PATHS
COLLECTIONS_PATHS = WORK_PATH / 'collections'

# RANKS PATHS
RANKS_PATHS = WORK_PATH / 'ranks'


def path_from_id(image_id):
    return Path(__get_prefix(image_id)) / ('%s.jpg' % image_id)


def rgb_from_id(image_id):
    return RGB_IMAGES / path_from_id(image_id)


def mask_from_id(image_id):
    return MASKS_PATH / path_from_id(image_id)


def lab_from_id(image_id):
    return LAB_IMAGES / __get_prefix(image_id) / ('%s.mat' % image_id)


def descriptor_from_id(image_id, descriptor_name):
    return DESCRIPTOR_PATHS / __get_prefix(image_id) / str(image_id) / ('%s.pkl' % descriptor_name)


def z_value_from_keyword(keyword, local=False):
    if local:
        return Z_VALUE_PATHS / ('%s-local.pkl' % keyword)
    return Z_VALUE_PATHS / ('%s.pkl' % keyword)


def collections_from_descriptor(descriptor_name):
    return COLLECTIONS_PATHS / ('%s.pkl' % descriptor_name)


def ranks_from_descriptor(descriptor_name):
    return RANKS_PATHS / ('%s.npz' % descriptor_name)


def __get_prefix(image_id):
    if image_id > 9:
        return str(image_id)[-2:]
    else:
        return "0%s" % str(image_id)[-1]
