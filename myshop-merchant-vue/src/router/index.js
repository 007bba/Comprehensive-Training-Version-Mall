import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Login.vue')
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
    redirect: '/dashboard',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/Dashboard.vue'),
        meta: { title: '数据概览' }
      },
      {
        path: 'goods',
        name: 'GoodsList',
        component: () => import('../views/goods/GoodsList.vue'),
        meta: { title: '商品管理' }
      },
      {
        path: 'goods/add',
        name: 'GoodsAdd',
        component: () => import('../views/goods/GoodsEdit.vue'),
        meta: { title: '新增商品' }
      },
      {
        path: 'goods/edit/:id',
        name: 'GoodsEdit',
        component: () => import('../views/goods/GoodsEdit.vue'),
        meta: { title: '编辑商品' }
      },
      {
        path: 'orders',
        name: 'OrderList',
        component: () => import('../views/order/OrderList.vue'),
        meta: { title: '订单管理' }
      },
      {
        path: 'orders/:id',
        name: 'OrderDetail',
        component: () => import('../views/order/OrderDetail.vue'),
        meta: { title: '订单详情' }
      },
      {
        path: 'shop',
        name: 'ShopInfo',
        component: () => import('../views/shop/ShopInfo.vue'),
        meta: { title: '店铺信息' }
      },
      {
        path: 'stats',
        name: 'Stats',
        component: () => import('../views/stats/Stats.vue'),
        meta: { title: '数据统计' }
      }
    ]
  }
]

const router = new VueRouter({
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isLoggedIn) {
      next({ path: '/login', query: { redirect: to.fullPath } })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
