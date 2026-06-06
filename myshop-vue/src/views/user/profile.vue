<template>
  <div>
    <myhead></myhead>

    <div class="profile-page">
      <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
      <!-- 面包屑 -->
      <nav class="breadcrumb">
        <a href="#">首页</a>
        <span class="breadcrumb__sep">/</span>
        <span>用户中心</span>
        <span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">个人资料</span>
      </nav>

      <div class="profile-layout">
        <!-- 左侧菜单 -->
        <aside class="profile-sidebar">
          <left></left>
        </aside>

        <!-- 右侧表单 -->
        <div class="profile-main">
          <div class="profile-card">
            <div class="profile-card__header">
              <h3 class="profile-card__title">个人资料</h3>
            </div>

            <div class="profile-card__body">
              <!-- 姓名 -->
              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label">姓名</label>
                  <input
                    name="truename"
                    type="text"
                    class="form-group__input"
                    size="25"
                    v-model="userinfo.truename"
                  />
                </div>
              </div>

              <!-- 性别 -->
              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label">性别</label>
                  <div class="radio-group">
                    <label
                      class="radio-pill"
                      :class="{ 'radio-pill--active': userinfo.sex == '1' }"
                    >
                      <input
                        type="radio"
                        name="sex"
                        value="1"
                        v-model="userinfo.sex"
                      />
                      <span class="radio-pill__text">男</span>
                    </label>
                    <label
                      class="radio-pill"
                      :class="{ 'radio-pill--active': userinfo.sex == '0' }"
                    >
                      <input
                        type="radio"
                        name="sex"
                        value="0"
                        v-model="userinfo.sex"
                      />
                      <span class="radio-pill__text">女</span>
                    </label>
                  </div>
                </div>
              </div>

              <!-- 邮箱 -->
              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label">
                    电子邮件地址 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="email"
                    type="text"
                    class="form-group__input"
                    size="25"
                    v-model="userinfo.email"
                  />
                </div>
              </div>

              <!-- 手机 -->
              <div class="form-row">
                <div class="form-group" id="extend_field5i">
                  <label class="form-group__label">
                    手机 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="extend_field5"
                    type="text"
                    class="form-group__input"
                    v-model="userinfo.mobile"
                  />
                </div>
              </div>
            </div>

            <div class="profile-card__actions">
              <input
                name="submit"
                type="button"
                class="btn btn--primary btn--block"
                value="确认修改"
                @click="updateUserinfo"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from '@/views/app/head';
import myfooter from '@/views/app/footer';
import left from '@/views/user/left';
import { getUsersByID, updateUsers } from '@/api/users'
export default {
  data() {
    return {
      userinfo:{
        birthday:'',
        sex:'0',
        email:'',
        mobile:''
      }
    };
  },
      components: {
      myhead,
      myfooter,
      left,
    },
  methods:{
      getData(){
        getUsersByID().then((response)=>{
          this.userinfo=response.data.data;
        }).catch(function(error){
          console.log(error);
        })
      },
      updateUserinfo(){
        updateUsers(this.userinfo).then((response)=>{
          alert('修改成功')
        }).catch(function(error){
          console.log(error);
          alert(JSON.stringify(error));
        })
      },
  },
  created(){
    this.getData();
  }
};
</script>
<style scoped>
/* ===== 页面容器 ===== */
.profile-page {
  --brand: #b23a2e;
  --brand-dark: #993023;
  --bg: #faf7f1;
  --surface: #ffffff;
  --line: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;

  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px 60px;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;
  color: var(--ink);
  background: var(--bg);
}

/* ===== 面包屑 ===== */
.breadcrumb {
  padding: 16px 0;
  font-size: 13px;
  color: var(--ink-3);
}
.breadcrumb a {
  color: var(--ink-2);
  text-decoration: none;
}
.breadcrumb a:hover {
  color: var(--brand);
}
.breadcrumb__sep {
  margin: 0 8px;
  color: var(--line);
}
.breadcrumb__current {
  color: var(--ink);
}

