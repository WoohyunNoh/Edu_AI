import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";
import router from "../router";

Vue.use(Vuex);

const SERVER_URL = "http://localhost:8081/";
// const SERVER_URL = "https://k3d207.p.ssafy.io/";

export default new Vuex.Store({
  
  state: {
    //data
    imageFiles: [
      {className: "class1", files: [], filePreview: []},
      {className: "class2", files: [], filePreview: []},
    ],
    textFiles: [
      {className: "class1", files: null},
      {className: "class2", files: null},
    ],
    textInputData: [
      {className: 'class1', texts : []},
      {className: 'class2', texts : []}
    ],
    isLogin: false,
    isLoginError: false,
    userInfo: null,
    epoch: 50,
    batchSize: 16,
    learningRate: 0.001,
    config: {
      headers: {},
    },
    trainData: null,
    putText: {},
    tagger: "mecab",
    model: "",
    tepochs: 50,
    tbatch_size: 16,
    tlearning_rate: 0.001,
    userInputData: "",
    textresult: 0,
    posnavBoolean: false,
    possample: false,
    navsample: false,
    toastMessage: false,
  },
  getters: {
    //computed
    //어떤걸 쓸 지 function안에 정의해주기 (state,mutations, actions,...)
    sitepageCount(state) {
      return state.sitepageNum;
    },
    getImageFiles(state) {
      return state.imageFiles;
    },
    getLength(state) {
      return state.imageFiles.length;
    },
    getTextFiles(state) {
      return state.textFiles;
    },
    getTextLength(state) {
      return state.textFiles.length;
    },
    getTextInput(state) {
      return state.textInputData;
    },
    getEpoch(state) {
      return state.epoch
    },
    getBatchSize(state) {
      return state.batchSize
    },
    getLearningRate(state) {
      return state.learningRate
    },
    getBackText(state) {
      return state.putText
    }
  },
  mutations: {
    //state값 변화
    imageFilesClear: (state) => {
      state.imageFiles = [
        {className: "class1", files: [], filePreview: []},
        {className: "class2", files: [], filePreview: []},
      ]
    },
    deleteClass: (state, payload) => {
      state.imageFiles.splice(payload, 1);
      console.log(state.imageFiles);
    },
    addClass: (state, payload) => {
      state.imageFiles.push(payload);
    },
    deleteText: (state, payload) => {
      state.textInputData.splice(payload, 1)
    },
    //로그인 성공 했을때
    loginSuccess(state, payload) {
      state.isLogin = true;
      state.isLoginError = false;
      state.userInfo = payload;
      console.log(state.userInfo);
      localStorage.setItem("isLogin", state.isLogin)
      localStorage.setItem("isLoginError", state.isLoginError)
      localStorage.setItem("userInfo", JSON.stringify(state.userInfo))
      alert("로그인 되었습니다")
      router.push({name:"Main"});
    },
    //로그인이 실패했을 때,
    loginError(state) {
      state.isLogin = false;
      state.isLoginError = true;
    },
    //logout시 localstorage한번에 삭제
    logout(state) {
      state.isLogin = false;
      state.isLoginError = false;
      state.userInfo = null;
      localStorage.clear()
      // localStorage.removeItem("isLogin")
      // localStorage.removeItem("isLoginError")
      // localStorage.removeItem("userInfo")
      // localStorage.removeItem("access_token")
      // localStorage.removeItem("trainData")
      alert("로그아웃 되었습니다")
    },
    //토큰 header에 넣어 보내기
    setHeader(state, payload) {
      state.config.headers = {"access-token": payload};
      console.log(state.config);
    },
    addTextClass: (state, payload) => {
      // state.textFiles.push(payload);
      state.textInputData.push(payload);
    },
    deleteTextClass: (state, payload) => {
      state.textInputData.splice(payload, 1);
    },
    changeEpoch: (state, epoch) => {
      state.epoch = epoch;
    },
    changeBatchSize: (state, batchSize) => {
      state.batchSize = batchSize;
    },
    changeLearningRate: (state, learningRate) => {
      state.learningRate = learningRate;
    },
    chooseTagger: (state, token) => {
      state.tagger = token;
      console.log("tagger", state.tagger)
    },
    chooseModel: (state, model) => {
      state.model = model;
      console.log('Tmodel', state.model)
    },
    chooseParameter: (state, epoch, batchSize, learningRate) => {
      state.tepochs = epoch;
      state.tbatch_size = batchSize;
      state.tlearning_rate = learningRate;
      console.log('parameter', state.tepochs, state.tbatch_size, state.tlearning_rate)
    },

    saveUserKey: (state, key) => {
      state.userInfo.key = key;
      console.log(state.userInfo.key);
    },
    pushTextData(state, payload, index) {
      for (var i = 0; i < payload.length; i++) {
        state.textInputData[index].texts.push(payload[i]);
      }
    }
  },
  actions: {
    //이미지 업로드
    async imageUpload({state, getters}) {
      console.log("USER정보:")
      console.log(state.userInfo)
      let fd = new FormData();
      let name = [];
      console.log(state.imageFiles)
      for (var i = 0; i < getters.getLength; i++) {
        let files = state.imageFiles[i].files;
        let className = state.imageFiles[i].className;
          if(files.length === 0){
            alert(className + "에 이미지를 넣어 주세요")
            return
          }
        console.log(className)
        console.log(files)
        name.push(className)
        for (var j = 0; j < files.length; j++) {
          fd.append(className, files[j].file);
          console.log(files[j].file);
        }     
      }
      await fd.append("name", name);
      console.log(name)
      await fd.append("id",state.userInfo.id)
      axios
        .post(SERVER_URL + "api/imageengines/upload/", fd)
        .then((res) => {
          console.log(res.data);
          if(res.data.status === 'success'){
            this.state.userInfo.key = res.data.key;
            alert("데이터가 저장되었습니다.")
            router.push("/image/second")
          }
        }) //다른 곳으로 이동 필요
        .catch((err) => console.error(err));
    },

    async imageTrain() {
      let trainData = {
        pk : this.state.userInfo.id,
        key : this.state.userInfo.key,
        epoch : this.state.epoch,
        batch : this.state.batchSize,
        rate : this.state.learningRate,
      }
      this.trainData = trainData
      localStorage.setItem("trainData", JSON.stringify(this.trainData));

      axios
        .post(SERVER_URL + "api/imageengines/training/", this.trainData)
        .then((res) => {
          console.log(res.data);
          if(res.data == 'success'){
            alert("이미지 학습이 완료되었습니다.");
          }
        })
        .catch((err) => console.error(err));
    },
    
    textBack({state}) {
      axios
        .get(SERVER_URL + "api/textengines/movie_set/")
        .then((res) => {
          // console.log(`pos,nag: ${res.data}`)
          state.putText = res.data
          // console.log("textGroup", textGroup)
          // state.putText = textGroup
          state.putText.p = state.putText.p.slice(0,10)
          state.putText.n = state.putText.n.slice(0,10)
          console.log("putText", state.putText)
          
        })
        .catch((err) => {
          console.log("첫번째페이지 에러입니다")
          console.log(err)
        })
      state.posnavBoolean = true
      alert("샘플 csv를 사용합니다");
      router.push("/text/second");
    },
    TextPush({state}, arr, index) {
      console.log("index:", index)
      console.log("arr:", arr)
      console.log("textarr:", state.textInputData)
      console.log(state.textInputData)
      for (var i = 0; i < arr.length; i++) {
        state.textInputData[index].texts.push(arr[i]);
      }
    },
    putParameter({state}) {
      let fd = new FormData();
      var data = {}
      var tagger = null
      var model = null
      console.log("-------------")
      if (state.posnavBoolean) {
        data = state.putText
      }
      else {
        for(var i =0; i<state.textInputData.length;i++){
          var inputData =state.textInputData[i]; //      {className: 'class1', texts : [{text:"",number:0}]}, 
          console.log("inputData",inputData)
          var temp = []
          
          for(var j = 0; j<inputData.texts.length;j++){
            temp.push(inputData.texts[j].text)
          }
          data[i] = temp
        }
      }
      tagger = state.tagger
      model = state.model
      state.toastMessage = true
      console.log("tagger, model", tagger, model)
      console.log("18",JSON.stringify(data))
      fd.append("data",JSON.stringify(data))
      fd.append("model",state.model)
      fd.append("tagger",state.tagger)       
      console.log("text data: ",fd)
      axios
        .post(SERVER_URL + "api/textengines/sklearn_analyze/", fd)
        .then((res) => {
          console.log(res.data);
          if(res.data == 'success'){
            alert("파라미터가 저장되었습니다.");
          }
        })
        .catch((err) => {
          console.log("두번째페이지 에러입니다")
          console.error(err);
        })
    },
    posNav({state}) {
      let fd = new FormData();
      var tagger = null
      var model = null
      console.log("-------------")
      tagger = state.tagger
      model = state.model
      state.toastMessage = true
      console.log("tagger, model", tagger, model)
      // console.log("18",JSON.stringify(data))
      // fd.append("data",JSON.stringify(data))
      fd.append("model",state.model)
      fd.append("tagger",state.tagger)       
      console.log("text data: ",fd)
      axios
        .post(SERVER_URL + "api/textengines/base_analyze/", fd)
        .then((res) => {
          console.log(res.data);
          if(res.data == 'success'){
            alert("파라미터가 저장되었습니다.");
          }
        })
        .catch((err) => {
          console.log("두번째페이지 에러입니다")
          console.error(err);
        })
    },
    

    userInput({state}) {
      let fd = new FormData();
      var userData = state.userInputData
      console.log("-------------")
      console.log("userData", userData)
      fd.append("input_content", userData)       
      axios
        .post(SERVER_URL + "api/textengines/sklearn_result_analyze/", fd)
        .then((res) => {
          console.log("res.data", res.data.result)
          if(res.data == 'success') {
            alert("분석을 시작합니다")
            state.textresult = res.result
            console.log("result", state.textresult)
          } 
        })
        .catch((err) => {
          console.log("네번째페이지 에러입니다")
          console.error(err);
        })
    },
    

    //로그인 시도
    login({dispatch}, loginObj) {
      //로그인 -> 토큰 반환
      axios
        .post(SERVER_URL + "api/accounts/login/", loginObj)
        .then((res) => {
          //비밀번호나 이메일이 틀릴경우
          if (res.data.error) {
            alert("이메일과 비밀번호를 확인하세요.");
            return;
          }
          //성공시 token
          //토큰을 헤더에 포함시켜서 유저 정보를 요청
          let token = res.data.token;

          //토큰을 로컬 스토리지에 저장
          localStorage.setItem("access_token", token);

          dispatch("getMemberInfo");
        })
        .catch(() => {
          alert("서버에 문제가 생겼습니다. 관리자에게 문의하세요");
        });
    },
    logout({commit}) {
      commit("logout");
      console.log("router",router)
      location.href = '/';
    },
    //회원가입
    async signUp({dispatch},userInfo){
      console.log(userInfo)
      let result;
      await axios
      .post(SERVER_URL+"api/accounts/checkemail/",{'email':userInfo.email})
      .then((response)=>{
        result = response.data.result       
      })
      .catch(()=>{
        alert("서버에 문제가 생겼습니다.")
      })
      console.log(result)
      if(result){
        alert("이메일이 중복입니다.")
        return
      }
      axios
      .post(SERVER_URL + "api/accounts/signup/",userInfo
      ).then((response)=>{
        if(response.data.error){
          alert("회원가입에 실패했습니다.")
        }else if(response.data.result){
          let loginObj = {
            email: userInfo.email,
            password: userInfo.password1,
          };
          alert("회원가입을 축하합니다.")
          dispatch("login",loginObj)
        }
      }).catch(()=>{      
        alert("서버에 문제가 생겼습니다.")
      })
    },
  
    getMemberInfo({state, commit}) {
      //로컬 스토리지에 저자되어 있는 토큰을 불러온다.
      let token = localStorage.getItem("access_token");
    
      //토큰 -> 멤버 정보를 반환
      //새로고침 -> 토큰만 가지고 멤버정보를 요청
      // console.log(token)
      axios
        .post(SERVER_URL + "api/accounts/profile/",null,{ headers: {
          "access-token": token,
        }})
        .then((response) => {
          let data = response.data;
        
          // console.log("userInfo: ", data);
          let userInfo = {
            id: data.id,
            email: data.email,
            name: data.name,
            key: null,
          };
          commit("loginSuccess", userInfo);
          console.log(state.userInfo)
        })
        .catch(() => {
          console.log("getMemberInfo")
          alert("이메일과 비밀번호를 확인하세요.");
        });
    },
  },
  modules: {},
});
