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