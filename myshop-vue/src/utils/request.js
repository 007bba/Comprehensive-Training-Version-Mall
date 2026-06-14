import axios from 'axios'

//var URL = 'http://192.168.77.102:8002/'
var URL = process.env.API_BASE_URL || 'http://localhost:8000/'
// 创建 axios 实例
const service = axios.create({
  baseURL: URL,
  timeout: 20000 // Supabase 连接首次查询可能较慢，避免用户端误判超时
})

// 是否正在刷新 token
let isRefreshing = false
// 重试队列，每一项是一个待重试的函数
let refreshSubscribers = []

function onRefreshed(newToken) {
  refreshSubscribers.forEach(cb => cb(newToken))
  refreshSubscribers = []
}

function addRefreshSubscriber(cb) {
  refreshSubscribers.push(cb)
}

// request拦截器
service.interceptors.request.use(
  config => {
    const { url } = config
    // 除了登录和注册接口，其他所有请求都带上 JWT
    var jwt = localStorage.getItem('token');
    if (jwt && jwt !== 'null' && jwt !== 'undefined') {
      if (url !== '/login/' && url !== '/users/' || config.method === 'get') {
        config.headers.Authorization = 'JWT ' + jwt;
      }
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)
// response拦截器
service.interceptors.response.use(
  response => {
    return response
  },
  error => {
    const { response } = error
    const originalRequest = error.config

    // 401 且不是刷新请求本身，且没有重试过
    if (response && response.status === 401 && !originalRequest._retry) {
      // 如果正在刷新，把当前请求挂起排队
      if (isRefreshing) {
        return new Promise((resolve) => {
          addRefreshSubscriber((newToken) => {
            originalRequest.headers.Authorization = 'JWT ' + newToken
            originalRequest._retry = true
            resolve(service(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      const oldToken = localStorage.getItem('token')
      return service.post('/token-refresh/', { token: oldToken })
        .then((res) => {
          const newToken = res.data.token
          localStorage.setItem('token', newToken)
          isRefreshing = false
          onRefreshed(newToken)
          // 用新 token 重试原始请求
          originalRequest.headers.Authorization = 'JWT ' + newToken
          return service(originalRequest)
        })
        .catch((refreshError) => {
          // 刷新也失败了，说明 token 彻底过期，需要重新登录
          isRefreshing = false
          refreshSubscribers = []
          localStorage.removeItem('token')
          localStorage.removeItem('userinfo')
          alert('登录已过期，请重新登录！')
          return Promise.reject(refreshError)
        })
    }

    return Promise.reject(response ? response.data : error)
  }
)

export default service
