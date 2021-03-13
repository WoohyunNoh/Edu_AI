"""
전처리 관련 함수 정의
"""
import os
import re
import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import LabelEncoder

#tokenizer
from konlpy.tag import Okt  
from konlpy.tag import Komoran
from eunjeon import Mecab
from konlpy.tag import Hannanum
from konlpy.tag import Kkma




def concat_texts_as_dataframe(data: dict) -> pd.DataFrame:
    """넘어온 텍스트 데이터를 하나의 dataframe 형태로 리턴

    Args:
        data (dict): {"class1": [글1, 글2], "class2": [글1, 글2], ... }

    Return:
        res (dataframe): 컬럼: label, data
    """
    print('concat_texts_as_dataframe')
    # print(data)       # 딕셔너리

    le = LabelEncoder()
    keys = data.keys()
    vals = data.values()
    res = pd.DataFrame(columns=["label", "data"])
    for k, v in zip(keys, vals):
        d = pd.DataFrame(columns=["label", "data"])
        d["data"] = v
        print("label")
        print(type(k))
        d["label"] = k

        res = pd.concat([res, d])
    res["label"] = le.fit_transform(res["label"])
    print(res)    # 표로 바뀜

    return res


def tokenizer(sentence: str) -> str:
    """텍스트를 토큰화 시킨다. Mecab을 사용해서 토큰화시킨다.

    Return:
        s (string): "안녕/NNG 부산/NNG ..."
    """
    #### Mecab##############
    tag = Okt()
    tag = Komoran()
    tag = Hannanum()
    tag = Kkma()
    tag = Mecab()
    pos = tag.pos(sentence)
    temp = []
    for p in pos:
        temp.append(p[0] + "/" + p[1])

    s = ' '.join(temp)
    return s

    ##################



def sampling_by_same_ratio(dataframe: pd.DataFrame, n_sample: int, shuffle=False, random_state=42):
    """label의 개수를 동일하게 맞춰서 dataframe을 return 함.

    ex) label이 [1, 2, 3] 이라고 할 때, n_sample 이 1000 이면 random 하게 각 label 의 데이터를 333개 뽑는다.
    그리고 이를 합쳐서 return 한다.

    Args:
        dataframe (pd.DataFrame): dataframe \n
        n_sample (int): 원하는 sample 개수 \n
        shuffle (bool): True 면 dataframe을 shuffle 시켜 줌. \n
        random_state (int, optional): None 이면 샘플링 추출할 때 결과가 바뀜. Defaults to 42. \n
    """
    if random_state:
        np.random.seed(random_state)

    n_by_label = n_sample // len(dataframe["label"].unique())
    gd = dataframe.groupby('label').apply(
        lambda x: x.take(np.random.permutation(len(x))[:n_by_label]))
    gd.index.names = ["temp_label", None]
    gd = gd.reset_index(level=[0])
    gd = gd.drop(["temp_label"], axis=1)

    np.random.seed(0)
    return shuffle(gd) if shuffle else gd


def get_preprocessed_data(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """전처리된 데이터 가져오기

    Args:
        data (pd.DataFrame)

    Returns:
        pd.DataFrame
    """
    # print('------------preprocessed')
    # print(data)                {'class1': ['나는 배가 너무 고파 화가난다', '넘어져서 기분이 않좋다'], 'class2': ['음식이 맛있어서 기분이 좋다', '새 컴퓨터를 사서 기분이 좋다']}
    print('get_preprecess까지 왔어!!!!!!!!')
    # print(data)
    # print(data) # 딕셔너리
    df = concat_texts_as_dataframe(data)
    if kwargs.get("n_sample"):
        df = sampling_by_same_ratio(df, **kwargs)
    print("get_preprecess마지막까지 왔어")

    # df["data"] = df["data"].apply(tokenizer)

    return df


def get_preprocessed_csv_data(directory: str, **kwargs) -> pd.DataFrame:
    """CSV 파일 풀기

    Args:
        directory (str): csv 파일의 경로

    Returns:
        pd.DataFrame
    """

    # df = concat_texts_as_dataframe(data)
    df = pd.read_csv(directory)

    if kwargs.get("n_sample"):
        df = sampling_by_same_ratio(df, **kwargs)

    # df["data"] = df["data"].apply(tokenizer)

    return df


def get_tfidf_vector_data(data: pd.DataFrame):
    """텍스트 데이터를 tf-idf 를 통하여 vector 화 시킨 후 return\n
    참조: `https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html`

    Args:
        data (pd.DataFrame): [description]

    Returns:
        numpy.ndarray
    """

    tfidf = TfidfVectorizer()
    tfidf_sparse_matrix = tfidf.fit_transform(data)
    return tfidf_sparse_matrix.toarray()


# def normalize_tfidf_vector_data(tfidf_vector)
