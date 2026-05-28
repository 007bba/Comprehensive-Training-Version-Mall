<template>
  <div>
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
    <myhead></myhead>
    <div class="list-page">
      <!-- 面包屑 -->
      <nav class="breadcrumb">
        <a href=".">首页</a>
        <span class="breadcrumb__sep">/</span>
        <router-link :to="id">{{ curr_cate_name }}</router-link>
      </nav>

      <div class="list-layout">
        <!-- 左侧分类导航 -->
        <aside class="list-sidebar">
          <listcategory
            :sub_cat="sub_cat"
            :categoryname="curr_cate_name"
          ></listcategory>
        </aside>

        <!-- 右侧主内容 -->
        <div class="list-main">
          <!-- 价格筛选卡片 -->
          <div class="filter-card">
            <div class="filter-card__header">
              <h3 class="filter-card__title">价格筛选</h3>
            </div>
            <div class="filter-card__body">
              <div class="price-tags">
                <button
                  class="price-tag"
                  @click="query_price(10, 60)"
                  type="button"
                >¥10 - ¥60</button>
                <button
                  class="price-tag"
                  @click="query_price(60, 110)"
                  type="button"
                >¥60 - ¥110</button>
                <button
                  class="price-tag"
                  @click="query_price(110, 160)"
                  type="button"
                >¥110 - ¥160</button>
                <button
                  class="price-tag"
                  @click="query_price(160, 210)"
                  type="button"
                >¥160 - ¥210</button>
              </div>
              <div class="price-custom">
                <span class="price-custom__label">自定义</span>
                <input
                  type="text"
                  name="price_min"
                  id="pricemin"
                  v-model="min_price"
                  class="price-custom__input"
                  placeholder="最低价"
                />
                <span class="price-custom__dash">—</span>
                <input
                  type="text"
                  name="price_max"
                  id="pricemax"
                  v-model="max_price"
                  class="price-custom__input"
                  placeholder="最高价"
                />
                <button
                  type="button"
                  @click="query_price(min_price, max_price)"
                  class="price-custom__btn"
                >确定</button>
              </div>
            </div>
          </div>

          <!-- 排序栏 -->
          <div class="sort-bar">
            <button
              class="sort-btn"
              :class="{ 'sort-btn--active': ordering === '-amount' || ordering === 'amount' }"
              @click="sort_amount(type1)"
              type="button"
            >
              销量
              <span class="sort-btn__arrow" :class="{ 'sort-btn__arrow--asc': type1 === 'amount' }">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="18 15 12 9 6 15"/></svg>
              </span>
            </button>
            <button
              class="sort-btn"
              :class="{ 'sort-btn--active': ordering === '-price' || ordering === 'price' }"
              @click="sort_price(type2)"
              type="button"
            >
              价格
              <span class="sort-btn__arrow" :class="{ 'sort-btn__arrow--asc': type2 === 'price' }">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="18 15 12 9 6 15"/></svg>
              </span>
            </button>
            <span class="sort-bar__count" v-if="goodsnum">共 {{ goodsnum }} 件商品</span>
          </div>

          <!-- 商品列表 -->
          <div class="product-grid" v-if="list_data.length">
            <div
              class="product-card"
              v-for="item in list_data"
              :key="item.id"
            >
              <router-link
                :to="'/detail/' + item.id"
                target="_blank"
                class="product-card__link"
              >
                <div class="product-card__img">
                  <img
                    :title="item.name"
                    :alt="item.name"
                    :src="item.main_img"
                  />
                </div>
                <h3 class="product-card__name">{{ item.name }}</h3>
                <p class="product-card__price">
                  <b>¥{{ item.price }}</b>
                </p>
                <p class="product-card__sales">
                  销量 <span>{{ item.amount }}</span> 件
                </p>
              </router-link>
            </div>
          </div>

          <div v-else class="empty-result">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#a89f94" stroke-width="1.5" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
            <p>暂无符合条件的商品</p>
          </div>

          <!-- 分页 -->
          <div class="pagination-wrap">
            <mypage :total_page="total_page" @get_page="get_page"></mypage>
          </div>
        </div>
      </div>
    </div>
    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from "@/views/app/head.vue";
