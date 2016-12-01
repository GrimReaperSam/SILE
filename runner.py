import logging
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
from pathlib import Path

from skimage.io import imread, imsave

from src.enhancer import ImageComparator
from src.enhancer.enhancers import ENHANCERS

from src.config_paths import z_value_from_keyword


LABELS = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow',
          'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train',
          'tvmonitor', 'void']


def color_map(N=256, normalized=False):
    def bitget(byteval, idx):
        return (byteval & (1 << idx)) != 0

    dtype = 'float32' if normalized else 'uint8'
    cmap = np.zeros((N, 3), dtype=dtype)
    for i in range(N):
        r = g = b = 0
        c = i
        for j in range(8):
            r |= bitget(c, 0) << 7 - j
            g |= bitget(c, 1) << 7 - j
            b |= bitget(c, 2) << 7 - j
            c >>= 3
        cmap[i] = np.array([r, g, b])
    cmap = cmap / 255 if normalized else cmap
    return cmap


def color_map_array():
    cmap = color_map()
    class_colors_ = {}
    for i in range(len(LABELS)):
        class_colors_[LABELS[i]] = cmap[i]
    class_colors_['void'] = cmap[-1]
    return class_colors_


if __name__ == '__main__':
    prefix = '/home/fayez/Downloads'

    logging.getLogger().setLevel(logging.INFO)
    class_colors = color_map_array()

    segmented = pd.read_csv('%s/VOCdevkit/VOC2012/ImageSets/Segmentation/train.txt' % prefix, header=None, names=['file'])

    seg_kw = LABELS[16]
    df = pd.read_csv('%s/VOCdevkit/VOC2012/ImageSets/Main/%s_train.txt' % (prefix, seg_kw),
                     header=None, sep=r'\s+', names=['file', 'label'])
    plants = df[df['label'] == 1]

    seg_plants = pd.merge(plants, segmented, how='right', on='file', right_index=False, left_index=False)
    files = seg_plants['file'].tolist()

    base_dir = Path('/data/lahoud/DB/examples')
    base_dir.mkdir(exist_ok=True, parents=True)

    for image_file in files[:30]:
        seg = imread('%s/VOCdevkit/VOC2012/SegmentationClass/%s.png' % (prefix, image_file))
        image = imread('%s/VOCdevkit/VOC2012/JPEGImages/%s.jpg' % (prefix, image_file))
        seg_b = np.all(seg == class_colors[seg_kw], axis=2)

        filename = z_value_from_keyword(seg_kw)
        z_collection = pickle.load(open(str(filename), 'rb'))

        save_dir = base_dir / seg_kw / image_file
        save_dir.mkdir(exist_ok=True, parents=True)

        image_comparator = ImageComparator()
        key, z_delta = image_comparator.compare(image, z_collection)

        # Global enhancement
        result_g = ENHANCERS[key].enhance(image, z_delta, 4)

        # Mask based enhancement
        weight_map = ENHANCERS[key].compute_weight_map(image, z_collection.descriptors[key].descriptor)
        result_w = weight_map * result_g + (1 - weight_map) * image
        result_w = result_w.astype(np.uint8)

        # Local enhancement
        result_l = ENHANCERS[key].enhance(image, z_delta, 4, mask=seg_b)

        imsave(str(save_dir / 'original.png'), image)
        imsave(str(save_dir / 'global.png'), result_g)
        imsave(str(save_dir / 'weight-map.png'), (weight_map * 255).astype(np.uint8))
        imsave(str(save_dir / 'weighted.png'), result_w)
        imsave(str(save_dir / 'segmentation.png'), seg_b.astype(np.uint8) * 255)
        imsave(str(save_dir / 'local.png'), result_l)

        # fig = plt.figure()
        # fig.text(0.51, 0.88, 'Full descriptor', ha='center', va='center')
        # fig.text(0.84, 0.88, 'Segmented descriptor', ha='center', va='center')
        # fig.text(0.05, 0.75, 'Global', ha='center', va='center', rotation='vertical')
        # fig.text(0.05, 0.45, 'Weight Map', ha='center', va='center', rotation='vertical')
        # fig.text(0.05, 0.19, 'Local', ha='center', va='center', rotation='vertical')
        #
        # plt.subplot(3, 3, 1)
        # plt.imshow(image)
        # plt.axis('off')
        #
        # plt.subplot(3, 3, 2)
        # plt.imshow(result_g)
        # plt.axis('off')
        #
        # plt.subplot(3, 3, 4)
        # plt.imshow(weight_map)
        # plt.axis('off')
        #
        # plt.subplot(3, 3, 5)
        # plt.imshow(result_w)
        # plt.axis('off')
        #
        # a = plt.subplot(3, 3, 7)
        # plt.imshow(seg_b, cmap='gray')
        # plt.axis('off')
        #
        # plt.subplot(3, 3, 8)
        # plt.imshow(result_l)
        # plt.axis('off')

        key, z_delta = image_comparator.compare(image, z_collection, mask=seg_b)

        # Global enhancement
        result_g = ENHANCERS[key].enhance(image, z_delta, 4)

        # Mask based enhancement
        weight_map = ENHANCERS[key].compute_weight_map(image, z_collection.descriptors[key].descriptor)
        result_w = weight_map * result_g + (1 - weight_map) * image
        result_w = result_w.astype(np.uint8)

        # Local enhancement
        result_l = ENHANCERS[key].enhance(image, z_delta, 4, mask=seg_b)

        imsave(str(save_dir / 'global-lenh.png'), result_g)
        imsave(str(save_dir / 'weighted-lenh.png'), result_w)
        imsave(str(save_dir / 'local-lenh.png'), result_l)

        # plt.subplot(3, 3, 3)
        # plt.imshow(result_g)
        # plt.axis('off')
        #
        # plt.subplot(3, 3, 6)
        # plt.imshow(result_w)
        # plt.axis('off')
        #
        # plt.subplot(3, 3, 9)
        # plt.imshow(result_l)
        # plt.axis('off')

        # plt.tight_layout()
        # plt.subplots_adjust(top=0.85)
        # plt.suptitle('%s - %s' % (image_file, key))
        #
        # plt.show()
