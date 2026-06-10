<template>
  <div>
    <el-card v-if="!hasShop">
      <div slot="header">创建店铺</div>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px" style="max-width:500px">
        <el-form-item label="店铺名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入店铺名称" />
        </el-form-item>
        <el-form-item label="店铺Logo">
          <el-upload
            :action="uploadAction"
            :headers="uploadHeaders"
            :name="uploadFieldName"
            :file-list="createLogoFileList"
            :limit="1"
            accept=".jpg,.jpeg,.png"
            list-type="picture-card"
            :class="{ 'logo-upload--hidden': createLogoFileList.length >= 1 }"
            :before-upload="beforeLogoUpload"
            :on-success="handleCreateLogoSuccess"
            :on-remove="handleCreateLogoRemove"
            :on-exceed="handleLogoExceed"
            :on-error="handleLogoError"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <div class="logo-upload-tip">仅支持 JPG/PNG，大小不超过 2MB</div>
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
          <el-upload
            :action="uploadAction"
            :headers="uploadHeaders"
            :name="uploadFieldName"
            :file-list="shopLogoFileList"
            :limit="1"
            accept=".jpg,.jpeg,.png"
            list-type="picture-card"
            :class="{ 'logo-upload--hidden': shopLogoFileList.length >= 1 }"
            :before-upload="beforeLogoUpload"
            :on-success="handleShopLogoSuccess"
            :on-remove="handleShopLogoRemove"
            :on-exceed="handleLogoExceed"
            :on-error="handleLogoError"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <div class="logo-upload-tip">仅支持 JPG/PNG，大小不超过 2MB</div>
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
      uploadAction: '/merchant/upload-logo/',
      uploadFieldName: 'file',
      createLogoFileList: [],
      shopLogoFileList: [],
      rules: {
        name: [{ required: true, message: '请输入店铺名称', trigger: 'blur' }]
      }
    }
  },
  computed: {
    uploadHeaders() {
      const token = this.$store.state.token || localStorage.getItem('merchant_token')
      return token ? { Authorization: 'JWT ' + token } : {}
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
          this.shopLogoFileList = this.buildLogoFileList(this.shop.logo)
        } else if (list && list.id) {
          this.shop = list
          this.hasShop = true
          this.shopLogoFileList = this.buildLogoFileList(this.shop.logo)
        }
      } catch (e) {}
    },
    buildLogoFileList(url) {
      return url ? [{ name: '店铺Logo', url }] : []
    },
    beforeLogoUpload(file) {
      const isAllowedType = ['image/jpeg', 'image/png'].includes(file.type) || /\.(jpe?g|png)$/i.test(file.name)
      const isAllowedSize = file.size / 1024 / 1024 <= 2

      if (!isAllowedType) {
        this.$message.error('Logo 只能上传 JPG/PNG 格式')
      }
      if (!isAllowedSize) {
        this.$message.error('Logo 图片大小不能超过 2MB')
      }

      return isAllowedType && isAllowedSize
    },
    handleLogoExceed() {
      this.$message.warning('店铺 Logo 只能上传一张图片')
    },
    handleLogoError() {
      this.$message.error('Logo 上传失败，请稍后重试')
    },
    handleCreateLogoSuccess(response, file) {
      this.handleLogoSuccess('form', response, file)
    },
    handleShopLogoSuccess(response, file) {
      this.handleLogoSuccess('shop', response, file)
    },
    handleCreateLogoRemove() {
      this.handleLogoRemove('form')
    },
    handleShopLogoRemove() {
      this.handleLogoRemove('shop')
    },
    handleLogoSuccess(target, response, file) {
      if (response && response.code && response.code !== 200) {
        this.$message.error(response.msg || 'Logo 上传失败')
        this.setLogoFileList(target, [])
        return
      }

      const url = this.resolveLogoUrl(response)
      if (!url) {
        this.$message.error('上传成功，但未返回图片地址')
        this.setLogoFileList(target, [])
        return
      }

      this[target].logo = url
      this.setLogoFileList(target, [{ name: file.name || '店铺Logo', url }])
      this.$message.success('Logo 上传成功')
    },
    handleLogoRemove(target) {
      this[target].logo = ''
      this.setLogoFileList(target, [])
    },
    setLogoFileList(target, fileList) {
      if (target === 'shop') {
        this.shopLogoFileList = fileList
      } else {
        this.createLogoFileList = fileList
      }
    },
    resolveLogoUrl(response) {
      const payload = response && response.data ? response.data : response
      let url = payload && (payload.url || payload.logo || payload.path)

      if (!url && payload && payload.data) {
        url = payload.data.url || payload.data.logo || payload.data.path
      }
      if (!url) return ''
      if (/^https?:\/\//i.test(url) || url.startsWith('/')) return url

      return '/media/' + url.replace(/^\/+/, '')
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

<style scoped>
.logo-upload-tip {
  margin-top: 8px;
  color: #909399;
  font-size: 12px;
  line-height: 1;
}

.logo-upload--hidden /deep/ .el-upload--picture-card {
  display: none;
}
</style>
