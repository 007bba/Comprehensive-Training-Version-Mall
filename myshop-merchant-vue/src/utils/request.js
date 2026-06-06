import axios from 'axios'
import { Message } from 'element-ui'
import router from '../router'

const request = axios.create({
  baseURL: '',
  timeout: 10000
})

// 请求拦截器：自动携带 JWT token
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('merchant_token')
    if (token) {
      config.headers.Authorization = 'JWT ' + token
    }
    return config
  },
  error => Promise.reject(error)
)

// 响应拦截器：统一错误处理
request.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      const status = error.response.status
      if (status === 401) {
        Message.error('登录已过期，请重新登录')
        localStorage.removeItem('merchant_token')
        localStorage.removeItem('merchant_user')
        router.push('/login')
      } else if (status === 403) {
        Message.error('无权限访问')
      } else {
        Message.error(error.response.data.msg || '请求失败')
      }
    } else {
      Message.error('网络异常')
    }
    return Promise.reject(error)
  }
)

export default request
