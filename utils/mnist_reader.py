import os
import gzip
import numpy as np


def load_mnist(path, label_suffix, img_suffix, kind):

    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-%s'
                               % (kind, label_suffix))
    images_path = os.path.join(path,
                               '%s-%s'
                               % (kind, img_suffix))

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels