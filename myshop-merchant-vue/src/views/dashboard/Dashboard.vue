<template>
  <div>
    <el-row :gutter="20" style="margin-bottom:20px">
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total_sales || 0 }}</div>
            <div class="stat-label">总销售额(元)</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total_orders || 0 }}</div>
            <div class="stat-label">总订单数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total_goods || 0 }}</div>
            <div class="stat-label">在售商品数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <div class="stat-card">
            <div class="stat-value">{{ stats.total_stock || 0 }}</div>
            <div class="stat-label">总库存</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-card>
      <div slot="header">快捷入口</div>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-button type="primary" style="width:100%" @click="$router.push('/goods/add')">新增商品</el-button>
        </el-col>
        <el-col :span="8">
          <el-button type="success" style="width:100%" @click="$router.push('/orders')">查看订单</el-button>
        </el-col>
        <el-col :span="8">
          <el-button type="warning" style="width:100%" @click="$router.push('/shop')">店铺设置</el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { getStats } from '@/api/merchant'

export default {
  name: 'Dashboard',
  data() {
    return { stats: {} }
  },
  created() {
    this.fetchStats()
  },
  methods: {
    async fetchStats() {
      try {
        const res = await getStats()
        this.stats = res.data || {}
      } catch (e) {}
    }
  }
}
</script>

<style scoped>
.stat-card { text-align: center; padding: 10px 0; }
.stat-value { font-size: 28px; font-weight: bold; color: #409EFF; }
.stat-label { font-size: 14px; color: #999; margin-top: 8px; }
</style>
