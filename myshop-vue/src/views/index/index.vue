<template>
  <div id="i1" class="m-page">
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
    <link href="../../static/css/index.css" rel="stylesheet" type="text/css" />
    <myhead></myhead>
    <main class="m-page__body">
      <slide v-reveal></slide>
      <trust-strip v-reveal></trust-strip>
      <recommend v-reveal></recommend>
      <origin-story v-reveal></origin-story>
      <categorygoods v-reveal></categorygoods>
    </main>
    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from "./../app/head";
import myfooter from "./../app/footer";
import slide from "./slide";
import trustStrip from "./trust-strip";
import recommend from "./recommend";
import originStory from "./origin-story";
import categorygoods from "./categorygoods";

const prefersReducedMotion = () =>
  typeof window !== "undefined" &&
  window.matchMedia &&
  window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const reveal = {
  bind(el) {
    if (typeof window === "undefined") return;
    if (prefersReducedMotion() || !("IntersectionObserver" in window)) {
      el.classList.add("m-reveal", "is-in");
      return;
    }
    el.classList.add("m-reveal");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-in");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );
    observer.observe(el);
    el.__revealObserver__ = observer;
  },
  unbind(el) {
    if (el.__revealObserver__) {
      el.__revealObserver__.disconnect();
      el.__revealObserver__ = null;
    }
  },
};

export default {
  data() {
    return {};
  },
  directives: {
    reveal,
  },
  components: {
    myhead,
    slide,
    trustStrip,
    recommend,
    originStory,
    categorygoods,
    myfooter,
  },
};
</script>

<!-- 全局字体、入场动画、prefers-reduced-motion 守卫 -->
<style>
#i1.m-page,
#i1.m-page * {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial,
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  box-sizing: border-box;
}

/* 衬线节点 */
#i1.m-page .m-cg__title,
#i1.m-page .m-rec__title,
#i1.m-page .m-slide__title,
#i1.m-page .m-origin__title,
#i1.m-page .m-trust__title,
#i1.m-page .m-footer__motto,
#i1.m-page .m-card__note,
#i1.m-page .m-logo,
#i1.m-page .m-topbar__slogan {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
}

/* —— 入场动画:fade + 上移 8px,200ms ease-out,只动 transform & opacity —— */
#i1.m-page .m-reveal {
  opacity: 0;
  transform: translateY(8px);
  transition: opacity 200ms ease-out, transform 200ms ease-out;
  will-change: opacity, transform;
}
#i1.m-page .m-reveal.is-in {
  opacity: 1;
  transform: translateY(0);
}

/* —— prefers-reduced-motion 全局守卫:关闭一切动效 —— */
@media (prefers-reduced-motion: reduce) {
  #i1.m-page *,
  #i1.m-page *::before,
  #i1.m-page *::after {
    transition-duration: 0ms !important;
    animation-duration: 0ms !important;
    animation-iteration-count: 1 !important;
  }
  #i1.m-page .m-reveal {
    opacity: 1 !important;
    transform: none !important;
  }
}
</style>

<!-- 页面级布局与节奏 -->
<style scoped>
.m-page {
  min-height: 100vh;
  background: #faf7f1;
  color: #2b2622;
}
.m-page__body {
  padding-bottom: 0;
}

.m-page__body >>> .m-slide {
  margin: 0 auto 8px;
  padding: 40px 24px 0;
  max-width: 1200px;
}
.m-page__body >>> .m-trust {
  margin: 0 auto;
  padding: 24px 24px;
  max-width: 1200px;
}
.m-page__body >>> .m-rec {
  margin: 0 auto 48px;
  padding: 0 24px;
  max-width: 1200px;
}
.m-page__body >>> .m-origin {
  margin: 0 auto 48px;
  padding: 16px 24px 32px;
  max-width: 1200px;
}
.m-page__body >>> .m-cg {
  margin: 0 auto 48px;
  padding: 0 24px;
  max-width: 1200px;
}

.m-page__body >>> .m-cg__floor:first-child {
  margin-top: 0;
}
</style>
