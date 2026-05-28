<template>
  <header class="m-header">
    <!-- 顶部欢迎条 -->
    <div class="m-topbar">
      <div class="m-topbar__inner">
        <span class="m-topbar__slogan">一方水土,一味家乡</span>
        <ul class="m-topbar__menu">
          <template v-if="userinfo">
            <li>
              <router-link to="/profile">{{ userinfo.username }}</router-link>
            </li>
            <li><a class="m-link" @click="logout">退出</a></li>
          </template>
          <template v-else>
            <li><router-link to="/login">请登录</router-link></li>
            <li class="m-topbar__sep"></li>
            <li><router-link to="/reg">免费注册</router-link></li>
          </template>
          <li class="m-topbar__sep"></li>
          <li>
            <router-link to="/profile">
              <svg class="m-ico" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2M12 11a4 4 0 1 0 0-8 4 4 0 0 0 0 8z"
                />
              </svg>
              会员中心
            </router-link>
          </li>
          <li>
            <router-link to="/myorder">
              <svg class="m-ico" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 11l3 3L22 4M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"
                />
              </svg>
              我的订单
            </router-link>
          </li>
          <li>
            <router-link to="/address">
              <svg class="m-ico" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"
                />
                <circle
                  cx="12"
                  cy="10"
                  r="3"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                />
              </svg>
              收货地址
            </router-link>
          </li>
        </ul>
      </div>
    </div>

    <!-- 主区域:Logo + 搜索 + 购物车 (64px) -->
    <div class="m-main">
      <div class="m-main__inner">
        <router-link to="/index" class="m-logo">特产小店</router-link>

        <form class="m-search" @submit.prevent="doSearch">
          <svg class="m-search__ico" viewBox="0 0 24 24" aria-hidden="true">
            <circle
              cx="11"
              cy="11"
              r="7"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
            />
            <path
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              d="M20 20l-3.5-3.5"
            />
          </svg>
          <input
            v-model="searchKeyword"
            class="m-search__input"
            type="text"
            autocomplete="off"
            placeholder="搜一搜你想念的味道"
          />
          <button type="submit" class="m-search__btn">搜索</button>
        </form>

        <div
          class="m-cart"
          :class="{ 'is-open': showCart }"
          @mouseover="overCart"
          @mouseout="outCart"
        >
          <router-link class="m-cart__tit" to="/checkout">
            <svg class="m-ico" viewBox="0 0 24 24" aria-hidden="true">
              <path
                fill="none"
                stroke="currentColor"
                stroke-width="1.6"
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"
              />
              <path
                fill="none"
                stroke="currentColor"
                stroke-width="1.6"
                d="M3 6h18"
              />
              <path
                fill="none"
                stroke="currentColor"
                stroke-width="1.6"
                stroke-linecap="round"
                d="M16 10a4 4 0 0 1-8 0"
              />
            </svg>
            <span>购物车</span>
            <em class="m-cart__num" v-if="totalNum">{{ totalNum }}</em>
          </router-link>

          <transition name="m-cart-fade">
            <div class="m-cart__panel" v-show="showCart">
            <div v-if="cart_lists && cart_lists.length" class="m-cart__list">
              <dl v-for="item in cart_lists" :key="item.id">
                <dt>
                  <img :src="item.goods.main_img" alt="" />
                </dt>
                <dd>
                  <router-link
                    class="m-cart__name"
                    :to="'detail' + item.goods.id"
                    >{{ item.goods.name }}</router-link
                  >
                  <p class="m-cart__price">
                    <span class="m-price">¥{{ item.goods.price }}</span>
                    <i>×{{ item.goods_num }}</i>
                  </p>
                </dd>
              </dl>
            </div>
            <p v-else class="m-cart__empty">购物车还是空的</p>

            <div class="m-cart__foot">
              <span
                >共 <b class="m-price">{{ totalNum }}</b> 件 · 合计
                <b class="m-price">¥{{ totalPrice }}</b></span
              >
              <router-link class="m-cart__checkout" to="/checkout"
                >去结算</router-link
              >
            </div>
          </div>
          </transition>
        </div>
      </div>
    </div>

    <!-- 导航栏 -->
    <div class="m-nav">
      <div class="m-nav__inner">
        <div
          class="m-allcat"
          @mouseover="overAllmenu"
          @mouseout="outAllmenu"
        >
          <div class="m-allcat__title">全部商品分类</div>
          <div class="m-allcat__panel" v-show="showmenu">
            <ul>
              <li
                :class="{ 'is-active': current === index }"
                v-for="(item, index) in allMenu"
                :key="index"
                @mouseover="oversubmenu(index)"
                @mouseout="outsubmenu(index)"
              >
                <router-link class="m-allcat__main" :to="'/list/' + item.id">{{
                  item.name
                }}</router-link>
                <div class="m-allcat__sub" v-show="showsubmenu === index">
                  <router-link
                    v-for="iteminfo in item.sub_cat"
                    :key="iteminfo.id"
                    :to="'/list/' + iteminfo.id"
                    >{{ iteminfo.name }}</router-link
                  >
                </div>
              </li>
            </ul>
          </div>
        </div>

        <ul class="m-nav__links">
          <li>
            <router-link to="/index">首页</router-link>
          </li>
          <template v-for="item in allMenu">
            <li v-if="item.is_nav" :key="item.id">
              <router-link :to="'/list/' + item.id">{{
                item.name
              }}</router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </header>
