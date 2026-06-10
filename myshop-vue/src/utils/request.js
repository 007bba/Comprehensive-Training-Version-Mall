import axios from 'axios'

//var URL = 'http://192.168.77.102:8002/'
var URL = process.env.API_BASE_URL || 'http://localhost:8000/'
// 创建 axios 实例
const service = axios.create({
  baseURL: URL,
  timeout: 20000 // Supabase 连接首次查询可能较慢，避免用户端误判超时
})

// request拦截器
service.interceptors.request.use(
  config => {
    const { url } = config
    //指定页面访问需要JWT认证。
    if (url == '/cart/' || url == '/order/' || url.indexOf('/order/') == 0 || url == '/checkout/' || url == '/myorder/' || url.indexOf('address/') > 0 || url == '/profile/' || url.indexOf('/users/') == 0 ) {
      var jwt = localStorage.getItem('token');
      if (jwt && jwt !== 'null' && jwt !== 'undefined') {
        config.headers.Authorization = 'JWT ' + jwt;
      }
    }
    return config
  },
  error => {
    Promise.reject(error)
  }
)
// response拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    console.log(error.response || error)
    //授权验证失败
    if (error.response && error.response.status === 401) {
      alert('请先登录！');
    }
    return Promise.reject(error.response ? error.response.data : error)
  }
)

export default service
