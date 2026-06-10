#!/usr/bin/env python3
"""Export PFSC agricultural product demo data and images.

The generated files are for demo data preparation only. Keep the source URL and
replace or re-authorize images before production use.
"""
import argparse
import csv
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import requests


PFSC_BASE_URL = 'https://pfsc.agri.cn'
PFSC_PAGE_URL = PFSC_BASE_URL + '/#/displayAgriculturalProducts'
PRODUCT_LIST_URL = PFSC_BASE_URL + '/price_portal/web/portal-product/selectList'

CATEGORY_BY_TYPE = {
    '01': '蔬菜',
    '02': '水果',
    '03': '畜产品',
    '04': '水产品',
    '05': '粮食',
    '06': '油料',
}

UNIT_BY_CATEGORY = {
    '蔬菜': '斤',
    '水果': '斤',
    '畜产品': '斤',
    '水产品': '斤',
    '粮食': '袋',
    '油料': '瓶',
}

BASE_PRICE_BY_CATEGORY = {
    '蔬菜': 4.8,
    '水果': 9.9,
    '畜产品': 28.8,
    '水产品': 32.8,
    '粮食': 39.8,
    '油料': 59.8,
}

CSV_HEADERS = [
    '商品名',
    '分类',
    '别名',
    '英文名',
    '产地',
    '规格',
    '单位',
    '市场参考价',
    '售价',
    '库存',
    '商品详情',
    '图片文件',
    '图片来源',
    '图片授权状态',
    '是否示意图',
    '参考图片URL',
    '数据来源',
    '来源链接',
    '参考特征',
    '备注',
]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Download a small PFSC demo product set and write an Excel-compatible CSV.'
    )
    parser.add_argument(
        '--output-dir',
        default='exports/pfsc_demo_products',
        help='Output directory for CSV and downloaded images.',
    )
    parser.add_argument(
        '--categories',
        nargs='*',
        default=['蔬菜', '水果', '粮食', '油料'],
        help='Categories to export. Available: 蔬菜 水果 畜产品 水产品 粮食 油料.',
    )
    parser.add_argument(
        '--per-category',
        type=int,
        default=5,
        help='Maximum products to export for each category.',
    )
    parser.add_argument(
        '--images-per-product',
        type=int,
        default=1,
        help='Maximum images to download for each product.',
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=20,
        help='HTTP timeout in seconds.',
    )
    parser.add_argument(
        '--sleep',
        type=float,
        default=0.2,
        help='Delay between image downloads in seconds.',
    )
    parser.add_argument(
        '--no-images',
        action='store_true',
        help='Only export the CSV and do not download images.',
    )
    return parser.parse_args()


def sanitize_filename(value):
    value = re.sub(r'[\\/:*?"<>|]+', '_', value.strip())
    value = re.sub(r'\s+', '_', value)
    return value[:80] or 'product'


def normalize_image_url(raw_url):
    if not raw_url:
        return ''
    url = raw_url.strip()
    if not url:
        return ''
    if url.startswith('http://') or url.startswith('https://'):
        return url
    if url.startswith('/'):
        return PFSC_BASE_URL + url
    return PFSC_BASE_URL + '/file/image/' + url


def split_picture_urls(picture):
    if not picture:
        return []
    urls = []
    for item in picture.split(','):
        url = normalize_image_url(item)
        if url:
            urls.append(url)
    return urls


