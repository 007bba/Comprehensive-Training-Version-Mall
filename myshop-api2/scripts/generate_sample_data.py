#!/usr/bin/env python3
"""生成示例数据并插入当前 Django 数据库。"""
import os
import sys
import random
from decimal import Decimal
from pathlib import Path
from datetime import datetime, date


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

import django

django.setup()

from apps.users.models import MyUser
from apps.goods.models import GoodsCategory, Goods, Slide
from apps.basic.models import Address
from apps.order.models import Cart, Order, OrderGoods


def random_mobile():
    return '1' + ''.join(str(random.randint(0, 9)) for _ in range(10))


def make_users(n=10):
    users = []
    for i in range(1, n + 1):
        username = f'user{i:03d}'
        email = f'{username}@example.com'
        if MyUser.objects.filter(username=username).exists():
            user = MyUser.objects.get(username=username)
        else:
            user = MyUser.objects.create_user(username=username, email=email, password='password')
        user.truename = f'姓名{i}'
        user.mobile = random_mobile()[:11]
        user.sex = random.choice([0, 1])
        user.birthday = date(1990 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28))
        user.save()
        users.append(user)
    return users


def make_categories():
    names = ['电子', '服装', '家居', '食品', '玩具']
    cats = []
    for name in names:
        obj, _ = GoodsCategory.objects.get_or_create(name=name, defaults={'logo': 'uploads/goods_img/default.png', 'sort': 0})
        cats.append(obj)
    return cats


def make_goods(categories, n_per_cat=5):
    goods_list = []
    for cat in categories:
        for i in range(n_per_cat):
            name = f'{cat.name}-商品-{i+1}'
            price = Decimal(random.randrange(100, 5000)) / Decimal('100')
            obj, _ = Goods.objects.get_or_create(name=name, defaults={
                'category': cat,
                'market_price': price * Decimal('1.2'),
                'price': price,
                'unit': '件',
                'click_num': random.randint(0, 1000),
                'amount': random.randint(0, 500),
                'stock_num': random.randint(10, 200),
                'fav_num': random.randint(0, 100),
                'goods_desc': f'这是{name}的描述',
                'status': 0,
            })
            goods_list.append(obj)
    return goods_list


def make_addresses(users):
    addrs = []
    for user in users:
        obj, _ = Address.objects.get_or_create(user=user, defaults={
            'province': '省',
            'city': '城市',
            'district': '区',
            'address': f'某街道{random.randint(1,100)}号',
            'contact_name': user.truename or user.username,
            'contact_mobile': user.mobile,
            'is_default': 1,
        })
        addrs.append(obj)
    return addrs


def make_carts(users, goods_list):
    for user in users:
        for _ in range(random.randint(0, 3)):
            g = random.choice(goods_list)
            Cart.objects.get_or_create(user=user, goods=g, defaults={'goods_num': random.randint(1, 5)})


def make_orders(users, goods_list, addrs):
    for user in users:
        if random.random() < 0.5:
            addr = random.choice(addrs)
            order = Order.objects.create(
                order_sn=f'ORD{datetime.now().strftime("%Y%m%d%H%M%S%f")}{random.randint(100,999)}',
                order_total=random.randint(1,5),
                order_price=Decimal('0.00'),
                address=f"{addr.province}{addr.city}{addr.district}{addr.address}",
                contact_name=addr.contact_name,
                contact_mobile=addr.contact_mobile,
                pay_method=1,
                memo='',
                order_state='payed',
                user=user,
            )
            total_price = Decimal('0.00')
            for _ in range(random.randint(1, 3)):
                g = random.choice(goods_list)
                qty = random.randint(1, 3)
                price = g.price
                OrderGoods.objects.create(order=order, goods=g, goods_num=qty, price=price)
                total_price += price * qty
            order.order_price = total_price
            order.order_total = OrderGoods.objects.filter(order=order).count()
            order.save()


def main():
    print('开始生成示例数据...')
    users = make_users(20)
    cats = make_categories()
    goods_list = make_goods(cats, n_per_cat=6)
    addrs = make_addresses(users)
    make_carts(users, goods_list)
    make_orders(users, goods_list, addrs)
    print('完成。')


if __name__ == '__main__':
    main()
