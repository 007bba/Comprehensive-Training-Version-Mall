<template>
  <div>
    <el-card>
      <div slot="header">{{ isEdit ? '编辑商品' : '新增商品' }}</div>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px" style="max-width:600px">
        <el-form-item label="商品名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入商品名称" />
        </el-form-item>
        <el-form-item label="商品分类" prop="category">
          <el-cascader
            v-model="form.categoryPath"
            :options="categoryTree"
            :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true }"
            placeholder="请选择分类"
            clearable
            style="width:100%"
            @change="handleCategoryChange"
          />
        </el-form-item>
        <el-form-item label="市场价" prop="market_price">
          <el-input-number v-model="form.market_price" :min="0" :precision="2" style="width:100%" />
        </el-form-item>
        <el-form-item label="实际价格" prop="price">
          <el-input-number v-model="form.price" :min="0" :precision="2" style="width:100%" />
        </el-form-item>
        <el-form-item label="计量单位" prop="unit">
          <el-input v-model="form.unit" placeholder="如：个、斤、包" />
        </el-form-item>
        <el-form-item label="库存数" prop="stock_num">
          <el-input-number v-model="form.stock_num" :min="0" style="width:100%" />
        </el-form-item>
        <el-form-item label="是否推荐">
          <el-switch v-model="form.is_recommend" />
        </el-form-item>
        <el-form-item label="商品主图">
          <el-input v-model="form.main_img" placeholder="图片路径，如 /media/goods/images/xxx.jpg" />
        </el-form-item>
        <el-form-item label="商品详情" prop="goods_desc">
          <el-input v-model="form.goods_desc" type="textarea" :rows="6" placeholder="请输入商品详情" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleSubmit">保存</el-button>
          <el-button @click="$router.back()">返回</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { getGoodsDetail, createGoods, updateGoods, getCategories } from '@/api/merchant'

export default {
  name: 'GoodsEdit',
  data() {
    return {
      loading: false,
      categoryTree: [],
      allCategories: [],
      form: {
        name: '',
        category: '',
        categoryPath: [],
        market_price: 0,
        price: 0,
        unit: '',
        stock_num: 0,
        is_recommend: false,
        main_img: '',
        goods_desc: ''
      },
      rules: {
        name: [{ required: true, message: '请输入商品名称', trigger: 'blur' }],
        category: [{ required: true, message: '请选择分类', trigger: 'change' }],
        price: [{ required: true, message: '请输入价格', trigger: 'blur' }]
      }
    }
  },
  computed: {
    isEdit() {
      return this.$route.name === 'GoodsEdit'
    }
  },
  created() {
    this.fetchCategories()
    if (this.isEdit) {
      this.fetchGoodsDetail()
    }
  },
  methods: {
    buildCategoryTree(list) {
      // 构建父子树形结构
      const map = {}
      const tree = []
      list.forEach(item => {
        map[item.id] = { id: item.id, name: item.name, parent: item.parent, children: [] }
      })
      list.forEach(item => {
        if (item.parent && map[item.parent]) {
          map[item.parent].children.push(map[item.id])
        } else {
          tree.push(map[item.id])
        }
      })
      // 移除空的 children 数组（叶子节点不需要展开箭头）
      function clean(nodes) {
        nodes.forEach(n => {
          if (n.children.length === 0) delete n.children
          else clean(n.children)
        })
      }
      clean(tree)
      return tree
    },
    getCategoryPath(categoryId) {
      // 根据分类ID找到从根到该分类的路径
      const path = []
      let current = this.allCategories.find(c => c.id === categoryId)
      while (current) {
        path.unshift(current.id)
        current = current.parent
          ? this.allCategories.find(c => c.id === current.parent)
          : null
      }
      return path
    },
    handleCategoryChange(value) {
      // 级联选择器改变时，取最后一级作为分类ID
      this.form.category = value.length > 0 ? value[value.length - 1] : ''
    },
    async fetchCategories() {
      try {
        const res = await getCategories()
        const list = res.results || res.data || res || []
        this.allCategories = list
        this.categoryTree = this.buildCategoryTree(list)
      } catch (e) {
        console.error('获取分类失败', e)
      }
    },
    async fetchGoodsDetail() {
      try {
        const res = await getGoodsDetail(this.$route.params.id)
        const data = res.data || res
        this.form = {
          name: data.name,
          category: data.category,
          categoryPath: this.getCategoryPath(data.category),
          market_price: Number(data.market_price),
          price: Number(data.price),
          unit: data.unit || '',
          stock_num: data.stock_num,
          is_recommend: data.is_recommend,
          main_img: data.main_img || '',
          goods_desc: data.goods_desc || ''
        }
      } catch (e) {
        console.error('获取商品详情失败', e)
      }
    },
    handleSubmit() {
      this.$refs.form.validate(async valid => {
        if (!valid) return
        this.loading = true
        try {
          const submitData = { ...this.form }
          delete submitData.categoryPath
          if (this.isEdit) {
            await updateGoods(this.$route.params.id, submitData)
            this.$message.success('修改成功')
          } else {
            await createGoods(submitData)
            this.$message.success('新增成功')
          }
          this.$router.push('/goods')
        } catch (e) {
          console.error('保存失败', e)
        } finally {
          this.loading = false
        }
      })
    }
  }
}
</script>