import myfooter from "@/views/app/footer.vue";
import { getGoods, getGoodsCategoryByID } from "@/api/goods";
//左侧菜单导航
import listcategory from "@/views/list/listcategory.vue";
import mypage from "@/views/list/page.vue";
export default {
  data() {
    return {
      sub_cat: [],
      curr_cate_name: "",
      id: "",
      list_data: [],
      goodsnum: 0,
      ordering: "-amount",
      curr_page: 1,
      type1: "-amount",
      type2: "-price",
      min_price: "",
      max_price: "",
    };
  },
  components: {
    myhead,
    myfooter,
    listcategory: listcategory,
    mypage: mypage,
  },
  methods: {
    getAllCategory() {
      this.id = this.$route.params.id;
      if (this.id && this.id !== "0") {
        getGoodsCategoryByID(this.id).then((response) => {
          this.sub_cat = response.data.data.sub_cat;
          this.curr_cate_name = response.data.data.name;
        });
      } else {
        this.sub_cat = [];
        this.curr_cate_name = this.$route.query.keyword
          ? "搜索结果"
          : "全部商品";
      }
    },
    getlistData() {
      const params = {
        min_price: this.min_price,
        max_price: this.max_price,
        ordering: this.ordering,
        page: this.curr_page,
      };
      if (this.$route.params.id && this.$route.params.id !== "0") {
        params.category = this.$route.params.id;
      }
      const keyword = this.$route.query.keyword;
      if (keyword) {
        params.name = keyword;
        params.search = keyword;
      }
      getGoods(params).then((response) => {
        this.list_data = response.data.data;
        this.goodsnum = response.data.count;
      });
    },
    sort_amount(type) {
      type == "-amount" ? (this.type1 = "amount") : (this.type1 = "-amount");
      this.ordering = type;
      this.getlistData();
    },
    sort_price(type) {
      type == "-price" ? (this.type2 = "price") : (this.type2 = "-price");
      this.ordering = type;
      this.getlistData();
    },
    get_page(data) {
      this.curr_page = data.curr_page;
      this.getlistData();
    },
    query_price(min_price, max_price) {
      this.min_price = min_price;
      this.max_price = max_price;
      this.getlistData();
    },
  },
  computed: {
    total_page() {
      return Math.ceil(this.goodsnum / 8);
    },
  },
  watch: {
    $route() {
      this.curr_page = 1;
      this.getAllCategory();
      this.getlistData();
    },
  },
  created() {
    this.getAllCategory(); //获取当前分类下的子分类
    this.getlistData(); //根据条件获取商品信息
  },
};
</script>
<style scoped>
/* ===== 页面容器 ===== */
.list-page {
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

/* ===== 左右布局 ===== */
.list-layout {
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

.list-sidebar {
  flex: 0 0 220px;
  width: 220px;
}

.list-main {
  flex: 1;
  min-width: 0;
}

/* ====== 左侧分类导航（子组件穿透） ====== */
.list-sidebar :deep(.sidebar) {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow: hidden;
}

.list-sidebar :deep(.cate-menu) {
  padding: 0;
}

.list-sidebar :deep(.cate-menu h3) {
  margin: 0;
}

.list-sidebar :deep(.cate-menu h3 a) {
  display: block;
  padding: 16px;
  background: var(--brand);
  color: #fff;
  text-decoration: none;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.list-sidebar :deep(.cate-menu h3 strong) {
  font-weight: 600;
}

.list-sidebar :deep(.cate-menu h3 i) {
  display: block;
  font-size: 12px;
  font-weight: 400;
  opacity: 0.8;
  margin-top: 4px;
  font-style: normal;
}

.list-sidebar :deep(.cate-menu dl) {
  padding: 8px 0;
}

.list-sidebar :deep(.cate-menu dt) {
  padding: 10px 16px;
  font-size: 13px;
  color: var(--ink-2);
  cursor: pointer;
  transition: color 150ms ease-out, background 150ms ease-out;
}

.list-sidebar :deep(.cate-menu dt:hover) {
  color: var(--brand);
  background: #fef9f8;
}

/* ====== 筛选卡片 ====== */
.filter-card {
  background: var(--surface);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  margin-bottom: 16px;
  overflow: hidden;
}

.filter-card__header {
  padding: 14px 16px 0;
}

.filter-card__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 15px;
  font-weight: 600;
  color: var(--ink);
  margin: 0;
}

.filter-card__body {
  padding: 12px 16px 16px;
}

/* 价格快捷标签 */
.price-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 14px;
}

.price-tag {
  padding: 6px 14px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  color: var(--ink-2);
  font-size: 13px;
  cursor: pointer;
  transition: border-color 150ms ease-out, color 150ms ease-out, background 150ms ease-out;
}

.price-tag:hover {
  border-color: var(--brand);
  color: var(--brand);
  background: #fef9f8;
}

.price-tag:active {
  background: #fdedeb;
}

/* 自定义价格 */
.price-custom {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price-custom__label {
  font-size: 13px;
  color: var(--ink-3);
  flex-shrink: 0;
}

.price-custom__input {
  width: 80px;
  height: 34px;
  padding: 0 10px;
  border: 1px solid var(--line);
  border-radius: 6px;
  font-size: 13px;
  color: var(--ink);
  background: #fff;
  box-sizing: border-box;
  transition: border-color 150ms ease-out;
}

.price-custom__input:focus {
  border-color: var(--brand);
  outline: none;
}

.price-custom__input::placeholder {
  color: var(--ink-3);
}

.price-custom__dash {
  color: var(--ink-3);
  font-size: 13px;
}

.price-custom__btn {
  height: 34px;
  padding: 0 16px;
  border: 0;
  border-radius: 6px;
  background: var(--brand);
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  transition: background 150ms ease-out;
}

.price-custom__btn:hover {
  background: var(--brand-dark);
}

/* ====== 排序栏 ====== */
.sort-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding: 10px 14px;
  background: var(--surface);
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.sort-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 14px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  color: var(--ink-2);
  font-size: 13px;
  cursor: pointer;
  transition: border-color 150ms ease-out, color 150ms ease-out, background 150ms ease-out;
}

.sort-btn:hover {
  border-color: var(--brand);
  color: var(--brand);
}

.sort-btn--active {
  border-color: var(--brand);
  color: var(--brand);
  background: #fef9f8;
}

.sort-btn__arrow {
  display: inline-flex;
  transition: transform 200ms ease-out;
}

.sort-btn__arrow--asc {
  transform: rotate(180deg);
}

.sort-bar__count {
  margin-left: auto;
  font-size: 13px;
  color: var(--ink-3);
}

/* ====== 商品网格 ====== */
.product-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

/* ====== 商品卡片 ====== */
.product-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: border-color 150ms ease-out, box-shadow 150ms ease-out, transform 150ms ease-out;
}

