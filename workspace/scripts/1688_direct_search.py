#!/usr/bin/env python3
"""
1688 直接搜索工具 - 无需API Key
使用httpx模拟搜索，获取批发价格信息
"""
import sys
import json
import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

async def search_1688(keyword, limit=10):
    """
    直接搜索1688，返回商品列表和价格
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }

    # 1688搜索URL
    search_url = f"https://s.1688.com/youyuan/index.htm?keywords={quote_plus(keyword)}&sugType="

    print(f"🔍 搜索关键词: {keyword}")
    print(f"📎 搜索URL: {search_url}")
    print("\n" + "="*60)

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(search_url, headers=headers)
            print(f"📡 状态码: {response.status_code}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                # 尝试提取商品信息
                products = []

                # 方法1: 查找搜索结果中的商品元素
                # 1688的搜索结果页面结构可能变化，这里用通用方法
                items = soup.find_all('div', class_=['item', 'offer-item', 'product-item'])

                if not items:
                    # 方法2: 查找所有可能的商品卡片
                    items = soup.find_all('div', attrs={'class': lambda x: x and 'offer' in x.lower()})

                if not items:
                    # 方法3: 查找包含价格信息的元素
                    items = soup.find_all('div', attrs={'class': lambda x: x and 'price' in x.lower()})

                print(f"📦 找到 {len(items)} 个商品元素")

                # 尝试直接获取页面中的价格数据
                price_elements = soup.find_all(text=lambda t: t and ('¥' in t or '元' in t) and any(c.isdigit() for c in t))

                if price_elements:
                    print(f"💰 找到 {len(price_elements)} 个价格元素")
                    for pe in price_elements[:5]:
                        print(f"   - {pe.strip()[:50]}")

                # 保存完整页面供分析
                with open('/tmp/1688_search_result.html', 'w', encoding='utf-8') as f:
                    f.write(response.text)
                print(f"\n✅ 页面已保存到 /tmp/1688_search_result.html")

                return {
                    "keyword": keyword,
                    "status": "success" if price_elements else "partial",
                    "items_found": len(items),
                    "prices_found": len(price_elements),
                    "page_saved": "/tmp/1688_search_result.html"
                }
            else:
                return {
                    "keyword": keyword,
                    "status": "error",
                    "status_code": response.status_code
                }

    except Exception as e:
        print(f"❌ 错误: {e}")
        return {
            "keyword": keyword,
            "status": "error",
            "error": str(e)
        }

def main():
    if len(sys.argv) < 2:
        print("用法: python3 1688_direct_search.py <关键词>")
        print("示例: python3 1688_direct_search.py 酒店蓝牙门锁")
        sys.exit(1)

    keyword = sys.argv[1]

    print(f"\n{'='*60}")
    print(f"🏨 1688 酒店采购价格查询")
    print(f"{'='*60}\n")

    result = asyncio.run(search_1688(keyword))

    print(f"\n{'='*60}")
    print("📊 查询结果:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
