import warnings
import pandas as pd
import numpy as np
from tensorflow.python.keras.backend import learning_phase
from tqdm import tqdm

import konlpy
from eunjeon import Mecab

# preprocess 용
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer
# 분석 모델
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from xgboost import XGBClassifier

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, RNN, SimpleRNN
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from .preprocess import get_preprocessed_data
from .preprocess import tokenizer as tkz

warnings.filterwarnings('ignore')


class BaseAnalyze:

    def __init__(self, df: pd.DataFrame, vocab_size: int, max_len: int, batch_size=16, epochs=50, learning_rate=0.001, ratio_train=0.8, ratio_val=0.1, ratio_test=0.1):
                            #  nd, vocab_size=30000, max_len=1000, batch_size=16, epochs=50, learning_rate=0.001
        # print('BaseAnalyze 입성!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(df)
        print(ratio_train)
        self.df = df
        self.vocab_size = vocab_size
        self.max_len = max_len
        self.len_categories = len(df["label"].unique())

        self.ratio_train = ratio_train
        self.ratio_val = ratio_val
        self.ratio_test = ratio_test

        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate

        self.X_train = None
        self.X_validation = None
        self.X_test = None
        self.y_train = None
        self.y_validation = None
        self.y_test = None
        # print('3333333333333333')
        self.set_train_validation_test_split()
        # print('22222222222222222')
        self._tokenizer = self.tokenizer()

        self.X_train_seq = None
        self.X_validation_seq = None
        self.X_test_seq = None
        # print('11111111111111111111')
        self.set_pad_sequences()

        self.y_train_category = None
        self.y_validation_category = None
        self.y_test_category = None
        print('BaseAnalyze 중간')
        self.set_categories()

    def set_train_validation_test_split(self, train_size=0.75, test_size=0.25, shuffle=True, random_state=42):
        print('qqq')
        # self.df["data"] = self.df["data"].apply(tkz)
        print(self.df["data"])
        x_remaining, self.X_test, y_remaining, self.y_test = train_test_split(
            self.df["data"],
            self.df["label"],
            test_size=self.ratio_test,
            shuffle=shuffle,
            random_state=random_state
        )
        print('aa')
        ratio_remaining = 1 - self.ratio_test
        ratio_val_adjusted = self.ratio_val / ratio_remaining

        self.X_train, self.X_validation, self.y_train, self.y_validation = train_test_split(
            x_remaining,
            y_remaining,
            test_size=ratio_val_adjusted,
            shuffle=shuffle,
            random_state=random_state
        )
        # print('x_train' + self.x_train)
        # print('y_train' + self.y_train)
        print('bb')

    def tokenizer(self):
        tk = Tokenizer(self.vocab_size)
        tk.fit_on_texts(self.X_train)
        return tk

    def set_pad_sequences(self):
        self.X_train_seq = pad_sequences(
            self._tokenizer.texts_to_sequences(self.X_train))
        self.X_validation_seq = pad_sequences(
            self._tokenizer.texts_to_sequences(self.X_validation))
        self.X_test_seq = pad_sequences(
            self._tokenizer.texts_to_sequences(self.X_test))

    def set_categories(self):
        print('셋 카테고리 온다.0')
        self.y_train_category = to_categorical(self.y_train)
        print('셋 카테고리 온다.1')
        self.y_validation_category = to_categorical(self.y_validation)
        print('셋 카테고리 온다.2')
        self.y_test_category = to_categorical(self.y_test)
        print('셋 카테고리 온다.3')

    def lstm_fit(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, 120))
        model.add(LSTM(120))
        model.add(Dense(self.len_categories, activation='softmax'))
        print('여기 보이나 혹시')
        print(self.learning_rate)
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam', metrics=['acc'])  # learning_rate  , learning_rate=self.learning_rate
        print('컴파일 완료')
        history = model.fit(
            self.X_train_seq, self.y_train_category, batch_size=self.batch_size, epochs=self.epochs)
        self.lstm_model = model
        self.train_loss, self.train_acc = history.history["loss"][-1], history.history["acc"][-1]

    def lstm_acc(self):
        self.validation_loss, self.validation_acc = self.lstm_model.evaluate(
            self.X_validation_seq, self.y_validation_category)
        self.test_loss, self.test_acc = self.lstm_model.evaluate(
            self.X_test_seq, self.y_test_category)

        res = {
            "train": [self.train_loss, self.train_acc],
            "validation": [self.validation_loss, self.validation_acc],
            "test": [self.test_loss, self.test_acc]
        }
        return res


