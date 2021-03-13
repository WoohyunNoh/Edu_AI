import json
from pprint import pprint
from asgiref.sync import sync_to_async

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView

from .preprocess import get_preprocessed_data
from .analyzer import BaseAnalyze
from .tasks import start_lstm_analyze
from .tasks import start_sklearn_analyze


# return  movie_set
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import urllib.request
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
# Create your views here.

# 모델 불러오기
import pickle
import os

# 전처리
# preprocess 용
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer



def engine(request):
    pass


@csrf_exempt
def text_classification(request):

    data = request.POST.get("data")
    # print(data)                 text
    nd = json.loads(data)
    # print(data)                 dic    {'class1': ['나는 배가 너무 고파 화가난다', '넘어져서 기분이 않좋다'], 'class2': ['음식이 맛있어서 기분이 좋다', '새 컴퓨터를 사서 기분이 좋다']}
    pdata = get_preprocessed_data(nd)
    # print(pdata)
    # res = lstm_analyze(pdata, 30000, 1000)
    start_lstm_analyze.delay(nd, 30000, 1000)

    return JsonResponse({"data": "res"})


def lstm_analyze(dataframe, vocab_size, max_len):
    ba = BaseAnalyze(dataframe, vocab_size, max_len)
    ba.lstm_fit()
    res = ba.lstm_acc()
    return res


class LstmRunAPIView(APIView):

    def run_lstm(self, nd, vocab_size=30000, max_len=1000, batch_size=16, epochs=50, learning_rate=0.001):
        # start_lstm_analyze.delay(
        #     nd, vocab_size, max_len, batch_size, epochs, learning_rate)
        start_lstm_analyze(
            nd, vocab_size, max_len, batch_size, epochs, learning_rate)


    def post(self, request):
        print('2222222222222222')
        data = request.POST.get("data")
        print(data)
        # batch_size = request.POST.get("batch_size")
        # epochs = request.POST.get("epochs")
        # learning_rate = request.POST.get("learning_rate")
        nd = json.loads(data)  # 딕셔너리 변환
        # 위 주석 부분을 run_lstm 파라미터로 넣어주시면 됩니다.
        self.run_lstm(nd)
        # self.run_lstm(nd, 1, 2, 0.001)

        return JsonResponse({"data": "학습을 시작했습니다."})



@csrf_exempt
def base_analyze(request):
    tagger = request.POST.get("tagger")  # ex) mecab
    model = request.POST.get("model")  # ex) logistic
    data = return_data()
    print(type(data))
    # print(data[1])
    print('111111111111111111111111111111111111111111')
    start_sklearn_analyze(data, tagger, model)

    return JsonResponse({"data": "학습을 시작했습니다."})




class SklearnAPIView(APIView):

    def run(self, nd, tagger, model):
        # start_sklearn_analyze.delay(nd, tagger, model)
        start_sklearn_analyze(nd, tagger, model)

    def post(self, request):
        data = request.POST.get("data")
        tagger = request.POST.get("tagger")  # ex) mecab
        model = request.POST.get("model")  # ex) logistic
        # batch_size = request.POST.get("batch_size")
        # epochs = request.POST.get("epochs")
        # learning_rate = request.POST.get("learning_rate")
        print(tagger)
        print(model)
        nd = json.loads(data)
        self.run(nd, tagger=tagger, model=model)

        return JsonResponse({"data": "학습을 시작했습니다."})

# async def lstm_analyze(dataframe, vocab_size, max_len):
#     ba = BaseAnalyze(dataframe, vocab_size, max_len)
#     ba.lstm_fit()
#     res = ba.lstm_acc()
#     return res

