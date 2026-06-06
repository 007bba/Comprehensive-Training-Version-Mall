<template>
  <footer class="m-footer">
    <!-- 品牌句 -->
    <p class="m-footer__motto">把好物,慢慢交给懂的人。</p>

    <!-- 多列信息区 -->
    <div class="m-footer__main">
      <div class="m-footer__col">
        <h4 class="m-footer__h">关于我们</h4>
        <ul>
          <li><a href="#" rel="nofollow">品牌故事</a></li>
          <li><a href="#" rel="nofollow">产地溯源</a></li>
          <li><a href="#" rel="nofollow">人才招聘</a></li>
          <li><a href="#" rel="nofollow">联系我们</a></li>
        </ul>
      </div>

      <div class="m-footer__col">
        <h4 class="m-footer__h">客户服务</h4>
        <ul>
          <li><a href="#" rel="nofollow">配送说明</a></li>
          <li><a href="#" rel="nofollow">退换货政策</a></li>
          <li><a href="#" rel="nofollow">常见问题</a></li>
          <li><a href="#" rel="nofollow">免责条款</a></li>
        </ul>
      </div>

      <div class="m-footer__col">
        <h4 class="m-footer__h">关注我们</h4>
        <ul class="m-footer__social">
          <li>
            <a href="#" aria-label="微信" rel="nofollow">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M9 4C5.13 4 2 6.69 2 10c0 1.86.99 3.51 2.55 4.6L4 17l2.86-1.5c.69.18 1.41.27 2.14.27"
                />
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M22 15c0-2.76-2.69-5-6-5s-6 2.24-6 5 2.69 5 6 5c.55 0 1.09-.06 1.6-.18L20 21l-.5-2c1.51-.91 2.5-2.4 2.5-4z"
                />
              </svg>
              <span>微信</span>
            </a>
          </li>
          <li>
            <a href="#" aria-label="微博" rel="nofollow">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <ellipse
                  cx="12"
                  cy="14"
                  rx="8"
                  ry="6"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                />
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  d="M16 6c2.5 0 4 1.5 4 4M16 3c4.5 0 7 3 7 7"
                />
              </svg>
              <span>微博</span>
            </a>
          </li>
          <li>
            <a href="#" aria-label="小红书" rel="nofollow">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <rect
                  x="3"
                  y="3"
                  width="18"
                  height="18"
                  rx="3"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                />
                <path
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.6"
                  stroke-linecap="round"
                  d="M8 8v8M8 12h3a2 2 0 0 0 0-4H8M14 8v8l3-4 3 4V8"
                />
              </svg>
              <span>小红书</span>
            </a>
          </li>
        </ul>
        <p class="m-footer__hint">服务时间 10:00 — 23:00</p>
      </div>

      <div class="m-footer__col m-footer__col--sub">
        <h4 class="m-footer__h">订阅时令信物</h4>
        <p class="m-footer__hint">
          每月一封,只讲产地、节气与餐桌
        </p>
        <form class="m-sub" @submit.prevent="onSubscribe">
          <input
            v-model="email"
            class="m-sub__input"
            type="email"
            placeholder="请输入你的邮箱"
            autocomplete="email"
          />
          <button type="submit" class="m-sub__btn">订阅</button>
        </form>
      </div>
    </div>

    <!-- 底部版权 -->
    <div class="m-footer__bottom">
      <p>
        &copy; 2021—2026 特产小店 · 版权所有
        <span class="m-footer__dot">·</span>
        服务时间 10:00—23:00
      </p>
    </div>
  </footer>
