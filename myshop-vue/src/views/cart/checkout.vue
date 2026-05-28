<template>
  <div>
    <myhead></myhead>
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css" />
    <div class="checkout-page">
      <div class="checkout-container">
        <!-- ====== 左侧：信息区 ====== -->
        <div class="checkout-main">
          <!-- ① 收货人信息 -->
          <div class="checkout-card">
            <div class="card-header">
              <h3 class="card-title">收货人信息</h3>
              <a href="#" class="card-action">管理收货地址</a>
            </div>
            <div class="card-body address-body">
              <div class="address-item">
                <span class="address-label">收货人</span>
                <span class="address-value">{{ contact_name }}</span>
              </div>
              <div class="address-item">
                <span class="address-label">手机号</span>
                <span class="address-value">{{ contact_mobile }}</span>
              </div>
              <div class="address-item">
                <span class="address-label">收货地址</span>
                <span class="address-value">{{ address }}</span>
              </div>
            </div>
          </div>

          <!-- ② 配送方式 -->
          <div class="checkout-card">
            <div class="card-header">
              <h3 class="card-title">配送方式</h3>
            </div>
            <div class="card-body">
              <div
                class="ship-option"
                :class="{ 'ship-option--active': ship_method === '3' }"
                @click="ship_method = '3'"
              >
                <input
                  name="shipping"
                  type="radio"
                  value="3"
                  v-model="ship_method"
                />
                <span class="ship-option__content">
                  <span class="ship-option__name">全场包邮</span>
                  <span class="ship-option__price">免费</span>
                </span>
              </div>
              <div
                class="ship-option"
                :class="{ 'ship-option--active': ship_method === '5' }"
                @click="ship_method = '5'"
              >
                <input
                  name="shipping"
                  type="radio"
                  value="5"
                  v-model="ship_method"
                />
                <span class="ship-option__content">
                  <span class="ship-option__name">顺丰速运</span>
                  <span class="ship-option__price">¥23.00</span>
                </span>
              </div>
              <div
                class="ship-option"
                :class="{ 'ship-option--active': ship_method === '4' }"
                @click="ship_method = '4'"
              >
                <input
                  name="shipping"
                  type="radio"
                  value="4"
                  v-model="ship_method"
                />
                <span class="ship-option__content">
                  <span class="ship-option__name">圆通速递</span>
                  <span class="ship-option__price">¥18.00</span>
                </span>
              </div>
            </div>
          </div>

          <!-- ③ 支付方式 -->
          <div class="checkout-card">
            <div class="card-header">
              <h3 class="card-title">支付方式</h3>
            </div>
            <div class="card-body pay-body">
              <div
                class="pay-option"
                :class="{ 'pay-option--active': pay_method === '1' }"
                @click="pay_method = '1'"
              >
                <input
                  type="radio"
                  name="payment"
                  value="1"
                  v-model="pay_method"
                  id="pay_check_value_1"
                />
                <span class="pay-option__icon pay-option__icon--alipay">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <rect x="2" y="4" width="20" height="16" rx="3" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M8 12h8M8 15h5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                  </svg>
                </span>
                <span class="pay-option__name">支付宝</span>
              </div>
              <div
                class="pay-option"
                :class="{ 'pay-option--active': pay_method === '2' }"
                @click="pay_method = '2'"
              >
                <input
                  type="radio"
                  name="payment"
                  value="2"
                  v-model="pay_method"
                  id="pay_check_value_2"
                />
                <span class="pay-option__icon pay-option__icon--wechat">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <rect x="2" y="4" width="20" height="16" rx="3" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M7 11c0 1.5 1 2.5 2.5 2.5S12 12.5 12 11s-1-2.5-2.5-2.5S7 9.5 7 11zM12 11c0 1.5 1 2.5 2.5 2.5S17 12.5 17 11s-1-2.5-2.5-2.5S12 9.5 12 11z" stroke="currentColor" stroke-width="1"/>
                  </svg>
                </span>
                <span class="pay-option__name">微信支付</span>
              </div>
            </div>
          </div>

          <!-- ④ 订单备注 -->
          <div class="checkout-card">
            <div class="card-header">
              <h3 class="card-title">订单备注</h3>
            </div>
            <div class="card-body">
              <div class="memo-wrapper">
                <textarea
                  name="postscript"
                  id="postscript"
                  v-model="memo"
                  class="memo-textarea"
                  placeholder="选填：请告诉我们您的特殊需求"
                  maxlength="200"
                  rows="3"
                ></textarea>
                <span class="memo-count">{{ memo.length }}/200</span>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== 右侧：结算栏 ====== -->
        <aside class="checkout-sidebar">
          <div class="sidebar-card">
            <div class="sidebar-card__header">
              <h3 class="sidebar-card__title">订单摘要</h3>
              <router-link to="/cart" class="sidebar-card__edit">编辑购物车</router-link>
            </div>

            <!-- 商品列表 -->
            <div class="sidebar-goods">
              <div
                class="sidebar-goods__item"
                v-for="item in cart_lists"
                :key="item.goods.id"
              >
                <img
                  class="sidebar-goods__thumb"
                  :src="item.goods.main_img"
                  :alt="item.goods.name"
                />
                <div class="sidebar-goods__info">
                  <p class="sidebar-goods__name">{{ item.goods.name }}</p>
                  <p class="sidebar-goods__meta">
                    <span>¥{{ item.goods.price }}</span>
                    <span>× {{ item.goods_num }}</span>
                  </p>
                </div>
                <p class="sidebar-goods__subtotal">
                  ¥{{ item.goods.price * item.goods_num }}
                </p>
              </div>
            </div>

            <!-- 费用明细 -->
            <div class="sidebar-totals">
              <div class="sidebar-totals__row">
                <span class="sidebar-totals__label">商品总价</span>
                <span class="sidebar-totals__value">¥{{ totalPrice }}</span>
              </div>
              <div class="sidebar-totals__row">
                <span class="sidebar-totals__label">运费</span>
                <span
                  class="sidebar-totals__value"
                  :class="{ 'sidebar-totals__value--free': shipCost === 0 }"
                >
                  {{ shipCost === 0 ? '包邮' : '¥' + shipCost.toFixed(2) }}
                </span>
              </div>
              <div class="sidebar-totals__row">
                <span class="sidebar-totals__label">优惠券</span>
                <span class="sidebar-totals__value">暂无</span>
              </div>
              <div class="sidebar-totals__divider"></div>
              <div class="sidebar-totals__row sidebar-totals__row--total">
                <span class="sidebar-totals__label">应付总额</span>
                <span class="sidebar-totals__value sidebar-totals__value--total">
                  ¥{{ orderTotal.toFixed(2) }}
                </span>
              </div>
            </div>

            <!-- 提交按钮 -->
            <button
              class="sidebar-submit"
              type="button"
              @click="submit_order"
            >
              提交订单
            </button>
          </div>
        </aside>
      </div>
    </div>
    <myfooter></myfooter>
  </div>
