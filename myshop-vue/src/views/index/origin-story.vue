<template>
  <section class="m-origin">
    <div class="m-origin__inner">
      <a class="m-origin__media" :href="story.link">
        <img :src="story.image" :alt="story.title" />
      </a>
      <div class="m-origin__body">
        <p class="m-origin__eyebrow">PRODUCER · 匠人故事</p>
        <h2 class="m-origin__title">{{ story.title }}</h2>
        <p class="m-origin__sub">{{ story.subtitle }}</p>
        <p class="m-origin__excerpt">{{ story.excerpt }}</p>
        <a class="m-origin__cta" :href="story.link">
          阅读匠人故事 <i aria-hidden="true">→</i>
        </a>
      </div>
    </div>
  </section>
</template>
<script>
export default {
  data() {
    return {
      story: {
        title: "六堡茶,在广西的山雾里慢慢老去",
        subtitle: "梧州 · 六堡镇 · 老韦",
        excerpt:
          "二十年前老韦从父亲手里接过这间木仓,茶叶在桂北的潮气里安静呼吸,十二个春夏秋冬,从青涩到沉郁。他说,茶不急,我也不急——这是我们想交给你的味道。",
        image: "https://picsum.photos/800/450?seed=origin",
        link: "#",
      },
    };
  },
};
</script>
<style scoped>
.m-origin {
  --brand: #b23a2e;
  --brand-dark: #993023;
  --bg: #faf7f1;
  --line: #ece6dc;
  --ink: #2b2622;
  --ink-2: #6e665e;
  --ink-3: #a89f94;
  --font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;
  --ease: cubic-bezier(0.22, 0.61, 0.36, 1);

  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
  background: transparent;
  font-family: var(--font-sans);
  color: var(--ink);
}

.m-origin__inner {
  display: grid;
  grid-template-columns: 1.1fr 1fr;
  gap: 56px;
  align-items: center;
}

/* —— 左图:16:9 圆角 20px —— */
.m-origin__media {
  display: block;
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  background: var(--bg);
  aspect-ratio: 16 / 9;
}
.m-origin__media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 150ms var(--ease);
}
.m-origin__media:hover img {
  transform: scale(1.03);
}

/* —— 右文 —— */
.m-origin__body {
  min-width: 0;
}
.m-origin__eyebrow {
  font-size: 12px;
  letter-spacing: 3px;
  color: var(--ink-3);
  margin: 0 0 14px;
  text-transform: uppercase;
}
.m-origin__title {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 600;
  line-height: 1.5;
  letter-spacing: 1.5px;
  color: var(--ink);
  margin: 0 0 12px;
}
.m-origin__sub {
  font-size: 13px;
  letter-spacing: 2px;
  color: var(--ink-3);
  margin: 0 0 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--line);
}
.m-origin__excerpt {
  font-size: 15px;
  line-height: 1.8;
  letter-spacing: 0.5px;
  color: var(--ink-2);
  margin: 0 0 28px;
}

.m-origin__cta {
  display: inline-flex;
  align-items: center;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2px;
  color: var(--ink);
  border-bottom: 1px solid var(--ink);
  padding: 6px 0;
  transition: color 150ms var(--ease), border-color 150ms var(--ease);
}
.m-origin__cta i {
  font-style: normal;
  margin-left: 8px;
  display: inline-block;
  transition: transform 150ms var(--ease);
}
.m-origin__cta:hover {
  color: var(--brand);
  border-color: var(--brand);
}
.m-origin__cta:hover i {
  transform: translateX(4px);
}

@media (max-width: 900px) {
  .m-origin__inner {
    grid-template-columns: 1fr;
    gap: 24px;
  }
}
</style>
