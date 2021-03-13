<template>
  <div id="text-four">
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
        <router-link to="/image/third">
          <li>학습데이터 고르기</li>
        </router-link>
        <router-link to="/image/third">
          <li>
            파이썬 코드확인<br />
            &학습시작
          </li>
        </router-link>
        <a class="is-active">
          <li>학습 결과확인</li>
        </a>
      </ul>
    </div>
    <div>
      <div id="textforth">
        <div class="text-forth-box">
          <div class="result-area">
            <select class="sbox" v-model="selected" style="margin-left:30px;">
              <option value="webcam">webcam</option>
              <option value="file">file</option>
            </select>
            <div>
              <Webcam v-if="selected == 'webcam'" id="Webcam" ref="Webcam" />
              <File v-else id="File" ref="File" />
            </div>
          </div>
          <div class="gauge-area">
            <div class="download-btn" style="margin-top:400px;">
              <button>Download</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Webcam from "@/components/imageform/Webcam.vue";
import File from "@/components/imageform/File.vue";

export default {
  name: "Image",
  title: "마인드컨트롤 | 분석결과",
  components: {
    Webcam,
    File,
  },
  data() {
    return {
      selected: "webcam",
    };
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/progressbar.scss";
#text-four {
  position: relative;
  width: 100vw;
  height: 100vh;
  // background: rgba(71, 71, 71, 0.479);
}
#textforth {
  margin: 0 auto;
  position: absolute;
  top: 54%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 80%;
  // background: rgba(144, 218, 236, 0.671);
  /* padding: 50px; */
  display: flex;
  align-items: center;
  justify-content: center;
}
.styled-select {
  border: 1px solid #ccc;
  box-sizing: border-box;
  border-radius: 3px;

  overflow: hidden;
  position: relative;
}
.result-area,
.styled-select select {
  width: 240px;
}
select:focus {
  outline: none;
}
.styled-select select {
  height: 34px;
  padding: 5px 0 5px 5px;
  background: transparent;
  border: none;

  /*hide default down arrow in webkit */
  -webkit-appearance: none;
}

@-moz-document url-prefix() {
  .styled-select select {
    width: 110%;
  }
}

.fa-sort-desc {
  position: absolute;
  top: 0;
  right: 12px;
  font-size: 24px;
}

select::-ms-expand {
  display: none;
} /* hide default down arrow in IE10*/

/* hack to fall back in opera */
_:-o-prefocus,
.selector {
  .styled-select {
    background: none;
  }
}
.forth-title {
  margin: 0;
  padding: 20px;
}
.analysis-box {
  display: flex;
  flex-direction: column;
}
.analysis-box input {
  // background: rgb(227, 240, 248);
  width: 460px;
  height: 10px;
  border-radius: 10px;
  border: 1px solid rgba(135, 207, 235, 0.685);
  padding: 20px;
  font-size: 15px;
  color: rgb(128, 182, 252);
}
.analysis-box input:focus {
  outline: none !important;
  border: 0;
  border: 2px solid rgba(135, 207, 235, 0.685);
  // box-shadow: 0 0 20px rgba(162, 250, 246, 0.253);
}
.analysis-box .anal-btn {
  width: 200px;
  height: 70px;
  margin: 50px auto 0 auto;
  border-radius: 8px;
  border: none;
  background: rgb(123, 164, 211);
  color: white;
  font-size: 20px;
}
.analysis-box .anal-btn:hover {
  cursor: pointer;
  /* transform: scale( 1.1 ); */
  background-color: #ffde4ae0;
}
.analysis-box .anal-btn:focus {
  outline: none !important;
  border: 0;
  border: 2px solid rgba(176, 224, 46, 0.616);
  box-shadow: 0 0 20px rgba(252, 204, 47, 0.616);
}
.text-forth-box {
  position: relative;
  background: rgba(192, 192, 192, 0.185);
  width: 90%;
  height: 90%;
  border-radius: 10px;
  display: flex;
  flex-direction: row;
}
.result-area {
  width: 50%;
  padding: 10px;
  height: 96%;
  display: flex;
  // justify-content: center;
  align-items: center;
  border-right: 2px solid rgba(110, 110, 110, 0.349);
}
.result-area div {
  margin: 0 auto;
  // margin-bottom: 100px;
}
.result-area textarea {
  width: 80%;
  height: 80%;
}
.sbox {
  padding: 5px;
  position: absolute;
  left: 105px;
  top: 60px;
}
.gauge-area {
  width: 50%;
  padding: 10px;
  height: 100%;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  flex-direction: column;
}
.gauge div {
  padding: 20px;
}
.download-btn button {
  width: 200px;
  height: 50px;
  border-radius: 5px;
  border: none;
  background: rgb(87, 136, 241);
  color: white;
  font-size: 20px;
}
.btn-box {
  position: absolute;
  bottom: 30px;
  left: 50%;
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
input[type="radio"]:checked + .labels {
  background: #0d358d62;
  color: white;
}
.confirm-before-btn {
  position: absolute;
  left: -3%;
  top: 38%;
  border: 0;
  color: rgba(133, 164, 250, 0.411);
  // margin-left: 10px;
  background: none;
  font-size: 30px;
  font-weight: 900;
}
.confirm-btn {
  position: absolute;
  left: -10%;
  top: 38%;
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
</style>