</template>
<script>
export default {
  data() {
    return {
      email: "",
    };
  },
  methods: {
    onSubscribe() {
      const v = this.email.trim();
      if (!v) return;
      // 预留:后续接订阅 API
      this.email = "";
    },
  },
};
</script>
<style scoped>
.m-footer {
  /* —— 色彩 —— */
  --bg: #2c2a28;
  --bg-soft: #3a3733;
  --text: #f5f2ed;
  --text-2: #c8c2b8;
  --text-3: #8e887e;
  --line: rgba(245, 242, 237, 0.08);
  --brand: #b23a2e;
  --brand-dark: #993023;

  /* —— 字体 —— */
  --font-serif: "Noto Serif SC", "Songti SC", "STSong", serif;
  --font-sans: -apple-system, BlinkMacSystemFont, "PingFang SC",
    "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", sans-serif;

  --ease: cubic-bezier(0.22, 0.61, 0.36, 1);

  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  padding: 48px 24px 0;
  margin-top: 64px;
}

/* —— 品牌句 —— */
.m-footer__motto {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 2px;
  text-align: center;
  color: var(--text);
  margin: 0 0 40px;
  padding: 0 0 32px;
  border-bottom: 1px solid var(--line);
}

/* —— 多列信息区 —— */
.m-footer__main {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(3, 1fr) 1.4fr;
  gap: 48px;
  padding-bottom: 40px;
}

.m-footer__h {
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 2px;
  color: var(--text);
  margin: 0 0 18px;
}

.m-footer__col ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.m-footer__col li {
  margin-bottom: 10px;
}
.m-footer__col a {
  font-size: 13px;
  color: var(--text-2);
  letter-spacing: 0.5px;
  transition: color 150ms var(--ease);
}
.m-footer__col a:hover {
  color: var(--text);
}

.m-footer__hint {
  font-size: 12px;
  color: var(--text-3);
  letter-spacing: 0.5px;
  margin: 0 0 12px;
  line-height: 1.6;
}

/* —— 社交图标 —— */
.m-footer__social {
  display: flex;
  gap: 14px;
  margin-bottom: 14px !important;
}
.m-footer__social li {
  margin: 0 !important;
}
.m-footer__social a {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid var(--line);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--text-2);
  transition: color 150ms var(--ease), border-color 150ms var(--ease),
    background-color 150ms var(--ease);
}
.m-footer__social a:hover {
  color: var(--text);
  border-color: var(--brand);
  background: rgba(178, 58, 46, 0.18);
}
.m-footer__social svg {
  width: 16px;
  height: 16px;
}
.m-footer__social span {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip: rect(0 0 0 0);
}

/* —— 订阅邮箱 —— */
.m-sub {
  display: flex;
  align-items: center;
  height: 40px;
  background: var(--bg-soft);
  border-radius: 40px;
  padding: 0 4px 0 16px;
  margin-top: 12px;
}
.m-sub__input {
  flex: 1;
  border: 0;
  outline: none;
  background: transparent;
  font-size: 13px;
  color: var(--text);
  font-family: inherit;
  letter-spacing: 0.5px;
  height: 100%;
  min-width: 0;
}
.m-sub__input::placeholder {
  color: var(--text-3);
}
.m-sub__btn {
  border: 0;
  cursor: pointer;
  height: 32px;
  padding: 0 22px;
  border-radius: 22px;
  background: var(--brand);
  color: #fff;
  font-size: 13px;
  font-weight: 500;
  letter-spacing: 2px;
  font-family: inherit;
  transition: background-color 150ms var(--ease);
}
.m-sub__btn:hover {
  background: var(--brand-dark);
}

/* —— 底部版权 —— */
.m-footer__bottom {
  border-top: 1px solid var(--line);
  padding: 20px 0 24px;
  text-align: center;
}
.m-footer__bottom p {
  margin: 0;
  font-size: 12px;
  color: var(--text-3);
  letter-spacing: 1px;
}
.m-footer__dot {
  margin: 0 8px;
  color: var(--text-3);
}

/* —— 窄屏简化(可选) —— */
@media (max-width: 900px) {
  .m-footer__main {
    grid-template-columns: 1fr 1fr;
    gap: 32px;
  }
  .m-footer__col--sub {
    grid-column: 1 / -1;
  }
}
</style>
