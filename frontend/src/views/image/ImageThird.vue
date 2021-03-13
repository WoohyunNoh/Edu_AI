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
        <router-link to="/image/first">
          <li>데이터 넣기</li>
        </router-link>
        <router-link to="/image/second">
          <li>학습데이터 고르기</li>
        </router-link>
        <router-link to="/image/third" class="is-active">
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
        <router-link to="/image/second">
          <i class="fas fa-angle-left fa-4x second"></i>
        </router-link>
      </button>
      <div class="code-box">
        <div class="code-up-down">
          <h2>
            CODE
            <!-- <i
              @click="disappearCode"
              class="fas fa-caret-square-up icon"
              v-if="appearCode"
            ></i>
            <i
              @click="disappearCode"
              class="fas fa-caret-square-down icon"
              v-if="!appearCode"
            ></i> -->
          </h2>
        </div>
        <div class="python-code" v-if="appearCode">
          <pre v-highlightjs>
            <code class="python">

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
import tensorflow as tf


imageGenerator = ImageDataGenerator (
    rescale=1. / 255,
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    brightness_range=[.2, .2],
    horizontal_flip=True,
    validation_split=0.1
)

train_set = imageGenerator.flow_from_directory (
    os.path.join(imageRoot),
    target_size=(224, 224),
    batch_size={{this.$store.state.batchSize}},
    subset='training'
)

validation_set = imageGenerator.flow_from_directory (
    os.path.join(imageRoot),
    target_size=(224, 224),
    batch_size={{this.$store.state.batchSize}},
    subset='validation'
)

model = Sequential()

model.add(layers.InputLayer(input_shape=(224, 224, 3)))
model.add(layers.Conv2D(16, (3, 3), (1, 1), 'same', activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(rate=0.3)

model.add(layers.Conv2D(32, (3, 3), (1, 1), 'same', activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(rate=0.3)

model.add(layers.Conv2D(64, (3, 3), (1, 1), 'same', activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(rate=0.3)

model.add(layers.Flatten())
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(10, activation='{{this.activation}}')

model.compile (
    optimizer='adam',
    loss='{{this.loss}}',
    metrics=['acc'],
)

epochs = {{this.$store.state.epoch}}

model.fit (
    train_set,
    epochs=epochs,
    steps_per_epoch=train_set.samples / epochs,
    validation_data=validation_set,
    validation_steps=train_set.samples / epochs,
)

model_file = '/model/path/file' #example
model.save(model_file)

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
        <router-link to="/image/fourth">
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
      trainData: {
        pk: "",
        key: "",
        epoch: "",
        batch: "",
        rate: "",
      },
      activation: "",
      loss: "",
      // isNotLearning: true,
    };
  },
  created() {
    // this.isNotLearning = false;
    // console.log(this.isNotLearning);
    var intval = setInterval(() => {
      if (this.percentage < 100) this.percentage += 0.3;
      else clearInterval(intval);
    }, 10);
  },
  mounted() {
    console.log("개새끼3");
    console.log(this.$store.state.userInfo);
  },
  beforeMount() {
    // console.log("id : " + this.$store.state.userInfo.id + ", key : " + this.$store.state.userInfo.key +
    // " , epoch : " + this.$store.state.epoch + ", batch : " + this.$store.state.batchSize + ", rate : " + this.$store.state.learningRate)
    if (this.$store.state.imageFiles.length == 2) {
      this.activation = "sigmoid";
      this.loss = "binary_crossentropy";
    } else {
      this.activation = "softmax";
      this.loss = "categorical_crossentropy";
    }
    this.$store.dispatch("imageTrain");
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

    trainStart: function() {},
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/progressbar.scss";
@import "~highlight.js/styles/atom-one-dark.css";

/* @import "../assets/srcery.css"; */
/*
Description: Srcery dark color scheme for highlight.js
Author: Chen Bin <chen.bin@gmail.com>
Website: https://srcery-colors.github.io/
Date: 2020-04-06
*/

code {
  height: 380px;
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
  overflow-y: auto;
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