def return_data():
    movie_data = pd.read_table('../NPLtest/ratings_train.txt')
    movie_data.drop_duplicates(subset = ['document'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
    movie_data['document'] = movie_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
    movie_data['document'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
    movei_data = movie_data.dropna(how='any') # Null 값 제거
    print('전처리 후 테스트용 샘플의 개수 :',len(movie_data))
    print(movie_data[:5])

    # for sentence in test_data['document']:
    #     print(sentence)

    movie_document = np.array(movie_data['document'])
    movie_label = np.array(movie_data['label'])
    print(movie_document)
    print(movie_label)
    print(len(movie_document), len(movie_label))
    positive_content = []
    negative_content = []
    for i in range(len(movie_document)):
        if movie_label[i]:
            if len(positive_content) > 2000:
                continue
            else:
                positive_content.append(movie_document[i])
        else:
            if len(negative_content) > 2000:
                continue
            else:
                negative_content.append(movie_document[i])

    # print(positive_content)
    # print(negative_content)
    print('end')

    nd = {"0": positive_content, "1": negative_content}
    print(type(nd))
    # print(nd[0][:5])
    # print(nd[1][:5])

    print('--------------------------------------------')
    # start_sklearn_analyze(nd, "mecab", "logistic")

    # return JsonResponse({"0": positive_content, "1": negative_content})
    return nd


###################a model analyze()
@csrf_exempt
def sklearn_result_analyze(request):
    input_content = request.POST.get("input_content")
    # input_label = request.POST.get("input_label")
    input_label = 1

    # input_data = request.POST.get("input_data")
    if request.POST.get("user_id"):
        user_id = request.POST.get("user_id")
    else:
        user_id = "test1"
    if request.POST.get("process_id"):
        process_id = request.POST.get("process_id")
    else:
        process_id = 13

    # print(input_content)
    # print(type(input_content))
    a = []
    a.append(input_content)
    # for _ in range(10):
    #     a.append(input_content)

    # b = []
    # b.append(input_label)
    # for _ in range(10):
    #     b.append(input_label)
    ##### 전처리
    # dataframe = json.loads(input_content)
    # dataframe = get_preprocessed_data(dataframe)
    tfidf = TfidfVectorizer(token_pattern='\S+')  # 띄어쓰기로 구분시킴
    tfidf.fit(a)
    # print('1')

    train_vector = tfidf.transform(a)
    # print(train_vector)
    # print('2')

    nmf = NMF(n_components=50)  # 차원축소
    nmf.fit(train_vector.toarray())
    train_features = nmf.transform(train_vector.toarray())
    # print(train_features)
    # print('3')


    norm = Normalizer()  # 0 ~ 1 사이로 변경
    train_nf = norm.fit_transform(train_features)
    # print(train_nf)
    # print('4')


    print(os.getcwd())
    # directory = f"C:Users\\multicampus\\Desktop\\finalproject\\s03p31d207\\backend\\data\\models\\{user_id}"
    # filename = f"\\{user_id}_{process_id}_model.sav"
    directory = ".\\textengines\\data\\models\\test1"
    filename = "\\test1_13_model.sav"
    # C:\Users\multicampus\Desktop\finalproject\s03p31d207\backend\textengines\data\models\test1
    # print('5')
    loaded_model = pickle.load(open(directory + filename, 'rb')) # 바이너리 파일을 읽기 위해서는 파일모드를 rb 로, 쓰기 위해서는 wb 로 지정
    # print('6')


    # input_label = int(input_label)


    # print(type(input_label))
    # print(train_nf)
    # print(b)
    # result = loaded_model.score(train_nf, b)
    k = np.array(train_nf)
    print(k)

    # persentage = 0
    # for _ in range(100):
    #     res = loaded_model.predict(k)
    #     final_res = res.tolist()
    #     print(final_res)
    #     if final_res[0]:
    #         persentage += 1
    # # print(res)
    # # print('7')
    # # print(type(res.tolist()))
    # # final_res = res.tolist()
    # print(persentage)
    # posi = 100- persentage
    # ne = persentage
    res = loaded_model.predict(k)
    final_res = res.tolist()

    # return JsonResponse({"0": posi}, {"1": ne})
    return JsonResponse({"result": final_res[0]})

