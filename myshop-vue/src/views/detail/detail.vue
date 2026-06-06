<template>
  <div>
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
    <myhead></myhead>
    <div class="detail-page">
      <div class="detail-state" v-if="loading">
        <p>加载中...</p>
      </div>

      <div class="detail-state detail-state--error" v-else-if="error">
        <p>加载失败，请稍后重试</p>
      </div>

      <template v-else>
        <!-- 面包屑 -->
        <nav class="breadcrumb">
          <a href="#">首页</a>
          <span class="breadcrumb__sep">/</span>
          <span class="breadcrumb__current">{{ goods.name }}</span>
        </nav>

        <!-- ====== 商品主区：左右分栏 ====== -->
        <div class="hero">
          <!-- 左侧：图片展示区 -->
          <div class="gallery">
            <div class="gallery__main">
              <button class="gallery__arrow gallery__arrow--left" aria-label="上一张">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <div class="gallery__view">
                <img :alt="goods.name" :src="goods.main_img" />
              </div>
              <button class="gallery__arrow gallery__arrow--right" aria-label="下一张">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
            <div class="gallery__thumbs">
              <div class="gallery__thumb gallery__thumb--active">
                <img :alt="goods.name" :src="goods.main_img" />
              </div>
            </div>
          </div>

          <!-- 右侧：商品信息 -->
          <div class="info">
            <h1 class="info__title">{{ goods.name }}</h1>
            <p class="info__subtitle">{{ goods.detail | stripHtml }}</p>

            <!-- 价格区 -->
            <div class="info__price-box">
              <div class="info__price-row">
                <span class="info__price">¥{{ totalPrice().toFixed(2) }}</span>
                <span class="info__market-price">¥{{ goods.market_price }}</span>
              </div>
              <div class="info__meta">
                <span>销量 <strong>{{ goods.sales }}</strong></span>
                <span class="info__meta-sep">|</span>
                <span>好评率 <strong>99%</strong></span>
              </div>
            </div>

            <!-- 服务保障 -->
            <div class="info__services">
              <div class="service-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2 2 7l10 5 10-5-10-5Z"/><path d="M2 17 12 22l10-5M2 12l10 5 10-5"/></svg>
                <span>产地直采</span>
              </div>
              <div class="service-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>
                <span>48h发货</span>
              </div>
              <div class="service-item">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
                <span>售后无忧</span>
              </div>
            </div>

            <!-- 数量选择 -->
            <div class="info__qty">
              <span class="info__qty-label">数量</span>
              <div class="info__qty-input">
                <button
                  class="info__qty-btn"
                  @click="reduce"
                  :disabled="buynum <= 1"
                  type="button"
                >−</button>
                <input
                  id="number"
                  name="number"
                  type="text"
                  min="1"
                  v-model="buynum"
                  class="info__qty-val"
                />
                <button
                  class="info__qty-btn"
                  @click="add"
                  type="button"
                >+</button>
              </div>
              <span class="info__qty-stock">（库存 {{ goods.stock_num }} 件）</span>
            </div>

            <!-- 操作按钮 -->
            <div class="info__actions">
              <button
                class="btn-cart"
                type="button"
                @click="addcart"
                id="buy_btn"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>
                加入购物车
              </button>
              <button class="btn-buy" type="button">
                立即购买
              </button>
            </div>

            <!-- 底部保障 -->
            <p class="info__guarantee">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
              支持7天无理由退换 · 正品保证 · 全国包邮
            </p>
          </div>
        </div>

        <!-- ====== 下方：Tab 内容区 ====== -->
        <div class="detail-section">
          <!-- CSS-only  Tab 切换 -->
          <input type="radio" name="detail-tab" id="tab-detail" checked class="tab-radio" />
          <input type="radio" name="detail-tab" id="tab-comment" class="tab-radio" />

          <div class="tab-bar">
            <label for="tab-detail" class="tab-bar__label">商品详情</label>
            <label for="tab-comment" class="tab-bar__label">评价（{{ goods.sales }}）</label>
          </div>

          <!-- 商品详情面板 -->
          <div class="tab-panel tab-panel--detail">
            <div class="detail-grid">
              <div class="detail-desc">
                <h3 class="detail-block-title">商品描述</h3>
                <div class="detail-desc__body" v-html="goods.detail"></div>
              </div>
              <div class="detail-card">
                <h3 class="detail-block-title">产品信息</h3>
                <table class="detail-card__table">
                  <tbody>
                    <tr>
                      <td class="detail-card__th">品名</td>
                      <td>{{ goods.name }}</td>
                    </tr>
                    <tr>
                      <td class="detail-card__th">市场价</td>
                      <td>¥{{ goods.market_price }}</td>
                    </tr>
                    <tr>
                      <td class="detail-card__th">销售价</td>
                      <td class="detail-card__price">¥{{ goods.price }}</td>
                    </tr>
                    <tr>
                      <td class="detail-card__th">库存</td>
                      <td>{{ goods.stock_num }} 件</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- 评价面板 -->
          <div class="tab-panel tab-panel--comment">
            <div class="comment-box">
              <div class="comment-box__icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a89f94" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M8 12h8M12 8v8"/></svg>
              </div>
              <p class="comment-box__text">温馨提示：购买前请与小二沟通！祝你购物愉快！</p>
            </div>
          </div>
        </div>
      </template>

      <!-- ====== 加入购物车弹窗 ====== -->
      <div class="modal-overlay" v-show="modelshow" @click.self="close">
        <div class="modal-card">
          <div class="modal-card__icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#23a052" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
          </div>
          <p class="modal-card__text">商品已成功加入购物车</p>
          <div class="modal-card__actions">
            <a class="modal-card__back" @click="close">&lt;&lt; 继续购物</a>
            <router-link class="modal-card__go" :to="'/cart'">去结算</router-link>
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
import { addCart } from "@/api/order"
import { getGoodsByID } from "@/api/goods"

