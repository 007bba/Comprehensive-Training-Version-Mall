<template>
<div>
  <myhead></myhead>
  <div id="wrapper" class="cle">
    <link href="../../static/css/style.css" rel="stylesheet" type="text/css">
    <div class="here cle"><a href="#">首页</a> <code>&gt;</code> 用户中心</div>

    <div class="my_nala_main">

      <left></left>

      <div class="my_nala_centre ilizi_centre">
        <div class="ilizi cle">
          <div class="box">
            <div class="box_1">
              <div class="userCenterBox boxCenterList clearfix" style="_height:1%;">

                <h5><span>我的订单</span></h5>
                <div class="blank"></div>
                <table width="100%" height="200px" border="1" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
                  <tbody>
                    <tr align="center">
                      <td bgcolor="#ffffff">订单号</td>
                      <td bgcolor="#ffffff">下单时间</td>
                      <td bgcolor="#ffffff">订单总金额</td>
                      <td bgcolor="#ffffff">订单状态</td>
                      <td bgcolor="#ffffff">操作</td>
                    </tr>
                    <tr v-for="item in order_lists">
                      <td align="center" bgcolor="#ffffff">
                        <a class="f6">{{item.order_sn}}</a>
                      </td>
                      <td align="center" bgcolor="#ffffff">{{item.create_date}}</td>
                      <td align="right" bgcolor="#ffffff">￥{{item.order_price}}元</td>
                      <td align="center" bgcolor="#ffffff">{{ getOrderStateText(item.order_state) }}</td>
                      <td align="center" bgcolor="#ffffff">
                        <font class="f6">
                          <a v-if="item.order_state === 'paying'" @click="pay(item)">
                            模拟支付
                          </a>
                          <span v-else>-</span>
                        </font>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div class="blank5"></div>

                <div class="blank5"></div>

              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
<myfooter></myfooter>
</div>
</template>
<script>
import myhead from '@/views/app/head';
import myfooter from '@/views/app/footer';
  import left from '@/views/user/left';
  import { getOrder, payOrder } from '@/api/order'
  export default {
    data() {
      return {
        order_lists: []
      };
    },
    methods: {
      getData() {
        getOrder({}).then((response) => {
          console.log(response.data);
          if (response.status === 200) {
            this.order_lists = response.data.data;
          }
        }).catch(function (error) {
          console.log(error);
        })
      },
      getOrderStateText(state) {
        const stateMap = {
          paying: "待支付",
          payed: "已支付/待发货",
          shipping: "配送中",
          complete: "已完成",
          cancel: "已取消",
        };
        return stateMap[state] || state;
      },
      pay(item) {
        payOrder(item.id).then((response) => {
          alert(response.data.msg || "支付成功");
          this.getData();
        }).catch(function (error) {
          console.log(error);
          const message = error && error.msg ? error.msg : "支付失败，请稍后再试";
          alert(message);
        })
      },
    },
      components: {
      myhead,
      myfooter,
      left,
    },
    created() {
      this.getData();
    }
  };
</script>
<style scoped>
  @import "../../static/css/user.css";
</style>
