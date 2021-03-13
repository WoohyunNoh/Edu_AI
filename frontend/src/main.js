import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueHighlightJS from 'vue-highlightjs'
import Toasted from 'vue-toasted';

Vue.config.productionTip = false
Vue.use(VueHighlightJS);
Vue.use(Toasted)

// import 'highlight.js/styles/srcery.css'

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

