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
            <div class="stat-label">商品总数</div>
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
      <div slot="header">销售数据图表</div>
      <div ref="chart" style="height:400px"></div>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getStats } from '@/api/merchant'

export default {
  name: 'Stats',
  data() {
    return { stats: {}, chart: null }
  },
  created() {
    this.fetchStats()
  },
  mounted() {
    this.$nextTick(() => {
      this.chart = echarts.init(this.$refs.chart)
    })
  },
  beforeDestroy() {
    if (this.chart) this.chart.dispose()
  },
  methods: {
    async fetchStats() {
      try {
        const res = await getStats()
        this.stats = res.data || {}
        this.renderChart()
      } catch (e) {}
    },
    renderChart() {
      if (!this.chart) return
      this.chart.setOption({
        tooltip: { trigger: 'item' },
        legend: { bottom: 0 },
        series: [
          {
            name: '经营数据',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
            label: { show: true, formatter: '{b}: {c}' },
            data: [
              { value: Number(this.stats.total_sales) || 0, name: '销售额' },
              { value: this.stats.total_orders || 0, name: '订单数' },
              { value: this.stats.total_goods || 0, name: '商品数' },
              { value: this.stats.total_stock || 0, name: '库存量' }
            ]
          }
        ]
      })
    }
  }
}
</script>

<style scoped>
.stat-card { text-align: center; padding: 10px 0; }
.stat-value { font-size: 28px; font-weight: bold; color: #409EFF; }
.stat-label { font-size: 14px; color: #999; margin-top: 8px; }
</style>
