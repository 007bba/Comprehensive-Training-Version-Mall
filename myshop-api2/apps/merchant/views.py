import os
from uuid import uuid4

from django.core.files.storage import default_storage
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
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


class MerchantPagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


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


class MerchantLogoUploadView(APIView):
    """商家店铺 Logo 上传"""
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    parser_classes = (MultiPartParser, FormParser)

    allowed_extensions = ('.jpg', '.jpeg', '.png')
    allowed_content_types = ('image/jpeg', 'image/png')
    max_size = 2 * 1024 * 1024

    def post(self, request, *args, **kwargs):
        upload_file = request.FILES.get('file')
        if not upload_file:
            return CustomResponse(code=400, msg='请上传图片文件', status=status.HTTP_400_BAD_REQUEST)

        ext = os.path.splitext(upload_file.name)[1].lower()
        content_type = getattr(upload_file, 'content_type', '')
        if ext not in self.allowed_extensions or content_type not in self.allowed_content_types:
            return CustomResponse(code=400, msg='仅支持 JPG/PNG 格式图片', status=status.HTTP_400_BAD_REQUEST)

        if upload_file.size > self.max_size:
            return CustomResponse(code=400, msg='图片大小不能超过 2MB', status=status.HTTP_400_BAD_REQUEST)

        file_path = f'shop/logo/{request.user.id}/{uuid4().hex}{ext}'
        saved_path = default_storage.save(file_path, upload_file)
        url = default_storage.url(saved_path)
        if request:
            url = request.build_absolute_uri(url)

        return CustomResponse(
            data={'url': url, 'path': saved_path},
            code=200,
            msg='上传成功',
            status=status.HTTP_200_OK
        )


# ==================== 商家商品管理 ====================

class MerchantGoodsViewSet(viewsets.ModelViewSet):
    """商家商品CRUD"""
    serializer_class = MerchantGoodsSerializer
    permission_classes = (IsAuthenticated, IsMerchant)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    pagination_class = MerchantPagePagination

    def get_queryset(self):
        queryset = Goods.objects.filter(user=self.request.user).order_by('-createDate', '-id')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search.strip())
        return queryset

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
