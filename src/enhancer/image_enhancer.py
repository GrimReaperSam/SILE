from .enhancers import ENHANCERS
from .image_comparator import ImageComparator

from ..collector import ZCollector
from ..filesystem.providers import MyDescriptorProvider, MyZProvider


class ImageEnhancer:
    def __init__(self):
        self.z_collector = ZCollector(MyDescriptorProvider(), MyZProvider())
        self.comparator = ImageComparator()

    def enhance(self, image, keyword, strength, mask=None):
        z_collection = self.z_collector.collect(keyword)
        key, z_delta = self.comparator.compare(image, z_collection)
        return ENHANCERS[key].enhance(image, z_delta, strength, mask=mask)


