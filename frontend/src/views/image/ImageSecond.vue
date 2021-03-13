<template>
  <div id="text-second">
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
        <router-link to="/image/second" class="is-active">
          <li>학습데이터 고르기</li>
        </router-link>
        <a>
          <li>
            파이썬 코드확인<br />
            &학습시작
          </li>
        </a>
        <a>
          <li>학습 결과확인</li>
        </a>
      </ul>
    </div>
    <div class="second-box">
      <div class="box-left">
        <ul class="menus">
          <li
            @click="clickModel"
            id="model"
            class="model text-color"
            data-value="model"
            :class="{addBackground: backColor[1], bright: sideColor[1]}"
          >
            Model 선택
          </li>
          <li
            id="parameter"
            class="parameter text-color"
            data-value="parameter"
            :class="{addBackground: backColor[2], bright: sideColor[2]}"
          >
            학습 Parameter선택
          </li>
        </ul>
      </div>
      <div class="box-right">
        <div
          class="model-control control-box"
          v-if="Option == 'tokenizer' || Option == 'model'"
        >
          <h2 class="token long-shadow">Model</h2>
          <div class="mcontrol-box cbox">
            <div class="m-table">
              <div class="tooltip2">
                <i class="far fa-question-circle fa-2x"></i>
                <div class="tooltip-content">
                  <p>
                    딥 러닝에서 심층 신경망으로 분류되며, 시각적 영상 분석에
                    주로 적용된다.
                  </p>
                </div>
              </div>
              <input
                v-model="model"
                @click="checkBtn"
                id="single"
                value="first"
                true-value="first"
                class="radios"
                type="radio"
              />
              <label for="single" class="labels">
                <p>{{ modelList[0] }}</p>
              </label>
            </div>
          </div>
          <button @click="checkModel" class="confirm-btn fa-3x">
            <i class="fas fa-angle-right fa-3x"></i>
          </button>
        </div>
        <div
          class="parameter-control control-box"
          v-if="Option == 'nextparameter'"
        >
          <h2 class="parameter-h2 long-shadow">
            PARAMETER
          </h2>
          <div class="parameter-box">
            <div class="epoch third-elem">
              <div class="parameter-content">
                <h1>Epoch</h1>
                <div class="tooltip">
                  <i class="far fa-question-circle fa-2x"></i>
                  <div class="tooltip-content">
                    <p>
                      1 Epoch 이란 트레이닝 데이터 셋 내의 모든 샘플이 적어도 한
                      번은 트레이닝 모델을 통해 공급된 것을 의미합니다. Epoch
                      50으로 설정하면 트레이닝 중인 모델은 트레이닝 데이터 셋
                      전체에서 50회 동작합니다. 일반적으로 Epoch 수치가 클수록
                      모델은 데이터의 예측을 보다 효율적으로 학습합니다.
                    </p>
                    <p>
                      좋은 훈련 결과를 얻을 때까지, 이 수치를 조정(일반적으로
                      증가)하는 것을 추천합니다.
                    </p>
                  </div>
                </div>
              </div>

              <div class="input-holder">
                <input
                  type="number"
                  @keypress="handlechange(epochD)"
                  v-model="epochD"
                  value="epochD"
                  min="0"
                  maxlength="4"
                  step="10"
                  style="width: 54px;"
                  max="100"
                  pattern="[0-9]{2}"
                  required
                />
                <button @click="appendEpoch" class="addnum">등록</button>
                <div class="tag-box">
                  <ul>
                    <li
                      v-for="(tag, index) in dataValue[0].epoch"
                      :key="tag.id"
                      class="tag-list"
                    >
                      {{ tag }}
                      <button class="del-btn" @click="deleteepochTag(index)">
                        &#10006;
                      </button>
                    </li>
                  </ul>
                </div>
                <!-- <input type="submit"> -->
              </div>
            </div>
            <div class="batch-size third-elem input-holder">
              <div class="parameter-content">
                <h1>Batch Size</h1>
                <div class="tooltip">
                  <i class="far fa-question-circle fa-2x"></i>
                  <div class="tooltip-content">
                    <p>
                      Batch란 1회 훈련에서 사용되는 샘플 세트입니다. 예를 들어
                      80개의 이미지가 있고 배치 사이즈로 16을 선택했다고
                      가정했을 때, 데이터는 80/16=5 Batch로 분할됩니다. 5개의
                      Batch 가 모두 모델을 통해 공급되면 1개의 Epoch이
                      완성됩니다.
                    </p>
                    <p>
                      좋은 훈련 결과를 얻기 위해 이 숫자를 미세 조정할 필요는
                      없습니다.
                    </p>
                  </div>
                </div>
              </div>
              <select
                class="input-holder"
                id="select-input"
                name="batch"
                v-model="batchD"
              >
                <option value="16">16</option>
                <option value="32">32</option>
                <option value="64">64</option>
                <option value="128">128</option>
                <option value="256">256</option>
                <option value="512">512</option>
              </select>
              <button @click="appendBatch" class="addnum">등록</button>
              <div class="tag-box">
                <ul>
                  <li
                    v-for="(tag, index) in dataValue[1].batch"
                    :key="tag.id"
                    class="tag-list"
                  >
                    {{ tag }}
                    <button class="del-btn" @click="deletebatchTag(index)">
                      &#10006;
                    </button>
                  </li>
                </ul>
              </div>
            </div>
            <div class="learning-rate third-elem">
              <div class="parameter-content">
                <h1>Learning Rate</h1>
                <div class="tooltip">
                  <i class="far fa-question-circle fa-2x"></i>
                  <div class="tooltip-content2">
                    <p>
                      이 숫자를 신중하게 미세 조정하세요! 아주 작은 차이라도
                      모델이 어느 정도 학습하는가에 큰 영향을 줄 수 있습니다.
                    </p>
                  </div>
                </div>
              </div>
              <div class="input-holder">
                <input
                  v-model="learningD"
                  type="number"
                  id="learning-rate-input"
                  value="0.001"
                  maxlength="6"
                  style="width: 80px; margin-left: 0px;"
                  min="0.00001"
                  max="0.1"
                  step="0.00001"
                  pattern="[0-9]{2}"
                  required
                />
                <button @click="appendLearning" class="addnum">등록</button>
                <div class="tag-box">
                  <ul>
                    <li
                      v-for="(tag, index) in dataValue[2].learning"
                      :key="tag.id"
                      class="tag-list"
                    >
                      {{ tag }}
                      <button class="del-btn" @click="deletelearningTag(index)">
                        &#10006;
                      </button>
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
          <button @click="clickModel" class="cancle-btn fa-3x">
            <i class="fas fa-angle-left fa-3x"></i>
          </button>
          <button @click="checkParameter" class="confirm-btn fa-3x">
            <router-link to="/image/third">
              <i class="fas fa-angle-right fa-3x"></i>
            </router-link>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextThird",
  data() {
    return {
      Option: "tokenizer",
      backColor: [false, false, false],
      sideColor: [true, true, false],
      model: "",
      parameter: "",
      PossibleNext: false,
      modelList: ["CNN(컨볼루션 신경망 분류 모델)"],
      dataValue: [{epoch: []}, {batch: []}, {learning: []}],
      epochD: 50,
      batchD: 16,
      learningD: 0.001,
      isNotLearning: true,
      percentage: 0,
    };
  },
  mounted() {
    console.log("개새끼2");
    console.log(this.$store.state.userInfo);
  },
  beforeMount() {
    console.log(
      "id : " +
        this.$store.state.userInfo.id +
        ", key : " +
        this.$store.state.userInfo.key +
        " , epoch : " +
        this.$store.state.epoch +
        ", batch : " +
        this.$store.state.batchSize +
        ", rate : " +
        this.$store.state.learningRate
    );
  },
  methods: {
    handlechange() {
      if (this.epochD < 0) this.epochD = 0;
      if (this.epochD > 100) this.epochD = 100;
    },
    appendEpoch() {
      let err = true;
      let maxOver = false;
      let overLap = false;
      if (this.epochD > 100) {
        alert("100이하 숫자만 가능합니다");
        err = false;
        this.epochD = 50;
      } else if (this.epochD < 0) {
        this.epochD = 50;
        alert("0이상 숫자만 가능합니다");
        err = false;
      }
      if (this.dataValue[0].epoch.length >= 1) {
        alert("값은 1개만 등록이 가능합니다.");
        maxOver = true;
      }
      // for (var i = 0; i < this.dataValue[0].epoch.length; i++) {
      //   console.log(this.dataValue[0].epoch[i]);
      //   console.log(this.epochD);
      //   if (this.dataValue[0].epoch[i] == this.epochD) {
      //     alert("중복되지 않는 값만 등록이 가능합니다");
      //     overLap = true;
      //   }
      // }

      if (err && !maxOver && !overLap) {
        this.dataValue[0].epoch.push(parseInt(this.epochD));
        this.$store.commit("changeEpoch", this.epochD);
      }
    },
    appendBatch() {
      //js에서 int로 변환 => parseInt
      let maxOver = false;
      let overLap = false;
      if (this.dataValue[1].batch.length >= 1) {
        alert("값은 1개만 등록이 가능합니다.");
        maxOver = true;
      }
      // if (!maxOver) {
      //   for (var i = 0; i < this.dataValue[1].batch.length; i++) {
      //     console.log(this.dataValue[1].batch[i]);
      //     console.log(this.batchD);
      //     if (this.dataValue[1].batch[i] == this.batchD) {
      //       alert("중복되지 않는 값만 등록이 가능합니다");
      //       overLap = true;
      //     }
      //   }
      // }
      if (!maxOver && !overLap) {
        this.dataValue[1].batch.push(parseInt(this.batchD));
        this.$store.commit("changeBatchSize", this.batchD);
      }
    },
    appendLearning() {
      let err = true;
      let maxOver = false;
      let overLap = false;
      if (this.learningD > 0.1) {
        alert("0.1이하 숫자만 가능합니다");
        err = false;
        this.learningD = 50;
      } else if (this.learningD < 0.00001) {
        this.learningD = 50;
        alert("0.00001이상 숫자만 가능합니다");
        err = false;
      }
      if (this.dataValue[2].learning.length >= 1) {
        alert("값은 1개만 등록이 가능합니다.");
        maxOver = true;
      }
      // for (var i = 0; i < this.dataValue[2].learning.length; i++) {
      //   console.log(this.dataValue[2].learning[i]);
      //   console.log(this.batchD);
      //   if (this.dataValue[2].learning[i] == this.learningD) {
      //     alert("중복되지 않는 값만 등록이 가능합니다");
      //     overLap = true;
      //   }
      // }
      if (err && !maxOver && !overLap) {
        this.dataValue[2].learning.push(parseFloat(this.learningD));
        this.$store.commit("changeLearningRate", this.learningD);
      }
    },
    deleteepochTag(index) {
      this.dataValue[0].epoch.splice(index, 1);
      console.log(this.dataValue[0].epoch.index);
    },
    deletebatchTag(index) {
      this.dataValue[1].batch.splice(index, 1);
      console.log(this.dataValue[1].batch.index);
    },
    deletelearningTag(index) {
      this.dataValue[2].learning.splice(index, 1);
      console.log(this.dataValue[2].learning.index);
    },
    clickTokenizer() {
      if (this.Option != "tokenizer") {
        if (confirm("이 전 선택이 초기화됩니다. 돌아가시겠습니까?")) {
          this.Option = "tokenizer";
          this.backColor = [false, false, false];
          this.sideColor = [true, false, false];
          this.model = "";
          this.parameter = "";
          this.PossibleNext = false;
        }
      }
    },
    clickModel() {
      if (this.Option == "nextparameter") {
        if (confirm("이 전 선택이 초기화됩니다. 돌아가시겠습니까?")) {
          this.Option = "model";
          this.backColor = [true, false, false];
          this.sideColor = [true, true, false];
          this.parameter = "";
          this.PossibleNext = false;
        }
      }
    },
    checkModel() {
      this.Option = "nextparameter";
      this.backColor[1] = true;
      this.sideColor[2] = true;
      console.log(this.backColor, this.sideColor);
      alert("Model이 저장되었습니다");
    },
    checkParameter() {
      this.PossibleNext = true;
      this.backColor = [true, true, true];
      this.sideColor = [true, true, true];
      alert("Parameter가 저장되었습니다");
    },

    //model
    checkBtn() {
      this.checked != this.checked;
    },

    // chooseOption(event) {
    //   var telem = document.getElementById('tokenizer')
    //   var melem = document.getElementById('model')
    //   var pelem = document.getElementById('parameter')
    //   var classname = event.toElement.className

    //   console.log('classname', classname)
    //   console.log(telem)
    //   console.log(document)
    //   if ('tokenizer' == classname) {
    //     this.Option = 'tokenizer';
    //       telem.setAttribute('class', 'tokenizer bright')
    //       melem.setAttribute('class', 'model')
    //       pelem.setAttribute('class', 'parameter')

    //   } else if ('nextmodel' == classname) {
    //       if (this.Option == 'tokenizer') {
    //         alert("Tokenizer를 선택해주세요")
    //       }
    //       else if (this.Option == 'nextmodel') {
    //         this.Option = 'model';
    //         telem.setAttribute('class', 'tokenizer add-background bright')
    //         melem.setAttribute('class', 'model bright')
    //         pelem.setAttribute('class', 'parameter')
    //       }

    //   } else if ('parameter' == classname){
    //     if (this.Option == 'tokenizer') {
    //       alert("Tokenizer를 선택해주세요")
    //     }
    //     else if (this.Option == 'nextmodel' || this.Option == 'Model') {
    //       alert("Model을 선택해주세요")
    //     }
    //     else {
    //       this.Option = 'nextparameter';
    //       telem.setAttribute('class', 'tokenizer add-background bright')
    //       melem.setAttribute('class', 'model add-background bright')
    //       pelem.setAttribute('class', 'parameter bright')
    //     }
    //   }

    // }
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/progressbar.scss";
// @import "@/assets/scss/longshadow.scss";

.parameter-h2 {
  margin-right: 100px;
}
.parameter-content {
  display: flex;
}
.parameter-content h1 {
  margin-left: 50px;
}

.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip2 {
  position: absolute;
  top: 235px;
  left: 240px;
  display: inline-block;
}

.tooltip .tooltip-content {
  visibility: hidden;
  width: 300px;
  height: 250px;
  background-color: rgba(0, 0, 0, 0.904);
  font-size: 15px;
  padding: 13px;
  margin-top: 10px;
  color: white;
  text-align: left;
  position: absolute;
  z-index: 1;
  font-family: "Noto Sans KR", sans-serif;
  left: 100%;
}
.tooltip2 .tooltip-content {
  visibility: hidden;
  width: 300px;
  background-color: rgba(0, 0, 0, 0.904);
  font-size: 15px;
  padding: 13px;
  margin-top: 10px;
  color: white;
  text-align: left;
  position: absolute;
  z-index: 1;
  font-family: "Noto Sans KR", sans-serif;
  top: -100px;
  right: 70%;
}

.tooltip .tooltip-content2 {
  visibility: hidden;
  width: 300px;
  background-color: rgba(0, 0, 0, 0.904);
  font-size: 15px;
  padding: 13px;
  margin-top: 10px;
  color: white;
  text-align: left;
  position: absolute;
  z-index: 1;
  font-family: "Noto Sans KR", sans-serif;
  bottom: -80px;
  right: 120%;
}

.tooltip:hover .tooltip-content {
  visibility: visible;
}

.tooltip2:hover .tooltip-content {
  visibility: visible;
}

.tooltip:hover .tooltip-content2 {
  visibility: visible;
}

.text-color {
  color: rgb(104, 153, 243);
}

.input-holder {
  display: inline-block;
  // margin-right: 40px;r
}

.input-holder input {
  border: 2px solid transparent;
  border-radius: 3px;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom: 2px solid #4285f4;
  width: 50px;
  padding: 4px;
  margin: 0 5px;
  text-align: center;
  font-size: inherit;
  color: inherit;
  font-family: "Google Sans", Helvetica, Arial, sans-serif;
}
.input-holder input:focus {
  outline: 0;
  border: 2px solid var(--focus-color);
}

input {
  padding: 4px;
}
.input-holder {
  display: inline-block;
}

.input-holder input[type="text"] {
  background-color: #e8f0fe;
  border: 0;
  outline: 0;
  border-radius: 3px;
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
  border-bottom: 2px solid #1967d2;
  width: 50px;
  padding: 4px;
  margin: 0 5px;
  text-align: center;
  font-size: inherit;
  color: #1967d2;
  font-size: 14px;
  font-weight: 500;
  font-family: "Google Sans", Helvetica, Arial, sans-serif;
}

.input-holder input[type="number"] {
  position: relative;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 42px;
  padding: 4px 6px;
  margin: 0 5px;
  border: 0;
  outline: 0;
  border-radius: 3px;
  background-color: #e8f0fe;
  color: #1967d2;
  font-size: 14px;
  letter-spacing: 0.3px;
  font-weight: 500;
  font-family: "Google Sans", Helvetica, Arial, sans-serif;
}
//요거

.input-holder input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  cursor: pointer;
  display: block;
  position: relative;
}
.input-holder input[type="number"]::-webkit-outer-spin-button,
.input-holder input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  opacity: 1;
  width: 19px;
  height: 26px;
  background-image: url("data:image/svg+xml,%3Csvg width='19' height='24' viewBox='0 0 19 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E %3Cpath d='M0 0H17C18.1046 0 19 0.895431 19 2V22C19 23.1046 18.1046 24 17 24H0V0Z' fill='%231967D2'/%3E %3Cpath d='M9.5 20L5.60289 14.75L13.3971 14.75L9.5 20Z' fill='%23FFFFFF'/%3E %3Cpath d='M9.5 4L13.3971 9.25H5.60289L9.5 4Z' fill='%23FFFFFF'/%3E %3C/svg%3E%0A");
  background-repeat: no-repeat, repeat;
  background-position: right 0 top 50%, 0 0;
  background-size: cover;
  position: absolute;
  top: 0;
  right: 0;
}

