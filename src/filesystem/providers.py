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
        pos = tag_ids[:20].tolist()
        neg = tag_not_ids[:20].tolist()
        return pos, neg
