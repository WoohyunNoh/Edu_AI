<template>
  <div class="captureModal">
    <div class="form-box">
      <button @click="cancleWrite" class="cancle-btn">
        <i style="color: black" class="fas fa-times fa-3x"></i>
      </button>
      <div class="capture-video">
        <div class="left-box">
          <h2>WebCam</h2>
          <vue-web-cam
            ref="webcam"
            :device-id="deviceId"
            width="300px"
            height="200px"
            @started="onStarted"
            @stopped="onStopped"
            @error="onError"
            @cameras="onCameras"
            @camera-change="onCameraChange"
          />
          <div class="btn-box">
            <!-- <button type="button" class="btn btn-primary" @click="onCapture"> -->
            <button
              class="button"
              :class="{active: interval}"
              @mousedown="start"
              @mouseleave="stop"
              @mouseup="stop"
              @touchstart="start"
              @touchend="stop"
              @touchcancel="stop"
            >
              Capture Photo
            </button>
            <button class="button" style="margin-top:10px" @click="comfirm">
              저장
            </button>
          </div>
        </div>

        <!-- <div class="col-md-12">
            <select v-model="camera">
              <option>-- Select Device --</option>
              <option
                v-for="device in devices"
                :key="device.deviceId"
                :value="device.deviceId"
                >{{ device.label }}</option
              >
            </select>
          </div> -->
        <!-- <div class="col-md-12">
          <button type="button" class="btn btn-primary" @click="onCapture">
            Capture Photo
          </button>
          <button type="button" class="btn btn-danger" @click="onStop">
            Stop Camera
          </button>
          <button type="button" class="btn btn-success" @click="onStart">
            Start Camera
          </button>
        </div> -->
        <div class="right-box">
          <h2>Captured Image</h2>
          <figure class="figure">
            <div class="wrap" v-for="(file, index) in files" :key="index">
              <div
                class="file-close-button"
                @click="deleteButton"
                :name="file.number"
              >
                x
              </div>
              <img
                class="img-responsive"
                :key="index"
                :src="file.preview"
                width="100px"
                height="100px"
              />
            </div>
          </figure>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {WebCam} from "vue-web-cam";
import {mapState, mapGetters} from "vuex";

// import axios from "axios";

export default {
  name: "ImageCapture",
  components: {
    "vue-web-cam": WebCam,
  },
  props: {
    showCapture: Boolean,
    index: Number,
  },
  data() {
    return {
      stream: null,
      img: null,
      camera: null,
      deviceId: null,
      devices: [],
      SERVER_URL: "http://localhost:8081/",
      interval: false,
      files: [], //업로드용 파일
      filePreview: [],
      uploadImageIndex: 0, // 이미지 업로드를 위한 변수
    };
  },
  mounted() {
    this.files = this.getImageFiles[this.index].files;
    this.filePreview = this.getImageFiles[this.index].filePreview;
  },
  computed: {
    ...mapState(["imageFiles"]),
    ...mapGetters(["getImageFiles", "getLength"]),

    device: function() {
      return this.devices.find((n) => n.deviceId === this.deviceId);
    },
  },
  watch: {
    camera: function(id) {
      this.deviceId = id;
    },
    devices: function() {
      // Once we have a list select the first one
      const [first, ...tail] = this.devices;
      if (first) {
        this.camera = first.deviceId;
        this.deviceId = first.deviceId;
      }
      if (tail) {
        console.log("?");
      }
    },
  },
  methods: {
    comfirm() {
      this.getImageFiles[this.index].files = this.files;
      this.getImageFiles[this.index].filePreview = this.filePreview;
      console.log(this.getImageFiles[this.index].files);
      this.$emit("modal-show");
    },
    cancleWrite() {
      this.$emit("modal-show");
    },
    //hold button
    start() {
      if (this.stream == null) {
        alert("카메라가 준비중입니다.");
        return;
      }
      if (!this.interval) {
        this.interval = setInterval(() => this.onCapture(), 100);
      }
    },
    stop() {
      clearInterval(this.interval);
      this.interval = false;
    },

    //blob
    dataURItoBlob(dataURI) {
      var byteString = atob(dataURI.split(",")[1]);

      var mimeString = dataURI
        .split(",")[0]
        .split(":")[1]
        .split(";")[0];

      var ab = new ArrayBuffer(byteString.length);
      var ia = new Uint8Array(ab);
      for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
      }

      var bb = new Blob([ab], {type: mimeString});
      return bb;
    },
    onCapture() {
      this.img = this.$refs.webcam.capture();
      var blob = this.dataURItoBlob(this.img);
      // let fd = new FormData();

      // fd.append("name", "test");
      // fd.append("test", blob);
      // axios
      //   .post(this.SERVER_URL + "api/imageengines/", fd)
      //   .then((res) => {
      //     console.log(res.data);
      //   }) //다른 곳으로 이동 필요
      //   .catch((err) => console.error(err));
      this.files = [
        ...this.files,
        //이미지 업로드
        {
          //실제 파일
          file: blob,
          //이미지 프리뷰
          preview: this.img,
          //삭제및 관리를 위한 number
          number: this.uploadImageIndex++,
        },
      ];
      console.log("files");
      console.log(this.files);
    },
    onStarted(stream) {
      console.log("On Started Event", stream);
      this.stream = stream;
    },
    onStopped(stream) {
      console.log("On Stopped Event", stream);
    },
    onStop() {
      this.$refs.webcam.stop();
    },
    onStart() {
      this.$refs.webcam.start();
    },
    onError(error) {
      console.log("On Error Event", error);
    },
    onCameras(cameras) {
      this.devices = cameras;
      console.log("On Cameras Event", cameras);
    },
    onCameraChange(deviceId) {
      this.deviceId = deviceId;
      this.camera = deviceId;
      console.log("On Camera Change Event", deviceId);
    },
    deleteButton(e) {
      console.log(e.target);
      const name = e.target.getAttribute("name");
      console.log(name);
      this.files = this.files.filter((data) => data.number !== Number(name));
      // console.log(this.files);
    },
  },
};
</script>
<style scoped>
/* 전체화면영역 */

