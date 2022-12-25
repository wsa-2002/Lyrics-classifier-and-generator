import math
import pickle
import re

import numpy as np
import pandas as pd

from base.enums import Genre


class Classifier:
    def __init__(self):
        with open(f'data/word_p.pickle', 'rb') as file:
            self.word_p = pickle.load(file)

    @staticmethod
    def tokenize(lyrics):
        return [item for item in re.split(r'[ \r\n,./\'"~!@#$%^&*()_`1234567890:;{}?\[\]+-]', lyrics) if item]

    @staticmethod
    def normalize(result):
        total = sum(np.exp(result['max_p_class']))
        result['normalized'] = np.exp(result['max_p_class']) / total
        return result

    @staticmethod
    def result_class(result):
        candidate = result[result['normalized'] < 1 / 19]
        return candidate[:3].value.tolist()

    def classification(self, lyrics):
        word_p = self.word_p
        lyrics = self.tokenize(lyrics)
        lyrics = [x for x in lyrics if x in word_p.keys()]
        training_set = {'Electronic': 11032, 'Pop': 47433, 'Blues': 5485, 'Religion': 6603, 'Rap': 15507, 'Rock': 81373,
                        'Metal': 19624, 'Dance': 12734,
                        'Folk': 10012, 'Hip Hop': 19848, 'R&B': 14023, 'Punk': 18821, 'Reggae': 2912, 'Indie': 18121,
                        'Soul Music': 7318,
                        'Country': 9567, 'Jazz': 3909, 'Funk': 2715, 'Latin': 7473}

        score = pd.DataFrame({'max_p_class': [], 'value': []})
        for c in training_set.keys():
            p_class = math.log(training_set[c] / sum(training_set.values()), 10)
            for word in lyrics:
                p_class += math.log(word_p[word][c]['in'], 10)
            score = pd.concat([score, pd.DataFrame({'max_p_class': -p_class, 'value': c}, index=[0])],
                              ignore_index=True)
        result = score.sort_values(by='max_p_class', ignore_index=True, ascending=True)  # ['value'].tolist()
        result = self.normalize(result=result)
        result = self.result_class(result=result)
        return [Genre(genre) for genre in result]


classifier = Classifier()
