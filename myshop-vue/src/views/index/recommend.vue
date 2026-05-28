<template>
  <section class="m-rec">
    <header class="m-rec__head">
      <div class="m-rec__title-wrap">
        <h2 class="m-rec__title">时令鲜货</h2>
        <p class="m-rec__subtitle">SEASONAL · 编辑推荐</p>
      </div>
      <router-link class="m-rec__more" to="/list/0">
        查看全部 <span aria-hidden="true">→</span>
      </router-link>
    </header>

    <div class="m-rec__rail" ref="rail">
      <article
        class="m-card"
        v-for="good in lists"
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
          <p class="m-card__note" v-if="good.note">{{ good.note }}</p>
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

    <div
      class="m-rec__preview"
      ref="preview"
      v-if="previewVisible"
      @click="closePreview"
    >
      <img class="m-rec__preview-img" :src="previewImg" alt="预览图" />
      <button
        class="m-rec__preview-close"
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
import { addCart } from "@/api/order";
export default {
  data() {
    return {
      previewVisible: false,
      previewImg: "",
      // mock 数据,后续接入 API 后替换
      lists: [
        {
          id: 1,
          name: "武夷山炭焙肉桂",
          note: "桂皮香深沉,岩骨花香,五月新焙",
          price: "168",
          main_img: require("@/static/images/rougui.jpg"),
        },
        {
          id: 2,
          name: "云南古树普洱生饼",
          note: "三百年老树,布朗山头春茶,357 克",
          price: "298",
          main_img: require("@/static/images/tea.jpg"),
        },
        {
          id: 3,
          name: "潮州手工老梅",
          note: "老树梅,带核生晒,微酸回甘",
          price: "58",
          main_img: require("@/static/images/meizi.jpg"),
        },
        {
          id: 4,
          name: "徽州石臼黑芝麻糖",
          note: "古法石臼,只用桂花蜜,薄而不脆",
          price: "42",
          main_img: require("@/static/images/zhima.jpg"),
        },
        {
          id: 5,
          name: "广西六堡老茶",
          note: "梧州木仓,慢发酵十二年,槟榔香",
          price: "228",
          main_img: "https://picsum.photos/id/225/400/400",
        },
        {
          id: 6,
          name: "潜山雪枣干",
          note: "皖南灰枣,日晒七天,无糖无蜜",
          price: "78",
          main_img: "https://picsum.photos/id/223/400/400",
        },
      ],
      _prevBodyOverflow: "",
    };
  },
  methods: {
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
      this._prevBodyOverflow = document.body.style.overflow;
      document.body.style.overflow = "hidden";
      this.$nextTick(() => {
        const el = this.$refs.preview;
        if (el && el.parentNode !== document.body) {
          document.body.appendChild(el);
        }
      });
    },
    closePreview() {
      this.previewVisible = false;
      this.previewImg = "";
      document.body.style.overflow = this._prevBodyOverflow || "";
    },
    handleEsc(e) {
      if (e.key === "Escape" && this.previewVisible) {
        this.closePreview();
      }
    },
  },
  mounted() {
    document.addEventListener("keydown", this.handleEsc);
  },
  beforeDestroy() {
    document.removeEventListener("keydown", this.handleEsc);
    const el = this.$refs.preview;
    if (el && el.parentNode === document.body) {
      document.body.removeChild(el);
    }
    document.body.style.overflow = this._prevBodyOverflow || "";
  },
};
</script>
<style scoped>
.m-rec {
  /* —— 色彩 —— */
  --brand: #b23a2e;
  --brand-dark: #993023;
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

  --ease: ease-out;

  max-width: 1200px;
  margin: 48px auto 0;
  padding: 0 16px;
  font-family: var(--font-sans);
  color: var(--ink);
  /* 显式声明,避免任何祖先样式继承导致脱离布局流的元素被困住 */
  transform: none;
  filter: none;
  perspective: none;
}

/* —— 楼层标题区(与 categorygoods 一致) —— */
.m-rec__head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  padding-bottom: 16px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--line);
}
.m-rec__title-wrap {
  min-width: 0;
}
.m-rec__title {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: 1px;
  color: var(--ink);
  margin: 0;
}
.m-rec__subtitle {
  margin: 6px 0 0;
  font-size: 13px;
  font-weight: 400;
  letter-spacing: 2px;
  color: var(--ink-3);
  line-height: 1.5;
}
.m-rec__more {
  flex-shrink: 0;
  font-size: 13px;
  letter-spacing: 1px;
  color: var(--ink-2);
  white-space: nowrap;
  transition: color 150ms var(--ease);
}
.m-rec__more span {
  margin-left: 4px;
  display: inline-block;
  transition: transform 150ms var(--ease);
}
.m-rec__more:hover {
  color: var(--brand);
}
.m-rec__more:hover span {
  transform: translateX(3px);
}

/* —— 横向滚动轨道 —— */
.m-rec__rail {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  overflow-y: visible;
  scroll-snap-type: x mandatory;
  scroll-padding-left: 0;
  /* 上下留点空间,避免阴影被裁掉 */
  padding: 4px 0 12px;
  -webkit-overflow-scrolling: touch;
}

/* 极细滚动条,与米线同色 */
.m-rec__rail::-webkit-scrollbar {
  height: 6px;
}
.m-rec__rail::-webkit-scrollbar-track {
  background: transparent;
}
.m-rec__rail::-webkit-scrollbar-thumb {
  background: var(--line);
  border-radius: 3px;
}
.m-rec__rail::-webkit-scrollbar-thumb:hover {
  background: #d8cdb9;
}

/* —— 商品卡片(对齐 categorygoods.vue) —— */
.m-card {
  flex: 0 0 268px;
  scroll-snap-align: start;
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
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* —— 编辑荐语:衬线小字,赋予内容感 —— */
.m-card__note {
  font-family: var(--font-serif);
  font-size: 13px;
  font-weight: 400;
  line-height: 1.5;
  letter-spacing: 0.5px;
  color: var(--ink-2);
  margin: 8px 0 0;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.m-card__foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 14px;
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
/* 该元素 mounted 后会被 JS 移动到 document.body 下,以绕过任何祖先 transform/filter/perspective */
.m-rec__preview {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  width: 100%;
  height: 100%;
  margin: 0;
  background: rgba(0, 0, 0, 0.92);
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5vh 5vw;
  box-sizing: border-box;
  z-index: 100000;
  cursor: zoom-out;
  /* 绝对防御:浮层自身不允许任何变换 */
  transform: none;
  filter: none;
  perspective: none;
  animation: m-rec-fade 180ms var(--ease);
}
.m-rec__preview-img {
  max-width: 90vw;
  max-height: 90vh;
  object-fit: contain;
  border-radius: 4px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
  animation: m-rec-zoom 200ms var(--ease);
}
.m-rec__preview-close {
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
.m-rec__preview-close:hover {
  background: #f0f0f0;
  transform: scale(1.05);
}
@keyframes m-rec-fade {
  from { opacity: 0; }
  to { opacity: 1; }
}
@keyframes m-rec-zoom {
  from { transform: scale(0.92); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>
