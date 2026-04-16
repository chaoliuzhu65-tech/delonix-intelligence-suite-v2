#!/usr/bin/env python3
"""
德胧1688商品搜索工具 v1.0
直接调用1688官方搜索接口，无需API Key
"""

import requests
import json
import sys
from urllib.parse import quote

# 1688搜索接口（官方公开接口）
SEARCH_URL = "https://s.1688.com/youyuan/index.htm?tab=simpleSearch&property=&keywords={keyword}&pageOffset={page}&charset=utf-8& specialChars="

# 1688商品详情接口（通过搜索结果获取）
DETAIL_URL = "https://detail.1688.com/offer/{offer_id}.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "https://www.1688.com/",
}


def search_products(keyword, page=1, limit=20):
    """
    搜索1688商品
    :param keyword: 搜索关键词
    :param page: 页码
    :param limit: 返回数量
    :return: 商品列表
    """
    url = SEARCH_URL.format(
        keyword=quote(keyword),
        page=(page - 1) * 20
    )
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            # 尝试提取商品数据
            text = response.text
            
            # 简单解析：提取价格和标题
            products = []
            
            # 方法1: 通过正则提取
            import re
            
            # 提取offer ID
            offer_ids = re.findall(r'"offerId":(\d+)', text)
            titles = re.findall(r'"title":"([^"]+)"', text)
            prices = re.findall(r'"price":"([^"]+)"', text)
            company_names = re.findall(r'"companyName":"([^"]+)"', text)
            moqs = re.findall(r'"moq":(\d+)', text)
            is_gold = re.findall(r'"isGoldSupplier":(true|false)', text)
            
            count = min(len(offer_ids), limit)
            for i in range(count):
                product = {
                    "offer_id": offer_ids[i] if i < len(offer_ids) else "",
                    "title": titles[i] if i < len(titles) else "",
                    "price": prices[i] if i < len(prices) else "",
                    "company_name": company_names[i] if i < len(company_names) else "",
                    "moq": moqs[i] if i < len(moqs) else "",
                    "is_gold_supplier": is_gold[i] == "true" if i < len(is_gold) else False,
                }
                products.append(product)
            
            return {
                "success": True,
                "keyword": keyword,
                "count": len(products),
                "products": products
            }
        else:
            return {
                "success": False,
                "error": f"HTTP {response.status_code}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def format_product(p):
    """格式化输出单个商品"""
    moq_str = f"{p.get('moq', 'N/A')}件起" if p.get('moq') else "N/A"
    gold_str = "🏅金牌供应商" if p.get('is_gold_supplier') else ""
    return f"""
📦 {p.get('title', 'N/A')}
💰 价格: ¥{p.get('price', 'N/A')}
🏭 供应商: {p.get('company_name', 'N/A')} {gold_str}
📊 起订量: {moq_str}
🔗 链接: https://detail.1688.com/offer/{p.get('offer_id', '')}.html
"""


def main():
    if len(sys.argv) < 2:
        print("用法: python alibaba_search.py <搜索关键词> [页码]")
        sys.exit(1)
    
    keyword = sys.argv[1]
    page = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    print(f"🔍 搜索1688: {keyword} (第{page}页)")
    print("=" * 60)
    
    result = search_products(keyword, page)
    
    if result["success"]:
        print(f"✅ 找到 {result['count']} 个商品\n")
        for i, p in enumerate(result["products"], 1):
            print(f"{i}. {format_product(p)}")
            print("-" * 60)
    else:
        print(f"❌ 搜索失败: {result.get('error', '未知错误')}")


if __name__ == "__main__":
    main()