</template>
<script>
import { mapGetters } from "vuex";
import { getGoodsCategory } from "@/api/goods";
export default {
  data() {
    return {
      showmenu: false,
      allMenu: [],
      showsubmenu: -1,
      first: false,
      current: false,
      showCart: false,
      searchKeyword: "",
    };
  },
  methods: {
    overAllmenu() {
      this.showmenu = true;
    },
    outAllmenu() {
      this.showmenu = false;
    },
    oversubmenu(index) {
      this.current = index;
      this.showsubmenu = index;
    },
    outsubmenu() {
      this.current = false;
      this.showsubmenu = -1;
    },
    overCart() {
      this.showCart = true;
    },
    outCart() {
      this.showCart = false;
    },
    doSearch() {
      const kw = this.searchKeyword.trim();
      if (!kw) return;
      this.$router.push({ path: "/list/0", query: { keyword: kw } });
    },
    getAllMenu() {
      getGoodsCategory().then((response) => {
        this.allMenu = response.data.data;
      });
    },
    logout() {
      this.$store.dispatch("delUser");
    },
  },
  computed: {
    ...mapGetters({
      userinfo: "userinfo",
      cart_lists: "cart_lists",
      totalNum: "totalNum",
      totalPrice: "totalPrice",
    }),
  },
  created() {
    this.getAllMenu();
  },
};
</script>
<style scoped>
.m-header {
  /* —— 色彩 —— */
  --brand: #b23a2e;
  --brand-dark: #993023;
  --brand-soft: #f4e3de;
  --bg: #faf7f1;
  --surface: #ffffff;
  --line: #e8e2d9;
  --line-soft: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;
  --search-bg: #f5f2ed;

  /* —— 字体 —— */
  --font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;

  --ease: cubic-bezier(0.22, 0.61, 0.36, 1);

  background: var(--surface);
  font-family: var(--font-sans);
  color: var(--ink);
  border-bottom: 1px solid var(--line);
}

/* —— 顶部欢迎条 —— */
.m-topbar {
  background: var(--surface);
  border-bottom: 1px solid var(--line-soft);
}
.m-topbar__inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 36px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--ink-3);
  letter-spacing: 1px;
}
.m-topbar__slogan {
  color: var(--ink-3);
  font-family: var(--font-serif);
  letter-spacing: 2px;
}
.m-topbar__menu {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  align-items: center;
  gap: 14px;
}
.m-topbar__menu a {
  color: var(--ink-3);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  transition: color 150ms var(--ease);
}
.m-topbar__menu a:hover {
  color: var(--brand);
}
.m-topbar__sep {
  width: 1px;
  height: 12px;
  background: var(--line);
}

