import numpy.core.multiarray
import numpy as np
import pickle
import os
from extractor import extract_features
import vectorutils


class Matcher(object):
    def __init__(self, pickled_db_path="features.pck"):
        """
            Proses inisialisasi objek matcher citra
        """
        with open(pickled_db_path, 'rb') as fp:
            self.data = pickle.load(fp)
        self.names = []
        self.matrix = []
        for k, v in self.data.items():
            self.names.append(k)
            self.matrix.append(v)
        self.matrix = np.array(self.matrix)
        self.names = np.array(self.names)

    def cosine_distance(self, vector):
        """
            Fungsi pendeteksi wajah dengan metriks jarak cosine
        """
        v = vector.reshape(1, -1)
        ans = []
        for img_vector in self.matrix:
            ans.append(1 - vectorutils.cosine_similarity(img_vector.reshape(-1), v.reshape(-1)))
        return np.array(ans)

    def euclidean_distance(self, vector):
        """
            Fungsi pendeteksi wajah dengan metriks jarak euclidian
        """
        v = vector.reshape(1, -1)
        ans = []
        for img_vector in self.matrix:
            ans.append(vectorutils.euclidian_distance(img_vector.reshape(-1), v.reshape(-1)))
        return np.array(ans)


    def match(self, image_path, topn=20, method='cosine'):
        """
            Fungsi implementasi pendeteksi wajah dengan memakai 2 metriks, yaitu
                1.  Metrik cosine  (default)
                2.  Metrik euclidian
        """
        features = extract_features(image_path)
        if(method == 'cosine'):
            img_distances = self.cosine_distance(features)
        else:
            img_distances = self.euclidean_distance(features)
        nearest_ids = np.argsort(img_distances)[:topn].tolist()
        nearest_img_paths = self.names[nearest_ids].tolist()

        return nearest_img_paths, img_distances[nearest_ids].tolist()


def get_match_img_path(img, source='features.pck', sample_size=0.2, topn=6, method='cosine'):
    """
        Fungsi untuk mengambil citra - citra dengan fitur paling sama dengan citra yang dimasukkan.
        Notes : Kumpulan fitur citra disimpan di sebuah file yang berdefault => features.pck
                Method yang digunakan ada 2 : 1. cosine
                                              2. euclidian
    """
    ma = Matcher(source)
    names, match = ma.match(img, topn=topn, method=method)
    ans = []
    for i in range(topn):
        ans.append(os.path.join(os.getcwd(), names[i]))
    return ans