.product-card:hover {
  border-color: #d8cdb9;
  box-shadow: 0 6px 20px rgba(0,0,0,0.08);
  transform: translateY(-3px);
}

.product-card__link {
  display: block;
  padding: 14px;
  color: inherit;
  text-decoration: none;
}

.product-card__img {
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg);
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-card__img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 150ms ease-out;
}

.product-card:hover .product-card__img img {
  transform: scale(1.04);
}

.product-card__name {
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  color: var(--ink);
  margin: 10px 0 6px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-card__price {
  margin: 0 0 4px;
}

.product-card__price b {
  font-size: 17px;
  font-weight: 700;
  color: var(--brand);
}

.product-card__sales {
  font-size: 12px;
  color: var(--ink-3);
  margin: 0;
}

.product-card__sales span {
  color: var(--ink-2);
}

/* ====== 空结果 ====== */
.empty-result {
  text-align: center;
  padding: 60px 0;
  color: var(--ink-3);
}

.empty-result svg {
  margin-bottom: 12px;
}

.empty-result p {
  font-size: 14px;
  margin: 0;
}

/* ====== 分页（子组件穿透） ====== */
.pagination-wrap {
  display: flex;
  justify-content: center;
  padding: 8px 0;
}

.pagination-wrap :deep(.pagenav) {
  text-align: center;
}

.pagination-wrap :deep(.pagenav ul) {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  justify-content: center;
}

.pagination-wrap :deep(.pagenav li) {
  display: contents;
}

.pagination-wrap :deep(.nextLink) {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 36px;
  height: 36px;
  padding: 0 10px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  color: var(--ink-2);
  font-size: 13px;
  cursor: pointer;
  text-decoration: none;
  transition: border-color 150ms ease-out, color 150ms ease-out, background 150ms ease-out;
  user-select: none;
}

.pagination-wrap :deep(.nextLink:hover) {
  border-color: var(--brand);
  color: var(--brand);
  background: #fef9f8;
}

.pagination-wrap :deep(.nextLink:active) {
  background: #fdedeb;
}

/* ====== 响应式 ====== */
@media (max-width: 1024px) {
  .product-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .list-layout {
    flex-direction: column;
  }

  .list-sidebar {
    flex: none;
    width: 100%;
  }

  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .price-custom {
    flex-wrap: wrap;
  }
}
</style>
