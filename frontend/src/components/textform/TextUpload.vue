<template>
  <div class="text-upload">
    <div class="form-box">
      <button
        class="cancle-btn e-cancle-button no-css-btn"
        style="float: right"
        @click="cancleWrite"
      >
        <i style="color: black" class="fas fa-times fa-2x"></i>
      </button>
      <div class="room-deal-information-container">
        <div class="room-deal-information-title"><h2>Text파일 업로드</h2></div>
        <div class="room-file-upload-wrapper">
          <div v-if="!files" class="room-file-upload-example-container">
            <div class="room-file-upload-example">
              <div class="room-file-image-example-wrapper">
                파일을 업로드 해주세요
              </div>
              <div class="room-file-notice-item room-file-notice-item-red">
                UTF-8로 인코딩한 txt파일만 업로드 하실 수 있습니다
              </div>
              <div class="room-file-notice-item room-file-upload-button">
                <div class="image-box">
                  <label for="file">Text파일 등록</label>
                  <input
                    type="file"
                    id="file"
                    ref="files"
                    accept=".txt"
                    @change="textUpload(evnet)"
                  />
                </div>
              </div>
            </div>
          </div>
          <div v-else class="file-preview-content-container">
            <div class="file-preview-container">
              <div class="file-preview-wrapper">
                <div class="file-close-button" @click="fileDeleteButton">
                  x
                </div>
                <img src="@/assets/textimage/textfile.png" />
                <p class="textname">{{ files[0].name }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="btn-ok">
          <button @click="comfirm">저장</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {mapState, mapGetters, mapActions} from "vuex";
export default {
  name: "TextUpload",
  props: {
    showUpload: Boolean,
    index: Number,
  },
  data() {
    return {
      files: null,
      filePreview: null,
      textList: null,
      textInput: [],
    };
  },
  computed: {
    ...mapGetters(["getTextFiles", "getTextLength", "getTextInput"]),
    ...mapState(["textFiles", "textInputData"]),
  },
  mounted() {
    this.files = this.getTextFiles[this.index].files;
    this.filePreview = this.getTextFiles[this.index].filePreview;
  },

  methods: {
    ...mapActions(["TextPush"]),
    comfirm() {
      this.getTextFiles[this.index].files = this.files;
      console.log("textList", this.textList);
      // this.getTextInput[this.index].texts.push(...this.textList);
      console.log(this.getTextFiles[this.index].files);
      this.$emit("modal-show");
    },
    cancleWrite() {
      this.$emit("modal-show");
    },
    textUpload(event) {
      console.log("filename", this.$refs.files.files[0].name);
      //하나의 배열로 넣기
      this.files = this.$refs.files.files;

      const selectedFiles = this.$refs.files.files;
      console.log("file: ", this.$refs.files.files);

      console.log("1111111111111111111111");
      let store = this.$store;
      let temp = this.index;
      console.log("확인", temp);
      for (const file of selectedFiles) {
        let reader = new FileReader();
        // function a(param , callback){
        //   console.log(param);
        //   callback();
        // }
        // function b (){

        // }
        // a(0,b()dfdf)
        reader.onload = function(window) {
          console.log(event.target);
          // textContents.innerText = reader.result;
          // console.log("text", reader.result);
          const sentences = reader.result;
          // console.log(sentences);
          const texts = sentences.split("\n");
          // console.log("text", texts);
          console.log("this", this.result);
          this.textList = [...texts];
          // console.log("gg", this.textList);
          console.log("44444444444444444");
          store.dispatch("TextPush", this.textList, window.idnex);
          // for (var i = 0; i < this.textList.length; i++) {
          //   console.log("textList있니", this.textList);
          // }
          this.textInput = this.textList;
          console.log(this.textInput);
        };
        reader.readAsText(file, "UTF-8");
        console.log("222222222222222", this.textList);
      }

      console.log("3333333333333333");
      console.log("들어감?", this.textList);

      // const fileTypes = ["text/plain"];

      // function validFileType(file) {
      //   return fileTypes.includes(file.type);
      // }
    },
    // textUpload() {
    //   console.log("filename", this.$refs.files.files[0].name);
    //   //하나의 배열로 넣기
    //   this.files = this.$refs.files.files;

    //   let reader = new FileReader();
    //   console.log(reader.readAsText(this.files, "UTF-8"));

    // reader.onload = function() {
    //   // textContents.innerText = reader.result;
    //   // console.log("text", reader.result);
    //   const sentences = reader.result;
    //   const texts = sentences.split("\n");
    //   // console.log("text", texts);
    //   this.textList = [...texts];
    //   // console.log("gg", this.textList);
    //   console.log("44444444444444444");
    //   store.dispatch("TextPush", this.textList, temp);

    //   // console.log("reader", reader.result);
    //   reader.readAsText(file, "UTF-8");
    //   console.log("222222222222222", this.textList);
    // };

    // console.log("3333333333333333");
    // console.log("들어감?", this.textList);

    // const fileTypes = ["text/plain"];

    // function validFileType(file) {
    //   return fileTypes.includes(file.type);
    // }
    // },

    fileDeleteButton() {
      this.files = null;
      this.textList = null;
      // console.log(this.files);
    },
  },
};
</script>

<style scoped>
/* 전체화면영역 */
.text-upload {
  /* display: flex; */
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

  width: 40%;
  height: 70%;
  background: white;
  margin: 0 auto;
}
.room-deal-information-container {
  /* display: flex; */
  margin-top: 50px;
  color: #222222;
}

.room-deal-information-title {
  text-align: center;
  font-size: 18px;
  line-height: 60px;
}

.room-deal-information-content-wrapper {
  min-height: 50px;
  display: flex;
}

.room-deal-informtaion-content-title {
  font-size: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 150px;
  background-color: #f9f9f9;
}

.room-deal-information-content {
  width: 100%;
  font-size: 14px;
}

.room-deal-option-selector {
  display: flex;
  align-items: center;
  padding: 15px;
}

.room-deal-option-item {
  width: 100px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #cccccc;
  border-radius: 5px;
  cursor: pointer;
}

.room-deal-option-item:last-child {
  margin-left: 10px;
}

.room-deal-option-notice {
  margin-left: auto;
  font-size: 14px;
  color: #888888;
}

.room-deal-option-item-deposit {
  margin-left: 10px;
}

.room-deal-information-wrapper {
  display: flex;
  flex-direction: column;
}

.room-deal-information-option {
  padding: 10px;
  display: flex;
  align-items: center;
}

.room-deal-information-option:last-child {
  border-bottom: 1px solid #dddddd;
}

.room-deal-information-item-type {
  font-size: 13px;
  color: #fff;
  background-color: #61b6e5;
  min-width: 50px;
  height: 26px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 3px;
}

.room-deal-information-item-wrapper {
  display: flex;
  align-items: center;
  margin-left: 10px;
  height: 46px;
  width: 100%;
}

.room-deal-information-item-wrapper > input {
  border: 1px solid #dddddd;
  width: 140px;
  height: 100%;
  padding: 0 15px;
  font-size: 15px;
}

.room-deal-inforamtion-won {
  margin: 0 10px;
}

.room-deal-information-example {
  color: #888888;
}

.room-deal-information-option:not(:first-child) {
  margin-top: 10px;
}

.room-deal-inforamtion-divide {
  font-size: 22px;
  margin: 0 8px;
  color: #222222;
  font-weight: 100;
}

.room-deal-close-button-wrapper {
  margin-left: auto;
  cursor: pointer;
}

.room-deal-close-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  background-color: #666666;
  color: rgb(220, 220, 220);
}

