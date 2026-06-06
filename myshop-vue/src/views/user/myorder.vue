<template>
  <div>
    <myhead></myhead>
    <div class="order-page">
      <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
      <!-- 面包屑 -->
      <nav class="breadcrumb">
        <a href="#">首页</a>
        <span class="breadcrumb__sep">/</span>
        <span>用户中心</span>
        <span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">我的订单</span>
      </nav>

      <div class="order-layout">
        <!-- 左侧菜单 -->
        <aside class="order-sidebar">
          <left></left>
        </aside>

        <!-- 右侧订单列表 -->
        <div class="order-main">
          <!-- 空状态 -->
          <div class="order-empty" v-if="!order_lists.length">
            <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#a89f94" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="18" rx="3"/><path d="M6 3v18"/><path d="M10 8h4M10 12h4M10 16h2"/></svg>
            <p class="order-empty__text">暂无订单记录</p>
          </div>

          <!-- 订单卡片列表 -->
          <div class="order-card" v-for="item in order_lists" :key="item.order_sn">
            <!-- 头部：订单号 + 时间 + 状态 -->
            <div class="order-card__header">
              <div class="order-card__header-left">
                <span class="order-card__sn">{{ item.order_sn }}</span>
                <span class="order-card__date">{{ item.create_date }}</span>
              </div>
              <span class="order-card__status">{{ item.order_state }}</span>
            </div>

            <!-- 底部：金额 + 操作 -->
            <div class="order-card__footer">
              <div class="order-card__total">
                <span class="order-card__total-label">订单总额</span>
                <span class="order-card__total-price">¥{{ item.order_price }}</span>
              </div>
              <div class="order-card__actions">
                <a class="order-card__action order-card__action--cancel" href="#">
                  取消订单
                </a>
              </div>
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
  import { getOrder } from '@/api/order'
  export default {
    data() {
      return {
        order_lists: []
      };
    },
    methods: {
      getData() {
        getOrder({}).then((response) => {
          console.log(response.data);
          if (response.status === 200) {
            this.order_lists = response.data.data;
          }
        }).catch(function (error) {
          console.log(error);
        })
      },
    },
      components: {
      myhead,
      myfooter,
      left,
    },
    created() {
      this.getData();
    }
  };
</script>
<style scoped>
/* ===== 页面容器 ===== */
.order-page {
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
.order-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* ====== 左侧菜单（穿透 left.vue，与 address/profile 页完全一致） ====== */
.order-sidebar {
  flex: 0 0 220px;
  width: 220px;
}

.order-sidebar :deep(.slidebar) {
  float: none;
  width: 100%;
}

.order-sidebar :deep(.slide_item) {
  background: var(--surface);
  border: 0;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
  margin-bottom: 0;
}

.order-sidebar :deep(.root_node) {
  padding: 14px 16px;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  border-bottom: 1px solid var(--line);
  letter-spacing: 0.5px;
}

.order-sidebar :deep(.item ul) {
  border-bottom: 0;
  padding: 4px 0;
}

.order-sidebar :deep(.item li) {
  margin-bottom: 0;
}

.order-sidebar :deep(.item li a) {
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

.order-sidebar :deep(.item li a:hover) {
  background: #fef9f8;
  color: var(--brand);
}

.order-sidebar :deep(.item li a.router-link-exact-active) {
  background: #fef9f8;
  color: var(--brand);
  font-weight: 600;
}

.order-sidebar :deep(.item li a.router-link-exact-active::before) {
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
.order-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

/* ====== 空状态 ====== */
.order-empty {
  text-align: center;
  padding: 80px 0;
  color: var(--ink-3);
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.order-empty__text {
  font-size: 14px;
  margin: 12px 0 0;
}

/* ====== 订单卡片 ====== */
.order-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
}

/* 头部 */
.order-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
  background: #fdfaf7;
}

.order-card__header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.order-card__sn {
  font-size: 14px;
  font-weight: 600;
  color: var(--ink);
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
}

.order-card__date {
  font-size: 12px;
  color: var(--ink-3);
}

/* 状态标签 */
.order-card__status {
  display: inline-block;
  padding: 3px 12px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.5px;
  flex-shrink: 0;
}

/* 状态颜色 */
.order-card__status--pending {
  background: #fdedeb;
  color: #c0392b;
}

.order-card__status--shipping {
  background: #ebf5fb;
  color: #2471a3;
}

.order-card__status--completed {
  background: #eafaf1;
  color: #1e8449;
}

.order-card__status--cancelled {
  background: #f2f3f4;
  color: #7f8c8d;
}

/* 底部 */
.order-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
}

.order-card__total {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.order-card__total-label {
  font-size: 13px;
  color: var(--ink-2);
}

.order-card__total-price {
  font-size: 20px;
  font-weight: 700;
  color: var(--brand);
}

/* 操作按钮 */
.order-card__actions {
  display: flex;
  gap: 8px;
}

.order-card__action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 7px 18px;
  border: 1px solid var(--line);
  border-radius: 6px;
  font-size: 13px;
  color: var(--ink-2);
  text-decoration: none;
  cursor: pointer;
  transition: border-color 150ms ease-out, color 150ms ease-out, background 150ms ease-out;
}

.order-card__action:hover {
  border-color: var(--brand);
  color: var(--brand);
  background: #fef9f8;
}

.order-card__action--cancel {
  color: var(--ink-3);
}

.order-card__action--cancel:hover {
  border-color: #c0392b;
  color: #c0392b;
  background: #fdedeb;
}

/* ====== 响应式 ====== */
@media (max-width: 768px) {
  .order-layout {
    flex-direction: column;
  }

  .order-sidebar {
    flex: none;
    width: 100%;
  }

  .order-card__header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .order-card__footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
