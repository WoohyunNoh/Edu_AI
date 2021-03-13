import math

import pandas as pd
from eunjeon import Mecab
import sentencepiece as spm
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence

data = pd.read_pickle('./backend/textengines/data/dc_data.pkl')

soynlp_model_fname = './backend/textengines/data/tokenizer_model/soyword.model'

sentences = data["title"].values

word_extractor = WordExtractor(
    min_frequency=100,
    min_cohesion_forward=0.05,
    min_right_branching_entropy=0.0
)

word_extractor.train(sentences)
word_extractor.save(soynlp_model_fname)

scores = word_extractor.word_scores()
scores = {key:(scores[key].cohesion_forward * math.exp(scores[key].right_branching_entropy)) for key in scores.keys()}
# soyToken = LTokenizer(scores=scores)
# soyToken.tokenize(data["title"].values[0])
#############################################################################
file = open("./backend/textengines/data/dc_title.txt", "w", encoding="utf-8")
for title in data["title"].values:
    file.write(title)
    file.write("\n")
file.close()

spm_train = """--input=./backend/textengines/data/dc_title.txt \
               --model_prefix=sentencepice \
               --vocab_size=32000 \
               --model_type=bpe \
               --character_coverage=0.9995"""
spm.SentencePieceTrainer.Train(spm_train)

token = spm.SentencePieceProcessor()
token.Load("./backend/textengines/data/tokenizer_model/sentencepice.model")
token.EncodeAsPieces(data["title"].values[0])
#############################################################################
import warnings
import numpy as np
from tqdm import tqdm
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, RNN, SimpleRNN
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

warnings.filterwarnings('ignore')
# tf.debugging.set_log_device_placement(True)

tqdm.pandas()

def get_prediction_accuracy_for_multiclasses(y_test, prediction, cutoff=0.5):
    pred_classes = []
    pred_acc = 0

    for pred in prediction:
        p = pred > cutoff
        check = list(p).count(True)
        if check == 0 or check > 1:
            pred_classes.append(np.argmax(pred))
        else:
            pred_classes.append(np.argmax(p.astype("int32")))

    for p, y in zip(pred_classes, y_test):
        if p == y:
            pred_acc += 1

    return np.array(pred_classes), pred_acc / len(y_test)

def get_prediction_accuracy_for_multiclasses2(y_test, prediction, cutoff=0.5):
    pred_classes = []
    pred_acc = 0

    for pred in prediction:
        p = pred > cutoff
        check = list(p).count(True)
        if check == 0 or check > 1:
            pred_classes.append(np.argmax(pred))
        else:
            pred_classes.append(np.argmax(p.astype("int32")))

    for p, y in zip(pred_classes, y_test):
        if p == np.argmax(y):
            pred_acc += 1

    return np.array(pred_classes), pred_acc / len(y_test)

# 동일한 비율의 샘플을 추출하기 위해서
def sampling_func(df, n_sample, random_state=42):
    np.random.seed(random_state)
    sample = df.take(np.random.permutation(len(df))[:n_sample])
    return sample

# title_data = data[["label", "title"]]
gd = data.groupby('label').apply(sampling_func, n_sample=13000)
gd.index.names = ["temp_label", None]
gd = gd.reset_index(level=[0])
gd = gd.drop(["temp_label"], axis=1)
gd = shuffle(gd)

mecab_processed_data = gd.copy()
etri_processed_data = gd.copy()
soynlp_processed_data = gd.copy()
spm_processed_data = gd.copy()

mecab = Mecab()
mecab_processed_data["title"] = mecab_processed_data["title"].progress_apply(lambda x: " ".join(mecab.morphs(x)))

def concat_text_with_pos(setence):
    tag = Mecab()
    pos = tag.pos(setence)
    temp = []
    for p in pos:
        temp.append(p[0] + "/" + p[1])
    
    s = ' '.join(temp)
    return s
etri_processed_data["title"] = etri_processed_data["title"].progress_apply(concat_text_with_pos)


word_extractor = WordExtractor(
    min_frequency=100,
    min_cohesion_forward=0.05,
    min_right_branching_entropy=0.0
)
soynlp_model_fname = './backend/textengines/data/tokenizer_model/soyword.model'
word_extractor.load(soynlp_model_fname)
scores = word_extractor.word_scores()
scores = {key:(scores[key].cohesion_forward * math.exp(scores[key].right_branching_entropy)) for key in scores.keys()}
soyToken = LTokenizer(scores=scores)
# soyToken.tokenize(soynlp_processed_data["title"].values[0])
soynlp_processed_data["title"] = soynlp_processed_data["title"].progress_apply(lambda x: " ".join(soyToken.tokenize(x)))

token = spm.SentencePieceProcessor()
token.Load("./backend/textengines/data/tokenizer_model/sentencepice.model")
spm_processed_data["title"] = spm_processed_data["title"].progress_apply(lambda x: " ".join(token.EncodeAsPieces(x)))
#############################################################################

td = etri_processed_data.copy()

ratio_train = 0.8
ratio_val = 0.1
ratio_test = 0.1

