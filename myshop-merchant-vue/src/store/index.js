import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: JSON.parse(localStorage.getItem('merchant_user') || 'null'),
    token: localStorage.getItem('merchant_token') || ''
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      localStorage.setItem('merchant_user', JSON.stringify(user))
    },
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('merchant_token', token)
    },
    LOGOUT(state) {
      state.user = null
      state.token = ''
      localStorage.removeItem('merchant_user')
      localStorage.removeItem('merchant_token')
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('SET_TOKEN', token)
      commit('SET_USER', user)
    },
    logout({ commit }) {
      commit('LOGOUT')
    }
  },
  getters: {
    isLoggedIn: state => !!state.token
  }
})