.room-deal-cliked {
  background-color: rgb(235, 235, 235);
  color: rgb(170, 170, 170);
}

.room-file-upload-example {
  height: 100%;
}

.room-write-content-container {
  border-top: 1px solid #dddddd;
  min-height: 260px;
}

.room-picture-notice {
  margin: 20px;
  padding: 20px 40px;
  border: 1px solid #dddddd;
}

.file-preview-content-container {
  height: 100%;
}

.room-file-upload-wrapper {
  overflow-y: auto;
  margin: 20px;
  border: 1px solid #dddddd;
  background-color: #f4f4f4;
  min-height: 300px;
  font-size: 15px;
  color: #888888;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 283px;
}

.room-file-upload-example-container {
  display: flex;
  align-items: center;
  justify-content: center;
  /* height: 100%;
width: 100%; */
}

.room-file-image-example-wrapper {
  text-align: center;
}

.room-file-notice-item {
  margin-top: 5px;
  text-align: center;
}

.room-file-notice-item-red {
  color: #ef4351;
}

.image-box {
  margin-top: 30px;
  padding-bottom: 20px;
  text-align: center;
}

.image-box input[type="file"] {
  position: absolute;
  width: 0;
  height: 0;
  padding: 0;
  overflow: hidden;
  border: 0;
}

.image-box label {
  display: inline-block;
  padding: 10px 20px;
  background-color: #232d4a;
  color: #fff;
  vertical-align: middle;
  font-size: 15px;
  cursor: pointer;
  border-radius: 5px;
}

.file-preview-wrapper {
  padding: 10px;
  position: relative;
}

.file-preview-wrapper > img {
  position: relative;
  width: 100px;
  height: 100px;
  z-index: 10;
}
.file-close-button {
  position: absolute;
  /* align-items: center; */
  line-height: 18px;
  z-index: 99;
  font-size: 18px;
  right: 5px;
  top: 10px;
  color: #fff;
  font-weight: bold;
  background-color: #666666;
  width: 20px;
  height: 20px;
  text-align: center;
  cursor: pointer;
}

.file-preview-container {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
}

.file-preview-wrapper-upload {
  margin: 10px;
  padding-bottom: 20px;
  /* background-color: #888888; */
  width: 120px;
  height: 100px;
}

.room-write-button-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #222222;
}

.room-write-button-wrapper > div {
  width: 160px;
  height: 50px;
  border: 1px solid #dddddd;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 15px;
  cursor: pointer;
}

.room-write-button {
  margin-left: 15px;
  color: #fff;
  background-color: #1564f9;
}

.room-write-button:hover {
  opacity: 0.8;
}
.cancle-btn {
  background: none;
  border: none;
  padding: 15px;
  position: absolute;
  right: 0;
  margin-right: 5px;
}
.btn-ok {
  text-align: center;
  margin: 10px;
}
.btn-ok > button {
  padding: 10px;
  width: 80px;
  border-radius: 5px;
  background-color: #232d4a;
  color: white;
}
.textname {
  text-align: center;
}
</style>