export default {
  data() {
    return {
      goods: {
        name: '',
        main_img: '',
        price: '',
        market_price: '',
        sales: 0,
        stock_num: 0,
        detail: '',
      },
      buynum: 1,
      modelshow: false,
      loading: true,
      error: false,
    };
  },
  components: {
    myhead,
    myfooter,
  },
  filters: {
    stripHtml(value) {
      if (!value) return '';
      return String(value).replace(/<[^>]+>/g, '').slice(0, 80);
    },
  },
  methods: {
    getDetail() {
      const id = this.$route.params.id;
      this.loading = true;
      this.error = false;
      getGoodsByID(id)
        .then((response) => {
          const data = response.data || {};
          this.goods = {
            ...data,
            sales: data.amount,
            detail: data.goods_desc,
          };
          this.loading = false;
        })
        .catch((err) => {
          console.log(err);
          this.error = true;
          this.loading = false;
        });
    },
    add() {
      this.buynum = this.buynum + 1;
    },
    reduce() {
      this.buynum = this.buynum - 1;
      if (this.buynum <= 1) {
        this.buynum = 1;
      }
    },
    totalPrice() {
      return (parseFloat(this.goods.price) || 0) * this.buynum;
    },
    addcart() {
      addCart({
        goods: this.goods_id,
        goods_num: this.buynum,
      })
        .then((response) => {
          if (response.status === 201) {
            this.modelshow = true;
            this.$store.dispatch('saveCart');
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    close() {
      this.modelshow = false;
    },
  },
  mounted() {
    this.goods_id = this.$route.params.id;
    this.getDetail();
  },
};
</script>
<style scoped>
/* ===== 变量 ===== */
.detail-page {
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

/* ===== 加载 / 错误状态 ===== */
.detail-state {
  padding: 80px 0;
  text-align: center;
  color: var(--ink-3);
  font-size: 14px;
}
.detail-state--error p {
  color: #c33;
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

/* ====== 商品主区 ====== */
.hero {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
}

/* ---- 左侧图片区 ---- */
.gallery {
  flex: 0 0 460px;
  width: 460px;
}

.gallery__main {
  position: relative;
  background: var(--surface);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  aspect-ratio: 1 / 1;
}

.gallery__view {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
}

.gallery__view img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

.gallery__arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 2;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 0;
  background: rgba(255,255,255,0.85);
  color: var(--ink);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  transition: background 150ms ease-out, box-shadow 150ms ease-out;
}
.gallery__arrow:hover {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.gallery__arrow--left  { left: 8px; }
.gallery__arrow--right { right: 8px; }

/* 缩略图 */
.gallery__thumbs {
  display: flex;
  gap: 10px;
  margin-top: 12px;
}

.gallery__thumb {
  width: 72px;
  height: 72px;
  border-radius: 8px;
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: border-color 150ms ease-out;
  background: var(--bg);
}

.gallery__thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.gallery__thumb--active {
  border-color: var(--brand);
}

/* ---- 右侧信息区 ---- */
.info {
  flex: 1;
  min-width: 0;
}

.info__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 22px;
  font-weight: 700;
  line-height: 1.4;
  color: var(--ink);
  margin: 0 0 8px;
}

.info__subtitle {
  font-size: 14px;
  color: var(--ink-2);
  margin: 0 0 20px;
  line-height: 1.6;
}

/* 价格 */
.info__price-box {
  background: #fef9f8;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}

.info__price-row {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 8px;
}

.info__price {
  font-size: 28px;
  font-weight: 700;
  color: var(--brand);
  line-height: 1;
}

.info__market-price {
  font-size: 14px;
  color: var(--ink-3);
  text-decoration: line-through;
}

.info__meta {
  font-size: 13px;
  color: var(--ink-2);
}

.info__meta strong {
  color: var(--brand);
  font-weight: 600;
}

.info__meta-sep {
  margin: 0 10px;
  color: var(--line);
}

/* 服务保障 */
.info__services {
  display: flex;
  gap: 20px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--line);
}

.service-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--ink-2);
}

.service-item svg {
  color: var(--brand);
  flex-shrink: 0;
}

/* 数量 */
.info__qty {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
}

.info__qty-label {
  font-size: 14px;
  color: var(--ink);
  flex-shrink: 0;
}

.info__qty-input {
  display: flex;
  align-items: center;
  border: 1px solid var(--line);
  border-radius: 6px;
  overflow: hidden;
}

.info__qty-btn {
  width: 34px;
  height: 34px;
  border: 0;
  background: var(--bg);
  color: var(--ink);
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 150ms ease-out;
}

.info__qty-btn:hover:not(:disabled) {
  background: #e8e2d6;
}

.info__qty-btn:disabled {
  color: var(--ink-3);
  cursor: not-allowed;
}

.info__qty-val {
  width: 48px;
  height: 34px;
  border: 0;
  border-left: 1px solid var(--line);
  border-right: 1px solid var(--line);
  text-align: center;
  font-size: 14px;
  color: var(--ink);
  background: #fff;
}

.info__qty-stock {
  font-size: 13px;
  color: var(--ink-2);
}

/* 操作按钮 */
.info__actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.btn-cart {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 13px 0;
  border: 2px solid var(--brand);
  border-radius: 8px;
  background: #fff;
  color: var(--brand);
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease-out, color 150ms ease-out;
}

.btn-cart:hover {
  background: #fef9f8;
}

.btn-cart:active {
  background: #fdedeb;
}

.btn-buy {
  flex: 1;
  padding: 13px 0;
  border: 0;
  border-radius: 8px;
  background: var(--brand);
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: background 150ms ease-out;
}

.btn-buy:hover {
  background: var(--brand-dark);
}

.btn-buy:active {
  transform: scale(0.98);
}

/* 保障文字 */
.info__guarantee {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--ink-3);
  margin: 0;
}

.info__guarantee svg {
  color: var(--brand);
  flex-shrink: 0;
}

/* ====== Tab 内容区 ====== */
.detail-section {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
}

/* 隐藏 radio，CSS-only 切换 */
.tab-radio {
  display: none;
}

.tab-bar {
  display: flex;
  border-bottom: 1px solid var(--line);
}

.tab-bar__label {
  flex: 1;
  padding: 16px 0;
  text-align: center;
  font-size: 15px;
  font-weight: 500;
  color: var(--ink-2);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: color 150ms ease-out, border-color 150ms ease-out;
  user-select: none;
}

.tab-bar__label:hover {
  color: var(--ink);
}

/* Tab 选中态 */
#tab-detail:checked ~ .tab-bar .tab-bar__label[for="tab-detail"],
#tab-comment:checked ~ .tab-bar .tab-bar__label[for="tab-comment"] {
  color: var(--brand);
  border-bottom-color: var(--brand);
}

/* 面板显隐 */
#tab-detail:checked ~ .tab-panel--detail { display: block; }
#tab-detail:checked ~ .tab-panel--comment { display: none; }
#tab-comment:checked ~ .tab-panel--comment { display: block; }
#tab-comment:checked ~ .tab-panel--detail { display: none; }

.tab-panel {
  display: none;
  padding: 24px;
}

/* 默认显示详情 */
#tab-detail:checked ~ .tab-panel--detail { display: block; }

/* ---- 详情面板 ---- */
.detail-grid {
  display: flex;
  gap: 24px;
}

.detail-desc {
  flex: 1;
  min-width: 0;
}

.detail-block-title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--ink);
  margin: 0 0 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
}

