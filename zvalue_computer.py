from src.collector import ZCollector
from src.filesystem.providers import *

collector = ZCollector(MyDescriptorProvider(), MyZProvider())

keywords = ['bee', 'butterflies', 'candle', 'ferrari', 'hamster', 'strawberry', 'sunflower']

for k in keywords:
    collector.collect(k)
