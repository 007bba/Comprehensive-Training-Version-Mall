<template>
  <div>
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
    <myhead></myhead>

    <div class="cart-page">
      <!-- 面包屑 -->
      <nav class="breadcrumb">
        <a href="#">首页</a>
        <span class="breadcrumb__sep">/</span>
        <span class="breadcrumb__current">购物车</span>
      </nav>

      <!-- 页面标题 -->
      <div class="cart-header">
        <h2 class="cart-header__title">我的购物车</h2>
        <span class="cart-header__count" id="itemsnum-top">{{ cart_lists.length }} 件商品</span>
      </div>

      <!-- 空状态 -->
      <div class="cart-empty" v-if="!cart_lists.length">
        <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#a89f94" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
        <p class="cart-empty__text">购物车是空的</p>
        <a href="#" class="cart-empty__link">去逛逛</a>
      </div>

      <template v-else>
        <!-- 商品卡片列表 -->
        <div class="cart-list">
          <div
            class="cart-card"
            v-for="(item, index) in cart_lists"
            :key="index"
          >
            <!-- 商品图片 -->
            <router-link :to="'/detail' + item.goods.id" class="cart-card__img">
              <img :alt="item.goods.name" :src="item.goods.main_img" />
            </router-link>

            <!-- 商品信息 -->
            <div class="cart-card__info">
              <router-link :to="'/detail' + item.goods.id" class="cart-card__name">
                {{ item.goods.name }}
              </router-link>
              <p class="cart-card__unit-price">单价 ¥{{ item.goods.price }}</p>
            </div>

            <!-- 数量选择器 -->
            <div class="cart-card__qty">
              <button
                class="qty-btn"
                type="button"
                title="减少1个数量"
                @click="reduce(item.goods.id, item.goods_num)"
              >−</button>
              <input
                type="text"
                class="qty-input"
                id="goods_number_270"
                v-model="item.goods_num"
              />
              <button
                class="qty-btn"
                type="button"
                title="增加1个数量"
                @click="add(item.goods.id, item.goods_num)"
              >+</button>
            </div>

            <!-- 小计 -->
            <p class="cart-card__subtotal" id="total_items_270">
              ¥{{ item.goods.price * item.goods_num }}
            </p>

            <!-- 删除 -->
            <button class="cart-card__del" type="button">删除</button>
          </div>
        </div>

        <!-- 底部结算栏 -->
        <div class="cart-footer" id="price-total">
          <div class="cart-footer__left">
            <a id="del-all" href="#" class="cart-footer__link cart-footer__link--danger">清空购物车</a>
            <a href="#" class="cart-footer__link">继续购物</a>
          </div>
          <div class="cart-footer__right">
            <p class="cart-footer__total">
              <span id="selectedCount">{{ cart_lists.length }}</span> 件商品，合计：
              <strong id="totalSkuPrice">¥{{ this.allprice }}</strong>
            </p>
            <router-link :to="'checkout'" class="cart-footer__checkout" id="checkout-top">
              去结算
            </router-link>
          </div>
        </div>
      </template>
    </div>

    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from "@/views/app/head";
import myfooter from "@/views/app/footer";
import { getCart, updateCart } from "@/api/order";
export default {
  data() {
    return {
      cart_lists: {},
      buynum: 1,
      modelshow: false,
      allprice: 0,
    };
  },
  components: {
    myhead,
    myfooter,
  },
  methods: {
    getCart() {
      getCart().then((response) => {
        console.log("2dsfds" + response.data);
        this.cart_lists = response.data.data;
        //console.log("cart"+JSON.stringify(this.cart_lists[0]));
        var totalprice = 0;
        for (var i = 0; i < this.cart_lists.length; i++) {
          var item = this.cart_lists[i];
          console.log("item" + item);
          totalprice += item.goods_num * item.goods.price;
        }
        console.log("okoko" + this.cart_lists[0]);
        //console.log("okoko"+this.cart_lists[0].goods_num);
        console.log("okoko" + this.cart_lists[0].goods.price);
        this.allprice = totalprice;
      });
    },
    add(id, nums) {
      updateCart(id, { goods_num: nums + 1 }).then((response) => {
        console.log(response.data);
        this.getCart();
        //这里对购物车进行vuex处理
        this.$store.dispatch("saveCart");
      });
    },
    reduce(id, nums) {
      updateCart(id, { goods_num: nums - 1 }).then((response) => {
        console.log(response.data);
        this.getCart();
        //这里对购物车进行vuex处理
        this.$store.dispatch("saveCart");
      });
    },
  },
  created() {
    this.getCart();
  },
};
</script>
<style scoped>
/* ===== 页面容器 ===== */
.cart-page {
  --brand: #b23a2e;
  --brand-dark: #993023;
  --bg: #faf7f1;
  --surface: #ffffff;
  --line: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;

  max-width: 960px;
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

/* ===== 页面标题 ===== */
.cart-header {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 20px;
}

.cart-header__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 22px;
  font-weight: 700;
  color: var(--ink);
  margin: 0;
  letter-spacing: 0.5px;
}

