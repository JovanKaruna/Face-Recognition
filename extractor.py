import numpy.core.multiarray
import cv2
import numpy as np
from imageio import imread
import pickle
import os
from tqdm import tqdm


def extract_features(image_path, vector_size=32):
    image = imread(image_path, pilmode="RGB")
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        kaze = cv2.KAZE_create()
        # Dinding image keypoints
        kps = kaze.detect(image)
        # Getting first 32 of them.
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = kaze.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print('Error: ', e)
        return None

    return dsc


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
