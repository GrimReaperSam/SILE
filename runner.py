import logging
from pathlib import Path

from skimage.io import imsave

from src.filesystem.providers import *
from src.collector import *

logging.getLogger().setLevel(logging.INFO)

a = ZCollector(MyDescriptorProvider(), MyZProvider())
hist = a.collect('night')
print(hist)

b = ImageComparator(a)

parent_path = Path('/data/lahoud/DB/examples')
parent_path.mkdir(exist_ok=True, parents=True)

for i in range(1, 20):
    result = b.compare(i, 'night', 2)
    imsave(str(parent_path / 'result-%s.jpg' % i), result)
