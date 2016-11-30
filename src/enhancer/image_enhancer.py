from src.collector import ZCollector
from src.enhancer.enhancers import ENHANCERS
from src.enhancer.image_comparator import ImageComparator
from src.filesystem.providers import MyDescriptorProvider, MyZProvider


class ImageEnhancer:
    def __init__(self):
        self.z_collector = ZCollector(MyDescriptorProvider(), MyZProvider())
        self.comparator = ImageComparator()

    def enhance(self, image, keyword, strength, mask=None):
        """
        :param image: The image to enhance
        :param keyword: The keyword to use for enhancement
        :param strength: The strength of the enhancement
        :param mask: Mask to apply for the enhancement
                    'weight-map' generates a weight map based on image/z-value correspondance
                    boolean numpy array creates a local enhancement based on the mask
                    None creates a global enhancement
        :return:
        """
        z_collection = self.z_collector.collect(keyword)
        key, z_delta = self.comparator.compare(image, z_collection)
        if mask == 'weight-map':
            enhanced = ENHANCERS[key].enhance(image, z_delta, strength)
            weight_map = ENHANCERS[key].compute_weight_map(image, z_collection.descriptors[key].descriptor)
            return weight_map * enhanced + (1 - weight_map) * image
        return ENHANCERS[key].enhance(image, z_delta, strength, mask=mask)


