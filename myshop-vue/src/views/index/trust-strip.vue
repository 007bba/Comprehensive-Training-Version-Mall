<template>
  <section class="m-trust">
    <div class="m-trust__inner">
      <div class="m-trust__item" v-for="item in items" :key="item.title">
        <div class="m-trust__ico" v-html="item.icon"></div>
        <div class="m-trust__text">
          <h4 class="m-trust__title">{{ item.title }}</h4>
          <p class="m-trust__sub">{{ item.sub }}</p>
        </div>
      </div>
    </div>
  </section>
</template>
<script>
export default {
  data() {
    return {
      items: [
        {
          title: "产地直采",
          sub: "跳过中间商",
          icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
            <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"
              d="M3 21h18M5 21V10l7-5 7 5v11M9 21v-6h6v6"/>
          </svg>`,
        },
        {
          title: "时令现摘",
          sub: "不卖隔年陈货",
          icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
            <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"
              d="M12 3c4 4 4 9 0 13-4-4-4-9 0-13zM12 16v5"/>
            <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"
              d="M5 13c2 1 4 1 7-1M19 13c-2 1-4 1-7-1"/>
          </svg>`,
        },
        {
          title: "48 小时直发",
          sub: "顺丰冷链",
          icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
            <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"
              d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/>
            <circle cx="7" cy="18" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/>
            <circle cx="17" cy="18" r="2" fill="none" stroke="currentColor" stroke-width="1.4"/>
          </svg>`,
        },
        {
          title: "不好吃可退",
          sub: "七天无忧",
          icon: `<svg viewBox="0 0 24 24" aria-hidden="true">
            <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"
              d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4z"/>
            <path fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"
              d="M9 12l2 2 4-4"/>
          </svg>`,
        },
      ],
    };
  },
};
</script>
<style scoped>
.m-trust {
  --line: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;
  --font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;

  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
  background: transparent;
  font-family: var(--font-sans);
  color: var(--ink);
}

.m-trust__inner {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  align-items: center;
}

.m-trust__item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 20px;
  border-left: 1px solid var(--line);
}
.m-trust__item:first-child {
  border-left: 0;
  padding-left: 0;
}
.m-trust__item:last-child {
  padding-right: 0;
}

.m-trust__ico {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  color: var(--ink);
  opacity: 0.7;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.m-trust__ico >>> svg {
  width: 28px;
  height: 28px;
  display: block;
}

.m-trust__text {
  min-width: 0;
}
.m-trust__title {
  font-family: var(--font-serif);
  font-size: 15px;
  font-weight: 500;
  letter-spacing: 1px;
  color: var(--ink);
  margin: 0 0 2px;
  line-height: 1.4;
}
.m-trust__sub {
  font-size: 12px;
  letter-spacing: 1px;
  color: var(--ink-3);
  margin: 0;
  line-height: 1.4;
}

@media (max-width: 900px) {
  .m-trust__inner {
    grid-template-columns: repeat(2, 1fr);
    row-gap: 24px;
  }
  .m-trust__item:nth-child(odd) {
    border-left: 0;
    padding-left: 0;
  }
}
</style>
