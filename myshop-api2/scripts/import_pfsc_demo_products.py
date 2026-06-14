#!/usr/bin/env python3
"""Import PFSC demo products from the generated CSV into Django."""
import argparse
import csv
import logging
import os
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

import django

django.setup()

logging.getLogger('django.db.backends').setLevel(logging.WARNING)

from django.core.files import File
from django.core.files.storage import default_storage
from django.db import transaction

from apps.goods.models import Goods, GoodsCategory
from apps.merchant.models import Shop
from apps.users.models import MyUser


DEFAULT_CSV_PATH = BASE_DIR / 'exports' / 'pfsc_demo_products' / 'pfsc_demo_products.csv'
DEFAULT_USERNAME = 'demo_merchant'
DEFAULT_PASSWORD = 'Demo@123456'
DEFAULT_SHOP_NAME = '助农演示店铺'
DEFAULT_CATEGORY_MAP = {
    '水果': '时令水果',
    '蔬菜': '新鲜蔬菜',
    '粮食': '面粉杂粮',
    '油料': '食用油',
}


def parse_args():
    parser = argparse.ArgumentParser(description='Import generated PFSC demo products into the database.')
    parser.add_argument('--csv', default=str(DEFAULT_CSV_PATH), help='Path to pfsc_demo_products.csv.')
    parser.add_argument('--username', default=DEFAULT_USERNAME, help='Merchant username to own imported goods.')
    parser.add_argument('--password', default=DEFAULT_PASSWORD, help='Password used when creating the merchant.')
    parser.add_argument('--shop-name', default=DEFAULT_SHOP_NAME, help='Shop name for the demo merchant.')
    parser.add_argument('--reset-password', action='store_true', help='Reset merchant password if the user exists.')
    parser.add_argument('--dry-run', action='store_true', help='Validate and print planned changes without writing.')
    return parser.parse_args()


def decimal_value(value, default='0.00'):
    if value in (None, ''):
        return Decimal(default)
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return Decimal(default)


def int_value(value, default=0):
    if value in (None, ''):
        return default
    try:
        return int(str(value).strip())
    except ValueError:
        return default


def safe_filename(value):
    value = re.sub(r'[\\/:*?"<>|]+', '_', value.strip())
    value = re.sub(r'\s+', '_', value)
    return value[:80] or 'product'


def load_rows(csv_path):
    with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        return [row for row in reader if (row.get('商品名') or '').strip()]


def get_or_create_merchant(username, password, shop_name, reset_password=False):
    user, created = MyUser.objects.get_or_create(
        username=username,
        defaults={
            'email': f'{username}@example.com',
            'mobile': '13800000000',
            'role': 1,
        },
    )
    if created or reset_password:
        user.set_password(password)
    user.role = 1
    user.is_active = True
    user.save()

    Shop.objects.update_or_create(
        merchant=user,
        defaults={
            'name': shop_name,
            'desc': '助农商城演示店铺，用于展示农产品商品、图片和订单流程。',
            'status': 0,
        },
    )
    return user, created


def get_or_create_category(name, sort):
    target_name = DEFAULT_CATEGORY_MAP.get(name, name)
    category, _ = GoodsCategory.objects.get_or_create(
        name=target_name,
        defaults={
            'logo': 'uploads/goods_img/default.png',
            'is_nav': True,
            'sort': sort,
        },
    )
    if not category.is_nav:
        category.is_nav = True
        category.save(update_fields=['is_nav'])
    return category


def first_image_path(value):
    if not value:
        return ''
    return value.split(';')[0].strip()


def copy_image(csv_path, row):
    relative_image = first_image_path(row.get('图片文件'))
    if not relative_image:
        return ''

    source_path = csv_path.parent / relative_image
    if not source_path.exists():
        print(f'[WARN] missing image file: {source_path}')
        return ''

    category = safe_filename(row.get('分类') or '未分类')
    filename = safe_filename(source_path.stem) + source_path.suffix.lower()
    target_path = f'goods/images/demo_pfsc/{category}/{filename}'

    if not default_storage.exists(target_path):
        with source_path.open('rb') as f:
            default_storage.save(target_path, File(f))
    return target_path


def build_goods_desc(row):
    desc = (row.get('商品详情') or '').strip()
    source = (row.get('数据来源') or '').strip()
    source_url = (row.get('来源链接') or '').strip()
    image_status = (row.get('图片授权状态') or '').strip()
    note = (row.get('备注') or '').strip()

    extra = (
        '<hr>'
        f'<p><strong>演示说明：</strong>{note}</p>'
        f'<p><strong>数据来源：</strong>{source} {source_url}</p>'
        f'<p><strong>图片状态：</strong>{image_status}</p>'
    )
    return desc + extra


def import_rows(rows, csv_path, merchant, dry_run=False):
    categories = {}
    created_count = 0
    updated_count = 0

    for index, row in enumerate(rows, start=1):
        category_name = (row.get('分类') or '未分类').strip()
        if category_name not in categories:
            categories[category_name] = get_or_create_category(category_name, len(categories) + 1)
        category = categories[category_name]

        name = (row.get('商品名') or '').strip()[:50]
        image_path = '' if dry_run else copy_image(csv_path, row)

        defaults = {
            'category': category,
            'market_price': decimal_value(row.get('市场参考价')),
            'price': decimal_value(row.get('售价')),
            'unit': (row.get('单位') or '件').strip()[:10],
            'stock_num': int_value(row.get('库存'), 100),
            'goods_desc': build_goods_desc(row),
            'status': 0,
            'is_recommend': index <= 8,
        }
        if image_path:
            defaults['main_img'] = image_path

        if dry_run:
            exists = Goods.objects.filter(name=name, user=merchant).exists()
            print(f'[DRY-RUN] {"update" if exists else "create"}: {name}')
            continue

        _, created = Goods.objects.update_or_create(
            name=name,
            user=merchant,
            defaults=defaults,
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    return created_count, updated_count, len(categories)


def main():
    args = parse_args()
    csv_path = Path(args.csv)
    if not csv_path.is_absolute():
        csv_path = BASE_DIR / csv_path
    if not csv_path.exists():
        raise FileNotFoundError(f'CSV file not found: {csv_path}')

    rows = load_rows(csv_path)
    if not rows:
        raise RuntimeError(f'No importable rows found in {csv_path}')

    if args.dry_run:
        merchant = MyUser(username=args.username, role=1)
        created_count, updated_count, category_count = import_rows(rows, csv_path, merchant, dry_run=True)
        print(f'Dry run rows: {len(rows)}, categories: {category_count}')
        return

    with transaction.atomic():
        merchant, merchant_created = get_or_create_merchant(
            args.username,
            args.password,
            args.shop_name,
            reset_password=args.reset_password,
        )
        created_count, updated_count, category_count = import_rows(rows, csv_path, merchant)

    print(f'Merchant: {merchant.username} (created={merchant_created})')
    print(f'Shop: {args.shop_name}')
    print(f'Categories touched: {category_count}')
    print(f'Goods created: {created_count}')
    print(f'Goods updated: {updated_count}')
    print(f'Demo login: {args.username} / {args.password if merchant_created or args.reset_password else "(existing password unchanged)"}')


if __name__ == '__main__':
    main()
