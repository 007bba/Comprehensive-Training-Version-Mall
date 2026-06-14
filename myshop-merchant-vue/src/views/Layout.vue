<template>
  <el-container style="height: 100vh">
    <el-aside width="220px" style="background-color: #304156">
      <div class="logo">商家管理中心</div>
      <el-menu
        :default-active="activeMenu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/dashboard">
          <i class="el-icon-data-board"></i>
          <span>数据概览</span>
        </el-menu-item>
        <el-menu-item index="/goods">
          <i class="el-icon-goods"></i>
          <span>商品管理</span>
        </el-menu-item>
        <el-menu-item index="/orders">
          <i class="el-icon-document"></i>
          <span>订单管理</span>
        </el-menu-item>
        <el-menu-item index="/shop">
          <i class="el-icon-shop"></i>
          <span>店铺信息</span>
        </el-menu-item>
        <el-menu-item index="/stats">
          <i class="el-icon-data-analysis"></i>
          <span>数据统计</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="display:flex;align-items:center;justify-content:space-between;background:#fff;border-bottom:1px solid #eee">
        <span style="font-size:18px;font-weight:bold">{{ $route.meta.title || '商家管理中心' }}</span>
        <div>
          <span style="margin-right:16px">{{ user ? user.username : '' }}</span>
          <el-button type="text" @click="handleLogout">退出登录</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'Layout',
  computed: {
    user() {
      return this.$store.state.user
    },
    activeMenu() {
      // 取路由的第一段作为菜单高亮 key，例如 /goods/add → /goods
      const path = this.$route.path
      const match = path.match(/^\/[^/]+/)
      return match ? match[0] : path
    }
  },
  methods: {
    handleLogout() {
      this.$store.dispatch('logout')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background-color: #263445;
}
.el-menu {
  border-right: none;
}
</style>
