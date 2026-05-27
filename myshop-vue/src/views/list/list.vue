<template>
  <div>
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
    <link
      href="../../static/css/category.css"
      rel="stylesheet"
      type="text/css"
    />
    <myhead></myhead>
    <div id="wrapper">
      <div class="here cle">
        <a href=".">首页</a> <code>&gt;</code>
        <router-link :to="id">{{ curr_cate_name }}</router-link>
      </div>
      <div class="main cle">
        <listcategory
          :sub_cat="sub_cat"
          :categoryname="curr_cate_name"
        ></listcategory>

        <div class="maincon">
          <div class="search-options" id="search-options">
            <div class="bd">
              <dl>
                <dt>价格：</dt>
                <dd class="dd-price">
                  <div class="items cle w500">
                    <div class="link">
                      <a @click="query_price(10, 60)" class="item"
                        >10&nbsp;-&nbsp;60</a
                      >
                    </div>
                    <div class="link">
                      <a @click="query_price(60, 110)" class="item"
                        >60&nbsp;-&nbsp;110</a
                      >
                    </div>
                    <div class="link">
                      <a @click="query_price(110, 160)" class="item"
                        >110&nbsp;-&nbsp;160</a
                      >
                    </div>
                    <div class="link">
                      <a @click="query_price(160, 210)" class="item"
                        >160&nbsp;-&nbsp;210</a
                      >
                    </div>
                  </div>
                  <div class="priceform" id="priceform">
                    <div class="form-bg">
                      <form action="#" method="post" id="freepriceform">
                        <span class="rmb"></span>
                        <input
                          type="text"
                          value=""
                          name="price_min"
                          id="pricemin"
                          v-model="min_price"
                        />
                        <span class="rmb rmb2"></span>
                        <input
                          type="text"
                          value=""
                          name="price_max"
                          id="pricemax"
                          v-model="max_price"
                        />
                        <input
                          type="button"
                          value="确定"
                          @click="query_price(min_price, max_price)"
                          class="submit"
                        />
                      </form>
                    </div>
                  </div>
                </dd>
              </dl>
            </div>
          </div>

          <div class="sort">
            <div class="bd">
              <form method="GET" name="listform">
                <a
                  title="销量"
                  class="curr"
                  rel="nofollow"
                  @click="sort_amount(type1)"
                  ><span
                    :class="type1 == '-amount' ? 'search_DESC' : 'search_ASC'"
                    >销量</span
                  ></a
                >
                <a
                  title="价格"
                  class="curr"
                  rel="nofollow"
                  @click="sort_price(type2)"
                  ><span
                    :class="type2 == '-price' ? 'search_DESC' : 'search_ASC'"
                    >价格</span
                  ></a
                >
              </form>
            </div>
          </div>
          <div class="productlist">
            <ul class="cle" v-if="list_data.length">
              <li v-for="item in list_data" :key="item.id">
                <router-link
                  :to="'/detail/' + item.id"
                  target="_blank"
                  class="productitem"
                >
                  <span class="productimg">
                    <img
                      width="150"
                      height="150"
                      :title="item.name"
                      :alt="item.name"
                      :src="item.main_img"
                      style="display: block"
                    />
                  </span>
                  <span class="nalaprice xszk">
                    <b> ￥{{ item.price }}元 </b>
                  </span>
                  <span class="productname">{{ item.name }}</span>
                  <span class="salerow">
                    销量：<span class="sales">{{ item.amount }}</span
                    >件
                  </span>
                </router-link>
              </li>
            </ul>
            <div v-else class="empty-result">暂无符合条件的商品</div>
            <br clear="all" />
          </div>
          <mypage :total_page="total_page" @get_page="get_page"> </mypage>
        </div>
      </div>
    </div>
    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from "@/views/app/head.vue";
import myfooter from "@/views/app/footer.vue";
import { getGoods, getGoodsCategoryByID } from "@/api/goods";
//左侧菜单导航
import listcategory from "@/views/list/listcategory.vue";
import mypage from "@/views/list/page.vue";
export default {
  data() {
    return {
      sub_cat: [],
      curr_cate_name: "",
      id: "",
      list_data: [],
      goodsnum: 0,
      ordering: "-amount",
      curr_page: 1,
      type1: "-amount",
      type2: "-price",
      min_price: "",
      max_price: "",
    };
  },
  components: {
    myhead,
    myfooter,
    listcategory: listcategory,
    mypage: mypage,
  },
  methods: {
    getAllCategory() {
      this.id = this.$route.params.id;
      if (this.id && this.id !== "0") {
        getGoodsCategoryByID(this.id).then((response) => {
          this.sub_cat = response.data.data.sub_cat;
          this.curr_cate_name = response.data.data.name;
        });
      } else {
        this.sub_cat = [];
        this.curr_cate_name = this.$route.query.keyword
          ? "搜索结果"
          : "全部商品";
      }
    },
    getlistData() {
      const params = {
        min_price: this.min_price,
        max_price: this.max_price,
        ordering: this.ordering,
        page: this.curr_page,
      };
      if (this.$route.params.id && this.$route.params.id !== "0") {
        params.category = this.$route.params.id;
      }
      const keyword = this.$route.query.keyword;
      if (keyword) {
        params.name = keyword;
        params.search = keyword;
      }
      getGoods(params).then((response) => {
        this.list_data = response.data.data;
        this.goodsnum = response.data.count;
      });
    },
    sort_amount(type) {
      type == "-amount" ? (this.type1 = "amount") : (this.type1 = "-amount");
      this.ordering = type;
      this.getlistData();
    },
    sort_price(type) {
      type == "-price" ? (this.type2 = "price") : (this.type2 = "-price");
      this.ordering = type;
      this.getlistData();
    },
    get_page(data) {
      this.curr_page = data.curr_page;
      this.getlistData();
    },
    query_price(min_price, max_price) {
      this.min_price = min_price;
      this.max_price = max_price;
      this.getlistData();
    },
  },
  computed: {
    total_page() {
      return Math.ceil(this.goodsnum / 8);
    },
  },
  watch: {
    $route() {
      this.curr_page = 1;
      this.getAllCategory();
      this.getlistData();
    },
  },
  created() {
    this.getAllCategory(); //获取当前分类下的子分类
    this.getlistData(); //根据条件获取商品信息
  },
};
</script>