</template>
<script>
import myhead from "@/views/app/head";
import myfooter from "@/views/app/footer";
import { mapGetters } from "vuex";
import { addOrder, payOrder } from "@/api/order";
import { getAddress } from "@/api/basic";
export default {
  data() {
    return {
      address_lists: {},
      address: "2222",
      contact_name: "张三",
      contact_mobile: "111111",
      memo: "",
      pay_method: "1",
      ship_method: "3",
    };
  },
  computed: {
    ...mapGetters({
      userinfo: "userinfo",
      cart_lists: "cart_lists",
      totalNum: "totalNum",
      totalPrice: "totalPrice",
    }),
    shipCost() {
      const map = { "3": 0, "4": 18, "5": 23 };
      return map[this.ship_method] || 0;
    },
    orderTotal() {
      return (parseFloat(this.totalPrice) || 0) + this.shipCost;
    },
  },
  methods: {
    submit_order() {
      addOrder({
        contact_name: this.contact_name,
        contact_mobile: this.contact_mobile,
        memo: this.memo,
        address: this.address,
        pay_method: this.pay_method,
      })
        .then((response) => {
          if (response.data.code != "200") {
            alert(response.data.msg);
            return;
          }
          const orderId = response.data.data.id;
          return payOrder(orderId)
            .then((payResponse) => {
              alert(payResponse.data.msg || "支付成功");
              this.$store.dispatch("saveCart");
              this.$router.push({ path: "/myorder" });
            })
            .catch((error) => {
              console.log(error);
              const message = error && error.msg ? error.msg : "支付失败，请稍后在我的订单中继续支付";
              alert(message);
              this.$router.push({ path: "/myorder" });
            });
        })
        .catch((error) => {
          console.log(error);
          alert("订单提交失败，请稍后再试");
        });
    },
    getAddressData() {
      getAddress()
        .then((response) => {
          console.log(response.data);
          if (response.status === 200) {
            this.address_lists = response.data.data;
            if (!this.address_lists.length) {
              alert("请先维护收货地址");
              return;
            }
            this.address =
              this.address_lists[0].province +
              this.address_lists[0].city +
              this.address_lists[0].district +
              this.address_lists[0].address;
            this.contact_name = this.address_lists[0].contact_name;
            this.contact_mobile = this.address_lists[0].contact_mobile;
          }
        })
        .catch(function (error) {
          console.log(error);
        });
    },
  },
  components: {
    myhead,
    myfooter,
  },
  created() {
    this.getAddressData();
  },
};
</script>
<style scoped>
/* ===== 页面容器 ===== */
.checkout-page {
  background: #faf7f1;
  min-height: 100vh;
  padding-bottom: 60px;
}

