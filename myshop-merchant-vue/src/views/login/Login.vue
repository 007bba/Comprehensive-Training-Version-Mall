<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2 style="text-align:center;margin-bottom:30px">商家登录</h2>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="登录" name="login">
          <el-form :model="loginForm" :rules="loginRules" ref="loginForm" @submit.native.prevent="handleLogin">
            <el-form-item prop="username">
              <el-input v-model="loginForm.username" prefix-icon="el-icon-user" placeholder="用户名/手机号" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="loginForm.password" prefix-icon="el-icon-lock" placeholder="密码" type="password" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" style="width:100%" :loading="loading" native-type="submit">登录</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="注册" name="register">
          <el-form :model="regForm" :rules="regRules" ref="regForm" @submit.native.prevent="handleRegister">
            <el-form-item prop="username">
              <el-input v-model="regForm.username" prefix-icon="el-icon-user" placeholder="用户名" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="regForm.password" prefix-icon="el-icon-lock" placeholder="密码" type="password" />
            </el-form-item>
            <el-form-item prop="mobile">
              <el-input v-model="regForm.mobile" prefix-icon="el-icon-mobile-phone" placeholder="手机号" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" style="width:100%" :loading="loading" native-type="submit">注册</el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { login, register } from '@/api/merchant'

export default {
  name: 'Login',
  data() {
    return {
      activeTab: 'login',
      loading: false,
      loginForm: { username: '', password: '' },
      regForm: { username: '', password: '', mobile: '' },
      loginRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      regRules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
        mobile: [{ required: true, message: '请输入手机号', trigger: 'blur' }]
      }
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(async valid => {
        if (!valid) return
        this.loading = true
        try {
          const res = await login(this.loginForm)
          const token = res.token
          this.$store.dispatch('login', { token, user: { username: this.loginForm.username } })
          this.$message.success('登录成功')
          this.$router.push(this.$route.query.redirect || '/dashboard')
        } catch (e) {
          // 错误已在拦截器中处理
        } finally {
          this.loading = false
        }
      })
    },
    handleRegister() {
      this.$refs.regForm.validate(async valid => {
        if (!valid) return
        this.loading = true
        try {
          await register(this.regForm)
          this.$message.success('注册成功，请登录')
          this.activeTab = 'login'
          this.loginForm.username = this.regForm.username
        } catch (e) {
          // 错误已在拦截器中处理
        } finally {
          this.loading = false
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.login-card {
  width: 420px;
  border-radius: 8px;
}
</style>
