import request from '@/utils/request'

// 商家登录
export function login(data) {
  return request.post('/login/', data)
}

// 商家注册
export function register(data) {
  return request.post('/merchant/register/', data)
}

// ==================== 店铺 ====================
export function getShop() {
  return request.get('/merchant/shop/')
}
export function createShop(data) {
  return request.post('/merchant/shop/', data)
}
export function updateShop(id, data) {
  return request.put('/merchant/shop/' + id + '/', data)
}

// ==================== 商品 ====================
export function getGoods(params) {
  return request.get('/merchant/goods/', { params })
}
export function getGoodsDetail(id) {
  return request.get('/merchant/goods/' + id + '/')
}
export function createGoods(data) {
  return request.post('/merchant/goods/', data)
}
export function updateGoods(id, data) {
  return request.put('/merchant/goods/' + id + '/', data)
}
export function deleteGoods(id) {
  return request.delete('/merchant/goods/' + id + '/')
}
export function toggleGoodsStatus(id) {
  return request.post('/merchant/goods/' + id + '/toggle_status/')
}

// ==================== 分类 ====================
export function getCategories() {
  return request.get('/merchant/categories/')
}

// ==================== 订单 ====================
export function getOrders(params) {
  return request.get('/merchant/orders/', { params })
}
export function getOrderDetail(id) {
  return request.get('/merchant/orders/' + id + '/')
}
export function shipOrder(id) {
  return request.post('/merchant/orders/' + id + '/ship/')
}
export function completeOrder(id) {
  return request.post('/merchant/orders/' + id + '/complete/')
}

// ==================== 统计 ====================
export function getStats() {
  return request.get('/merchant/stats/')
}
