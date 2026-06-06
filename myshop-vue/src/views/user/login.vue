<template>
  <div>
    <myhead></myhead>
    <div class="login-page">
      <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />

      <div class="login-container">
        <!-- 顶部注册引导 -->
        <p class="login-hint">
          如未注册，点此
          <router-link to="/reg" class="login-hint__link">注册</router-link>
        </p>

        <!-- 登录主卡片 -->
        <div class="login-card">
          <h2 class="login-card__title">用户登录</h2>

          <form name="formLogin" class="login-form" action="" method="post">
            <!-- 用户名 -->
            <div class="form-group">
              <span class="form-group__icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </span>
              <input
                type="text"
                name="username"
                id="username"
                v-model="username"
                placeholder="用户名 / 手机号 / 邮箱"
                class="form-group__input"
              />
            </div>
            <div class="form-error" id="username_notice">
              <em>{{ err_username }}</em>
            </div>

            <!-- 密码 -->
            <div class="form-group">
              <span class="form-group__icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
              </span>
              <input
                type="password"
                name="password"
                id="password"
                v-model="password"
                placeholder="请输入你的密码"
                class="form-group__input"
              />
            </div>
            <div class="form-error" id="password_notice">
              <em>{{ err_password }}</em>
            </div>

            <!-- 隐藏字段 -->
            <input type="hidden" name="login_type" value="0" id="login_type" />
            <input type="hidden" name="act" value="act_login" />
            <input type="hidden" name="back_act" value="./index.php" />

            <!-- 登录按钮 -->
            <button
              type="button"
              name="submit"
              class="login-submit"
              @click="login"
            >
              登 录
            </button>
          </form>
        </div>
      </div>
    </div>
    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from "@/views/app/head";
import myfooter from "@/views/app/footer";
import { mapMutations, mapActions, mapGetters } from "vuex";
import { login } from "@/api/index";
export default {
  data() {
    return {
      username: "",
      password: "",
      message: "",
      err_username: "",
      err_password: "",
    };
  },
  components: {
    myhead,
    myfooter,
  },
  methods: {
    login() {
      var that = this;
      this.message = "";
      login({
        username: this.username,
        password: this.password,
      })
        .then((Response) => {
          console.log(Response);
          if (Response.status === 200) {
            //保存数据到本地存储
            console.log(Response.data.token);
            //同时保存到vuex
            //this.saveUser(Response.data);
            //localStorage.setItem('user',{'token':Response.data.token,'id':Response.data.id,'username':Response.data.username});
            localStorage.setItem("token", Response.data.token),
              this.$store.dispatch("saveUser", Response.data);
            //console.log(this.$store.user.id);
            this.username = "";
            this.password = "";
            this.$router.push("/index"); //跳转到首页
            //alert('登陆成功');
          }
        })
        .catch(function (error) {
          if (error && "username" in error) {
            that.err_username = error.username[0];
          } else if (error && "password" in error) {
            that.err_password = error.password[0];
          } else if (error && "non_field_errors" in error) {
            alert(error.non_field_errors[0]);
          } else if (error && error.detail) {
            alert(error.detail);
          } else {
            alert("登录失败");
          }
        });
    },
  },
};
</script>
<style scoped>
/* ===== 页面容器 ===== */
.login-page {
  --brand: #b23a2e;
  --brand-dark: #993023;
  --bg: #faf7f1;
  --surface: #ffffff;
  --line: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;

  min-height: 100vh;
  padding: 0 16px 60px;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;
  color: var(--ink);
  background: var(--bg);
}

.login-container {
  max-width: 420px;
  margin: 0 auto;
  padding-top: 32px;
}

/* ===== 顶部注册引导 ===== */
.login-hint {
  text-align: right;
  font-size: 13px;
  color: var(--ink-2);
  margin: 0 0 10px;
}

.login-hint__link {
  color: var(--brand);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 150ms ease-out;
}

.login-hint__link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

/* ===== 登录卡片 ===== */
.login-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 32px 28px 28px;
}

.login-card__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  text-align: center;
  margin: 0 0 24px;
  letter-spacing: 1px;
}

/* ===== 表单 ===== */
.login-form {
  display: flex;
  flex-direction: column;
}

/* ===== 输入框组 ===== */
.form-group {
  position: relative;
  margin-bottom: 4px;
}

.form-group__icon {
  position: absolute;
  left: 13px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ink-3);
  display: flex;
  align-items: center;
  pointer-events: none;
  transition: color 150ms ease-out;
  z-index: 1;
}

.form-group:focus-within .form-group__icon {
  color: var(--brand);
}

.form-group__input {
  width: 100%;
  height: 46px;
  padding: 0 14px 0 40px;
  border: 1px solid var(--line);
  border-radius: 8px;
  font-size: 14px;
  color: var(--ink);
  background: #fafaf8;
  box-sizing: border-box;
  transition: border-color 150ms ease-out, background 150ms ease-out, box-shadow 150ms ease-out;
}

.form-group__input:focus {
  border-color: var(--brand);
  background: #fff;
  outline: none;
  box-shadow: 0 0 0 3px rgba(178,58,46,0.08);
}

.form-group__input::placeholder {
  color: var(--ink-3);
}

.form-group__input:-webkit-autofill {
  -webkit-box-shadow: 0 0 0 100px #fafaf8 inset;
}

/* ===== 错误提示 ===== */
.form-error {
  min-height: 20px;
  margin-bottom: 8px;
  padding-left: 2px;
}

.form-error em {
  display: block;
  font-size: 12px;
  color: #c0392b;
  font-style: normal;
  line-height: 1.5;
}

/* ===== 登录按钮 ===== */
.login-submit {
  display: block;
  width: 100%;
  margin-top: 12px;
  padding: 13px 0;
  border: 0;
  border-radius: 8px;
  background: var(--brand);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 4px;
  cursor: pointer;
  transition: background 150ms ease-out, transform 150ms ease-out;
}

.login-submit:hover {
  background: var(--brand-dark);
}

.login-submit:active {
  background: var(--brand-dark);
  transform: scale(0.98);
}

.login-submit:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* ===== 响应式 ===== */
@media (max-width: 480px) {
  .login-card {
    padding: 24px 18px;
  }

  .login-card__title {
    font-size: 20px;
  }
}
</style>