.input-holder select {
  position: relative;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 62px;
  padding: 4px 8px;
  margin: 0 5px;
  border: 0;
  outline: 0;
  background-color: #e8f0fe;
  color: #1967d2;
  font-size: 14px;
  letter-spacing: 0.3px;
  font-weight: 500;
  font-family: "Google Sans", Helvetica, Arial, sans-serif;

  background-image: url("data:image/svg+xml,%3Csvg width='19' height='24' viewBox='0 0 19 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0H17C18.1046 0 19 0.895431 19 2V22C19 23.1046 18.1046 24 17 24H0V0Z' fill='%231967D2'/%3E%3Cpath d='M9.5 15L5.60289 9.75L13.3971 9.75L9.5 15Z' fill='%23FFFFFF'/%3E%3C/svg%3E%0A");
  background-repeat: no-repeat, repeat;
  background-position: right 0 top 50%, 0 0;
  background-size: 1.75em auto, 100%;
}

.input-holder select[disabled] {
  background-image: url("data:image/svg+xml,%3Csvg width='19' height='24' viewBox='0 0 19 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0H17C18.1046 0 19 0.895431 19 2V22C19 23.1046 18.1046 24 17 24H0V0Z' fill='%23F1F3F4'/%3E%3Cpath d='M9.5 15L5.60289 9.75L13.3971 9.75L9.5 15Z' fill='%23FFFFFF'/%3E%3C/svg%3E%0A");
  background-color: #f1f3f4;
  color: #bdc1c6;
}

