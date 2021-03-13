<template>
  <div>
    <div id="textforth">
      <!-- <div class="text-forth-box"> -->
      <div class="result-area">
        <!-- <div>웹캠입니당 ㅎㅎ</div> -->
        <button class="button" type="button" @click="init()">Start</button>
        <div>
          <div id="webcam-container" style="margin-top:20px"></div>
        </div>
      </div>
      <div class="gauge-area">
        <div class="gauge">
          <div
            id="label-container"
            style="margin-bottom:100px; margin-left:100px;"
          ></div>
        </div>
      </div>
      <!-- </div> -->
    </div>
  </div>
</template>

<script>
// import * as tf from '@tensorflow/tfjs';
import * as tmImage from "@teachablemachine/image";

export default {
  data() {
    return {
      // URL: "http://localhost:8081/static/model/",
      URL: "https://k3d207.p.ssafy.io/static/model/",
      model: "",
      webcam: "",
      labelContainer: "",
      maxPredictions: "",
    };
  },
  methods: {
    async init() {
      const modelURL =
        this.URL +
        this.$store.state.userInfo.id +
        "/" +
        this.$store.state.userInfo.key +
        "/model.json";
      const metadataURL =
        this.URL +
        this.$store.state.userInfo.id +
        "/" +
        this.$store.state.userInfo.key +
        "/metadata.json";

      this.model = await tmImage.load(modelURL, metadataURL);
      this.maxPredictions = this.model.getTotalClasses();

      // Convenience function to setup a webcam
      const flip = true; // whether to flip the webcam
      this.webcam = new tmImage.Webcam(300, 300, flip); // width, height, flip
      await this.webcam.setup(); // request access to the webcam
      await this.webcam.play();
      window.requestAnimationFrame(this.loop);

      // append elements to the DOM
      document
        .getElementById("webcam-container")
        .appendChild(this.webcam.canvas);
      this.labelContainer = document.getElementById("label-container");
      for (let i = 0; i < this.maxPredictions; i++) {
        // and class labels
        this.labelContainer.appendChild(document.createElement("div"));
      }
    },
    async loop() {
      this.webcam.update(); // update the webcam frame
      await this.predict();
      window.requestAnimationFrame(this.loop);
    },
    async predict() {
      // predict can take in an image, video or canvas html element
      const prediction = await this.model.predict(this.webcam.canvas);
      for (let i = 0; i < this.maxPredictions; i++) {
        const classPrediction =
          prediction[i].className +
          ": " +
          prediction[i].probability.toFixed(2) +
          "<br>" +
          '<progress style="width:200px; height:40px" value="' +
          prediction[i].probability.toFixed(2) +
          '" max="1">';
        +"</progress>";
        this.labelContainer.childNodes[i].innerHTML = classPrediction;
      }
    },
  },
  destroyed() {
    this.webcam.stop();
  },
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

.button {
  background-color: white; /* màu của Quản trị mạng ^^ */
  border: 1px solid black;
  color: black;
  padding: 10px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 15px;
  border-radius: 8px;
  height: 37px;
  position: absolute;
  top: -17px;
  left: 110px;
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
  display: block;
  justify-content: center;
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
.label-container progress {
  padding: 500px;
}
</style>