.checkout-container {
  max-width: 1200px;
  margin: 24px auto 0;
  padding: 0 16px;
  display: flex;
  gap: 24px;
  align-items: flex-start;
}

/* ===== 左侧主区域 ===== */
.checkout-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* ===== 卡片 ===== */
.checkout-card {
  background: #fff;
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ece6dc;
}

.card-title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 16px;
  font-weight: 600;
  color: #2b2622;
  margin: 0;
  letter-spacing: 0.5px;
}

.card-action {
  font-size: 13px;
  color: #b23a2e;
  text-decoration: none;
  transition: opacity 150ms ease-out;
}

.card-action:hover {
  opacity: 0.8;
}

/* ===== 收货地址 ===== */
.address-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.address-item {
  display: flex;
  align-items: baseline;
  line-height: 1.6;
}

.address-label {
  flex-shrink: 0;
  width: 72px;
  font-size: 13px;
  color: #6e665e;
}

.address-value {
  font-size: 14px;
  color: #2b2622;
}

/* ===== 配送方式 ===== */
.ship-option {
  display: flex;
  align-items: center;
  padding: 12px 14px;
  border: 1px solid #ece6dc;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 150ms ease-out, background-color 150ms ease-out;
  margin-bottom: 8px;
}

.ship-option:last-child {
  margin-bottom: 0;
}

.ship-option:hover {
  border-color: #d8cdb9;
}

.ship-option input[type="radio"] {
  accent-color: #b23a2e;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.ship-option--active {
  border-color: #b23a2e;
  background: #fef9f8;
}

.ship-option--disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ship-option--disabled:hover {
  border-color: #ece6dc;
}

.ship-option__content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex: 1;
  margin-left: 10px;
}

.ship-option__name {
  font-size: 14px;
  color: #2b2622;
}

.ship-option__price {
  font-size: 13px;
  color: #6e665e;
}

/* ===== 支付方式 ===== */
.pay-body {
  display: flex;
  gap: 12px;
}

.pay-option {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 16px;
  border: 1px solid #ece6dc;
  border-radius: 8px;
  cursor: pointer;
  transition: border-color 150ms ease-out, background-color 150ms ease-out;
}

.pay-option:hover {
  border-color: #d8cdb9;
}

.pay-option input[type="radio"] {
  accent-color: #b23a2e;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.pay-option--active {
  border-color: #b23a2e;
  background: #fef9f8;
}

.pay-option__icon {
  display: flex;
  align-items: center;
  color: #6e665e;
}

.pay-option--active .pay-option__icon--alipay {
  color: #1677ff;
}

.pay-option--active .pay-option__icon--wechat {
  color: #07c160;
}

.pay-option__name {
  font-size: 14px;
  color: #2b2622;
  font-weight: 500;
}

