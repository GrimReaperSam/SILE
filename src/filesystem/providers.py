from skimage.io import imread

from ..collector.z_collector import ZProvider, ImageProvider

from .flicker_reader import FlickerDB


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
        pos = [imread(self.flicker_db.rgb_from_id(tag_id)) for tag_id in tag_ids[:50]]
        neg = [imread(self.flicker_db.rgb_from_id(tag_not_id)) for tag_not_id in tag_not_ids[:50]]
        return pos, neg
