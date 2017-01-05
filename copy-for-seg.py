import sys
from shutil import copy2


from src.filesystem import FlickerDB
from src.config_paths import rgb_from_id
from pathlib import Path

if __name__ == '__main__':
    db = FlickerDB()

    pos, _ = db.ids_by_tag(sys.argv[1])

    save_path = Path('/data/lahoud/DB/images/') / sys.argv[1]
    save_path.mkdir(exist_ok=True, parents=True)

    for p in pos:
        img_path = rgb_from_id(p)
        copy2(str(img_path), str(save_path))