def fetch_products(session, timeout):
    response = session.post(PRODUCT_LIST_URL, json={'name': '', 'type': ''}, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if payload.get('code') != 0:
        raise RuntimeError(f'PFSC response error: {payload}')
    return payload.get('data') or []


def stable_demo_price(name, category):
    base = BASE_PRICE_BY_CATEGORY.get(category, 9.9)
    bump = (sum(ord(ch) for ch in name) % 9) * 0.6
    price = round(base + bump, 2)
    market_price = round(price * 1.18, 2)
    return market_price, price


def build_description(product, category, unit):
    name = (product.get('name') or '').strip()
    alias = (product.get('alias') or '').strip()
    alias_text = f'，又称{alias}' if alias else ''
    return (
        f'<p>{name}{alias_text}，属于{category}类农产品，适合助农商城演示、专题推荐和日常采购场景。</p>'
        f'<p>当前信息用于演示数据初始化，规格、产地、检测信息和包装说明请在正式上线前由商家补充确认。</p>'
        f'<p>建议销售单位：{unit}。</p>'
    )


def download_image(session, url, image_path, timeout):
    image_path.parent.mkdir(parents=True, exist_ok=True)
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    content_type = response.headers.get('content-type', '')
    if content_type and not content_type.startswith('image/'):
        raise RuntimeError(f'Not an image response: {url} ({content_type})')
    image_path.write_bytes(response.content)


def image_extension(url):
    suffix = Path(urlparse(url).path).suffix.lower()
    if suffix in {'.jpg', '.jpeg', '.png', '.webp', '.gif'}:
        return suffix
    return '.jpg'


def export_rows(products, args, output_dir, session):
    selected_categories = set(args.categories)
    category_counts = {category: 0 for category in selected_categories}
    rows = []

    for product in products:
        name = (product.get('name') or '').strip()
        category = CATEGORY_BY_TYPE.get(str(product.get('type') or '').zfill(2), '')
        if not name or category not in selected_categories:
            continue
        if category_counts[category] >= args.per_category:
            continue

        unit = UNIT_BY_CATEGORY.get(category, '件')
        market_price, price = stable_demo_price(name, category)
        image_urls = split_picture_urls(product.get('picture'))
        local_images = []

        if not args.no_images:
            for index, image_url in enumerate(image_urls[:args.images_per_product], start=1):
                ext = image_extension(image_url)
                filename = f'{sanitize_filename(name)}_{index}{ext}'
                relative_path = Path('images') / sanitize_filename(category) / filename
                target_path = output_dir / relative_path
                try:
                    download_image(session, image_url, target_path, args.timeout)
                    local_images.append(str(relative_path).replace('\\', '/'))
                    time.sleep(args.sleep)
                except Exception as exc:
                    print(f'[WARN] image download failed: {name} {image_url} ({exc})')

        rows.append({
            '商品名': name,
            '分类': category,
            '别名': product.get('alias') or '',
            '英文名': product.get('nameEn') or '',
            '产地': '',
            '规格': '',
            '单位': unit,
            '市场参考价': market_price,
            '售价': price,
            '库存': 100,
            '商品详情': build_description(product, category, unit),
            '图片文件': ';'.join(local_images),
            '图片来源': '全国农产品批发市场价格信息系统（PFSC）',
            '图片授权状态': '仅用于课程/项目演示，上线前需替换或确认授权',
            '是否示意图': '是',
            '参考图片URL': ';'.join(image_urls),
            '数据来源': '全国农产品批发市场价格信息系统（PFSC）',
            '来源链接': PFSC_PAGE_URL,
            '参考特征': product.get('feature') or '',
            '备注': '演示数据，正式经营前请补充真实产地、规格、库存和授权图片。',
        })
        category_counts[category] += 1

    return rows


def write_csv(rows, csv_path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)


def main():
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (compatible; myshop-demo-data-exporter/1.0)',
        'Referer': PFSC_PAGE_URL,
    })

    products = fetch_products(session, args.timeout)
    rows = export_rows(products, args, output_dir, session)
    csv_path = output_dir / 'pfsc_demo_products.csv'
    write_csv(rows, csv_path)

    print(f'Fetched products: {len(products)}')
    print(f'Exported rows: {len(rows)}')
    print(f'CSV: {csv_path}')
    if not args.no_images:
        image_count = sum(1 for row in rows if row['图片文件'])
        print(f'Products with downloaded image: {image_count}')
        print(f'Images dir: {output_dir / "images"}')


if __name__ == '__main__':
    main()
