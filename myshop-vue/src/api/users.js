import request from '@/utils/request'
// 封装请求的方式
export function login(data) {
  return request({
    url: '/login/',
    method: 'post',
    data
  })
}

export function reg(data) {
  return request({
    url: '/users/',
    method: 'post',
    data
  })
}

export function getUsersByID(userId) {
  return request({
    url: '/users/' + userId + '/',
    method: 'get',
  })
}

export function updateUsers(userId, data) {
  return request({
    url: '/users/' + userId + '/',
    method: 'patch',
    data
  })
}

export function updatePwd(userId, data) {
  return request({
    url: '/users/' + userId + '/',
    method: 'patch',
    data
  })
}
