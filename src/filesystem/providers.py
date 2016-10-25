import numpy as np
import pandas as pd

from ..collector.z_collector import ZProvider, ImageProvider
from ..characteristics.descriptors_calculator import DescriptorProvider

from .flicker_reader import FlickerDB
from .config_paths import z_value_from_keyword, descriptor_from_id


# TODO try to find a better way!
class MyZProvider(ZProvider):
    def provide(self, keyword):
        z_value_path = z_value_from_keyword(keyword)
        if z_value_path.exists():
            store = pd.HDFStore(str(z_value_path))
            z_values = {}
            for key in store.keys():
                z_values[key] = store[key].as_matrix()
            store.close()
            return z_values
        else:
            return None

    def save(self, keyword, z_values_map):
        z_value_path = z_value_from_keyword(keyword)
        z_value_path.parent.mkdir(exist_ok=True, parents=True)
        store = pd.HDFStore(str(z_value_path))
        for key, z_value_matrix in z_values_map.items():
            if z_value_matrix.ndim == 1:
                store.put(key, pd.Series(z_value_matrix))
            elif z_value_matrix.ndim == 2:
                store.put(key, pd.DataFrame(z_value_matrix))
            elif z_value_matrix.ndim == 3:
                store.put(key, pd.Panel(z_value_matrix))
            else:
                store.put(key, pd.Panel4D(z_value_matrix), format='table')
        store.close()


class MyImageProvider(ImageProvider):
    def __init__(self):
        self.flicker_db = FlickerDB()

    def provide(self, keyword):
        tag_ids, tag_not_ids = self.flicker_db.ids_by_tag(keyword)
        pos = tag_ids[:50].tolist()
        neg = tag_not_ids[:50].tolist()
        return pos, neg


class MyDescriptorProvider(DescriptorProvider):
    def provide(self, image_id, descriptor_name):
        descriptor_path = descriptor_from_id(image_id, descriptor_name)
        if descriptor_path.exists():
            return np.load(str(descriptor_path))
        else:
            return None

    def save(self, image_id, descriptor_name, description):
        descriptor_path = descriptor_from_id(image_id, descriptor_name)
        descriptor_path.parent.mkdir(exist_ok=True, parents=True)
        description.dump(str(descriptor_path))
