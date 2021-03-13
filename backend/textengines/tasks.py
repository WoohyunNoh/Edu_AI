from __future__ import absolute_import
import os
import json
import pickle
from pathlib import Path
import pandas as pd

from django.core.cache import cache
from django.http import JsonResponse

from .preprocess import get_preprocessed_data
from .analyzer import BaseAnalyze, BaseAnalyze2
from mindlap.celery import app

dir_path = os.path.dirname(os.path.realpath(__file__))


# bind=True 를 해줘야지, 해당 task 의 제일 처음 인자에 self 를 사용할 수 있다!
# Celery는 기본적으로 수행 결과(return)을 저장 해야 작업이 끝난다.
# @app.task(bind=True, ignore_result=True)
def start_lstm_analyze(dataframe, vocab_size, max_len, batch_size, epochs, learning_rate=0.01, user_id="test1", process_id=12):
                            # nd, vocab_size=30000, max_len=1000, batch_size=16, epochs=50, learning_rate=0.001
    print('delay 성공')
    print(dataframe)
    dataframe = get_preprocessed_data(dataframe)
    print(dataframe)
    
    print('get_preprocessed_data/ tasks.py')
    ba = BaseAnalyze(dataframe, vocab_size, max_len,
                     batch_size, epochs, learning_rate)
    print('analyze')
    ba.lstm_fit()              # 여기가 바로 모델만들고 fit까지
    print('fit완료')
    print(ba.lstm_acc())

    # 사용자의 아이디가 test1 이라고 가정할 때,
    # 실행한 학습의 pk 번호가 12 라고 가정할 때,
    # TODO: check point 를 통해서 해당 경로에 저장시켜 주는 방식으로 바꿔야 함.

    directory = dir_path + f"\\data\\models\\{user_id}"
    # 해당 경로에 디렉토리가 없으면 추가.
    Path(directory).mkdir(parents=True, exist_ok=True)

    ba.lstm_model.save(directory + f"\\{user_id}_{process_id}_model.h5")
    # 해당 task 를 terminate 시키는 것!!
    # app.control.revoke(self.request.id, terminate=True)
    return JsonResponse({"data": "done!!"})


# @app.task(bind=True, ignore_result=True)
def start_sklearn_analyze(dataframe, tagger, model, user_id="test1", process_id=13):
    # print(dataframe)
    print('aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbb')
    dataframe = get_preprocessed_data(dataframe)
    print(dataframe)
    ba = BaseAnalyze2(df=dataframe, tagger=tagger, model=model)
    print('2')
    ba.run()

    print(
        f"train_score: {ba.train_score}\nvalidation_score: {ba.validation_score}\ntest_score: {ba.test_score}")

    directory = dir_path + f"\\data\\models\\{user_id}"
    # 해당 경로에 디렉토리가 없으면 추가.
    Path(directory).mkdir(parents=True, exist_ok=True)
    filename = f"\\{user_id}_{process_id}_model.sav"
    pickle.dump(ba.model, open(directory + filename, 'wb'))  # 저장하는 로직 => dump
    print("모델 저장완료")

    """
    pickle.load(파일) 을 통해서 파일 내용을 읽어오려면, pickle.dump를 사용해서 데이터를 입력한 파일이어야한다.
    sklearn 으로 저장시킨 모델을 불러와서 score 확인하는 방법은 다음과 같습니다.
    loaded_model = pickle.load(open(directory + filename, 'rb'))
    result = loaded_model.score(X_test, Y_test)
    print(result)

    X_test, Y_test 는 전처리과정을 통해 변경시켜주셔야 합니다.
    """
    # app.control.revoke(self.request.id, terminate=True)
    return JsonResponse({"data": "done!!"})