.detail-desc__body {
  font-size: 14px;
  line-height: 1.8;
  color: var(--ink-2);
}

.detail-desc__body :deep(img) {
  max-width: 100%;
  border-radius: 8px;
}

.detail-desc__body :deep(p) {
  margin: 0 0 12px;
}

/* ---- 产品信息卡片 ---- */
.detail-card {
  flex: 0 0 260px;
  background: var(--bg);
  border-radius: 10px;
  padding: 16px;
}

.detail-card__table {
  width: 100%;
  border-collapse: collapse;
}

.detail-card__table td {
  padding: 8px 0;
  font-size: 13px;
  line-height: 1.6;
  border-bottom: 1px dashed var(--line);
}

.detail-card__table tr:last-child td {
  border-bottom: 0;
}

.detail-card__th {
  color: var(--ink-3);
  width: 56px;
  white-space: nowrap;
}

.detail-card__price {
  color: var(--brand);
  font-weight: 600;
}

/* ---- 评价面板 ---- */
.comment-box {
  text-align: center;
  padding: 40px 0;
  color: var(--ink-3);
}

.comment-box__icon {
  margin-bottom: 12px;
}

.comment-box__text {
  font-size: 14px;
  margin: 0;
}

/* ====== 弹窗 ====== */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-card {
  background: #fff;
  border-radius: 14px;
  padding: 32px 40px;
  text-align: center;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  animation: modal-in 200ms ease-out;
}