class BaseAnalyze2:

    def __init__(self, df, tagger="mecab", model="logistic", ratio_train=0.8, ratio_val=0.1, ratio_test=0.1):
        self.df = df
        self.len_categories = len(df["label"].unique())

        self.ratio_train = ratio_train
        self.ratio_val = ratio_val
        self.ratio_test = ratio_test
        # print('2')
        self.tagger = self.set_tagger(tagger)
        self.model = self.set_model(model)
        # print('3')
        self.set_train_validation_test_split()
        print('33')
        self.set_tfidf_process()
        print('4')

    def set_tagger(self, tagger):
        tag = None
        if tagger == "mecab":
            tag = Mecab()
        elif tagger == 'komoran':
            from konlpy.tag import Komoran
            tag = Komoran()
        elif tagger == 'kkma':
            from konlpy.tag import Kkma
            tag = Kkma()
        elif tagger == 'hannanum':
            from konlpy.tag import Hannanum
            tag = Hannanum()
        elif tagger == 'okt':
            from konlpy.tag import Okt
            tag = Okt()
        elif tagger == 'twitter':
            from konlpy.tag import Twitter
            tag = Twitter()

        return tag

    def set_model(self, model):
        mod = None
        if model == "logistic":
            mod = LogisticRegression()
        elif model == "decisiontree":
            mod = DecisionTreeClassifier(max_depth=10, random_state=42)
        elif model == "randomforest":
            mod = RandomForestClassifier(max_depth=10, random_state=42)
        elif model == "xgb":
            mod = XGBClassifier(max_depth=10, learning_rate=0.01,
                                n_estimators=500, verbosity=0)
        elif model == "naive":
            mod = MultinomialNB()

        return mod

    def tokenizer(self, sentence):
        pos = self.tagger.pos(sentence)

        temp = []
        for p in pos:
            temp.append(p[0] + "/" + p[1])

        s = ' '.join(temp)
        return s

    def set_train_validation_test_split(self, train_size=0.75, test_size=0.25, shuffle=True, random_state=42):
        # print('88')
        # self.df["data"] = self.df["data"].apply(self.tokenizer)
        # print('77')
        x_remaining, self.X_test, y_remaining, self.y_test = train_test_split(
            self.df["data"],
            self.df["label"],
            test_size=self.ratio_test,
            shuffle=shuffle,
            random_state=random_state
        )
        # print(x_remaining)
        # print(y_remaining)

        ratio_remaining = 1 - self.ratio_test
        ratio_val_adjusted = self.ratio_val / ratio_remaining

        self.X_train, self.X_validation, self.y_train, self.y_validation = train_test_split(
            x_remaining,
            y_remaining,
            test_size=ratio_val_adjusted,
            shuffle=shuffle,
            random_state=random_state
        )
        # print(self.X_train)
        # print(self.y_train)

    def set_tfidf_process(self):
        print('1')
        tfidf = TfidfVectorizer(token_pattern='\S+')  # 띄어쓰기로 구분시킴
        print('11')
        print(self.X_train)
        tfidf.fit(self.X_train.astype('U'))
        print('2')
        train_vector = tfidf.transform(self.X_train.astype('U'))
        print('22')
        validation_vector = tfidf.transform(self.X_validation.astype('U'))
        print('33')
        test_vector = tfidf.transform(self.X_test.astype('U'))
        # print('3')
        print('44')


        nmf = NMF(n_components=50)  # 차원축소
        nmf.fit(train_vector.toarray())
        train_features = nmf.transform(train_vector.toarray())
        validation_features = nmf.transform(validation_vector.toarray())
        test_features = nmf.transform(test_vector.toarray())
        print('4')
        norm = Normalizer()  # 0 ~ 1 사이로 변경
        self.train_nf = norm.fit_transform(train_features)
        self.validation_nf = norm.fit_transform(validation_features)
        self.test_nf = norm.fit_transform(test_features)
        print('5')

    def run(self):
        self.model.fit(self.train_nf, self.y_train)

        self.train_score = self.model.score(self.train_nf, self.y_train)
        self.validation_score = self.model.score(
            self.validation_nf, self.y_validation)
        self.test_score = self.model.score(self.test_nf, self.y_test)
