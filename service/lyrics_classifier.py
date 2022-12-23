import math
import pickle
import re

import pandas as pd

from base.enums import Genre


class Classifier:
    def __init__(self):
        with open(f'data/word_p.pickle', 'rb') as file:
            self.word_p = pickle.load(file)

    @staticmethod
    def tokenize(lyrics):
        return [item for item in re.split(r'[ \r\n,./\'"~!@#$%^&*()_`1234567890:;{}?\[\]+-]', lyrics) if item]

    def classification(self, lyrics):
        word_p = self.word_p
        lyrics = self.tokenize(lyrics)
        lyrics = [x for x in lyrics if x in word_p.keys()]
        training_set = {'Electronic': 12, 'Pop': 53, 'Blues': 6, 'Religion': 7, 'Rap': 17, 'Rock': 90, 'Metal': 22,
                        'Dance': 14,
                        'Folk': 11, 'Hip Hop': 22, 'R&B': 16, 'Punk': 21, 'Reggae': 3, 'Indie': 20, 'Soul Music': 8,
                        'Country': 11, 'Jazz': 5, 'Funk': 3, 'Latin': 8}

        score = pd.DataFrame({'max_p_class': [], 'value': []})
        for c in training_set.keys():
            p_class = math.log(training_set[c] / sum(training_set.values()), 10)
            for word in lyrics:
                p_class += math.log(word_p[word][c]['in'], 10)
            score = pd.concat([score, pd.DataFrame({'max_p_class': p_class, 'value': c}, index=[0])], ignore_index=True)

        result = score.sort_values(by='max_p_class', ignore_index=True, ascending=False)['value'].tolist()[:3]
        return [Genre(genre) for genre in result]


classifier = Classifier()