/* —— 主区域 64px —— */
.m-main__inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 64px;
  padding: 0 24px;
  display: flex;
  align-items: center;
  gap: 40px;
}

/* Logo:衬线 */
.m-logo {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 700;
  letter-spacing: 4px;
  color: var(--brand);
  white-space: nowrap;
  transition: color 150ms var(--ease);
}
.m-logo:hover {
  color: var(--brand-dark);
}

/* 搜索框 */
.m-search {
  flex: 1;
  max-width: 520px;
  height: 40px;
  background: var(--search-bg);
  border-radius: 40px;
  display: flex;
  align-items: center;
  padding: 0 4px 0 16px;
  transition: background-color 150ms var(--ease);
}
.m-search:focus-within {
  background: #efe9df;
}
.m-search__ico {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  color: var(--ink-3);
  margin-right: 8px;
}
.m-search__input {
  flex: 1;
  border: 0;
  outline: none;
  background: transparent;
  font-size: 13px;
  color: var(--ink);
  height: 100%;
  font-family: inherit;
  letter-spacing: 0.5px;
}
.m-search__input::placeholder {
  color: var(--ink-3);
}
.m-search__btn {
  border: 0;
  background: var(--brand);
  color: #fff;
  height: 32px;
  padding: 0 22px;
  border-radius: 22px;
  cursor: pointer;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2px;
  font-family: inherit;
  transition: background-color 150ms var(--ease);
}
.m-search__btn:hover {
  background: var(--brand-dark);
}

/* 购物车 */
.m-cart {
  position: relative;
  margin-left: auto;
}
.m-cart__tit {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 18px;
  border-radius: 40px;
  color: var(--ink);
  background: transparent;
  border: 1px solid var(--line);
  font-size: 13px;
  letter-spacing: 1px;
  transition: color 150ms var(--ease), border-color 150ms var(--ease),
    background-color 150ms var(--ease);
}
.m-cart__tit:hover,
.m-cart.is-open .m-cart__tit {
  color: var(--brand);
  border-color: var(--brand);
  background: var(--brand-soft);
}
.m-cart__num {
  background: var(--brand);
  color: #fff;
  font-style: normal;
  font-weight: 500;
  min-width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  border-radius: 9px;
  padding: 0 6px;
  font-size: 11px;
}

.m-cart__panel {
  position: absolute;
  right: 0;
  top: calc(100% + 12px);
  width: 320px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(43, 38, 34, 0.08);
  z-index: 100;
  padding: 12px;
}

/* —— 购物车浮层柔出柔入(只动 opacity + transform 4px) —— */
.m-cart-fade-enter-active,
.m-cart-fade-leave-active {
  transition: opacity 150ms var(--ease), transform 150ms var(--ease);
}
.m-cart-fade-enter,
.m-cart-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
.m-cart-fade-enter-to,
.m-cart-fade-leave {
  opacity: 1;
  transform: translateY(0);
}

