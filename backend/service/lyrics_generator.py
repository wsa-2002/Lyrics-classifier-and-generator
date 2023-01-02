import pickle
import random
import re
from collections import defaultdict, Counter

import const


# This class is modified from https://towardsdatascience.com/text-generation-using-n-gram-model-8d12d9802aa0
class NgramModel:
    START_TOKEN = '<s>'

    def __init__(self, n, documents=None, context=None, ngram_counter=None, init=True):
        self.n = n
        self.documents = documents
        self.context = context or defaultdict(list)
        self.ngram_counter = ngram_counter or defaultdict(int)
        if init:
            self.init_model()

    def init_model(self):
        for lyrics in self.documents:
            lyrics = lyrics.split('\n')
            for sentence in lyrics:
                sentence += '.'
                self.update(sentence)

    def load_pickle(self, genre):
        with open(f'data/{genre}_context.pickle', 'rb') as file:
            self.context = pickle.load(file)
        with open(f'data/{genre}_ngram_counter.pickle', 'rb') as file:
            self.ngram_counter = pickle.load(file)

    @staticmethod
    def tokenize(text: str):
        for punct in '!?,.~$':
            text = text.replace(punct, f' {punct} ')
        for special_token in ['(repeat)', *[f"x{i}" for i in range(10)]]:  # remove special token e.g. (repeat), x1, x3.
            text = text.replace(special_token, " ")
        return [item for item in re.split(r'[ /"@#%^&*()_`:;{}\[\]+-]', text) if item]

    def get_ngrams(self, tokens: list) -> list:
        tokens = (self.n - 1) * [self.START_TOKEN] + tokens  # padding
        return [(tuple([tokens[i - p - 1] for p in range(self.n - 2, -1, -1)]), tokens[i]) for i in
                range(self.n - 1, len(tokens))]

    def update(self, sentence: str):
        for ngram in self.get_ngrams(self.tokenize(sentence)):
            self.ngram_counter[ngram] += 1
            prev_words, target_word = ngram
            self.context[prev_words].append(target_word)
        return self

    def prob(self, context, token):
        return self.ngram_counter[(context, token)] / len(self.context[context])

    def random_token(self, context):
        r = random.random()
        map_to_probs = {token: self.prob(context, token) for token in self.context[context]}

        prob_sum = 0
        for token in sorted(map_to_probs):
            prob_sum += map_to_probs[token]
            if prob_sum > r:
                return token

    def generate_text(self, token_count: int):
        print("start generation")
        n = self.n
        prev_context = (n - 1) * [self.START_TOKEN]
        result = []
        for _ in range(token_count):
            obj = self.random_token(tuple(prev_context))
            result.append(obj)
            if n > 1:
                prev_context.pop(0)
                if obj == '.':  # new sentence
                    prev_context = (n - 1) * [self.START_TOKEN]
                else:
                    prev_context.append(obj)
        print("generation done")
        return ' '.join(result)

    def to_pickle(self, genre: str):
        with open(f'{genre}_context.pickle', 'wb') as file:
            pickle.dump(self.context, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f'{genre}_ngram_counter.pickle', 'wb') as file:
            pickle.dump(self.ngram_counter, file, protocol=pickle.HIGHEST_PROTOCOL)


class UserModel(NgramModel):
    def __init__(self, genres, n=const.N):
        super().__init__(n, init=False)
        self.load_pickle(genres)

    def load_pickle(self, genres):
        for genre in genres:
            with open(f'data/{genre.value}_context.pickle', 'rb') as file:
                data: dict = pickle.load(file)
                for prev, now in data.items():
                    self.context[prev].extend(now)
            with open(f'data/{genre.value}_ngram_counter.pickle', 'rb') as file:
                data = pickle.load(file)
                self.ngram_counter = sum((Counter(item) for item in [self.ngram_counter, data]), Counter())

    def update(self, sentence: str, ratio: int = 10000):
        print("start updating....")
        sentences = sentence.split('\n')
        for sentence in sentences:
            for ngram in self.get_ngrams(self.tokenize(sentence)):
                self.ngram_counter[ngram] += ratio
                prev_words, target_word = ngram
                self.context[prev_words].extend([target_word] * ratio)
        print("updated.")
        return self
