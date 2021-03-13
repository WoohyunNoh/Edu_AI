import Vue from 'vue'
import VueRouter from 'vue-router'
import Main from '../views/Main.vue'
import TextFirst from '@/views/text/TextFirst.vue'
import TextSecond from '@/views/text/TextSecond.vue'
import TextThird from '@/views/text/TextThird.vue'
import TextFourth from '@/views/text/TextFourth.vue'
import NotFound from '@/views/etc/NotFound.vue'
import ImageFourth from '@/views/image/ImageFourth.vue'
import ImageFirst from '@/views/image/ImageFirst.vue'
import ImageSecond from '@/views/image/ImageSecond.vue'
import ImageThird from '@/views/image/ImageThird.vue'
import Login from '@/views/account/Login.vue'
import Signup from '@/views/account/Signup.vue'

// education
import BaseEducation from '@/views/BaseEducation.vue'
import tokenization from '@/views/tokenization.vue'
import layerdue from '@/views/layerdue.vue'
import modeledu from '@/views/modeledu.vue'
import Tutorial from '@/views/tutorial/Tutorial.vue'
import store from '../store/index.js'


const rejectAuthUser = (to, from, next) => {
  if (store.state.isLogin|| localStorage.getItem('isLogin')) {
    alert('이미 로그인 되었습니다')
    next("/")
  }
  else {
    next()
  }
}

Vue.use(VueRouter);

const routes = [
  {
    path: "*",
    name: "NotFound",
    component: NotFound,
  },
  {
    path: "/",
    name: "Main",
    component: Main,
  },
  {
    path: "*",
    name: "NotFound",
    component: NotFound,
  },
  {
    path: "/text/first",
    name: "TextFirst",
    component: TextFirst,
  },
  {
    path: "/text/second",
    name: "TextSecond",
    component: TextSecond,
  },
  {
    path: "/text/third",
    name: "TextThird",
    component: TextThird,
  },
  {
    path: "/text/fourth",
    name: "TextFourth",
    component: TextFourth,
  },
  {
    path: "/image/fourth",
    name: "ImageFourth",
    component: ImageFourth,
  },
  {
    path: "/image/first",
    name: "ImageFirst",
    component: ImageFirst,
  },
  {
    path: "/image/second",
    name: "ImageSecond",
    component: ImageSecond,
  },
  {
    path: "/image/third",
    name: "ImageThird",
    component: ImageThird,
  },
  {
    path: "/account/login",
    name: "Login",
    beforeEnter: rejectAuthUser,
    component: Login,
  },
  {
    path: "/account/signup",
    name: "Signup",
    component: Signup,
  },
  {
    path: "/base/education",
    name: "BaseEducation",
    component: BaseEducation,
  },
  {
    path: '/base/tokenization',
    name: 'tokenization',
    component: tokenization
  },
  {
    path: '/base/layer',
    name: 'layerdue',
    component: layerdue
  },
  {
    path: '/base/model',
    name: 'modeledu',
    component: modeledu
  },
  {
    path: '/image/first',
    name: 'ImageFirst',
    component: ImageFirst
  },
  {
    path: '/tutorial',
    name: 'Tutorial',
    component: Tutorial

  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