.modal-card__icon {
  margin-bottom: 12px;
}

.modal-card__text {
  font-size: 16px;
  color: var(--ink);
  margin: 0 0 24px;
}

.modal-card__actions {
  display: flex;
  gap: 14px;
  justify-content: center;
}

.modal-card__back {
  padding: 10px 22px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  color: var(--ink-2);
  font-size: 14px;
  cursor: pointer;
  text-decoration: none;
  transition: border-color 150ms ease-out;
}

.modal-card__back:hover {
  border-color: var(--brand);
  color: var(--brand);
}

.modal-card__go {
  padding: 10px 28px;
  border: 0;
  border-radius: 6px;
  background: var(--brand);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  text-decoration: none;
  transition: background 150ms ease-out;
}

.modal-card__go:hover {
  background: var(--brand-dark);
}

@keyframes modal-in {
  from { opacity: 0; transform: scale(0.92); }
  to   { opacity: 1; transform: scale(1); }
}

/* ====== 响应式 ====== */
@media (max-width: 860px) {
  .hero {
    flex-direction: column;
  }

  .gallery {
    flex: none;
    width: 100%;
  }

  .gallery__main {
    aspect-ratio: 1 / 1;
  }

  .detail-grid {
    flex-direction: column;
  }

  .detail-card {
    flex: none;
  }
}
</style>
