from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from apps.order.models import *
from apps.order.serializers import  *
# Create your views here.
from rest_framework import viewsets, status

from common.custommodelviewset import CustomModelViewSet
from common.customresponse import CustomResponse
from common.permissions import IsOwnerOrReadOnly

from common.permissions import IsOwnerOrReadOnly


def index(request):

    return render(request,'index.html')

class CartViewset(CustomModelViewSet):
    '''
    购物车视图类
    list：
        获取购物车中的商品详情
    create：
        新增一条数据加入到购物车
    update：
        修改购物车数据
    delete：
        删除购物车数据
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CartModelSerializer
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action=="list":
            return CartDetailModelSerializer 
        else:
            return CartModelSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user) #只显示当前登录用户的购物车信息

    def perform_create(self, serializer):
        shop_cart = serializer.save()#获取购物车保存后的实例
        print(shop_cart)
        goods = shop_cart.goods #获取购物车中的商品实例
        goods.stock_num -= shop_cart.goods_num #商品库存减少
        goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods #获取购物车中的商品实例
        goods.stock_num += instance.goods_num #商品库存增加
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        #获取购物车表里的数据
        shop_cart_db = Cart.objects.get(id=serializer.instance.id)
		#获取购物车表里的商品数量
        db_nums = shop_cart_db.goods_num
        #保存购物车数据
        shop_cart = serializer.save()
		#当前购物车里的商品数量-购物车表里的商品数量
        nums = shop_cart.goods_num-db_nums
        #获取购物车中的商品实例
        goods = shop_cart.goods
        if nums>0:#如果当前购物车里的商品数量-购物车表里的商品数量>0，说明商品数量增加，因此商品库存做减少操作
            goods.stock_num -= nums
        else:
            goods.stock_num += nums #商品库存做新增操作
        goods.save()


class OrderView(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    def get(self,request):
        # 判断用户是否登录
            user = self.request.user
            print(user)
            if not user.is_authenticated:
            # 用户未登录
                return CustomResponse(code=401, msg="401-UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)

            orders = Order.objects.filter(user=request.user)
            order_json = OrderModelSerializer(orders, many=True)
            print(order_json.data)
            #return CustomResponse(order_json.data)
            return CustomResponse(data=order_json.data, code=200, msg="OK", status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self,request):
        user = self.request.user
        if not user.is_authenticated:
            return CustomResponse(code=401, msg="401-UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
        carts = Cart.objects.filter(user=request.user)
        if not carts.exists():
            return CustomResponse(code=400, msg="购物车为空，无法生成订单", status=status.HTTP_400_BAD_REQUEST)
        #订单编号

        order_sn=self.build_order_sn()
        print(order_sn)
        #联系人相关信息
        contact_name=request.data['contact_name']
        contact_mobile = request.data['contact_mobile']
        memo = request.data['memo']
        pay_method=request.data['pay_method']
        address=request.data['address']
        order_total=0
        order_price=0

        #创建保存点
        save_id=transaction.savepoint()
        print(request.data)
        #ser_data=OrderModelSerializer(data=request.data,many=True)
        #orderinfo=''
        #if ser_data.is_valid():
        #    orderinfo=ser_data.save()
        #print("2222222 "+str(request.user))
        orderinfo=Order.objects.create(
            order_sn=order_sn,
            address=address,
            contact_name=contact_name,
            contact_mobile=contact_mobile,
            memo=memo,
            pay_method=pay_method,
            user=self.request.user,
        )
        # 购物车加入时已经占用库存，下单时只生成订单商品快照并增加销量
        for cart in carts:
            goods=cart.goods
            goods.amount+=cart.goods_num
            goods.save()

            #创建子表
            OrderGoods.objects.create(
                order=orderinfo,
                goods=goods,
                goods_num=cart.goods_num,
                price=goods.price
            )

            order_total+=cart.goods_num
            order_price+=cart.goods.price*cart.goods_num


            #订单主表中有个订单总金额字段，我们实时计算
        orderinfo.order_total=order_total
        orderinfo.order_price=order_price

        orderinfo.save()
        #删除购物车数据
        aa=Cart.objects.filter(user=request.user).delete()
        print(aa)

        #事务提交
        transaction.savepoint_commit(save_id)
        return Response({
            'code': '200',
            'msg': '订单生成成功',
            'data': {
                'id': orderinfo.id,
                'order_sn': orderinfo.order_sn,
                'order_price': orderinfo.order_price,
                'order_state': orderinfo.order_state,
            }
        })

    def build_order_sn(self):
        order_sn = datetime.now().strftime('%Y%m%d%H%M%S') + str(self.request.user.id)
        return order_sn

class PayOrderView(APIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def post(self, request, order_id=None, pk=None):
        user = self.request.user
        if not user.is_authenticated:
            return CustomResponse(code=401, msg="401-UNAUTHORIZED", status=status.HTTP_401_UNAUTHORIZED)
        order_id = order_id or pk
        try:
            order = Order.objects.get(id=order_id, user=user)
        except Order.DoesNotExist:
            return CustomResponse(code=404, msg="订单不存在", status=status.HTTP_404_NOT_FOUND)
        if order.order_state == "payed":
            return CustomResponse(code=400, msg="订单已支付，不能重复支付", status=status.HTTP_400_BAD_REQUEST)
        if order.order_state == "cancel":
            return CustomResponse(code=400, msg="订单已取消，不能支付", status=status.HTTP_400_BAD_REQUEST)
        if order.order_state != "paying":
            return CustomResponse(code=400, msg="当前订单状态不能支付", status=status.HTTP_400_BAD_REQUEST)
        order.order_state = "payed"
        order.save()
        return CustomResponse(
            data={
                "id": order.id,
                "order_sn": order.order_sn,
                "order_price": order.order_price,
                "order_state": order.order_state,
            },
            code=200,
            msg="支付成功",
            status=status.HTTP_200_OK,
        )

class OrderViewset(viewsets.ModelViewSet):
    '''
    购物车视图类
    list：
        获取订单详情
    create：
        生成一张订单
    update：
        修改订单数据
    delete：
        删除订单数据
    '''
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderModelSerializer
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action=="retrieve":
            return CartDetailModelSerializer
        else:
            return CartModelSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        shop_cart = serializer.save()
        print(shop_cart)
        #goods = shop_cart.goods
        #goods.stock_num -= shop_cart.goods_num
        #goods.save()

    def perform_destroy(self, instance):
        goods = instance.goods
        goods.stock_num += instance.goods_num
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        existed_record = Cart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.goods_num
        saved_record = serializer.save()
        nums = saved_record.goods_num-existed_nums
        goods = saved_record.goods
        goods.stock_num -= nums
        goods.save()

