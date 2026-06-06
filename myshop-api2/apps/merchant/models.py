from django.db import models
from datetime import datetime

from apps.users.models import MyUser
from common.base_model import BaseModel


class Shop(BaseModel):
    """商家店铺"""
    merchant = models.OneToOneField(
        MyUser, on_delete=models.CASCADE,
        verbose_name='商家', related_name='shop'
    )
    name = models.CharField(max_length=100, verbose_name='店铺名称', default='')
    logo = models.ImageField(
        upload_to='shop/logo/', verbose_name='店铺Logo',
        blank=True, null=True
    )
    desc = models.TextField(blank=True, default='', verbose_name='店铺描述')
    STATUS = (
        (0, '正常'),
        (1, '关闭'),
    )
    status = models.IntegerField(default=0, choices=STATUS, verbose_name='店铺状态')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商家店铺'
        db_table = 'd_shop'
