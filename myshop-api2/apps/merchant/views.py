from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from apps.goods.models import Goods, GoodsCategory
from apps.order.models import Order, OrderGoods
from .models import Shop
from .serializers import (
    MerchantRegSerializer,
    ShopSerializer,
    MerchantGoodsSerializer,
    MerchantGoodsCategorySerializer,
    MerchantOrderSerializer,
    MerchantStatsSerializer,
)
from .permissions import IsMerchant, IsShopOwner
from common.customresponse import CustomResponse


# ==================== 商家注册 ====================

class MerchantRegView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """商家注册"""
    serializer_class = MerchantRegSerializer
    authentication_classes = ()
    permission_classes = ()


# ==================== 店铺管理 ====================

class ShopViewSet(viewsets.ModelViewSet):
    """店铺信息管理"""
    serializer_class = ShopSerializer
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Shop.objects.filter(merchant=self.request.user)

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user)


# ==================== 商家商品管理 ====================

class MerchantGoodsViewSet(viewsets.ModelViewSet):
    """商家商品CRUD"""
    serializer_class = MerchantGoodsSerializer
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Goods.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def toggle_status(self, request, pk=None):
        """商品上下架"""
        goods = self.get_object()
        goods.status = 1 if goods.status == 0 else 0
        goods.save()
        status_text = '下架' if goods.status == 1 else '上架'
        return CustomResponse(
            data={'id': goods.id, 'status': goods.status},
            code=200, msg=f'商品已{status_text}', status=status.HTTP_200_OK
        )


class MerchantCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """商品分类（只读）"""
    serializer_class = MerchantGoodsCategorySerializer
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    queryset = GoodsCategory.objects.all()


# ==================== 商家订单管理 ====================

class MerchantOrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """商家订单管理"""
    serializer_class = MerchantOrderSerializer
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        # 查询包含本商家商品的订单
        my_goods_ids = Goods.objects.filter(user=self.request.user).values_list('id', flat=True)
        order_ids = OrderGoods.objects.filter(goods_id__in=my_goods_ids).values_list('order_id', flat=True)
        return Order.objects.filter(id__in=order_ids).order_by('-create_date')

    @action(detail=True, methods=['post'])
    def ship(self, request, pk=None):
        """发货"""
        order = self.get_object()
        if order.order_state != 'payed':
            return CustomResponse(code=400, msg='当前订单状态不允许发货', status=status.HTTP_400_BAD_REQUEST)
        order.order_state = 'shipping'
        order.save()
        return CustomResponse(
            data={'id': order.id, 'order_state': order.order_state},
            code=200, msg='发货成功', status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """完成订单"""
        order = self.get_object()
        if order.order_state != 'shipping':
            return CustomResponse(code=400, msg='当前订单状态不允许完成', status=status.HTTP_400_BAD_REQUEST)
        order.order_state = 'complete'
        order.save()
        return CustomResponse(
            data={'id': order.id, 'order_state': order.order_state},
            code=200, msg='订单已完成', status=status.HTTP_200_OK
        )


# ==================== 数据统计 ====================

class MerchantStatsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """商家数据统计"""
    serializer_class = MerchantStatsSerializer
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def list(self, request, *args, **kwargs):
        user = request.user
        my_goods = Goods.objects.filter(user=user)

        # 本店商品对应的订单商品明细
        my_order_goods = OrderGoods.objects.filter(goods__in=my_goods)
        total_sales = my_order_goods.aggregate(
            total=Sum('price')
        )['total'] or 0

        # 订单数
        order_ids = my_order_goods.values_list('order_id', flat=True).distinct()
        total_orders = order_ids.count()

        # 商品数和库存
        total_goods = my_goods.count()
        total_stock = my_goods.aggregate(
            total=Sum('stock_num')
        )['total'] or 0

        data = {
            'total_sales': total_sales,
            'total_orders': total_orders,
            'total_goods': total_goods,
            'total_stock': total_stock,
        }
        serializer = MerchantStatsSerializer(data)
        return CustomResponse(data=serializer.data, code=200, msg='OK', status=status.HTTP_200_OK)
