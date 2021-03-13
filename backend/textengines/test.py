from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB, BaseDiscreteNB
from sklearn.linear_model import LogisticRegression
import json
import pandas as pd
import numpy as np
from sklearn.utils import shuffle
import warnings
from tqdm import tqdm

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, RNN, SimpleRNN
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

from backend.textengines.preprocess import get_preprocessed_data, sampling_by_same_ratio, tokenizer

data = pd.read_pickle('./backend/textengines/data/dc_data.pkl')

df = sampling_by_same_ratio(data, n_sample=30000)


warnings.filterwarnings('ignore')


class BaseAnalyze:

    def __init__(self, df: pd.DataFrame, vocab_size: int, max_len: int, ratio_train=0.8, ratio_val=0.1, ratio_test=0.1):
        self.df = df
        self.vocab_size = vocab_size
        self.max_len = max_len
        self.len_categories = len(df["label"].unique())

        self.ratio_train = ratio_train
        self.ratio_val = ratio_val
        self.ratio_test = ratio_test

        self.X_train = None
        self.X_validation = None
        self.X_test = None
        self.y_train = None
        self.y_validation = None
        self.y_test = None

        self.set_train_validation_test_split()

        self._tokenizer = self.tokenizer()

        self.X_train_seq = None
        self.X_validation_seq = None
        self.X_test_seq = None
        self.set_pad_sequences()

        self.y_train_category = None
        self.y_validation_category = None
        self.y_test_category = None
        self.set_categories()

    def set_train_validation_test_split(self, train_size=0.75, test_size=0.25, shuffle=True, random_state=42):
        x_remaining, self.X_test, y_remaining, self.y_test = train_test_split(
            self.df["data"],
            self.df["label"],
            test_size=self.ratio_test,
            shuffle=shuffle,
            random_state=random_state
        )

        ratio_remaining = 1 - self.ratio_test
        ratio_val_adjusted = self.ratio_val / ratio_remaining

        self.X_train, self.X_validation, self.y_train, self.y_validation = train_test_split(
            x_remaining,
            y_remaining,
            test_size=ratio_val_adjusted,
            shuffle=shuffle,
            random_state=random_state
        )

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
        self.y_train_category = to_categorical(self.y_train)
        self.y_validation_category = to_categorical(self.y_validation)
        self.y_test_category = to_categorical(self.y_test)

    def lstm_fit(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, 120))
        model.add(LSTM(120))
        model.add(Dense(self.len_categories, activation='softmax'))
        model.compile(loss='categorical_crossentropy',
                      optimizer='adam', metrics=['acc'])

        history = model.fit(
            self.X_train_seq, self.y_train_category, batch_size=128, epochs=7)
        self.lstm_model = model
        self._history = history.history
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


ndf = df[["label", "title"]]
ndf = ndf.rename(columns={"title": "data"})
ba = BaseAnalyze(ndf, 30000, 1000)
ba.lstm_fit()
ba.lstm_acc()


ndf.to_json("sample.json")
nn = ndf.reset_index()
nn = nn.drop(columns=["index"])

nn[nn["label"] == 0]["data"].values
dt = {
    "0": list(nn[nn["label"] == 0]["data"].values[:500]),
    "1": list(nn[nn["label"] == 1]["data"].values[:500]),
    "2": list(nn[nn["label"] == 2]["data"].values[:500]),
}
with open('sample.json', 'w') as outfile:
    json.dump(dt, outfile)


nn = sampling_by_same_ratio(data, 4500)
nn = shuffle(nn)
nn = nn[["label", "title"]]


nn["title"] = nn["title"].apply(tokenizer)

X_train, X_test, y_train, y_test = train_test_split(
    nn["title"],
    nn["label"],
    test_size=0.25
)

tfidf = TfidfVectorizer(token_pattern='\S+')  # 띄어쓰기로 구분시킴
tfidf.fit(X_train)
train_vector = tfidf.transform(X_train)
test_vector = tfidf.transform(X_test)
tfidf.vocabulary_

nmf = NMF(n_components=50)  # 차원축소
nmf.fit(train_vector.toarray())
train_features = nmf.transform(train_vector.toarray())
test_features = nmf.transform(test_vector.toarray())

norm1 = Normalizer()
train_nf = norm1.fit_transform(train_features)  # 0 ~ 1 사이로 변경시켜줌.
norm2 = Normalizer()
test_nf = norm2.fit_transform(test_features)  # 0 ~ 1 사이로 변경시켜줌.

logreg = LogisticRegression(C=2).fit(train_nf, y_train)

logreg.score(train_nf, y_train)
logreg.score(test_nf, y_test)


mod = MultinomialNB()
mod.fit(train_nf, y_train)
mod.score(train_nf, y_train)
mod.score(test_nf, y_test)


foc = RandomForestClassifier(
    n_estimators=200, random_state=0).fit(train_nf, y_train)
foc.score(train_nf, y_train)
foc.score(test_nf, y_test)


xgc = XGBClassifier(max_depth=10, learning_rate=0.01,
                    n_estimators=500, verbosity=0).fit(train_nf, y_train)
xgc.score(train_nf, y_train)
xgc.score(test_nf, y_test)


class T:
    def __init__(self):
        self._dr = "hello"

    @classmethod
    def fi(cls):
        return cls()._dr

    @staticmethod
    def sfi():
        return T()._dr


class A(T):
    pass


a = A()

a._dr
a._dr = "wdwd"
a._dr

a.fi()

t = T()
t.sfi()
t._dr = "NNNNN"
t.fi()
t.sfi()
