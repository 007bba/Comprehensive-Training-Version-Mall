<template>
  <div>
    <myhead></myhead>
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />

    <div class="address-page">
      <!-- 面包屑 -->
      <nav class="breadcrumb">
        <a href="#">首页</a>
        <span class="breadcrumb__sep">/</span>
        <span>用户中心</span>
        <span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">收货地址</span>
      </nav>

      <div class="address-layout">
        <!-- 左侧菜单 -->
        <aside class="address-sidebar">
          <left></left>
        </aside>

        <!-- 右侧主内容 -->
        <div class="address-main">
          <!-- ====== 已有地址列表 ====== -->
          <div
            class="addr-card"
            v-for="(item,index) in address_lists"
            :key="index"
          >
            <div class="addr-card__header">
              <h3 class="addr-card__title">收货地址 {{ index + 1 }}</h3>
              <span class="addr-card__badge" v-if="item.is_default">默认</span>
            </div>

            <div class="addr-card__body">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label">
                    省份 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="province"
                    type="text"
                    class="form-group__input"
                    v-model="item.province"
                  />
                </div>
                <div class="form-group">
                  <label class="form-group__label">
                    城市 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="city"
                    type="text"
                    class="form-group__input"
                    v-model="item.city"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label">
                    区域 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="district"
                    type="text"
                    class="form-group__input"
                    v-model="item.district"
                  />
                </div>
                <div class="form-group form-group--wide">
                  <label class="form-group__label">
                    详细地址 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="address"
                    type="text"
                    class="form-group__input"
                    v-model="item.address"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label">
                    联系人 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="contact_name"
                    type="text"
                    class="form-group__input"
                    v-model="item.contact_name"
                  />
                </div>
                <div class="form-group">
                  <label class="form-group__label">
                    联系电话 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="contact_mobile"
                    type="text"
                    class="form-group__input"
                    v-model="item.contact_mobile"
                  />
                </div>
              </div>

              <div class="form-row">
                <label class="checkbox-label">
                  <input
                    name="is_default"
                    type="checkbox"
                    v-model="item.is_default"
                  />
                  <span>设为默认地址</span>
                </label>
              </div>
            </div>

            <div class="addr-card__actions">
              <button
                type="button"
                class="btn btn--primary"
                @click="update(item.id,index)"
              >确认修改</button>
              <button
                type="button"
                class="btn btn--outline"
                @click="del(item.id,index)"
              >删除</button>
            </div>
          </div>

          <!-- 无地址提示 -->
          <div class="addr-empty" v-if="!address_lists.length">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a89f94" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <p>暂无收货地址，请在下方添加</p>
          </div>

          <!-- ====== 新增地址表单 ====== -->
          <div class="addr-card addr-card--new">
            <div class="addr-card__header">
              <h3 class="addr-card__title">新增收货地址</h3>
            </div>

            <div class="addr-card__body">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label" for="province">
                    省份 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="province"
                    type="text"
                    class="form-group__input"
                    id="province"
                    v-model="addinfo.province"
                  />
                </div>
                <div class="form-group">
                  <label class="form-group__label" for="city">
                    城市 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="city"
                    type="text"
                    class="form-group__input"
                    id="city"
                    v-model="addinfo.city"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label" for="district">
                    区域 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="district"
                    type="text"
                    class="form-group__input"
                    id="district"
                    v-model="addinfo.district"
                  />
                </div>
                <div class="form-group form-group--wide">
                  <label class="form-group__label" for="address">
                    详细地址 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="address"
                    type="text"
                    class="form-group__input"
                    id="address"
                    v-model="addinfo.address"
                  />
                </div>
              </div>

              <div class="form-row">
                <div class="form-group">
                  <label class="form-group__label" for="contact_name">
                    联系人 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="contact_name"
                    type="text"
                    class="form-group__input"
                    id="contact_name"
                    v-model="addinfo.contact_name"
                  />
                </div>
                <div class="form-group">
                  <label class="form-group__label" for="contact_phone">
                    联系电话 <span class="form-group__star">*</span>
                  </label>
                  <input
                    name="contact_phone"
                    type="text"
                    class="form-group__input"
                    id="contact_phone"
                    v-model="addinfo.contact_mobile"
                  />
                </div>
              </div>

              <div class="form-row">
                <label class="checkbox-label">
                  <input
                    name="is_default"
                    type="checkbox"
                    v-model="addinfo.is_default"
                  />
                  <span>设为默认地址</span>
                </label>
              </div>
            </div>

            <div class="addr-card__actions">
              <input type="hidden" name="act" value="act_edit_address" />
              <input name="address_id" type="hidden" value="" />
              <button
                type="button"
                name="submit"
                class="btn btn--primary btn--block"
                @click="addAddr"
              >新增收货地址</button>
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
  import { addAddress, getAddress, updateAddress, deleteAddress } from '@/api/basic'
  export default {
    data() {
      return {
        address_lists: [],
        addinfo: {
          province: '',
          city: '',
          district: '',
          address: '',
          contact_name: '',
          contact_mobile: '',
          is_default: false
        }
      };
    },
    components: {
      myhead,
      myfooter,
      left
    },
    methods: {
      getData() {
        getAddress({}).then((response) => {
          console.log(response.data);
          if (response.status === 200) {
            this.address_lists = response.data.data;
          }
        }).catch(function (error) {
          console.log(error);
        })
      },
      update(id, i) {
        this.address_lists[i].is_default=this.address_lists[i].is_default?1:0;
        updateAddress(id, this.address_lists[i]).then((response) => {
          console.log(response.data);
          this.getData();
        }).catch(function (error) {
          alert(error)
          console.log(error);
        })
      },
      addAddr() {
        this.addinfo.is_default=this.addinfo.is_default?1:0
        addAddress(this.addinfo).then((response) => {
          console.log(response.data);
          this.getData();
            this.addinfo = {
              province: '',
              city: '',
              district: '',
              address: '',
              contact_name: '',
              contact_mobile: '',
              is_default: false
            };
        }).catch(function (error) {
          alert(error)
          console.log(error);
        })
      },
      del(id) {
        deleteAddress(id).then((response) => {
          console.log(response.data);
          this.getData();
        }).catch(function (error) {
          alert(error && error.msg ? error.msg : "删除失败")
          console.log(error);
        })
      }
    },
    created() {
      this.getData();
    }
  };
