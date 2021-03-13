<template>
  <div id="text-first">
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
    <div></div>
    <div class="container-fluid">
      <br />
      <ul class="list-unstyled multi-steps">
        <router-link to="/text/first" class="is-active">
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
    <div class="sample-csv">
      <button @click="alertBox">긍/부정 샘플 csv 사용</button>
    </div>
    <div id="textfirst">
      <div class="file-boxs">
        <div
          class="fbox1 fbox"
          v-for="(item, index) in $store.state.textInputData"
          :key="index"
        >
          <div class="input-boxs">
            <div v-if="editBooleans[index]" class="edit-mode">
              <input
                type="text"
                v-model="$store.state.textInputData[index].className"
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
            <div class="input-data mini-box" @click="popInputModal(index)">
              <i class="fas fa-pencil-alt fa-3x pencil"></i>
              <p class="fmini-size">학습 DATA입력</p>
            </div>
            <div class="upload-data mini-box" @click="popUploadModal(index)">
              <i class="fas fa-upload fa-3x"></i>
              <p class="fmini-size">UPLOAD</p>
            </div>
          </div>
        </div>
        <div
          class="append-box fbox"
          v-if="$store.state.textInputData.length < 5"
        >
          <div class="plus-fbox" @click="addInput()">
            <i class="fas fa-plus fa-3x"></i>
          </div>
        </div>
      </div>
    </div>
    <button class="confirm-btn second" @click="alertconfirm">
      <router-link to="/text/second">
        <i class="fas fa-angle-right fa-4x second"></i>
      </router-link>
    </button>
    <div class="card-modal" v-if="showInput">
      <TextInput
        :showInput="showInput"
        :index="index"
        @modal-show="popInputModal"
      />
    </div>
    <div class="card-modal" v-if="showUpload">
      <TextUpload
        :showUpload="showUpload"
        :index="index"
        @modal-show="popUploadModal"
      />
    </div>
  </div>
</template>

<script>
import TextUpload from "@/components/textform/TextUpload.vue";
import TextInput from "@/components/textform/TextInput.vue";

import {mapMutations, mapActions} from "vuex";

export default {
  name: "TextFirst",
  components: {
    TextUpload,
    TextInput,
  },
  data() {
    return {
      editBooleans: [false, false],
      endIndex: "2",
      showUpload: false,
      showInput: false,
    };
  },
  methods: {
    ...mapMutations(["deleteTextClass", "addTextClass"]),
    ...mapActions(["textBack"]),
    alertBox() {
      // alert("샘플 csv를 사용합니다");
      this.$store.dispatch("textBack");
      this.$store.state.posnavBoolean = true;
      this.$store.getters.getTextInput[0].className = "긍정";
      this.$store.getters.getTextInput[1].className = "부정";
      // this.$router.push("/text/second");
    },
    popUploadModal(index) {
      this.showUpload = !this.showUpload;
      this.index = index;
    },
    popInputModal(index) {
      this.showInput = !this.showInput;
      this.index = index;
    },
    confirmClass(index) {
      let list = [...this.editBooleans];
      if (
        this.validateClassName(
          index,
          this.$store.state.textInputData[index].className
        )
      ) {
        list.splice(index, 1, !this.editBooleans[index]);
        console.log("editboolians", list);
        this.editBooleans = list;
      }
    },
    editClass(index) {
      let list = [...this.editBooleans];
      list.splice(index, 1, !this.editBooleans[index]);
      this.editBooleans = list;
    },
    validateClassName(index, newClassName) {
      if (newClassName === "") {
        alert("클래스 이름은 빈값일 수 없습니다.");
        return false;
      }

      let list = [...this.$store.state.textInputData];
      list.splice(index, 1);
      let isExist = list.some((className) => className === newClassName);

      if (isExist) {
        alert("동일한 클래스가 존재합니다.");
        return false;
      }
      return true;
    },
    remove(index) {
      this.editBooleans.splice(index, 1);
      this.deleteTextClass(index);
    },
    addInput() {
      if (this.$store.state.textInputData.length == 5) {
        alert("클래스는 5개까지 추가 가능합니다.");
      } else {
        if (this.editBooleans.length <= 5) {
          this.editBooleans.push(false);
        }
        // this.items.push("class" + ++this.endIndex);
      }
      let obj = {
        className: "class" + ++this.endIndex,
        texts: [],
      };
      this.addTextClass(obj);
      console.log();
    },
    alertconfirm() {
      alert("텍스트 학습이 완료되었습니다.");
    },
  },
};
</script>

<style lang="scss" scoped>
@import "@/assets/scss/progressbar.scss";

.sample-csv button {
  padding: 10px;
  border: 0;
  background: rgb(53, 152, 233);
  color: white;
  font-weight: 700;
}
.sample-csv button:hover {
  cursor: pointer;
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

#text-first {
  position: relative;
  width: 100vw;
  height: 100vh;
  /* background: rgba(105, 233, 133, 0.479); */
}
#textfirst {
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
</style>
