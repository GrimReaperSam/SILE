import logging

from src.collector import ZCollector
from src.filesystem.providers import MyDescriptorProvider, MyZProvider

logging.getLogger().setLevel(logging.INFO)

z_collector = ZCollector(MyDescriptorProvider(), MyZProvider())

z_collector.collect('aeroplane')
z_collector.collect('banana')
z_collector.collect('strawberry')
z_collector.collect('sunflower')
z_collector.collect('candle')
z_collector.collect('autumn')