</script>
<style scoped>
/* ===== 页面容器 ===== */
.address-page {
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
.address-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* ====== 左侧菜单（穿透子组件 left.vue） ====== */
.address-sidebar {
  flex: 0 0 220px;
  width: 220px;
}

.address-sidebar :deep(.slidebar) {
  float: none;
  width: 100%;
}

.address-sidebar :deep(.slide_item) {
  background: var(--surface);
  border: 0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
  margin-bottom: 0;
}

.address-sidebar :deep(.root_node) {
  padding: 14px 16px;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  border-bottom: 1px solid var(--line);
  letter-spacing: 0.5px;
}

.address-sidebar :deep(.item ul) {
  border-bottom: 0;
  padding: 4px 0;
}

.address-sidebar :deep(.item li) {
  margin-bottom: 0;
}

.address-sidebar :deep(.item li a) {
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

.address-sidebar :deep(.item li a:hover) {
  background: #fef9f8;
  color: var(--brand);
}

.address-sidebar :deep(.item li a.router-link-exact-active) {
  background: #fef9f8;
  color: var(--brand);
  font-weight: 600;
}

.address-sidebar :deep(.item li a.router-link-exact-active::before) {
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
.address-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ====== 地址卡片 ====== */
.addr-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
}

.addr-card--new {
  border: 2px dashed var(--line);
  box-shadow: none;
}

.addr-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
}

.addr-card__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  margin: 0;
  letter-spacing: 0.5px;
}

.addr-card__badge {
  display: inline-block;
  padding: 2px 10px;
  background: var(--brand);
  color: #fff;
  font-size: 11px;
  font-weight: 600;
  border-radius: 10px;
  letter-spacing: 0.5px;
}

.addr-card__body {
  padding: 16px 18px 8px;
}

.addr-card__actions {
  display: flex;
  gap: 10px;
  padding: 0 18px 16px;
}

/* ====== 表单行 ====== */
.form-row {
  display: flex;
  gap: 14px;
  margin-bottom: 14px;
}

.form-group {
  flex: 1;
  min-width: 0;
}

.form-group--wide {
  flex: 2;
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
  height: 38px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  font-size: 13px;
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

/* ====== 复选框 ====== */
.checkbox-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--ink-2);
  cursor: pointer;
  user-select: none;
}

.checkbox-label input[type="checkbox"] {
  width: 16px;
  height: 16px;
  accent-color: var(--brand);
  cursor: pointer;
}

/* ====== 按钮 ====== */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 9px 20px;
  border: 0;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease-out, color 150ms ease-out, border-color 150ms ease-out, transform 150ms ease-out;
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

.btn--outline {
  background: #fff;
  color: var(--ink-2);
  border: 1px solid var(--line);
}

.btn--outline:hover {
  border-color: var(--brand);
  color: var(--brand);
}

.btn--block {
  width: 100%;
  padding: 13px 0;
  font-size: 15px;
  letter-spacing: 1px;
}

/* ====== 空状态 ====== */
.addr-empty {
  text-align: center;
  padding: 60px 0;
  color: var(--ink-3);
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.addr-empty svg {
  margin-bottom: 12px;
}

.addr-empty p {
  font-size: 14px;
  margin: 0;
}

/* ====== 响应式 ====== */
@media (max-width: 768px) {
  .address-layout {
    flex-direction: column;
  }

  .address-sidebar {
    flex: none;
    width: 100%;
  }

  .form-row {
    flex-direction: column;
    gap: 12px;
  }
}
</style>
