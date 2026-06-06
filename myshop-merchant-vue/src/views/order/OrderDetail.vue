<template>
  <div v-loading="loading">
    <el-card v-if="order">
      <div slot="header">
        <el-button icon="el-icon-arrow-left" @click="$router.back()">返回</el-button>
        订单详情
      </div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单号">{{ order.order_sn }}</el-descriptions-item>
        <el-descriptions-item label="买家">{{ order.username }}</el-descriptions-item>
        <el-descriptions-item label="订单状态">
          <el-tag :type="stateTagType(order.order_state)">{{ stateText(order.order_state) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="订单金额">{{ order.order_price }} 元</el-descriptions-item>
        <el-descriptions-item label="商品数量">{{ order.order_total }}</el-descriptions-item>
        <el-descriptions-item label="支付方式">{{ order.pay_method === 0 ? '未支付' : '在线支付' }}</el-descriptions-item>
        <el-descriptions-item label="收货地址">{{ order.address }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ order.contact_name }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ order.contact_mobile }}</el-descriptions-item>
        <el-descriptions-item label="订单备注">{{ order.memo || '无' }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ order.create_date }}</el-descriptions-item>
      </el-descriptions>

      <h4 style="margin:20px 0 10px">商品明细</h4>
      <el-table :data="order.order_goods || []" border>
        <el-table-column prop="goods_name" label="商品名称" />
        <el-table-column prop="goods_img" label="图片" width="100">
          <template slot-scope="{ row }">
            <el-image v-if="row.goods_img" :src="row.goods_img" style="width:50px;height:50px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column prop="price" label="单价" width="100" />
        <el-table-column prop="goods_num" label="数量" width="80" />
      </el-table>

      <div style="margin-top:20px" v-if="order.order_state === 'payed'">
        <el-button type="primary" @click="handleShip">确认发货</el-button>
      </div>
      <div style="margin-top:20px" v-if="order.order_state === 'shipping'">
        <el-button type="success" @click="handleComplete">确认完成</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { getOrderDetail, shipOrder, completeOrder } from '@/api/merchant'

export default {
  name: 'OrderDetail',
  data() {
    return { order: null, loading: false }
  },
  created() {
    this.fetchOrder()
  },
  methods: {
    stateText(state) {
      const map = { paying: '待支付', payed: '已支付', shipping: '配送中', complete: '已完成', cancel: '已取消' }
      return map[state] || state
    },
    stateTagType(state) {
      const map = { paying: 'warning', payed: '', shipping: '', complete: 'success', cancel: 'info' }
      return map[state] || ''
    },
    async fetchOrder() {
      this.loading = true
      try {
        const res = await getOrderDetail(this.$route.params.id)
        this.order = res.data || res
      } catch (e) {} finally {
        this.loading = false
      }
    },
    async handleShip() {
      try {
        await shipOrder(this.$route.params.id)
        this.$message.success('发货成功')
        this.fetchOrder()
      } catch (e) {}
    },
    async handleComplete() {
      try {
        await completeOrder(this.$route.params.id)
        this.$message.success('订单已完成')
        this.fetchOrder()
      } catch (e) {}
    }
  }
}
</script>
