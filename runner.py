import logging
from src.filesystem.providers import *
from src.collector import *

logging.getLogger().setLevel(logging.INFO)

a = ZCollector(MyDescriptorProvider(), MyImageProvider(), MyZProvider())
hist = a.collect('night')
print(hist)

b = ImageComparator(a)
b.compare(12, 'night')
