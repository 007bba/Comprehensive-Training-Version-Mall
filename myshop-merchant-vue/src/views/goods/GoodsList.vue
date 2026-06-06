<template>
  <div>
    <div style="margin-bottom:16px;display:flex;justify-content:space-between">
      <el-input v-model="search" placeholder="搜索商品名称" style="width:300px" clearable @clear="fetchGoods" @keyup.enter.native="fetchGoods">
        <el-button slot="append" icon="el-icon-search" @click="fetchGoods" />
      </el-input>
      <el-button type="primary" icon="el-icon-plus" @click="$router.push('/goods/add')">新增商品</el-button>
    </div>

    <el-table :data="goodsList" border stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="main_img" label="主图" width="100">
        <template slot-scope="{ row }">
          <el-image v-if="row.main_img" :src="row.main_img" style="width:60px;height:60px" fit="cover" />
        </template>
      </el-table-column>
      <el-table-column prop="name" label="商品名称" show-overflow-tooltip />
      <el-table-column prop="category_name" label="分类" width="120" />
      <el-table-column prop="price" label="售价" width="100" />
      <el-table-column prop="market_price" label="市场价" width="100" />
      <el-table-column prop="stock_num" label="库存" width="80" />
      <el-table-column prop="amount" label="销量" width="80" />
      <el-table-column prop="status" label="状态" width="80">
        <template slot-scope="{ row }">
          <el-tag :type="row.status === 0 ? 'success' : 'info'">
            {{ row.status === 0 ? '上架' : '下架' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right">
        <template slot-scope="{ row }">
          <el-button size="mini" @click="$router.push('/goods/edit/' + row.id)">编辑</el-button>
          <el-button size="mini" :type="row.status === 0 ? 'warning' : 'success'" @click="handleToggle(row)">
            {{ row.status === 0 ? '下架' : '上架' }}
          </el-button>
          <el-button size="mini" type="danger" @click="handleDelete(row)">删除</el-button>
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
import { getGoods, deleteGoods, toggleGoodsStatus } from '@/api/merchant'

export default {
  name: 'GoodsList',
  data() {
    return {
      goodsList: [],
      loading: false,
      search: '',
      page: 1,
      pageSize: 10,
      total: 0
    }
  },
  created() {
    this.fetchGoods()
  },
  methods: {
    async fetchGoods() {
      this.loading = true
      try {
        const res = await getGoods({ page: this.page, page_size: this.pageSize, search: this.search })
        // 兼容分页和非分页返回
        if (res.results) {
          this.goodsList = res.results
          this.total = res.count
        } else if (Array.isArray(res.data)) {
          this.goodsList = res.data
          this.total = res.data.length
        }
      } catch (e) {} finally {
        this.loading = false
      }
    },
    handlePageChange(val) {
      this.page = val
      this.fetchGoods()
    },
    async handleToggle(row) {
      try {
        await toggleGoodsStatus(row.id)
        this.$message.success('操作成功')
        this.fetchGoods()
      } catch (e) {}
    },
    handleDelete(row) {
      this.$confirm('确定删除该商品吗？', '提示', { type: 'warning' }).then(async () => {
        try {
          await deleteGoods(row.id)
          this.$message.success('删除成功')
          this.fetchGoods()
        } catch (e) {}
      }).catch(() => {})
    }
  }
}
</script>
