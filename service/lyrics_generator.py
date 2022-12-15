import pickle
import random
import re
from collections import defaultdict

import const


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
        for special_token in ['(repeat)', *[f"x{i}" for i in range(10)]]:
            text = text.replace(special_token, " ")
        t = [item for item in re.split(r'[ /"@#%^&*()_`:;{}\[\]+-]', text) if item]
        return t

    def get_ngrams(self, tokens: list) -> list:
        tokens = (self.n - 1) * [self.START_TOKEN] + tokens
        ngram_list = [(tuple([tokens[i - p - 1] for p in reversed(range(self.n - 1))]), tokens[i]) for i in
                      range(self.n - 1, len(tokens))]
        return ngram_list

    def update(self, sentence: str):
        for ngram in self.get_ngrams(self.tokenize(sentence)):
            self.ngram_counter[ngram] += 1.0
            prev_words, target_word = ngram
            self.context[prev_words].append(target_word)
        return self

    def prob(self, context, token):
        count_of_token = self.ngram_counter[(context, token)]
        count_of_context = float(len(self.context[context]))
        result = count_of_token / count_of_context
        return result

    def random_token(self, context):
        r = random.random()
        map_to_probs = {}
        token_of_interest = self.context[context]
        for token in token_of_interest:
            map_to_probs[token] = self.prob(context, token)

        summ = 0
        for token in sorted(map_to_probs):
            summ += map_to_probs[token]
            if summ > r:
                return token

    def generate_text(self, token_count: int):
        print("start generation")
        n = self.n
        context_queue = (n - 1) * [self.START_TOKEN]
        result = []
        for _ in range(token_count):
            obj = self.random_token(tuple(context_queue))
            result.append(obj)
            if n > 1:
                context_queue.pop(0)
                if obj == '.':
                    context_queue = (n - 1) * [self.START_TOKEN]
                else:
                    context_queue.append(obj)
        print("generation done")
        return ' '.join(result)

    def to_pickle(self, genre: str):
        with open(f'{genre}_context.pickle', 'wb') as file:
            pickle.dump(self.context, file, protocol=pickle.HIGHEST_PROTOCOL)
        with open(f'{genre}_ngram_counter.pickle', 'wb') as file:
            pickle.dump(self.ngram_counter, file, protocol=pickle.HIGHEST_PROTOCOL)


class UserModel(NgramModel):
    def __init__(self, genre, n=const.N):
        super().__init__(n, init=False)
        self.load_pickle(genre)

    def load_pickle(self, genre):
        with open(f'data/{genre}_context.pickle', 'rb') as file:
            self.context = pickle.load(file)
        with open(f'data/{genre}_ngram_counter.pickle', 'rb') as file:
            self.ngram_counter = pickle.load(file)

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