/* ===== 备注 ===== */
.memo-wrapper {
  position: relative;
}

.memo-textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #ece6dc;
  border-radius: 8px;
  font-size: 14px;
  line-height: 1.6;
  color: #2b2622;
  background: #fafafa;
  resize: vertical;
  box-sizing: border-box;
  font-family: inherit;
  transition: border-color 150ms ease-out;
}

.memo-textarea:focus {
  border-color: #b23a2e;
  background: #fff;
  outline: none;
}

.memo-textarea::placeholder {
  color: #a89f94;
}

.memo-count {
  position: absolute;
  right: 10px;
  bottom: 8px;
  font-size: 12px;
  color: #a89f94;
}

/* ===== 右侧结算栏 ===== */
.checkout-sidebar {
  width: 380px;
  flex-shrink: 0;
  position: sticky;
  top: 20px;
}

.sidebar-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.sidebar-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #ece6dc;
}

.sidebar-card__title {
  font-family: "Noto Serif SC", "Songti SC", "STSong", serif;
  font-size: 16px;
  font-weight: 600;
  color: #2b2622;
  margin: 0;
  letter-spacing: 0.5px;
}

.sidebar-card__edit {
  font-size: 13px;
  color: #6e665e;
  text-decoration: none;
  transition: color 150ms ease-out;
}

.sidebar-card__edit:hover {
  color: #b23a2e;
}

/* ===== 侧栏商品列表 ===== */
.sidebar-goods {
  max-height: 300px;
  overflow-y: auto;
  margin-bottom: 16px;
}

.sidebar-goods::-webkit-scrollbar {
  width: 4px;
}

.sidebar-goods::-webkit-scrollbar-thumb {
  background: #ece6dc;
  border-radius: 2px;
}

.sidebar-goods__item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed #ece6dc;
}

.sidebar-goods__item:last-child {
  border-bottom: 0;
}

.sidebar-goods__thumb {
  width: 56px;
  height: 56px;
  border-radius: 8px;
  object-fit: cover;
  flex-shrink: 0;
  background: #faf7f1;
}

.sidebar-goods__info {
  flex: 1;
  min-width: 0;
}

.sidebar-goods__name {
  font-size: 13px;
  color: #2b2622;
  margin: 0 0 4px;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.sidebar-goods__meta {
  font-size: 12px;
  color: #6e665e;
  margin: 0;
}

.sidebar-goods__meta span + span {
  margin-left: 8px;
}

.sidebar-goods__subtotal {
  font-size: 14px;
  font-weight: 600;
  color: #2b2622;
  margin: 0;
  flex-shrink: 0;
}

/* ===== 费用明细 ===== */
.sidebar-totals__row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 0;
}

.sidebar-totals__label {
  font-size: 13px;
  color: #6e665e;
}

.sidebar-totals__value {
  font-size: 14px;
  color: #2b2622;
}

.sidebar-totals__value--free {
  color: #23a052;
}

.sidebar-totals__divider {
  height: 1px;
  background: #ece6dc;
  margin: 8px 0;
}

.sidebar-totals__row--total {
  padding: 4px 0 0;
}

.sidebar-totals__value--total {
  font-size: 22px;
  font-weight: 700;
  color: #b23a2e;
}

/* ===== 提交按钮 ===== */
.sidebar-submit {
  display: block;
  width: 100%;
  margin-top: 20px;
  padding: 14px 0;
  background: #b23a2e;
  color: #fff;
  border: 0;
  border-radius: 8px;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background-color 150ms ease-out, transform 150ms ease-out;
}

.sidebar-submit:hover {
  background: #993023;
}

.sidebar-submit:active {
  background: #993023;
  transform: scale(0.98);
}

.sidebar-submit:focus-visible {
  outline: 2px solid #b23a2e;
  outline-offset: 2px;
}

/* ===== 响应式：窄屏堆叠 ===== */
@media (max-width: 860px) {
  .checkout-container {
    flex-direction: column;
  }

  .checkout-sidebar {
    width: 100%;
    position: static;
  }

  .pay-body {
    flex-direction: column;
  }
}
</style>
