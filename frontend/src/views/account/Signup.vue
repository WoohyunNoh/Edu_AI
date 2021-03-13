<template>
  <div class="form-structor">
    <div class="signup">
      <h1 class="form-title" id="signup">Edu_AI</h1>
      <div class="form-holder">
        <input
          class="input"
          type="text"
          v-model="signupData.email"
          id="email"
          placeholder="email@gmail.com"
        />
      </div>
      <div class="form-holder">
        <input
          class="input"
          type="text"
          v-model="signupData.name"
          id="username"
          placeholder="USERNAME"
        />
      </div>
      <div class="form-holder">
        <input
          class="input"
          id="password1"
          v-model="signupData.password1"
          type="password"
          placeholder="PASSWORD"
        />
      </div>
      <div class="form-holder">
        <input
          class="input"
          id="password2"
          v-model="signupData.password2"
          type="password"
          placeholder="Confirm Password"
        />
      </div>
      <button class="submit-btn" @click="checkHandler">Sign up</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "Signup",
  title: "Signup",
  data() {
    return {
      signupData: {
        email: null,
        name: null,
        password1: null,
        password2: null,
      },
      errorMessage: null,
    };
  },
  methods: {
    signup() {
      console.log(this.signupData);
      this.$store.dispatch("signUp", this.signupData);
    },
    // checkEmail(){
    //   this.$store.dispatch("checkEmail",this.signupData.email)
    // },
    checkHandler() {
      let err = true;
      let msg = "";

      err &&
        !this.signupData.email &&
        ((msg = "이메일을 확인해주세요."), (err = false));
      err &&
        !this.signupData.name &&
        ((msg = "닉네임을 입력해주세요."), (err = false));
      err &&
        !this.signupData.password1 &&
        ((msg = "비밀번호를 입력해주세요."), (err = false));
      err &&
        !this.signupData.password2 &&
        ((msg = "비밀번호확인을 입력해주세요."), (err = false));
      err &&
        this.signupData.password1 != this.signupData.password2 &&
        ((msg = "비밀번호가 다릅니다."), (err = false));

      if (!err) alert(msg);
      else this.signup();
    },
  },
};
</script>

<style scoped lang="scss">
@import url("https://fonts.googleapis.com/css?family=Fira+Sans");

// html,
// body {
//   position: relative;
//   min-height: 100vh;
//   min-width: 100vw;
//   background-color: #e1e8ee;
//   display: flex;
//   align-items: center;
//   justify-content: center;
//   font-family: "Fira Sans", Helvetica, Arial, sans-serif;
//   -webkit-font-smoothing: antialiased;
//   -moz-osx-font-smoothing: grayscale;
// }

