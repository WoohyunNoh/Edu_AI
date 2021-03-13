<template>
  <div id="image-first">
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
        <router-link to="/image/first" class="is-active">
          <li>데이터 넣기</li>
        </router-link>
        <a>
          <li>학습데이터 고르기</li>
        </a>
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
    <div id="imagefirst">
      <div class="file-boxs">
        <div
          class="fbox1 fbox"
          v-for="(item, index) in $store.state.imageFiles"
          :key="index"
        >
          <div class="input-boxs">
            <div v-if="editBooleans[index]" class="edit-mode">
              <input
                type="text"
                v-model="$store.state.imageFiles[index].className"
              />
              <button @click="confirmClass(index)">OK</button>
            </div>
            <div v-if="!editBooleans[index]" class="name-mode">
              <h3>{{ item.className }}</h3>
              <div class="edit-class" @click="editClass(index)">
                <i class="fas fa-edit fa-lg"></i>
              </div>
            </div>
            <div>
              <button class="times-btn" @click="remove(index)">
                <i class="fas fa-times fa-2x"></i>
              </button>
            </div>
          </div>
          <div class="mini-boxes">
            <div class="input-data mini-box" @click="popFileModal(index)">
              <i class="fas fa-pencil-alt fa-3x"></i>
              <p class="fmini-size">학습 DATA입력</p>
            </div>
            <div class="upload-data mini-box" @click="popCaptureModal(index)">
              <i class="fas fa-upload fa-3x"></i>
              <p class="fmini-size">학습 DATA(웹캠)</p>
            </div>
          </div>
        </div>
        <div class="append-box fbox" v-if="$store.state.imageFiles.length < 5">
          <div class="plus-fbox" @click="addInput()">
            <i class="fas fa-plus fa-3x"></i>
          </div>
        </div>
      </div>

      <!-- <div class="btn-box">
        <a href="/">
          <button>BACK</button>
        </a>
        <a href="/image/second">
          <button>NEXT</button>
        </a>
      </div> -->
    </div>
    <div class="card-modal" v-if="showFile">
      <ImageFile
        :showFile="showFile"
        :index="index"
        @modal-show="popFileModal"
      />
    </div>
    <div class="card-modal" v-if="showCapture">
      <ImageCapture
        :showCapture="showCapture"
        :index="index"
        @modal-show="popCaptureModal"
      />
    </div>
    <button class="confirm-btn second" @click="alertconfirm">
      <!-- <a href="/image/second"> -->
      <i class="fas fa-angle-right fa-4x second"></i>
      <!-- </a> -->
    </button>
  </div>
</template>

<script>
import ImageCapture from "@/components/imageform/ImageCapture.vue";
import ImageFile from "@/components/imageform/ImageFile.vue";
import {mapMutations, mapState, mapGetters} from "vuex";

export default {
  name: "ImageInput",
  components: {
    ImageCapture,
    ImageFile,
  },
  data() {
    return {
      editBooleans: [false, false],
      endIndex: "3",
      showCapture: false,
      showFile: false,
      index: "",
    };
  },
  mounted() {
    console.log("개새끼");
    console.log(this.$store.state.userInfo);
  },
  computed: {
    ...mapGetters(["getImageFiles", "getLength"]),
    ...mapState(["imageFiles"]),
  },
  methods: {
    ...mapMutations(["imageFilesClear", "deleteClass", "addClass"]),

    popFileModal(index) {
      this.showFile = !this.showFile;
      this.index = index;
    },
    popCaptureModal(index) {
      this.showCapture = !this.showCapture;
      this.index = index;
    },
    confirmClass(index) {
      let list = [...this.editBooleans];
      list.splice(index, 1, !this.editBooleans[index]);
      this.editBooleans = list;
    },
    editClass(index) {
      let list = [...this.editBooleans];

      list.splice(index, 1, !this.editBooleans[index]);
      this.editBooleans = list;
    },
    remove(index) {
      this.editBooleans.splice(index, 1);
      this.deleteClass(index);
    },
    addInput() {
      if (this.getLength == 5) {
        alert("클래스는 5개까지 추가 가능합니다.");
      } else {
        if (this.editBooleans.length <= 5) {
          this.editBooleans.push(false);
        }
        let obj = {
          className: "class" + this.endIndex++,
          files: [],
          filePreview: [],
        };
        this.addClass(obj);
        console.log(this.$store.state.imageFiles);
      }
    },
    alertconfirm() {
      this.$store.dispatch("imageUpload");

      // alert("Data가 저장되었습니다");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/progressbar.scss";

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

.times-btn {
  border: none;
  background: none;
  position: absolute;
  top: 0;
  left: 0;
  padding: 5px 8px;
}
.times-btn:hover {
  cursor: pointer;
}
.times-btn:focus {
  outline: none !important;
  border: 0;
}

#image-first {
  position: relative;
  width: 100vw;
  height: 100vh;
  /* background: rgba(105, 233, 133, 0.479); */
}
#imagefirst {
  margin: 0 auto;
  position: absolute;
  top: 54%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  height: 80%;
  // background: rgba(144, 218, 236, 0.671);
  padding: 20px;
}
.confirm-btn {
  position: absolute;
  right: 5%;
  top: 45%;
  border: 0;
  color: rgba(133, 164, 250, 0.411);
  // margin-left: 10px;
  background: none;
  font-size: 30px;
  font-weight: 900;
}
.file-boxs {
  position: relative;
  display: flex;
  justify-content: center;
  height: 100%;
  flex-wrap: wrap;
  align-content: center;
  padding-top: 20px;
}
.fbox {
  position: relative;
  margin: 20px;
  width: 300px;
  height: 200px;
  background: rgb(243, 243, 243);
  border-radius: 5px;
  margin-top: 20px;
  bottom: 20px;
  z-index: 10;
  opacity: 0.99;
}
.input-boxs {
  padding: 10px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.input-boxs input {
  padding: 5px;
  width: 130px;
}
.edit-mode button {
  margin-left: 10px;
  padding: 5px;
  border-radius: 5px;
  border: none;
  color: white;
  background: rgb(27, 18, 151);
}
.edit-mode button:hover {
  cursor: pointer;
  /* transform: scale( 1.1 ); */
  background-color: #ffde4ae0;
}
.edit-mode button:focus {
  outline: none !important;
  border: 0;
}
.name-mode {
  display: flex;
}
.name-mode h3 {
  width: 150px;
  text-align: center;
}
.edit-class {
  margin-left: 10px;
  display: flex;
  align-items: center;
}
.edit-class:hover {
  cursor: pointer;
  color: yellow;
}
.mini-boxes {
  margin-top: 15px;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}
.mini-box {
  padding-top: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 85px;
  height: 80px;
  background: rgb(53, 152, 233);
  border-radius: 3px;
  border: rgb(255, 255, 255) solid 10px;
}
.fas {
  color: white;
}
.fmini-size {
  font-size: 10px;
  font-weight: 700;
  color: white;
  text-align: center;
  margin-bottom: 0;
}
.append-box {
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgb(53, 152, 233);
}
.plus-fbox {
  width: 70px;
  height: 70px;
  background: rgb(53, 152, 233);
  border-radius: 50%;
  border: white 10px solid;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
