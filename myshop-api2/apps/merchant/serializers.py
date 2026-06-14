import os
from urllib.parse import urlparse

from django.conf import settings
from rest_framework import serializers
from .models import Shop
from apps.goods.models import Goods, GoodsCategory
from apps.order.models import Order, OrderGoods
from apps.users.models import MyUser


# ==================== 商家注册 ====================

class MerchantRegSerializer(serializers.ModelSerializer):
    """商家注册序列化器"""
    class Meta:
        model = MyUser
        fields = ('username', 'password', 'mobile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        user.role = 1  # 商家角色
        user.save()
        return user


# ==================== 店铺信息 ====================

class ShopSerializer(serializers.ModelSerializer):
    """店铺信息序列化器"""
    merchant_name = serializers.CharField(source='merchant.username', read_only=True)
    logo = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ('merchant',)

    def validate_logo(self, value):
        if not value:
            return value

        path = urlparse(value).path if value.startswith(('http://', 'https://')) else value
        if path.startswith(settings.MEDIA_URL):
            path = path[len(settings.MEDIA_URL):]

        path = path.lstrip('/')
        normalized_path = os.path.normpath(path).replace('\\', '/')
        if normalized_path == '..' or normalized_path.startswith('../'):
            raise serializers.ValidationError('Logo地址不合法')

        return normalized_path

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.logo:
            try:
                url = instance.logo.url
            except ValueError:
                url = settings.MEDIA_URL + str(instance.logo).lstrip('/')

            request = self.context.get('request')
            if request and url.startswith('/'):
                url = request.build_absolute_uri(url)
            data['logo'] = url
        else:
            data['logo'] = ''

        return data

    def create(self, validated_data):
        validated_data['merchant'] = self.context['request'].user
        return super().create(validated_data)


# ==================== 商家商品管理 ====================

class MerchantGoodsSerializer(serializers.ModelSerializer):
    """商家商品序列化器"""
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Goods
        fields = '__all__'
        read_only_fields = ('user', 'click_num', 'amount', 'fav_num', 'createDate')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MerchantGoodsCategorySerializer(serializers.ModelSerializer):
    """商品分类（只读）"""
    class Meta:
        model = GoodsCategory
        fields = ('id', 'name', 'parent')


# ==================== 商家订单管理 ====================

class MerchantOrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品明细"""
    goods_name = serializers.CharField(source='goods.name', read_only=True)
    goods_img = serializers.ImageField(source='goods.main_img', read_only=True)

    class Meta:
        model = OrderGoods
        fields = ('id', 'goods', 'goods_name', 'goods_img', 'goods_num', 'price', 'create_date')


class MerchantOrderSerializer(serializers.ModelSerializer):
    """商家订单序列化器"""
    order_goods = MerchantOrderGoodsSerializer(source='ordergoods_set', many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'


# ==================== 数据统计 ====================

class MerchantStatsSerializer(serializers.Serializer):
    """商家数据统计"""
    total_sales = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_orders = serializers.IntegerField()
    total_goods = serializers.IntegerField()
    total_stock = serializers.IntegerField()
