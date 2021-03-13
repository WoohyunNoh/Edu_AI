<template>
  <div id="text-third">
    <nav style="position:absolute">
      <tm-hamburger-menu disabledriveview>
        <div id="menu-holder">
          <span id="app-name">
            <router-link to="/" class="u-image u-logo u-image-1">
              <img
                src="@/assets/images/default-logo.png"
                style="width:80px; height:30px"
                class="u-logo-image u-logo-image-1"
              /> </router-link
          ></span>
        </div>
      </tm-hamburger-menu>
    </nav>
    <div class="container-fluid">
      <br />
      <ul class="list-unstyled multi-steps">
        <router-link to="/text/first">
          <li>데이터 넣기</li>
        </router-link>
        <router-link to="/text/second">
          <li>학습데이터 고르기</li>
        </router-link>
        <router-link to="/text/third" class="is-active">
          <li>
            파이썬 코드확인<br />
            &학습시작
          </li>
        </router-link>
        <a>
          <li>학습 결과확인</li>
        </a>
      </ul>
    </div>
    <div class="textthird">
      <button class="confirm-before-btn second">
        <router-link to="/text/second">
          <i class="fas fa-angle-left fa-4x second"></i>
        </router-link>
      </button>
      <div class="code-box">
        <div class="code-up-down">
          <h2>
            CODE
          </h2>
        </div>
        <div class="python-code" v-if="appearCode">
          <pre v-highlightjs>
            <code class="python">
import os
import json
import pickle
from pathlib import Path
import pandas as pd

from django.core.cache import cache
from django.http import JsonResponse

from mindlap.celery import app

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



def post(self, request):
    data = request.POST.get("data")
    tagger = request.POST.get("tagger")  # ex) mecab
    model = request.POST.get("model")  # ex) logistic
    batch_size = request.POST.get("batch_size")
    epochs = request.POST.get("epochs")
    learning_rate = request.POST.get("learning_rate")
    print(tagger)
    print(model)
    nd = json.loads(data)
    self.run(nd, tagger=tagger, model=model)

def run(self, nd, tagger, model):
    # start_sklearn_analyze.delay(nd, tagger, model)
    start_sklearn_analyze(nd, tagger, model)


# @app.task(bind=True, ignore_result=True)
def start_sklearn_analyze(dataframe, tagger, model, user_id="test1", process_id=13):
    dataframe = get_preprocessed_data(dataframe)
    ba = BaseAnalyze2(df=dataframe, tagger=tagger, model=model)
    ba.run()

    print(
        f"train_score: {ba.train_score}\nvalidation_score: {ba.validation_score}\ntest_score: {ba.test_score}")

    directory = dir_path + f"\\data\\models\\{user_id}"
    # 해당 경로에 디렉토리가 없으면 추가.
    Path(directory).mkdir(parents=True, exist_ok=True)
    filename = f"\\{user_id}_{process_id}_model.sav"
    pickle.dump(ba.model, open(directory + filename, 'wb'))  # 저장하는 로직 => dump
    print("모델 저장완료")


def get_preprocessed_data(data: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """전처리된 데이터 가져오기

    Args:
        data (pd.DataFrame)

    Returns:
        pd.DataFrame
    """
    df = concat_texts_as_dataframe(data)
    if kwargs.get("n_sample"):
        df = sampling_by_same_ratio(df, **kwargs)
    return df

def concat_texts_as_dataframe(data: dict) -> pd.DataFrame:
    """넘어온 텍스트 데이터를 하나의 dataframe 형태로 리턴

    Args:
        data (dict): {"class1": [글1, 글2], "class2": [글1, 글2], ... }

    Return:
        res (dataframe): 컬럼: label, data
    """
    le = LabelEncoder()
    keys = data.keys()
    vals = data.values()
    res = pd.DataFrame(columns=["label", "data"])
    for k, v in zip(keys, vals):
        d = pd.DataFrame(columns=["label", "data"])
        d["data"] = v
        print(type(k))
        d["label"] = k

        res = pd.concat([res, d])
    res["label"] = le.fit_transform(res["label"])
    return res


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



class BaseAnalyze2:

    def __init__(self, df, tagger="mecab", model="logistic", ratio_train=0.8, ratio_val=0.1, ratio_test=0.1):
        self.df = df
        self.len_categories = len(df["label"].unique())

        self.ratio_train = ratio_train
        self.ratio_val = ratio_val
        self.ratio_test = ratio_test
        self.tagger = self.set_tagger(tagger)
        self.model = self.set_model(model)
        self.set_train_validation_test_split()
        self.set_tfidf_process()

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


    def set_tfidf_process(self):
        tfidf = TfidfVectorizer(token_pattern='\S+')  # 띄어쓰기로 구분시킴
        print(self.X_train)
        tfidf.fit(self.X_train.astype('U'))
        train_vector = tfidf.transform(self.X_train.astype('U'))
        validation_vector = tfidf.transform(self.X_validation.astype('U'))
        test_vector = tfidf.transform(self.X_test.astype('U'))


        nmf = NMF(n_components=50)  # 차원축소
        nmf.fit(train_vector.toarray())
        train_features = nmf.transform(train_vector.toarray())
        validation_features = nmf.transform(validation_vector.toarray())
        test_features = nmf.transform(test_vector.toarray())
        norm = Normalizer()  # 0 ~ 1 사이로 변경
        self.train_nf = norm.fit_transform(train_features)
        self.validation_nf = norm.fit_transform(validation_features)
        self.test_nf = norm.fit_transform(test_features)

    def run(self):
        self.model.fit(self.train_nf, self.y_train)

        self.train_score = self.model.score(self.train_nf, self.y_train)
        self.validation_score = self.model.score(
        self.validation_nf, self.y_validation)
        self.test_score = self.model.score(self.test_nf, self.y_test)

            </code>
          </pre>
        </div>
        <div class="container">
          <div class="learning-text" v-if="percentage < 100">
            {{ parseInt(percentage) }}% 학습중...
          </div>
          <div class="learning-text" v-if="percentage >= 100">학습완료</div>
          <div class="loading-bar">
            <div class="percentage" :style="{width: percentage + '%'}"></div>
          </div>
        </div>
      </div>
      <!-- <button @click="learning" class="learning">학습하기</button> -->
      <button class="confirm-btn second">
        <router-link to="/text/fourth">
          <i class="fas fa-angle-right fa-4x second"></i>
        </router-link>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextThird",
  data() {
    return {
      appearCode: true,
      percentage: 0,
      // isNotLearning: true,
    };
  },
  mounted() {
    console.log(this.$store.state.textInputData);
  },
  created() {
    // this.isNotLearning = false;
    // console.log(this.isNotLearning);
    var intval = setInterval(() => {
      if (this.percentage < 100) this.percentage += 0.3;
      else clearInterval(intval);
    }, 10);
    console.log(this.$store.state.textInputData);
  },
  beforeMount() {
    // console.log("id : " + this.$store.state.userInfo.id + ", key : " + this.$store.state.userInfo.key +
    // " , epoch : " + this.$store.state.epoch + ", batch : " + this.$store.state.batchSize + ", rate : " + this.$store.state.learningRate)
    this.$store.dispatch("textTrain");
  },
  methods: {
    // disappearCode() {
    //   this.appearCode = !this.appearCode;
    //   console.log(this.appearCode);
    // },
    // alertlearning() {
    //   this.isLearning = true;
    //   alert("학습이 시작됩니다");
    // },
  },
};
</script>