.captureModal {
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  position: fixed;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.5);
  transition: 0.5s;
  /* position: relative; */
}
.form-box {
  border-radius: 5px;
  position: absolute;
  /* 정가운데 정렬 */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

  width: 70%;
  height: 70%;
  background: white;
  margin: 0 auto;
}
.cancle-btn {
  background: none;
  border: none;
  padding: 15px;
  position: absolute;
  right: 0;
  margin-right: 5px;
}
.cancle-btn:hover {
  cursor: pointer;
}
.cancle-btn:focus {
  outline: none !important;
  border: 0;
}
.capture-video {
  /* background: blue; */
  margin-top: 50px;
  width: calc(100% - 60px);
  height: 80%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  padding: 30px;
  margin-left: 30px;
}
.button {
  background-color: rgb(53, 152, 233); /* màu của Quản trị mạng ^^ */
  border: none;
  color: white;
  padding: 10px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 15px;
  border-radius: 8px;
  width: 60%;
}
.left-box {
  padding-right: 15px;
  width: 30%;
  height: 100%;
  margin: 0 auto;
  /* background: blueviolet; */
  border-right: 2px solid rgba(161, 161, 161, 0.562);
}
.left-box h2 {
  margin-left: 15px;
}
.right-box {
  width: 70%;
  height: 100%;
  margin: 0 auto;
  /* background: rgb(63, 107, 202); */
}
.right-box h2 {
  margin-left: 40px;
}
.figure {
  height: 80%;
  width: 82%;
  overflow-x: hidden;
  overflow-y: scroll;
  -ms-overflow-style: none;

  display: flex;
  flex-direction: row;
  align-items: baseline;
  margin-top: 10px;
  flex-wrap: wrap;
  align-content: flex-start;
}

.figure::-webkit-scrollbar {
  width: 5px;
  background: rgb(171, 196, 241);
  border-radius: 5px;
}
.figure::-webkit-scrollbar-thumb {
  background-color: #6fb2e99c;
}
.figure::-webkit-scrollbar-track {
  background-color: rgb(236, 236, 236);
}
.figure img {
  margin: 5px;
}
.btn-box {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  /* justify-content: center; */
  margin-top: 20px;
  flex-wrap: wrap;
}
.btn-primary {
  text-align: center;
  padding: 10px;
  background: cornflowerblue;
  border-radius: 5px;
  border: none;
  color: white;
  font-weight: 700;
}
.figure img {
  object-fit: cover;
}
.wrap {
  position: relative;
}
.file-close-button {
  position: absolute;
  /* align-items: center; */
  line-height: 18px;
  z-index: 99;
  font-size: 18px;
  right: 5px;
  top: 5px;
  color: #fff;
  font-weight: bold;
  background-color: #666666;
  width: 20px;
  height: 20px;
  text-align: center;
  cursor: pointer;
}
</style>
