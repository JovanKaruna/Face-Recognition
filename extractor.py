import numpy.core.multiarray
import cv2
import numpy as np
from imageio import imread
import pickle
import os
from tqdm import tqdm


def extract_features(image_path, vector_size=32):
    """
    Fungsi untuk melakukan ekstraksi fitur dengan menggunakan feature extractor KAZE.
    Fungsi ini mengambil fitur dengan besar matriks 32.
    Fungsi ini menggunakan 64 image descriptor dalam mencatat fitur fitur penting gambar.
    """
    image = imread(image_path, pilmode="RGB")
    try:
        kaze = cv2.KAZE_create()
        fiture = kaze.detect(image)
        fiture = sorted(fiture, key=lambda x: -x.response)[:vector_size]
        fiture, vector = kaze.compute(image, fiture)
        vector = vector.flatten()
        needed_size = (vector_size * 64)
        if vector.size < needed_size:
            vector = np.concatenate([vector, np.zeros(needed_size - vector.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return vector


result = {}


def batch_extractor(images_path):
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]
    for f in tqdm(files):
        name = f.split('\\')[-1].lower()
        result[name] = extract_features(f)


def batch_dump(path):
    with open(path, 'wb') as fp:
        pickle.dump(result, fp)


def run(resources_path=r'resources/base/'):
    batch_extractor(resources_path)
    batch_dump("features.pck")


if __name__ == '__main__':
    run(r'resources/base/')
