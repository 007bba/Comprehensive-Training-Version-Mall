<template>
  <section class="m-cg">
    <div
      class="m-cg__floor"
      v-for="(item, index) in lists"
      :key="index"
    >
      <header class="m-cg__head">
        <div class="m-cg__title-wrap">
          <h2 class="m-cg__title">{{ item.name }}</h2>
          <p class="m-cg__subtitle" v-if="item.sub_cat && item.sub_cat.length">
            <router-link
              v-for="(iteminfo, i) in item.sub_cat"
              :key="iteminfo.id"
              :to="'/list/' + iteminfo.id"
            >
              <span v-if="i > 0" class="m-cg__sep">·</span>{{ iteminfo.name }}
            </router-link>
          </p>
        </div>
        <router-link class="m-cg__more" :to="'/list/' + item.id">
          查看全部 <span aria-hidden="true">→</span>
        </router-link>
      </header>

      <div class="m-cg__grid">
        <article
          class="m-card"
          v-for="good in item.goods"
          :key="good.id"
        >
          <router-link class="m-card__link" :to="'/detail/' + good.id">
            <div class="m-card__pic">
              <img
                :src="good.main_img"
                :alt="good.name"
                @click.prevent.stop="openPreview(good.main_img)"
              />
            </div>
            <h3 class="m-card__name">{{ good.name }}</h3>
          </router-link>

          <div class="m-card__foot">
            <p class="m-card__price">
              <small>¥</small>{{ good.price }}
            </p>
            <button
              class="m-card__cart"
              type="button"
              :aria-label="'加入购物车 ' + good.name"
              @click="addcart(good)"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                aria-hidden="true"
              >
                <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z" />
                <path d="M3 6h18" />
                <path d="M16 10a4 4 0 0 1-8 0" />
              </svg>
            </button>
          </div>
        </article>
      </div>
    </div>

    <div
      class="m-cg__preview"
      v-if="previewVisible"
      @click="closePreview"
    >
      <img class="m-cg__preview-img" :src="previewImg" alt="预览图" />
      <button
        class="m-cg__preview-close"
        type="button"
        aria-label="关闭预览"
        @click.stop="closePreview"
      >
        ×
      </button>
    </div>
  </section>
</template>
<script>
import { getCategoryGoods } from "@/api/goods";
import { addCart } from "@/api/order";
export default {
  data() {
    return {
      lists: [],
      previewVisible: false,
      previewImg: "",
    };
  },
  methods: {
    getData() {
      getCategoryGoods().then((response) => {
        this.lists = response.data.data;
      });
    },
    addcart(good) {
      addCart({
        goods: good.id,
        goods_num: 1,
      })
        .then((response) => {
          if (response.status === 201) {
            this.$store.dispatch("saveCart");
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
    openPreview(img) {
      this.previewImg = img;
      this.previewVisible = true;
    },
    closePreview() {
      this.previewVisible = false;
      this.previewImg = "";
    },
    handleEsc(e) {
      if (e.key === "Escape" && this.previewVisible) {
        this.closePreview();
      }
    },
  },
  created() {
    this.getData();
  },
  mounted() {
    document.addEventListener("keydown", this.handleEsc);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.handleEsc);
  },
};
</script>
<style scoped>
.m-cg {
  /* —— 色彩 —— */
  --brand: #b23a2e;
  --brand-dark: #993023;
  --brand-soft: #f4e3de;
  --bg: #faf7f1;
  --surface: #ffffff;
  --line: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;

  /* —— 字体 —— */
  --font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;

  /* —— 节奏 —— */
  --ease: ease-out;

  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  font-family: var(--font-sans);
  color: var(--ink);
}

/* —— 楼层间距 48px —— */
.m-cg__floor + .m-cg__floor {
  margin-top: 48px;
}
.m-cg__floor:first-child {
  margin-top: 48px;
}

/* —— 楼层标题区 —— */
.m-cg__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  padding-bottom: 16px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--line);
}
.m-cg__title-wrap {
  min-width: 0;
}
.m-cg__title {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: 1px;
  color: var(--ink);
  margin: 0;
}
.m-cg__subtitle {
  margin: 6px 0 0;
  font-size: 13px;
  font-weight: 400;
  letter-spacing: 2px;
  color: var(--ink-3);
  line-height: 1.5;
}
.m-cg__subtitle a {
  color: var(--ink-3);
  transition: color 150ms var(--ease);
}
.m-cg__subtitle a:hover {
  color: var(--brand);
}
.m-cg__sep {
  margin: 0 8px;
  color: var(--ink-3);
}
.m-cg__more {
  flex-shrink: 0;
  font-size: 13px;
  letter-spacing: 1px;
  color: var(--ink-2);
  transition: color 150ms var(--ease);
  white-space: nowrap;
}
.m-cg__more span {
  margin-left: 4px;
  transition: transform 150ms var(--ease);
  display: inline-block;
}
.m-cg__more:hover {
  color: var(--brand);
}
.m-cg__more:hover span {
  transform: translateX(3px);
}

/* —— 4 列网格 —— */
.m-cg__grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  column-gap: 24px;
  row-gap: 32px;
}

/* —— 商品卡片 —— */
.m-card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(43, 38, 34, 0.04);
  padding: 16px;
  display: flex;
  flex-direction: column;
  transition: border-color 150ms var(--ease);
}
.m-card:hover {
  border-color: #d8cdb9;
}

.m-card__link {
  display: block;
  color: inherit;
}

.m-card__pic {
  border-radius: 10px;
  overflow: hidden;
  background: var(--bg);
  aspect-ratio: 1 / 1;
}
.m-card__pic img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
  cursor: zoom-in;
  transition: transform 150ms var(--ease);
}
.m-card:hover .m-card__pic img {
  transform: scale(1.03);
}

.m-card__name {
  font-family: var(--font-sans);
  font-size: 15px;
  font-weight: 500;
  line-height: 1.6;
  color: var(--ink);
  margin: 12px 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 48px;
}

.m-card__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 12px;
}

.m-card__price {
  font-family: var(--font-sans);
  font-size: 19px;
  font-weight: 700;
  line-height: 1.2;
  color: var(--brand);
  margin: 0;
}
.m-card__price small {
  font-size: 13px;
  font-weight: 700;
  margin-right: 1px;
  position: relative;
  top: -1px;
}

/* 加购按钮：36x36 圆形,朱砂红,颜色 + 按下反馈 */
.m-card__cart {
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 50%;
  background: var(--brand);
  color: #fff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: background-color 150ms var(--ease), transform 150ms var(--ease);
}
.m-card__cart:hover {
  background: var(--brand-dark);
}
.m-card__cart:active {
  background: var(--brand-dark);
  transform: scale(0.96);
}
.m-card__cart:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* —— 图片预览浮层(Lightbox) —— */
.m-cg__preview {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5vh 5vw;
  box-sizing: border-box;
  z-index: 9999;
  cursor: zoom-out;
  animation: m-cg-fade 180ms var(--ease);
}
.m-cg__preview-img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
  animation: m-cg-zoom 200ms var(--ease);
}
.m-cg__preview-close {
  position: absolute;
  top: 24px;
  right: 32px;
  width: 44px;
  height: 44px;
  border: 0;
  border-radius: 50%;
  background: #fff;
  color: #2b2622;
  font-size: 26px;
  line-height: 1;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 150ms var(--ease), transform 150ms var(--ease);
}
.m-cg__preview-close:hover {
  background: #f0f0f0;
  transform: scale(1.05);
}
@keyframes m-cg-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes m-cg-zoom {
  from { transform: scale(0.92); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>
