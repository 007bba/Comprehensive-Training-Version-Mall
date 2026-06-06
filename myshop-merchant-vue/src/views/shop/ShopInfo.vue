<template>
  <div>
    <el-card v-if="!hasShop">
      <div slot="header">创建店铺</div>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px" style="max-width:500px">
        <el-form-item label="店铺名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入店铺名称" />
        </el-form-item>
        <el-form-item label="店铺Logo">
          <el-input v-model="form.logo" placeholder="Logo图片路径" />
        </el-form-item>
        <el-form-item label="店铺描述">
          <el-input v-model="form.desc" type="textarea" :rows="4" placeholder="请输入店铺描述" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleCreate">创建店铺</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card v-else>
      <div slot="header">店铺信息</div>
      <el-form :model="shop" label-width="100px" style="max-width:500px">
        <el-form-item label="店铺名称">
          <el-input v-model="shop.name" />
        </el-form-item>
        <el-form-item label="店铺Logo">
          <el-image v-if="shop.logo" :src="shop.logo" style="width:100px;height:100px" fit="cover" />
          <el-input v-model="shop.logo" placeholder="Logo图片路径" style="margin-top:8px" />
        </el-form-item>
        <el-form-item label="店铺描述">
          <el-input v-model="shop.desc" type="textarea" :rows="4" />
        </el-form-item>
        <el-form-item label="店铺状态">
          <el-tag :type="shop.status === 0 ? 'success' : 'danger'">
            {{ shop.status === 0 ? '正常' : '关闭' }}
          </el-tag>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleUpdate">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getShop, createShop, updateShop } from '@/api/merchant'

export default {
  name: 'ShopInfo',
  data() {
    return {
      loading: false,
      hasShop: false,
      shop: {},
      form: { name: '', logo: '', desc: '' },
      rules: {
        name: [{ required: true, message: '请输入店铺名称', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.fetchShop()
  },
  methods: {
    async fetchShop() {
      try {
        const res = await getShop()
        const list = res.results || res.data || res
        if (Array.isArray(list) && list.length > 0) {
          this.shop = list[0]
          this.hasShop = true
        } else if (list && list.id) {
          this.shop = list
          this.hasShop = true
        }
      } catch (e) {}
    },
    handleCreate() {
      this.$refs.form.validate(async valid => {
        if (!valid) return
        this.loading = true
        try {
          await createShop(this.form)
          this.$message.success('店铺创建成功')
          this.fetchShop()
        } catch (e) {} finally {
          this.loading = false
        }
      })
    },
    async handleUpdate() {
      this.loading = true
      try {
        await updateShop(this.shop.id, this.shop)
        this.$message.success('修改成功')
      } catch (e) {} finally {
        this.loading = false
      }
    }
  }
}
</script>
