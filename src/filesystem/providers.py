from ..collector.z_collector import ZProvider, ImageProvider
from ..characteristics.descriptors_calculator import DescriptorProvider

from .flicker_reader import FlickerDB
from .config_paths import descriptor_from_id

import numpy as np


class MyZProvider(ZProvider):
    def exists(self, keyword):
        return False

    def provide(self, keyword):
        return None, None


class MyImageProvider(ImageProvider):
    def __init__(self):
        self.flicker_db = FlickerDB()

    def provide(self, keyword):
        tag_ids, tag_not_ids = self.flicker_db.ids_by_tag(keyword)
        pos = tag_ids[:20].tolist()
        neg = tag_not_ids[:20].tolist()
        return pos, neg


class MyDescriptorProvider(DescriptorProvider):
    def provide(self, image_id, descriptor_name):
        descriptor_path = descriptor_from_id(image_id, descriptor_name)
        if descriptor_path.exists():
            return np.load(descriptor_path)
        else:
            return None

    def save(self, image_id, descriptor_name, description):
        descriptor_path = descriptor_from_id(image_id, descriptor_name)
        description.dump(descriptor_path)