.input-holder input[type="number"][disabled] {
  background-color: #f1f3f4;
  color: #bdc1c6;
}

.input-holder input[type="number"][disabled]::-webkit-outer-spin-button,
.input-holder input[type="number"][disabled]::-webkit-inner-spin-button {
  background-image: url("data:image/svg+xml,%3Csvg width='19' height='24' viewBox='0 0 19 24' fill='none' xmlns='http://www.w3.org/2000/svg'%3E %3Cpath d='M0 0H17C18.1046 0 19 0.895431 19 2V22C19 23.1046 18.1046 24 17 24H0V0Z' fill='%23 ==$0F1F3F4'/%3E %3Cpath d='M9.5 20L5.60289 14.75L13.3971 14.75L9.5 20Z' fill='%23FFFFFF'/%3E %3Cpath d='M9.5 4L13.3971 9.25H5.60289L9.5 4Z' fill='%23FFFFFF'/%3E %3C/svg%3E%0A");
}

.input-holder input:focus,
.input-holder select:focus {
  outline: 2px solid var(--focus-color);
}
.fa-3x {
  color: rgba(133, 164, 250, 0.411);
}
.fa-3x:hover {
  color: rgba(133, 164, 250);
  cursor: pointer;
}
.fa-3x:focus {
  outline: none !important;
  border: 0;
}
#text-second {
  position: relative;
  width: 100vw;
  height: 100vh;
  position: relative;
  // background: rgba(71, 71, 71, 0.479);
}
.second-box {
  margin-top: 10px;
  width: 100%;
  height: 70%;
  // background: cornflowerblue;
}
.box-left {
  padding: 10px;
  width: 20%;
  height: calc(100% - 20px);
  // background: crimson;
  float: left;
  position: relative;
}
.box-left:after {
  content: "";
  display: block;
  height: 350px;
  width: 1px;
  position: absolute;
  right: 0;
  top: 18%;
  border-right: solid rgb(170, 170, 170) 2px;
}
.menus {
  list-style: none;
  height: 350px;
  padding: 10px 0;
  // background: royalblue;
  position: absolute;
  right: 0;
  top: 15%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.menus li {
  font-size: 20px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 10px;
  font-weight: 800;
  // background: salmon;
}
select.input-holder {
  border-radius: 5px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.363);
  position: relative;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 62px;
  padding: 4px 8px;
  margin: 0 5px;
  border: 0;
  outline: 0;
  background-color: #e8f0fe;
  color: #1967d2;
  font-size: 14px;
  letter-spacing: 0.3px;
  font-weight: 500;
  font-family: "Google Sans", Helvetica, Arial, sans-serif;
  // background-image: url(data:image/svg+xml,%3Csvg width=19 height=24 viewBox=0 0 19 24 fill=none xmlns=http://www.w3.org/2000/svg%3E%3Cpath d=M0 0H17C18.1046 0 19 0.895431 19 2V22C19 23.1046 18.1046 24 17 24H0V0Z fill=%231967D2/%3E%3Cpath d=M9.5 15L5.60289 9.75L13.3971 9.75L9.5 15Z fill=%23FFFFFF/%3E%3C/svg%3E%0A);
  background-repeat: no-repeat, repeat;
  background-position: right 0 top 50%, 0 0;
  background-size: 1.75em auto, 100%;
}
.bright {
  border-right: solid rgba(40, 99, 209, 0.411) 8px;
}
.addBackground {
  background: rgba(40, 99, 209, 0.411);
  color: white;
}
.box-right {
  width: 77%;
  height: 100%;
  float: left;
  // background: cyan;
}
.control-box {
  margin: 0 auto;
  width: 90%;
  height: 90%;
  position: relative;
  // background: sandybrown;
}
.control-box h2 {
  text-align: center;
  padding-top: 50px;
  margin-right: 100px;
  font-size: 30px;
  text-transform: uppercase;
  color: rgb(53, 152, 233);
}
.tcontrol-box {
  display: flex;
  flex-direction: row;
  margin: 0;
}