.cart-header__count {
  font-size: 14px;
  color: var(--ink-3);
}

/* ===== 空状态 ===== */
.cart-empty {
  text-align: center;
  padding: 80px 0;
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.cart-empty svg {
  display: block;
  margin: 0 auto 12px;
}

.cart-empty__text {
  font-size: 14px;
  color: var(--ink-3);
  margin: 0 0 16px;
}

.cart-empty__link {
  display: inline-block;
  padding: 8px 24px;
  border: 1px solid var(--brand);
  border-radius: 8px;
  color: var(--brand);
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: background 150ms ease-out, color 150ms ease-out;
}

.cart-empty__link:hover {
  background: #fef9f8;
}

/* ===== 商品列表 ===== */
.cart-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

/* ===== 商品卡片 ===== */
.cart-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 16px;
  transition: box-shadow 150ms ease-out;
}

.cart-card:hover {
  box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

/* 图片 */
.cart-card__img {
  flex-shrink: 0;
  width: 88px;
  height: 88px;
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg);
  display: block;
}

.cart-card__img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 信息 */
.cart-card__info {
  flex: 1;
  min-width: 0;
}

.cart-card__name {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--ink);
  text-decoration: none;
  line-height: 1.5;
  margin-bottom: 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cart-card__name:hover {
  color: var(--brand);
}

.cart-card__unit-price {
  font-size: 13px;
  color: var(--ink-3);
  margin: 0;
}

/* 数量选择器 */
.cart-card__qty {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  border: 1px solid var(--line);
  border-radius: 6px;
  overflow: hidden;
}

.qty-btn {
  width: 30px;
  height: 30px;
  border: 0;
  background: var(--bg);
  color: var(--ink);
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 150ms ease-out;
}

.qty-btn:hover {
  background: #e8e2d6;
}

.qty-input {
  width: 40px;
  height: 30px;
  border: 0;
  border-left: 1px solid var(--line);
  border-right: 1px solid var(--line);
  text-align: center;
  font-size: 14px;
  color: var(--ink);
  background: #fff;
}

/* 小计 */
.cart-card__subtotal {
  flex-shrink: 0;
  width: 100px;
  text-align: right;
  font-size: 16px;
  font-weight: 700;
  color: var(--brand);
  margin: 0;
}

/* 删除按钮 */
.cart-card__del {
  flex-shrink: 0;
  padding: 4px 10px;
  border: 0;
  border-radius: 4px;
  background: transparent;
  color: var(--ink-3);
  font-size: 12px;
  cursor: pointer;
  transition: color 150ms ease-out, background 150ms ease-out;
}

.cart-card__del:hover {
  color: #c0392b;
  background: #fdedeb;
}

/* ===== 底部结算栏 ===== */
.cart-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  padding: 16px 20px;
  position: sticky;
  bottom: 0;
}

.cart-footer__left {
  display: flex;
  gap: 16px;
}

.cart-footer__link {
  font-size: 13px;
  color: var(--ink-2);
  text-decoration: none;
  transition: color 150ms ease-out;
}

.cart-footer__link:hover {
  color: var(--ink);
}

.cart-footer__link--danger {
  color: #c0392b;
}

.cart-footer__link--danger:hover {
  color: #a93226;
}

.cart-footer__right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.cart-footer__total {
  font-size: 14px;
  color: var(--ink);
  margin: 0;
}

.cart-footer__total strong {
  font-size: 22px;
  font-weight: 700;
  color: var(--brand);
}

.cart-footer__checkout {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 32px;
  border: 0;
  border-radius: 8px;
  background: var(--brand);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  text-decoration: none;
  letter-spacing: 1px;
  transition: background 150ms ease-out, transform 150ms ease-out;
}

.cart-footer__checkout:hover {
  background: var(--brand-dark);
}

.cart-footer__checkout:active {
  background: var(--brand-dark);
  transform: scale(0.98);
}

/* ===== 响应式 ===== */
@media (max-width: 640px) {
  .cart-card {
    flex-wrap: wrap;
    gap: 10px;
    padding: 12px;
  }

  .cart-card__img {
    width: 72px;
    height: 72px;
  }

  .cart-card__info {
    flex: 1 1 calc(100% - 96px);
  }

  .cart-card__subtotal {
    width: auto;
  }

  .cart-footer {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .cart-footer__right {
    justify-content: space-between;
  }
}
</style>
