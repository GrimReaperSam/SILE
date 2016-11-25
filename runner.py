import logging
from pathlib import Path

from skimage.io import imread, imsave

from src.filesystem.providers import *
from src.filesystem.config_paths import rgb_from_id
from src.collector import ZCollector
from src.enhancer import ImageEnhancer

logging.getLogger().setLevel(logging.INFO)

a = ZCollector(MyDescriptorProvider(), MyZProvider())
keyword_descriptors = a.collect('night')

b = ImageEnhancer()

parent_path = Path('/data/lahoud/DB/examples')
parent_path.mkdir(exist_ok=True, parents=True)

for i in range(1, 20):
    image = imread(rgb_from_id(i))
    imsave(str(parent_path / ('image-%s.jpg' % i)), image)
    result = b.enhance(image, 'night', 2)
    imsave(str(parent_path / ('result-%s.jpg' % i)), result)
