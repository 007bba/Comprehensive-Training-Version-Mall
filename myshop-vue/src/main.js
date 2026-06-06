// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'      //引入路由，会去寻找index.js配置文件
import axios from './axios'
//全局状态控制引入
import store from './vuex/store';
Vue.config.productionTip = false        //关闭生产模式下的提示
//axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed'
//axios.defaults.headers.post["Content-Type"]="application/json"
/* eslint-disable no-new */
router.beforeEach((to, from, next) => {
  /* 路由发生变化修改页面title */
  if (to.meta.title) {
    document.title = to.meta.title
  }
  next()
})

new Vue({
  el: '#app',
  router,          //在框架中使用路由功能
  store,
  components: { App },
  template: '<App/>'
})