# Produces test split.
x_remaining, x_test, y_remaining, y_test = train_test_split(
    td["title"], 
    td["label"], test_size=ratio_test)

# Adjusts val ratio, w.r.t. remaining dataset.
ratio_remaining = 1 - ratio_test
ratio_val_adjusted = ratio_val / ratio_remaining
# Produces train and val splits.
x_train, x_val, y_train, y_val = train_test_split(
    x_remaining, y_remaining, test_size=ratio_val_adjusted)


vocab_size = 50000
tokenizer = Tokenizer(vocab_size) 
tokenizer.fit_on_texts(x_train)
X_train = tokenizer.texts_to_sequences(x_train)
X_val = tokenizer.texts_to_sequences(x_val)
X_test = tokenizer.texts_to_sequences(x_test)

max_len = 1000
X_train = pad_sequences(X_train, maxlen = max_len)
X_val = pad_sequences(X_val, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)

y_train = to_categorical(y_train)
y_val = to_categorical(y_val)
y_test = to_categorical(y_test)

model = Sequential()
model.add(Embedding(vocab_size, 120))
model.add(LSTM(120))
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
history = model.fit(X_train, y_train, batch_size=128, epochs=7)
history.history["acc"][-1]
arr1, acc1 = get_prediction_accuracy_for_multiclasses2(y_val, model.predict(X_val))
arr2, acc2 = get_prediction_accuracy_for_multiclasses2(y_test, model.predict(X_test))

X_all = tokenizer.texts_to_sequences(data["title"])
X_all = pad_sequences(X_all, maxlen=max_len)
y_all = to_categorical(data["label"])

model.evaluate(X_all, y_all)
arr3, acc3 = get_prediction_accuracy_for_multiclasses2(y_all, model.predict(X_all))

##################################################################################

vocab_size = 50000
tokenizer = Tokenizer(vocab_size) 
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

max_len = 1000
X_train = pad_sequences(X_train, maxlen = max_len)
X_test = pad_sequences(X_test, maxlen = max_len)
y_train = to_categorical(y_train)

model = Sequential()
model.add(Embedding(vocab_size, 120))
model.add(LSTM(120))
model.add(Dense(3, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
history = model.fit(X_train, y_train, batch_size=128, epochs=7)

arr, acc = get_prediction_accuracy_for_multiclasses(y_test, model.predict(X_test))

validation_accuracies = []
models = []
tokenized_datas = [mecab_processed_data, etri_processed_data, soynlp_processed_data, spm_processed_data]


for td in tokenized_datas:
    X_train, X_test, y_train, y_test = train_test_split(
        td["title"], 
        td["category"],
        test_size=0.25,
        train_size=0.75,
        shuffle=True,
        random_state=42
    )

    
    vocab_size = 50000
    tokenizer = Tokenizer(vocab_size) 
    tokenizer.fit_on_texts(X_train)
    X_train = tokenizer.texts_to_sequences(X_train)
    X_test = tokenizer.texts_to_sequences(X_test)

    max_len = 1000
    X_train = pad_sequences(X_train, maxlen = max_len)
    X_test = pad_sequences(X_test, maxlen = max_len)
    y_train = to_categorical(y_train)

    model = Sequential()
    model.add(Embedding(vocab_size, 120))
    model.add(LSTM(120))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
    history = model.fit(X_train, y_train, batch_size=128, epochs=7)

    models.append(model)

    arr, acc = get_prediction_accuracy_for_multiclasses2(y_test, model.predict(X_test))

    validation_accuracies.append(acc)

test_accuracies = []
for td, model in zip(tokenized_datas, models):
    vocab_size = 50000
    vals = td["title"].values

    tokenizer = Tokenizer(vocab_size) 
    tokenizer.fit_on_texts(vals)

    X_test = tokenizer.texts_to_sequences(vals)

    max_len = 1000
    X_test = pad_sequences(X_test, maxlen = max_len)
    y_test = to_categorical(td["category"].values)

    arr, acc = get_prediction_accuracy_for_multiclasses2(y_test, model.predict(X_test))

    test_accuracies.append(acc)

#############################################################################

origin = data[["label", "title"]]
origin["title"] = origin["title"].progress_apply(concat_text_with_pos)
md = models[1]

vocab_size = 50000
vals = origin["title"].values

tokenizer = Tokenizer(vocab_size) 
tokenizer.fit_on_texts(vals)

X_test = tokenizer.texts_to_sequences(vals)

max_len = 1000
X_test = pad_sequences(X_test, maxlen = max_len)
y_test = to_categorical(origin["label"].values)

arr, acc = get_prediction_accuracy_for_multiclasses2(y_test, md.predict(X_test))

#############################################################################

from nltk.stem import WordNetLemmatizer
wl = WordNetLemmatizer()
"""


1. 훈련, 검증에서 정확도가 괜찮게 나오는데 테스트 데이터에서 점수가 나쁘다. 어떻게 하면 높일 수 있을까?
2. 지금이라도 스켈레톤코드를 주실 수 있는지?

"""

"""train, validation 이랑 섞였는지?
sampling 을 다시 해보자."""
