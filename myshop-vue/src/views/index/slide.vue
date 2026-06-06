<template>
  <section class="m-slide">
    <div class="m-slide__inner">
      <swiper ref="mySwiper" :options="swiperOptions">
        <swiper-slide v-for="(item, index) in lists" :key="index">
          <router-link
            class="m-slide__item"
            :to="'/detail/' + item.goods"
            target="_blank"
          >
            <img class="m-slide__img" :src="item.images" alt="" />
            <div class="m-slide__mask"></div>
            <div class="m-slide__caption">
              <p class="m-slide__sub">{{ item.subtitle || "SEASONAL · 时令" }}</p>
              <h2 class="m-slide__title">
                {{ item.title || "山间一味,等你慢慢品" }}
              </h2>
              <span class="m-slide__cta">
                了解详情 <i aria-hidden="true">→</i>
              </span>
            </div>
          </router-link>
        </swiper-slide>
        <div class="swiper-pagination" slot="pagination"></div>
        <div class="swiper-button-prev" slot="button-prev"></div>
        <div class="swiper-button-next" slot="button-next"></div>
      </swiper>
    </div>
  </section>
</template>
<script>
import { swiper, swiperSlide } from "vue-awesome-swiper";
import { getSlide } from "@/api/goods";
import "swiper/dist/css/swiper.css";
export default {
  name: "default",
  data() {
    return {
      swiperOptions: {
        loop: true,
        autoplay: {
          delay: 5000,
          stopOnLastSlide: false,
          disableOnInteraction: false,
        },
        speed: 700,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        navigation: {
          nextEl: ".swiper-button-next",
          prevEl: ".swiper-button-prev",
        },
      },
      lists: [],
    };
  },
  components: {
    swiper,
    swiperSlide,
  },
  methods: {
    getData() {
      getSlide()
        .then((response) => {
          this.lists = response.data.data;
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  created() {
    this.getData();
  },
};
</script>
<style scoped>
.m-slide {
  /* —— 色彩 —— */
  --brand: #b23a2e;
  --bg: #faf7f1;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;
  --line: #ece6dc;

  /* —— 字体 —— */
  --font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;

  --ease: ease-out;

  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 16px 0;
  font-family: var(--font-sans);
  color: var(--ink);
}

.m-slide__inner {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: var(--bg);
  border: 1px solid var(--line);
}

/* —— 单张 slide —— */
.m-slide__item {
  display: block;
  position: relative;
  width: 100%;
  height: 400px;
  color: inherit;
  text-decoration: none;
}
.m-slide__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* 暖色渐变遮罩,让文案可读但不压死图 */
.m-slide__mask {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    100deg,
    rgba(43, 38, 34, 0.42) 0%,
    rgba(43, 38, 34, 0.18) 45%,
    rgba(43, 38, 34, 0) 70%
  );
  pointer-events: none;
}

/* 三段式文案 */
.m-slide__caption {
  position: absolute;
  left: 56px;
  bottom: 64px;
  max-width: 460px;
  color: #fff;
}
.m-slide__sub {
  margin: 0 0 12px;
  font-size: 13px;
  font-weight: 400;
  letter-spacing: 3px;
  color: rgba(255, 255, 255, 0.78);
  text-transform: uppercase;
}
.m-slide__title {
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 600;
  line-height: 1.4;
  letter-spacing: 2px;
  margin: 0 0 24px;
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.18);
}
.m-slide__cta {
  display: inline-flex;
  align-items: center;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2px;
  padding: 10px 0;
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.65);
  transition: color 150ms var(--ease), border-color 150ms var(--ease);
}
.m-slide__cta i {
  font-style: normal;
  margin-left: 8px;
  display: inline-block;
  transition: transform 150ms var(--ease);
}
.m-slide__item:hover .m-slide__cta {
  color: #fff;
  border-color: #fff;
}
.m-slide__item:hover .m-slide__cta i {
  transform: translateX(4px);
}

/* —— 分页:克制的细线条 —— */
.m-slide__inner >>> .swiper-pagination {
  bottom: 24px;
  left: 56px;
  text-align: left;
  width: auto;
}
.m-slide__inner >>> .swiper-pagination-bullet {
  width: 24px;
  height: 2px;
  border-radius: 1px;
  background: rgba(255, 255, 255, 0.5);
  opacity: 1;
  margin: 0 4px !important;
  transform-origin: left center;
  transition: background-color 150ms var(--ease), transform 150ms var(--ease);
}
.m-slide__inner >>> .swiper-pagination-bullet-active {
  background: #fff;
  transform: scaleX(1.5);
}

/* —— 左右箭头:暖墨细线圆,hover 转朱砂 —— */
.m-slide__inner >>> .swiper-button-prev,
.m-slide__inner >>> .swiper-button-next {
  width: 40px;
  height: 40px;
  margin-top: -20px;
  border-radius: 50%;
  background: rgba(250, 247, 241, 0.86);
  color: var(--ink);
  opacity: 0;
  transition: opacity 150ms var(--ease), background-color 150ms var(--ease),
    color 150ms var(--ease);
  box-shadow: 0 2px 8px rgba(43, 38, 34, 0.08);
}
.m-slide__inner >>> .swiper-button-prev {
  left: 24px;
}
.m-slide__inner >>> .swiper-button-next {
  right: 24px;
}
.m-slide__inner:hover >>> .swiper-button-prev,
.m-slide__inner:hover >>> .swiper-button-next {
  opacity: 1;
}
.m-slide__inner >>> .swiper-button-prev:hover,
.m-slide__inner >>> .swiper-button-next:hover {
  background: var(--brand);
  color: #fff;
}
.m-slide__inner >>> .swiper-button-prev::after,
.m-slide__inner >>> .swiper-button-next::after {
  font-size: 14px;
  font-weight: 600;
}
</style>