/* ===== 左右布局 ===== */
.profile-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* ====== 左侧菜单（穿透子组件 left.vue，与 address 页一致） ====== */
.profile-sidebar {
  flex: 0 0 220px;
  width: 220px;
}

.profile-sidebar :deep(.slidebar) {
  float: none;
  width: 100%;
}

.profile-sidebar :deep(.slide_item) {
  background: var(--surface);
  border: 0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
  margin-bottom: 0;
}

.profile-sidebar :deep(.root_node) {
  padding: 14px 16px;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  border-bottom: 1px solid var(--line);
  letter-spacing: 0.5px;
}

.profile-sidebar :deep(.item ul) {
  border-bottom: 0;
  padding: 4px 0;
}

.profile-sidebar :deep(.item li) {
  margin-bottom: 0;
}

.profile-sidebar :deep(.item li a) {
  display: block;
  height: auto;
  line-height: 1.4;
  padding: 10px 16px 10px 40px;
  font-size: 13px;
  color: var(--ink-2);
  text-decoration: none;
  transition: color 150ms ease-out, background 150ms ease-out;
  position: relative;
}

.profile-sidebar :deep(.item li a:hover) {
  background: #fef9f8;
  color: var(--brand);
}

.profile-sidebar :deep(.item li a.router-link-exact-active) {
  background: #fef9f8;
  color: var(--brand);
  font-weight: 600;
}

.profile-sidebar :deep(.item li a.router-link-exact-active::before) {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  background: var(--brand);
  border-radius: 0 3px 3px 0;
}

/* ===== 右侧主内容 ===== */
.profile-main {
  flex: 1;
  min-width: 0;
}

/* ====== 表单卡片 ====== */
.profile-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
}

.profile-card__header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--line);
}

.profile-card__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--ink);
  margin: 0;
  letter-spacing: 0.5px;
}

.profile-card__body {
  padding: 20px;
}

.profile-card__actions {
  padding: 0 20px 20px;
}

/* ====== 表单行 ====== */
.form-row {
  margin-bottom: 18px;
}

.form-row:last-child {
  margin-bottom: 0;
}

.form-group__label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--ink);
  margin-bottom: 6px;
}

.form-group__star {
  color: var(--brand);
  font-weight: 700;
}

.form-group__input {
  width: 100%;
  max-width: 400px;
  height: 40px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  font-size: 14px;
  color: var(--ink);
  background: #fff;
  box-sizing: border-box;
  transition: border-color 150ms ease-out;
}

.form-group__input:focus {
  border-color: var(--brand);
  outline: none;
}

.form-group__input::placeholder {
  color: var(--ink-3);
}

/* ====== 性别单选（胶囊按钮） ====== */
.radio-group {
  display: flex;
  gap: 10px;
}

.radio-pill {
  display: flex;
  align-items: center;
  padding: 8px 28px;
  border: 1px solid var(--line);
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 150ms ease-out, background 150ms ease-out;
  user-select: none;
}

.radio-pill:hover {
  border-color: #d8cdb9;
}

.radio-pill--active {
  border-color: var(--brand);
  background: #fef9f8;
}

.radio-pill input[type="radio"] {
  display: none;
}

.radio-pill__text {
  font-size: 14px;
  color: var(--ink-2);
  transition: color 150ms ease-out;
}

.radio-pill--active .radio-pill__text {
  color: var(--brand);
  font-weight: 600;
}

/* ====== 按钮 ====== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease-out, transform 150ms ease-out;
}

.btn:active {
  transform: scale(0.97);
}

.btn--primary {
  background: var(--brand);
  color: #fff;
}

.btn--primary:hover {
  background: var(--brand-dark);
}

.btn--block {
  width: 100%;
  max-width: 400px;
  padding: 13px 0;
  font-size: 15px;
  letter-spacing: 1px;
}

/* ====== 响应式 ====== */
@media (max-width: 768px) {
  .profile-layout {
    flex-direction: column;
  }

  .profile-sidebar {
    flex: none;
    width: 100%;
  }

  .form-group__input,
  .btn--block {
    max-width: 100%;
  }
}
</style>
