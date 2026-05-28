
import request from '@/utils/request'
// 封装请求的方式
export function addCart(data) {
  return request({
    url: '/cart/',
    method: 'post',
    data
  })
}

export function getCart(data) {
  return request({
    url: '/cart/',
    method: 'get',
    data
  })
}

export function updateCart(id,data) {
  return request({
    url: '/cart/'+id+'/',
    method: 'patch',
    data
  })
}

export function deleteCart(id) {
  return request({
    url: '/cart/'+id+'/',
    method: 'delete'
  })
}

export function addOrder(data) {
  return request({
    url: '/order/',
    method: 'post',
    data
  })
}

export function getOrder(data) {
  return request({
    url: '/order/',
    method: 'get',
    data
  })
}

export function payOrder(id) {
  return request({
    url: '/order/' + id + '/mock-pay/',
    method: 'post'
  }).catch(error => {
    if (error && error.status === 404) {
      return request({
        url: '/order/' + id + '/pay/',
        method: 'post'
      })
    }
    return Promise.reject(error)
  })
}

