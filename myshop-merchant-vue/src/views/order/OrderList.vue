<template>
  <div>
    <div style="margin-bottom:16px;display:flex;justify-content:space-between">
      <el-select v-model="orderState" placeholder="订单状态" clearable style="width:200px" @change="handleFilterChange">
        <el-option label="待支付" value="paying" />
        <el-option label="已支付" value="payed" />
        <el-option label="配送中" value="shipping" />
        <el-option label="已完成" value="complete" />
        <el-option label="已取消" value="cancel" />
      </el-select>
    </div>

    <el-table :data="orders" border stripe v-loading="loading">
      <el-table-column prop="id" label="订单ID" width="80" />
      <el-table-column prop="order_sn" label="订单号" width="180" />
      <el-table-column prop="username" label="买家" width="120" />
      <el-table-column prop="order_total" label="商品数量" width="100" />
      <el-table-column prop="order_price" label="订单金额" width="120" />
      <el-table-column prop="order_state" label="状态" width="100">
        <template slot-scope="{ row }">
          <el-tag :type="stateTagType(row.order_state)">{{ stateText(row.order_state) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_date" label="下单时间" width="180" />
      <el-table-column label="操作" width="200" fixed="right">
        <template slot-scope="{ row }">
          <el-button size="mini" @click="$router.push('/orders/' + row.id)">详情</el-button>
          <el-button v-if="row.order_state === 'payed'" size="mini" type="primary" @click="handleShip(row)">发货</el-button>
          <el-button v-if="row.order_state === 'shipping'" size="mini" type="success" @click="handleComplete(row)">完成</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      v-if="total > 0"
      style="margin-top:16px;text-align:right"
      :current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script>
import { getOrders, shipOrder, completeOrder } from '@/api/merchant'

export default {
  name: 'OrderList',
  data() {
    return {
      orders: [],
      loading: false,
      orderState: '',
      page: 1,
      pageSize: 10,
      total: 0
    }
  },
  created() {
    this.fetchOrders()
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
    async fetchOrders() {
      this.loading = true
      try {
        const params = { page: this.page, page_size: this.pageSize }
        if (this.orderState) params.order_state = this.orderState
        const res = await getOrders(params)
        if (res.results) {
          this.orders = res.results
          this.total = res.count
        } else if (Array.isArray(res.data)) {
          this.orders = res.data
          this.total = res.data.length
        }
      } catch (e) {} finally {
        this.loading = false
      }
    },
    handlePageChange(val) {
      this.page = val
      this.fetchOrders()
    },
    handleFilterChange() {
      this.page = 1
      this.fetchOrders()
    },
    async handleShip(row) {
      try {
        await shipOrder(row.id)
        this.$message.success('发货成功')
        this.fetchOrders()
      } catch (e) {}
    },
    async handleComplete(row) {
      try {
        await completeOrder(row.id)
        this.$message.success('订单已完成')
        this.fetchOrders()
      } catch (e) {}
    }
  }
}
</script>
