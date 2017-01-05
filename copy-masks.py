import sys
from shutil import copy2


from src.filesystem import FlickerDB
from src.config_paths import rgb_from_id
from pathlib import Path


def __get_prefix(image_id):
    if image_id > 9:
        return str(image_id)[-2:]
    else:
        return "0%s" % str(image_id)[-1]


if __name__ == '__main__':
    keywords = ['banana', 'boeing', 'cheese', 'dessert', 'ferrari', 'lily',
                'orchid', 'strawberry', 'sunflower', 'tulip']

    base_path = Path('/data/bjin/Mirflickr/masks')

    save_path = Path('/data/lahoud/DB/masks')
    save_path.mkdir(exist_ok=True, parents=True)

    for kw in keywords:
        origin = base_path / kw

        for image in origin.iterdir():
            name = image.stem
            name_int = int(name)

            prefix = __get_prefix(name_int)
            save_in = save_path / prefix
            save_in.mkdir(exist_ok=True, parents=True)

            copy2(str(image), str(save_in / image.name))