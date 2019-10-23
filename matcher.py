import numpy.core.multiarray
import numpy as np
from scipy import spatial
from imageio import imread
import pickle
import os
import matplotlib.pyplot as plt
from extractor import extract_features
import vectorutils


class Matcher(object):
    def __init__(self, pickled_db_path="features.pck"):
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cos_cdist(self, vector):
        # getting cosine distance between search image and images database
        v = vector.reshape(1, -1)
        return vectorutils.cosine_similarity(self.matrix,v)
    
    def euclidean_dist(self, vector):
        # To get euclidean distance between search image and images database
        v = vector.reshape(1,-1)
        return vectorutils.euclidian_distance(self.matrix,v)

    def match(self, image_path, topn=5):
        features = extract_features(image_path)
        img_distances = self.cos_cdist(features)
        # getting top 5 records
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()


def show_img(path):
    print(path)
    img = imread(path, pilmode="RGB")
    plt.imshow(img)
    plt.show()


def get_match_img_path(img, source='features.pck', sample_size=0.2):
    ma = Matcher(source)
    T = 5
    print(os.path.dirname(img))
    names, match = ma.match(img, topn=T)
    print(os.getcwd())
    for i in range(T):
        print('Match %s' % (1 - match[i]))
        print(img, names[i])
        yield (os.path.join(os.getcwd(), img.split('\\')[-3], img.split('\\')[-2], names[i]))


def run():
    name = 'alexandra daddario'
    folder = 'resources/pins_' + name + '/'
    for img in get_match_img_path(os.path.join(os.getcwd(), folder, os.listdir(folder)[3]), os.path.join(os.getcwd(), 'result/pins_' + name)):
        show_img(img)


if __name__ == '__main__':
    run()

