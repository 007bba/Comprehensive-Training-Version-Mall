<template>
  <div>
    <myhead></myhead>
    <div class="reg-page">
      <link
        href="../../static/css/style.css"
        rel="stylesheet"
        type="text/css"
      />

      <div class="reg-container">
        <!-- 顶部登录引导 -->
        <p class="reg-login-hint">
          如已注册，点此
          <router-link to="/login" class="reg-login-hint__link">登录</router-link>
        </p>

        <!-- 注册主卡片 -->
        <div class="reg-card">
          <h2 class="reg-card__title">新用户注册</h2>

          <form name="formUser" class="reg-form">
            <!-- 用户名 -->
            <div class="form-group">
              <span class="form-group__icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
              </span>
              <input
                type="text"
                name="username"
                v-model="username"
                id="username"
                placeholder="用户名"
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
                v-model="password"
                id="password1"
                placeholder="密码"
                class="form-group__input"
              />
            </div>
            <div class="form-error" id="password_notice">
              <em>{{ err_password }}</em>
            </div>

            <!-- 手机 -->
            <div class="form-group">
              <span class="form-group__icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><path d="M12 18h.01"/></svg>
              </span>
              <input
                id="mobile"
                name="mobile"
                v-model="mobile"
                type="text"
                placeholder="手机号"
                class="form-group__input"
              />
            </div>
            <div class="form-error">
              <em>{{ err_mobile }}</em>
            </div>

            <!-- 用户协议 -->
            <div class="form-agreement">
              <label class="agreement-label">
                <input
                  name="agreement"
                  type="checkbox"
                  value="1"
                  checked="checked"
                  tabindex="5"
                  class="agreement-label__check"
                />
                <span class="agreement-label__text">
                  我已看过并接受《<a
                    href="#"
                    target="_blank"
                    class="agreement-label__link"
                  >用户协议</a>》
                </span>
              </label>
            </div>

            <div class="form-error"><em></em></div>

            <!-- 注册按钮 -->
            <button
              name="Submit"
              @click="register"
              type="button"
              class="reg-submit"
            >
              同意协议并注册登录
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
import { reg } from "@/api/users";
export default {
  data() {
    return {
      username: "",
      password: "",
      mobile: "",
      err_username: "",
      err_password: "",
      err_mobile: "",
    };
  },
  components: {
    myhead,
    myfooter,
  },
  methods: {
    register() {
      var that = this;
      that.err_username = "";
      that.err_password = "";
      that.err_mobile = "";
      reg({
        username: this.username,
        password: this.password,
        mobile: this.mobile,
      })
        .then((response) => {
          console.log(response.data);
          if (response.data.code === 201) {
            //跳转到登陆页面进行登陆
            this.$router.push({ name: "login" });
          }
        })
        .catch(function (error) {
          console.log("reg" + error);
          if ("non_field_errors" in error) {
            that.error = error.non_field_errors[0];
          }
          if ("username" in error) {
            that.err_username = error.username[0];
          }
          if ("password" in error) {
            that.err_password = error.password[0];
          }
          if ("mobile" in error) {
            that.err_mobile = error.mobile[0];
          }
        });
    },
  },
};
</script>

<style scoped>
/* ===== 页面容器 ===== */
.reg-page {
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

.reg-container {
  max-width: 420px;
  margin: 0 auto;
  padding-top: 32px;
}

/* ===== 顶部登录引导 ===== */
.reg-login-hint {
  text-align: right;
  font-size: 13px;
  color: var(--ink-2);
  margin: 0 0 10px;
}

.reg-login-hint__link {
  color: var(--brand);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 150ms ease-out;
}

.reg-login-hint__link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

/* ===== 注册卡片 ===== */
.reg-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 32px 28px 28px;
}

.reg-card__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  text-align: center;
  margin: 0 0 24px;
  letter-spacing: 1px;
}

/* ===== 表单 ===== */
.reg-form {
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

/* ===== 用户协议 ===== */
.form-agreement {
  margin-top: 8px;
}

.agreement-label {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
}

.agreement-label__check {
  width: 16px;
  height: 16px;
  accent-color: var(--brand);
  cursor: pointer;
  flex-shrink: 0;
}

.agreement-label__text {
  font-size: 13px;
  color: var(--ink-2);
  line-height: 1.5;
}

.agreement-label__link {
  color: var(--brand);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 150ms ease-out;
}

.agreement-label__link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

/* ===== 注册按钮 ===== */
.reg-submit {
  display: block;
  width: 100%;
  margin-top: 16px;
  padding: 13px 0;
  border: 0;
  border-radius: 8px;
  background: var(--brand);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background 150ms ease-out, transform 150ms ease-out;
}

.reg-submit:hover {
  background: var(--brand-dark);
}

.reg-submit:active {
  background: var(--brand-dark);
  transform: scale(0.98);
}

.reg-submit:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* ===== 响应式 ===== */
@media (max-width: 480px) {
  .reg-card {
    padding: 24px 18px;
  }

  .reg-card__title {
    font-size: 20px;
  }
}
</style>
