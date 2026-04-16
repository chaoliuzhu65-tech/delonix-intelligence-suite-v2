#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1688 商品搜索脚本
用于德胧采购比价系统 - 获取酒店相关品类批发价数据

使用方式:
  # 方式1: 官方API（需要AppKey/AppSecret）
  export APP_KEY="your_key" APP_SECRET="your_secret"
  python scripts/1688_search.py --keywords "酒店门锁" --provider official

  # 方式2: 第三方API（订单侠，无需申请）
  export DINGDANXIA_APIKEY="your_key"
  python scripts/1688_search.py --keywords "酒店门锁" --provider dingdanxia

  # 方式3: 浏览器搜索（完全无需API，作为最后兜底）
  python scripts/1688_search.py --keywords "酒店门锁" --provider browser
"""

import os
import time
import json
import re
import csv
import argparse
import hashlib
import urllib.parse
import urllib.request

# ============================================================
# 方案1：官方开放平台 API（需要 APP_KEY + APP_SECRET）
# ============================================================

def generate_sign(params: dict, app_secret: str) -> str:
    """
    1688 官方签名算法（MD5 模式）
    secret + ASCII排序的参数串 + secret -> MD5 -> 大写
    """
    sorted_pairs = sorted(params.items(), key=lambda x: x[0])
    query_str = "&".join([f"{k}={v}" for k, v in sorted_pairs])
    raw = f"{app_secret}{query_str}{app_secret}"
    return hashlib.md5(raw.encode("utf-8")).hexdigest().upper()


def search_official(keyword: str, page: int = 1, page_size: int = 20,
                    app_key: str = None, app_secret: str = None) -> list:
    """
    通过1688官方开放平台 API 搜索商品
    需要: APP_KEY, APP_SECRET 环境变量
    """
    app_key = app_key or os.getenv("APP_KEY")
    app_secret = app_secret or os.getenv("APP_SECRET")

    if not app_key or not app_secret:
        raise ValueError("官方API模式需要设置 APP_KEY 和 APP_SECRET")

    url = f"https://gw.open.1688.com/openapi/param2/1/portals.open.api.item.search/{app_key}"

    params = {
        "app_key": app_key,
        "method": "alibaba.item.search",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "v": "2.0",
        "sign_method": "md5",
        "q": keyword,
        "page": page,
        "pageSize": page_size,
        "sort": "sale",
    }

    params["sign"] = generate_sign(params, app_secret)

    req = urllib.request.Request(
        url + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"官方API请求失败: {e}") from e

    if data.get("error_code"):
        raise RuntimeError(f"API错误: {data.get('error_message', data)}")

    # 解析返回结构（不同版本字段略有差异）
    try:
        result = data.get("result") or data.get("result_trade") or {}
        products = result.get("products") or result.get("result") or []
        return _normalize_products(products, keyword)
    except Exception as e:
        raise RuntimeError(f"解析返回数据失败: {e}\n原始数据: {json.dumps(data, ensure_ascii=False)[:500]}") from e


# ============================================================
# 方案2：第三方聚合 API（订单侠，无需申请）
# ============================================================

def search_dingdanxia(keyword: str, page: int = 1, page_size: int = 20,
                       api_key: str = None) -> list:
    """
    通过订单侠 (dingdanxia.com) 第三方API搜索商品
    注册地址: https://www.dingdanxia.com（注册送免费次数）
    无需申请，直接可用
    """
    api_key = api_key or os.getenv("DINGDANXIA_APIKEY")
    if not api_key:
        raise ValueError("第三方API模式需要设置 DINGDANXIA_APIKEY（注册: https://www.dingdanxia.com）")

    url = "https://api.ds.dingdanxia.com/1688/item_search"
    params = {
        "apikey": api_key,
        "keyword": keyword,
        "page": page,
        "pageSize": page_size,
    }

    req = urllib.request.Request(
        url + "?" + urllib.parse.urlencode(params),
        headers={"User-Agent": "Mozilla/5.0"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        raise RuntimeError(f"订单侠API请求失败: {e}") from e

    if data.get("code") != 200:
        raise RuntimeError(f"订单侠API错误: {data.get('msg', data)}")

    items = (data.get("data", {}) or {}).get("result", [])
    results = []
    for item in items:
        results.append({
            "offerId": item.get("num_iid", ""),
            "title": item.get("title", ""),
            "price": item.get("price", ""),
            "saleCount": item.get("sales", ""),
            "supplier": item.get("shop_name", ""),
            "supplierId": item.get("shop_id", ""),
            "picUrl": item.get("pic_url", ""),
            "detailUrl": item.get("detail_url", ""),
            "keyword": keyword,
        })
    return results


# ============================================================
# 方案3：搜索引擎兜底（完全无需API）
# ============================================================

def search_browser(keyword: str, page: int = 1) -> list:
    """
    通过 Bing 搜索1688商品，作为完全兜底方案
    数据量有限，仅推荐在无API密钥时使用
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError("search_browser 需要 beautifulsoup4: pip install beautifulsoup4")

    search_url = (
        "https://www.bing.com/search?q=site%3A1688.com+"
        + urllib.parse.quote(keyword)
        + (f"&first={(page - 1) * 10}" if page > 1 else "")
    )

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,*/*",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }

    req = urllib.request.Request(search_url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = BeautifulSoup(resp.read().decode("utf-8", errors="ignore"), "html.parser")
    except Exception as e:
        raise RuntimeError(f"搜索引擎请求失败: {e}") from e

    results = []
    for link in html.select("h2 a[href*='1688.com/offer']")[:20]:
        href = link.get("href", "")
        m = re.search(r'1688\.com/offer/(\d+)', href)
        if m:
            offer_id = m.group(1)
            results.append({
                "offerId": offer_id,
                "title": link.get_text(strip=True),
                "price": "",
                "saleCount": "",
                "supplier": "",
                "detailUrl": f"https://detail.1688.com/offer/{offer_id}.html",
                "keyword": keyword,
            })

    if not results and page == 1:
        # 百度备选
        baidu_url = (
            "https://www.baidu.com/s?wd=site%3A1688.com+"
            + urllib.parse.quote(keyword)
        )
        req2 = urllib.request.Request(baidu_url, headers=headers)
        try:
            with urllib.request.urlopen(req2, timeout=15) as resp2:
                html2 = BeautifulSoup(resp2.read().decode("utf-8", errors="ignore"), "html.parser")
            for link in html2.select("h3 a[href*='1688.com/offer']")[:20]:
                href2 = link.get("href", "")
                m2 = re.search(r'1688\.com/offer/(\d+)', href2)
                if m2 and not any(r["offerId"] == m2.group(1) for r in results):
                    results.append({
                        "offerId": m2.group(1),
                        "title": link.get_text(strip=True),
                        "price": "",
                        "saleCount": "",
                        "supplier": "",
                        "detailUrl": f"https://detail.1688.com/offer/{m2.group(1)}.html",
                        "keyword": keyword,
                    })
        except Exception as e:
            print(f"  百度备选失败: {e}")

    return results


# ============================================================
# 数据规范化
# ============================================================

def _normalize_products(products: list, keyword: str) -> list:
    """统一不同API返回的商品数据结构"""
    results = []
    for p in products:
        results.append({
            "offerId": str(p.get("offerId") or p.get("productId") or ""),
            "title": p.get("title") or p.get("subject") or "",
            "price": p.get("price") or p.get("salePrice") or "",
            "saleCount": p.get("saleCount") or p.get("sales") or "",
            "supplier": p.get("supplier") or p.get("companyName") or p.get("shopName") or "",
            "supplierId": p.get("supplierId") or p.get("memberId") or "",
            "picUrl": p.get("picUrl") or p.get("imageUrl") or p.get("pic_url") or "",
            "detailUrl": p.get("detailUrl") or p.get("detail_url")
                        or f"https://detail.1688.com/offer/{p.get('offerId', '')}.html",
            "keyword": keyword,
        })
    return results


# ============================================================
# 主搜索逻辑
# ============================================================

def search(keyword: str, provider: str = "official",
           app_key: str = None, app_secret: str = None,
           api_key: str = None,
           max_pages: int = 3, page_size: int = 20) -> list:
    """
    统一搜索入口
    provider:
      - "official"    : 官方API（需要APP_KEY/APP_SECRET）
      - "dingdanxia"  : 第三方订单侠（需要DINGDANXIA_APIKEY）
      - "browser"     : 搜索引擎（无需Key，但数据量少）
    """
    print(f"🔍 搜索关键词: [{keyword}] (provider={provider})")

    if provider == "official":
        all_products = []
        for page in range(1, max_pages + 1):
            print(f"   第 {page}/{max_pages} 页...")
            try:
                products = search_official(
                    keyword, page=page, page_size=page_size,
                    app_key=app_key, app_secret=app_secret
                )
                if not products:
                    print(f"   ⚠️ 第{page}页无数据")
                    break
                all_products.extend(products)
                print(f"   ✅ 获取 {len(products)} 条，累计 {len(all_products)} 条")
                time.sleep(1.5)
            except Exception as e:
                print(f"   ❌ 第{page}页失败: {e}")
                break
        return all_products

    elif provider == "dingdanxia":
        all_products = []
        for page in range(1, max_pages + 1):
            print(f"   第 {page}/{max_pages} 页...")
            try:
                products = search_dingdanxia(
                    keyword, page=page, page_size=page_size, api_key=api_key
                )
                if not products:
                    print(f"   ⚠️ 第{page}页无数据")
                    break
                all_products.extend(products)
                print(f"   ✅ 获取 {len(products)} 条，累计 {len(all_products)} 条")
                time.sleep(1)
            except Exception as e:
                print(f"   ❌ 第{page}页失败: {e}")
                break
        return all_products

    elif provider == "browser":
        all_products = []
        for page in range(1, max_pages + 1):
            print(f"   第 {page}/{max_pages} 页（搜索引擎）...")
            try:
                products = search_browser(keyword, page=page)
                if not products:
                    print(f"   ⚠️ 第{page}页无数据")
                    break
                all_products.extend(products)
                print(f"   ✅ 获取 {len(products)} 条")
                time.sleep(2)
            except Exception as e:
                print(f"   ❌ 第{page}页失败: {e}")
                break
        return all_products

    else:
        raise ValueError(f"未知provider: {provider}")


# ============================================================
# 结果处理
# ============================================================

def to_csv(products: list, output_path: str):
    """保存结果到CSV"""
    if not products:
        print("⚠️ 没有数据可保存")
        return

    fields = ["offerId", "title", "price", "saleCount", "supplier", "supplierId", "detailUrl", "keyword"]
    available = [f for f in fields if any(f in p for p in products)]
    for f in ["offerId", "title", "keyword"]:
        if f not in available:
            available.append(f)

    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=available, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(products)

    print(f"💾 已保存 {len(products)} 条记录到 {output_path}")


def print_results(products: list, limit: int = 10):
    """打印结果摘要"""
    if not products:
        print("⚠️ 没有找到商品")
        return

    print(f"\n📦 共获取 {len(products)} 条商品数据:")
    print("-" * 80)

    for i, p in enumerate(products[:limit]):
        title = (p.get("title") or "")[:50]
        price = p.get("price") or "待查"
        supplier = (p.get("supplier") or "")[:30]
        offer_id = p.get("offerId") or ""
        print(f"{i+1}. [{offer_id}] {title}")
        print(f"   💰 {price} | 🏭 {supplier}")

    if len(products) > limit:
        print(f"\n... 还有 {len(products) - limit} 条")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="1688商品搜索 - 德胧采购比价系统\n\n"
                    "推荐流程：\n"
                    "  1. 优先用官方API（最全）：\n"
                    "     export APP_KEY=xxx APP_SECRET=xxx\n"
                    "     python scripts/1688_search.py --provider official\n\n"
                    "  2. 其次用订单侠（免申请）：\n"
                    "     export DINGDANXIA_APIKEY=xxx\n"
                    "     python scripts/1688_search.py --provider dingdanxia\n\n"
                    "  3. 最后用搜索引擎（数据少，作为兜底）：\n"
                    "     python scripts/1688_search.py --provider browser",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--keywords", nargs="+",
                        default=["酒店门锁", "酒店床垫", "酒店枕头"],
                        help="搜索关键词列表")
    parser.add_argument("--provider", default="official",
                        choices=["official", "dingdanxia", "browser"],
                        help="API方案（默认official）")
    parser.add_argument("--max-pages", type=int, default=3,
                        help="最大页数（默认3）")
    parser.add_argument("--page-size", type=int, default=20,
                        help="每页条数（默认20，最大50）")
    parser.add_argument("--output", "-o", default=None,
                        help="输出CSV文件路径")
    parser.add_argument("--app-key", default=os.getenv("APP_KEY"),
                        help="1688官方API AppKey")
    parser.add_argument("--app-secret", default=os.getenv("APP_SECRET"),
                        help="1688官方API AppSecret")
    parser.add_argument("--api-key", default=os.getenv("DINGDANXIA_APIKEY"),
                        help="订单侠API Key")

    args = parser.parse_args()

    output_file = args.output
    if not output_file:
        ts = time.strftime("%Y%m%d_%H%M%S")
        kw_str = "_".join(args.keywords[:2])
        output_file = f"1688_search_{kw_str}_{ts}.csv"

    all_results = []

    for kw in args.keywords:
        print(f"\n{'=' * 60}")
        try:
            results = search(
                keyword=kw,
                provider=args.provider,
                app_key=args.app_key,
                app_secret=args.app_secret,
                api_key=args.api_key,
                max_pages=args.max_pages,
                page_size=args.page_size,
            )
            all_results.extend(results)
        except Exception as e:
            print(f"❌ 搜索 '{kw}' 失败: {e}")

    print(f"\n{'=' * 60}")
    print_results(all_results)

    if all_results:
        to_csv(all_results, output_file)

    print(f"\n✅ 完成！共搜索 {len(args.keywords)} 个关键词，获取 {len(all_results)} 条数据")


if __name__ == "__main__":
    main()