.m-cart__list {
  max-height: 280px;
  overflow-y: auto;
}
.m-cart__list dl {
  display: flex;
  gap: 12px;
  padding: 12px 0;
  margin: 0;
  border-bottom: 1px solid var(--line-soft);
}
.m-cart__list dl:last-child {
  border-bottom: 0;
}
.m-cart__list dt img {
  width: 56px;
  height: 56px;
  object-fit: cover;
  border-radius: 8px;
}
.m-cart__list dd {
  flex: 1;
  margin: 0;
  min-width: 0;
}
.m-cart__name {
  display: block;
  color: var(--ink);
  font-size: 13px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color 150ms var(--ease);
}
.m-cart__name:hover {
  color: var(--brand);
}
.m-cart__price {
  margin: 6px 0 0;
  color: var(--ink-3);
  font-size: 12px;
}
.m-cart__price i {
  font-style: normal;
  margin-left: 6px;
}
.m-cart__empty {
  text-align: center;
  color: var(--ink-3);
  padding: 32px 0;
  font-size: 13px;
}
.m-cart__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 4px 4px;
  color: var(--ink-2);
  font-size: 12px;
  border-top: 1px solid var(--line-soft);
}
.m-cart__checkout {
  background: var(--brand);
  color: #fff;
  padding: 8px 18px;
  border-radius: 20px;
  font-size: 13px;
  letter-spacing: 1px;
  transition: background-color 150ms var(--ease);
}
.m-cart__checkout:hover {
  background: var(--brand-dark);
}
.m-price {
  color: var(--brand);
  font-weight: 700;
}

/* —— 导航栏 —— */
.m-nav {
  background: var(--surface);
  border-top: 1px solid var(--line-soft);
}
.m-nav__inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: stretch;
}

/* 全部分类入口 */
.m-allcat {
  position: relative;
  width: 200px;
  flex-shrink: 0;
  margin-right: 8px;
}
.m-allcat__title {
  height: 44px;
  line-height: 44px;
  font-size: 14px;
  letter-spacing: 2px;
  color: var(--ink);
  cursor: pointer;
  transition: color 150ms var(--ease);
}
.m-allcat__title::before {
  content: "";
  display: inline-block;
  vertical-align: middle;
  margin-right: 8px;
  width: 14px;
  height: 1px;
  background: currentColor;
  position: relative;
}
.m-allcat:hover .m-allcat__title {
  color: var(--brand);
}
.m-allcat__panel {
  position: absolute;
  left: 0;
  top: 100%;
  width: 200px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 0 0 12px 12px;
  box-shadow: 0 8px 24px rgba(43, 38, 34, 0.08);
  z-index: 50;
  padding: 6px 0;
}
.m-allcat__panel ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.m-allcat__panel li {
  position: relative;
}
.m-allcat__main {
  display: block;
  padding: 10px 20px;
  font-size: 13px;
  color: var(--ink);
  letter-spacing: 1px;
  transition: background-color 150ms var(--ease), color 150ms var(--ease);
}
.m-allcat__panel li.is-active .m-allcat__main {
  background: var(--brand-soft);
  color: var(--brand);
}
.m-allcat__sub {
  position: absolute;
  left: 200px;
  top: -1px;
  min-width: 320px;
  min-height: calc(100% + 2px);
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 0 12px 12px 0;
  box-shadow: 4px 4px 16px rgba(43, 38, 34, 0.06);
  padding: 16px 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px 24px;
}
.m-allcat__sub a {
  color: var(--ink-2);
  font-size: 13px;
  transition: color 150ms var(--ease);
}
.m-allcat__sub a:hover {
  color: var(--brand);
}

/* 主导航链接:hover 下划线动画 */
.m-nav__links {
  display: flex;
  align-items: stretch;
  list-style: none;
  margin: 0;
  padding: 0;
  flex: 1;
  gap: 4px;
}
.m-nav__links li {
  display: flex;
  align-items: stretch;
}
.m-nav__links a {
  position: relative;
  display: inline-flex;
  align-items: center;
  height: 44px;
  padding: 0 18px;
  color: var(--ink);
  font-size: 14px;
  letter-spacing: 2px;
  transition: color 150ms var(--ease);
}
.m-nav__links a::after {
  content: "";
  position: absolute;
  left: 18px;
  right: 18px;
  bottom: 8px;
  height: 1px;
  background: var(--brand);
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 150ms var(--ease);
}
.m-nav__links a:hover,
.m-nav__links a.router-link-active {
  color: var(--brand);
}
.m-nav__links a:hover::after,
.m-nav__links a.router-link-active::after {
  transform: scaleX(1);
}

/* 通用图标尺寸 */
.m-ico {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}
</style>
