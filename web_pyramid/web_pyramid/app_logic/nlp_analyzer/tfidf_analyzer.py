from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np


class TfidfSimilarity:
    def __init__(self):
        self._matrix = None

    def analyze_documents(self, document_set):
        tf_idf = TfidfVectorizer(ngram_range=(1, 3))

        self._matrix = tf_idf.fit_transform(document_set)
        self._matrix = np.dot(self._matrix, self._matrix.T)

        print(self._matrix.shape)

    def find_similar(self, threshold=0.8):
        similar_list = np.argwhere(self._matrix > threshold)

        similar_list = list(filter(lambda x: x[0] < x[1], similar_list))
        # pozbywamy się zarówno równych, jak i jednego trójkąta macierzy, wynikiem jest macierz symetryczna

        return similar_list

    def sort_by_similarity(self, similar_list):
        values = {(s[0], s[1]): self._matrix[s[0], s[1]] for s in similar_list}

        return sorted(values, key=lambda k: values[k], reverse=True)