<style lang="scss" scoped>
@import "~highlight.js/styles/hybrid.css";
@import "@/assets/scss/progressbar.scss";
/* @import "../assets/srcery.css"; */
/*
Description: Srcery dark color scheme for highlight.js
Author: Chen Bin <chen.bin@gmail.com>
Website: https://srcery-colors.github.io/
Date: 2020-04-06
*/
.confirm-before-btn {
  position: absolute;
  left: 0%;
  top: 43%;
  border: 0;
  color: rgba(133, 164, 250, 0.411);
  // margin-left: 10px;
  background: none;
  font-size: 30px;
  font-weight: 900;
}
.confirm-btn {
  position: absolute;
  right: 0%;
  top: 43%;
  border: 0;
  color: rgba(133, 164, 250, 0.411);
  // margin-left: 10px;
  background: none;
  font-size: 30px;
  font-weight: 900;
}
.second {
  color: rgba(133, 164, 250, 0.411) !important;
}
.second:hover {
  color: rgba(133, 164, 250) !important;
  cursor: pointer;
}
.second:focus {
  outline: none !important;
  border: 0;
}
.icon:hover {
  cursor: pointer;
}
.learning {
  position: absolute;
  bottom: 8%;
  right: 50%;
}
.python-code {
  margin: 0 auto;
  padding: 0;
  width: 70%;
  height: 50%;
}
code {
  height: 400px;
  overflow: auto;
}
code::-webkit-scrollbar {
  width: 5px;
  background: rgb(171, 196, 241);
  border-radius: 5px;
}
code::-webkit-scrollbar-thumb {
  background-color: #6fb2e99c;
}
code::-webkit-scrollbar-track {
  background-color: rgb(236, 236, 236);
}
#text-third {
  position: relative;
  width: 100vw;
  height: 100vh;
  /* background: rgba(105, 233, 133, 0.479); */
}
.textthird {
  margin: 0 auto;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 70%;
  // background: rgba(144, 218, 236, 0.671);
  padding: 20px;
}
.text-third {
  height: 40px;
}

.code-up-down {
  height: 45px;
  text-align: center;
}

.container {
  width: 100%;
  height: 80%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.loading-bar {
  background: rgba(228, 228, 228, 0.479);
  position: relative;
  margin: 3px auto;
  margin-top: 20px;
  width: 800px;
  height: 20px;
  overflow: hidden;
  border-radius: 50px;
  border-bottom: 1px solid #ddd;
  box-shadow: insert 0 1px 2px rgba($color: #000, $alpha: 0.4), 0 -1px 1px #fff,
    0 1px 0 #fff;
}

.percentage {
  position: absolute;
  top: 1px;
  left: 1px;
  right: 1px;
  display: block;
  height: 100%;
  width: 50%;
  border-radius: 50px;
  background: #41a0dfc4;
  background-size: 30px 30px;
  // background-image: linear-gradient(
  //   135deg,
  //   rgba($color: #fff, $alpha: 0.15) 25%,
  //   transparent 25%,
  //   transparent 50%,
  //   rgba($color: #fff, $alpha: 0.15) 50%,
  //   rgba($color: #fff, $alpha: 0.15) 75%,
  //   transparent 75%,
  //   transparent
  // );
  animation: animate-stripes 3s linear infinite;
}

@keyframes animate-stripes {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 60px 0;
  }
}
.learning-text {
  // margin-top: 50px;
  font-size: 20px;
  font-weight: 700;
}
</style>
