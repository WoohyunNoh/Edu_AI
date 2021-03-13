<template>
  <div id="tutorial">
    <div id="text-tutorial" v-if="!isImage">
      <div class="container-fluid">
        <br />
        <ul class="list-unstyled multi-steps">
          <router-link :class="{'is-active': Tfirst}" @click="TfirstBtn">
            <li>데이터 넣기</li>
          </router-link>
          <router-link :class="{'is-active': Tsecond}" @click="TsecondBtn">
            <li>학습데이터 고르기</li>
          </router-link>
          <router-link :class="{'is-active': Tthird}" @click="TthirdBtn">
            <li>
              파이썬 코드확인<br />
              &학습시작
            </li>
          </router-link>
          <router-link :class="{'is-active': Tfourth}" @click="TfourthBtn">
            <li>학습 결과확인</li>
          </router-link>
        </ul>
      </div>
      <div class="tutorial-box">
        <div class="text-tutor tutorial" v-if="Tfirst">
          <Textone />
        </div>
        <div class="text-tutor tutorial" v-if="Tsecond">
          <Texttwo />
        </div>
        <div class="text-tutor tutorial" v-if="Tthird">
          <Textthree />
        </div>
        <div class="text-tutor tutorial" v-if="Tfourth">
          <Textfour />
        </div>
      </div>
    </div>
    <div id="image-tutorial" v-if="isImage">
      <div class="container-fluid">
        <br />
        <ul class="list-unstyled multi-steps">
          <router-link :class="{'is-active': Ifirst}" @click="IfirstBtn">
            <li>데이터 넣기</li>
          </router-link>
          <router-link :class="{'is-active': Isecond}" @click="IsecondBtn">
            <li>학습데이터 고르기</li>
          </router-link>
          <router-link :class="{'is-active': Ithird}" @click="IthirdBtn">
            <li>
              파이썬 코드확인<br />
              &학습시작
            </li>
          </router-link>
          <router-link :class="{'is-active': Ifourth}" @click="IfourthBtn">
            <li>학습 결과확인</li>
          </router-link>
        </ul>
      </div>
      <div class="tutorial-box">
        <div class="text-tutor tutorial" v-if="Ifirst">
          <Imageone />
        </div>
        <div class="text-tutor tutorial" v-if="Isecond">
          <Imagetwo />
        </div>
        <div class="text-tutor tutorial" v-if="Ithird">
          <Imagethree />
        </div>
        <div class="text-tutor tutorial" v-if="Ifourth">
          <Imagefour />
        </div>
      </div>
    </div>
    <div class="switch-box">
      <label>
        <input
          type="checkbox"
          name="checkboxName"
          class="checkbox"
          v-model="isImage"
        />
        {{ isImage }}
        <div class="switch" :class="{switchOn: isImage}"></div>
      </label>
    </div>
  </div>
</template>

<script>
import Textone from "@/components/tutorial/Textone.vue";
import Texttwo from "@/components/tutorial/Texttwo.vue";
import Textthree from "@/components/tutorial/Textthree.vue";
import Textfour from "@/components/tutorial/Textfour.vue";
import Imageone from "@/components/tutorial/Imageone.vue";
import Imagetwo from "@/components/tutorial/Imagetwo.vue";
import Imagethree from "@/components/tutorial/Imagethree.vue";
import Imagefour from "@/components/tutorial/Imagefour.vue";

export default {
  name: "Tutorial",
  components: {
    Textone,
    Texttwo,
    Textthree,
    Textfour,
    Imageone,
    Imagetwo,
    Imagethree,
    Imagefour,
  },
  data() {
    return {
      isImage: false,
      Tfirst: true,
      Ifirst: true,
      Tsecond: false,
      Isecond: false,
      Tthird: false,
      Ithird: false,
      Tfourth: false,
      Ifourth: false,
    };
  },
  mounted() {
    if (this.isImage == true) {
      this.isImage = true;
    } else {
      this.isImage = false;
    }
  },
  methods: {
    switchOn() {
      this.isImage != this.isImage;
      console.log(this.isImage);
      this.$router.push("/tutorial");
    },
    TfirstBtn() {
      (this.Tfirst = true),
        (this.Tsecond = false),
        (this.Tthird = false),
        (this.Tfourth = false);
    },
    TsecondBtn() {
      (this.Tfirst = false),
        (this.Tsecond = true),
        (this.Tthird = false),
        (this.Tfourth = false);
      console.log(this.$router);
    },
    TthirdBtn() {
      (this.Tfirst = false),
        (this.Tsecond = false),
        (this.Tthird = true),
        (this.Tfourth = false);
    },
    TfourthBtn() {
      (this.Tfirst = false),
        (this.Tsecond = false),
        (this.Tthird = false),
        (this.Tfourth = true);
    },
    IfirstBtn() {
      (this.Ifirst = true),
        (this.Isecond = false),
        (this.Ithird = false),
        (this.Ifourth = false);
    },
    IsecondBtn() {
      (this.Ifirst = false),
        (this.Isecond = true),
        (this.Ithird = false),
        (this.Ifourth = false);
      console.log(this.$router);
    },
    IthirdBtn() {
      (this.Ifirst = false),
        (this.Isecond = false),
        (this.Ithird = true),
        (this.Ifourth = false);
    },
    IfourthBtn() {
      (this.Ifirst = false),
        (this.Isecond = false),
        (this.Ithird = false),
        (this.Ifourth = true);
    },
  },
};
</script>

<style lang="scss" scoped>
@import "../../assets/scss/progressbar.scss";

#tutorial {
  width: 100vw;
  height: 100vh;
}
.tutorial {
  margin-top: 50px;
}

.switch-box {
  position: fixed;
  bottom: 20px;
  right: 20px;
}

.checkbox {
  display: none;
}
.switchOn,
.switchOn:before {
  background: #e5e5e5 !important;
}
.switchOn:after {
  content: "IMAGE" !important;
  left: 60px !important;
  border-bottom-right-radius: 10px !important;
  border-top-right-radius: 10px !important;
  border-top-left-radius: 0px !important;
  border-bottom-left-radius: 0px !important;
  background: #4abedb !important;
}
.switch {
  width: 120px;
  height: 40px;
  background: #e5e5e5;
  z-index: 0;
  margin: 0;
  padding: 0;
  appearance: none;
  border: none;
  cursor: pointer;
  position: relative;
  border-radius: 10px;
}
.switch:before {
  content: " ";
  position: absolute;
  left: 1px;
  top: 1px;
  width: 60px;
  height: 38px;
  z-index: 1;
  border-radius: 10px;
}
.switch:after {
  content: "TEXT";
  color: white;
  font-weight: 900;
  padding-top: 5px;
  text-align: center;
  height: 33px;
  width: 60px;
  background: #4abedb;
  border-top-left-radius: 10px;
  border-bottom-left-radius: 10px;
  position: absolute;
  z-index: 2;
  top: 1px;
  left: 1px;
  -webkit-transition-duration: 300ms;
  transition-duration: 300ms;
  // -webkit-box-shadow: 0 2px 5px #999999;
  // box-shadow: 0 2px 5px #999999;
}
</style>
