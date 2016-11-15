import numpy as np
import pickle

from ..collector.z_collector import ZProvider
from ..descriptors.descriptors_calculator import DescriptorProvider

from .config_paths import z_value_from_keyword, descriptor_from_id


# TODO try to find a better way!
class MyZProvider(ZProvider):
    def provide(self, keyword):
        z_value_path = z_value_from_keyword(keyword)
        if z_value_path.exists():
            return pickle.load(open(str(z_value_path), 'rb'))
        else:
            return None

    def save(self, keyword, z_collection):
        z_value_path = z_value_from_keyword(keyword)
        z_value_path.parent.mkdir(exist_ok=True, parents=True)
        pickle.dump(z_collection, open(str(z_value_path), 'wb'))


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