.form-structor {
  height: 100%;
  width: 100%;
  position: relative;
  z-index: 2;
  overflow: none;
  background-image: url("../../assets/images/2.png");
  background-size: 100vw 100vh;
  background-repeat: no-repeat;
  padding-top: 66.64%;

  .signup {
    position: absolute;
    top: 30%;
    left: 50%;
    -webkit-transform: translate(-50%, -50%);
    width: 500px;
    z-index: 5;
    -webkit-transition: all 0.3s ease;

    &.slide-up {
      top: 5%;
      -webkit-transform: translate(-50%, 0%);
      -webkit-transition: all 0.3s ease;
    }

    &.slide-up .form-holder,
    &.slide-up .submit-btn {
      opacity: 0;
      visibility: hidden;
    }

    &.slide-up .form-title {
      font-size: 1em;
      cursor: pointer;
    }

    &.slide-up .form-title span {
      margin-right: 5px;
      opacity: 1;
      visibility: visible;
      -webkit-transition: all 0.3s ease;
    }

    .form-title {
      color: black;
      font-size: 1.7em;
      text-align: center;

      span {
        color: rgba(0, 0, 0, 0.4);
        opacity: 0;
        visibility: hidden;
        -webkit-transition: all 0.3s ease;
      }
    }

    .form-holder {
      border-radius: 15px;
      background-color: #fff;
      overflow: hidden;
      height: 50px;
      margin-top: 20px;
      opacity: 1;
      visibility: visible;
      -webkit-transition: all 0.3s ease;

      .input {
        text-align: center;
        border: 0;
        outline: none;
        box-shadow: none;
        display: block;
        height: 30px;
        line-height: 30px;
        padding: 8px 15px;
        // border-bottom: 1px solid #eee;
        width: 100%;
        font-size: 12px;

        &:last-child {
          border-bottom: 0;
        }
        &::-webkit-input-placeholder {
          color: rgba(0, 0, 0, 0.685);
        }
      }
    }

    .submit-btn {
      background-color: rgba(0, 0, 0, 0.664);
      color: rgba(256, 256, 256, 0.7);
      border: 0;
      border-radius: 15px;
      display: block;
      margin: 15px auto;
      padding: 15px 45px;
      width: 100%;
      font-size: 13px;
      font-weight: bold;
      cursor: pointer;
      opacity: 1;
      visibility: visible;
      -webkit-transition: all 0.3s ease;

      &:hover {
        transition: all 0.3s ease;
        background-color: rgba(0, 0, 0, 0.8);
      }
    }
  }

  .login {
    position: absolute;
    top: 20%;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #fff;
    z-index: 5;
    -webkit-transition: all 0.3s ease;

    &::before {
      content: "";
      position: absolute;
      left: 50%;
      top: -20px;
      -webkit-transform: translate(-50%, 0);
      background-color: #fff;
      width: 200%;
      height: 250px;
      border-radius: 50%;
      z-index: 4;
      -webkit-transition: all 0.3s ease;
    }

    .center {
      position: absolute;
      top: calc(50% - 10%);
      left: 50%;
      -webkit-transform: translate(-50%, -50%);
      width: 65%;
      z-index: 5;
      -webkit-transition: all 0.3s ease;

      .form-title {
        color: #000;
        font-size: 1.7em;
        text-align: center;

        span {
          color: rgba(0, 0, 0, 0.4);
          opacity: 0;
          visibility: hidden;
          -webkit-transition: all 0.3s ease;
        }
      }

      .form-holder {
        border-radius: 15px;
        background-color: #fff;
        border: 1px solid #eee;
        overflow: hidden;
        margin-top: 30px;
        opacity: 1;
        visibility: visible;
        -webkit-transition: all 0.3s ease;

        .input {
          border: 0;
          outline: none;
          box-shadow: none;
          display: block;
          height: 30px;
          line-height: 30px;
          padding: 8px 15px;
          border-bottom: 1px solid #eee;
          width: 100%;
          font-size: 12px;

          &:last-child {
            border-bottom: 0;
          }
          &::-webkit-input-placeholder {
            color: rgba(0, 0, 0, 0.4);
          }
        }
      }

      .submit-btn {
        background-color: #6b92a4;
        color: rgba(256, 256, 256, 0.7);
        border: 0;
        border-radius: 15px;
        display: block;
        margin: 15px auto;
        padding: 15px 45px;
        width: 100%;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        opacity: 1;
        visibility: visible;
        -webkit-transition: all 0.3s ease;

        &:hover {
          transition: all 0.3s ease;
          background-color: rgba(0, 0, 0, 0.8);
        }
      }
    }

    &.slide-up {
      top: 90%;
      -webkit-transition: all 0.3s ease;
    }

    &.slide-up .center {
      top: 10%;
      -webkit-transform: translate(-50%, 0%);
      -webkit-transition: all 0.3s ease;
    }

    &.slide-up .form-holder,
    &.slide-up .submit-btn {
      opacity: 0;
      visibility: hidden;
      -webkit-transition: all 0.3s ease;
    }

    &.slide-up .form-title {
      font-size: 1em;
      margin: 0;
      padding: 0;
      cursor: pointer;
      -webkit-transition: all 0.3s ease;
    }

    &.slide-up .form-title span {
      margin-right: 5px;
      opacity: 1;
      visibility: visible;
      -webkit-transition: all 0.3s ease;
    }
  }
}
</style>