.cbox {
  // background: seagreen;
  justify-content: center;
  align-items: center;
  width: 90%;
  height: 60%;
  margin: 0 auto;
}
.mcontrol-box {
  display: flex;
  flex-direction: column;
}
// .mcontrol-box button {
//   padding: 20px 50px;
//   border-radius: 10px;
//   border: 0;
//   margin-left: 10px;
//   background: none;
//   font-size: 30px;
//   color: rgb(53, 131, 233);
//   font-weight: 900;
// }

.m-table {
  width: 500px;
  height: 400px;
  margin-top: 100px;
  margin-right: 100px;
}

.labels {
  width: 100%;
  height: 60px;
}
.labels p {
  border-radius: 10px;
  background: #e2f5fdc0;
  font-size: 20px;
  padding: 20px;
  text-align: center;
  margin: 5px;
  // color: white;
  font-weight: 700;
  // color: rgb(124, 192, 255);
}
.radios[type="radio"] {
  display: none;
}
input[type="radio"]:checked + .labels p {
  background: rgb(135, 202, 247);
  color: white;
}

.tcontrol-box select {
  padding: 20px 50px;
  font-size: 20px;
  border-radius: 10px;
}

.confirm-btn {
  position: absolute;
  right: 0%;
  top: 45%;
  // padding: 20px 50px;
  border-radius: 10px;
  border: 0;
  // margin-left: 10px;
  background: none;
  font-size: 30px;
  color: rgb(196, 211, 223);
  font-weight: 900;
}
.cancle-btn {
  position: absolute;
  left: 0%;
  top: 45%; // padding: 20px 50px;
  border-radius: 10px;
  border: 0;
  // margin-left: 10px;
  background: none;
  font-size: 30px;
  color: rgb(196, 211, 223);
  font-weight: 900;
}
.parameter-box {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  margin: 0 auto;
  width: 100%;
  height: 60%;
  text-align: center;
}
.second-elem {
  width: 300px;
  height: 200px;
  // background: tomato;
  text-align: center;
}
.second-elem h1 {
  margin-top: 0;
}
.addnum {
  padding: 3px;
  border: none;
  border-radius: 2px;
  margin-left: 5px;
  background: rgb(55, 102, 233);
  color: white;
}
.input-holder input[type="number"] {
  position: relative;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 42px;
  padding: 4px 6px;
  margin: 0 5px;
  border: 0;
  outline: 0;
  border-radius: 3px;
  background-color: #e8f0fe;
  color: #1967d2;
  font-size: 14px;
  letter-spacing: 0.3px;
  font-weight: 500;
  font-family: "Google Sans", Helvetica, Arial, sans-serif;
}
input {
  padding: 4px;
}
input[type="number" i] {
  padding: 1px 2px;
}
.setting-box {
  font-size: 14px;
  border-top: 1px solid #eaeaea;
  padding: 18px;
}
ul {
  padding: 0;
}
.tag-list {
  display: inline;
  margin-right: 10px;
  /* border: 1px solid black; */
  background-color: rgba(243, 255, 131, 0.349);
  border-radius: 5px;
  padding: 4px;
}
.del-btn {
  background: none;
  padding: 0;
  border: none;
}
.tag-box {
  height: 20px;
}
.learning-button {
  margin: 0 auto;
  width: 200px;
  height: 70px;
  border-radius: 5px;
  border: none;
  background: none;
  color: rgb(76, 76, 211);
  font-size: 30px;
  font-weight: 700;
}
.Lbutton-box {
  text-align: center;
}
.learning-button:hover {
  cursor: pointer;
  /* transform: scale( 1.1 ); */
  background-color: #ffde4ae0;
}
.learning-button:focus {
  outline: none !important;
  border: 0;
  // border: 2px solid rgba(224, 153, 46, 0.616);
  // box-shadow: 0 0 20px rgba(219, 98, 17, 0.616);
}
.btn-box {
  position: absolute;
  bottom: 30px;
  left: 57%;
  transform: translate(-50%, -50%);
  display: flex;
  margin: 100px auto 0 auto;
  width: 50%;
  justify-content: space-evenly;
}
.btn-box button {
  background: violet;
  width: 200px;
  height: 50px;
  border: 0;
  border-radius: 30px;
  font-size: 20px;
  color: white;
}
.btn-box button:hover {
  cursor: pointer;
  /* transform: scale( 1.1 ); */
  background-color: #ffde4ae0;
}
.btn-box button:focus {
  outline: none !important;
  border: 0;
  border: 2px solid rgba(224, 153, 46, 0.616);
  box-shadow: 0 0 20px rgba(219, 98, 17, 0.616);
}
</style>
