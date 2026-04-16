#!/usr/bin/env python3
"""
德胧采购底价雷达 - 京东/淘宝 API 价格查询工具
支持个人开发者账号，无需企业资质

使用方法：
1. 填入你的 AppKey 和 AppSecret
2. 运行 python ecommerce_price_checker.py
"""

import requests
import hashlib
import time
import json
import sys
from typing import Optional, Dict, Any

# ========== 配置区 - 请填入你的凭证 ==========
JD_APP_KEY = "your_jd_appkey"
JD_APP_SECRET = "your_jd_appsecret"

TAOBAO_APP_KEY = "your_taobao_appkey"
TAOBAO_APP_SECRET = "your_taobao_appsecret"
# ===========================================


class JdPriceChecker:
    """京东价格查询"""

    BASE_URL = "https://api.jd.com/routerjson"

    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret

    def _generate_sign(self, params: Dict) -> str:
        """生成京东签名"""
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = "".join([f"{k}{v}" for k, v in sorted_params]) + self.app_secret
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()

    def get_item_info(self, sku_id: str) -> Optional[Dict]:
        """获取京东商品信息"""
        params = {
            "app_key": self.app_key,
            "method": "jingdong.item.base.info.get",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "format": "json",
            "v": "2.0",
            "360buy_param_json": json.dumps({"skuId": sku_id})
        }
        params["sign"] = self._generate_sign(params)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"京东API调用失败: {e}")
        return None

    def search_items(self, keyword: str, page: int = 1) -> Optional[Dict]:
        """搜索京东商品"""
        params = {
            "app_key": self.app_key,
            "method": "jingdong.item.search.search",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "format": "json",
            "v": "2.0",
            "360buy_param_json": json.dumps({
                "keyword": keyword,
                "page": page,
                "pageSize": 10
            })
        }
        params["sign"] = self._generate_sign(params)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"京东搜索API调用失败: {e}")
        return None


class TaobaoPriceChecker:
    """淘宝价格查询"""

    BASE_URL = "https://gw.api.taobao.com/router/rest"

    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret

    def _generate_sign(self, params: Dict) -> str:
        """生成淘宝签名"""
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        sign_str = "".join([f"{k}{v}" for k, v in sorted_params]) + self.app_secret
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()

    def get_item(self, num_iid: str) -> Optional[Dict]:
        """获取淘宝商品信息"""
        params = {
            "app_key": self.app_key,
            "method": "taobao.item.get",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "format": "json",
            "v": "2.0",
            "num_iid": num_iid
        }
        params["sign"] = self._generate_sign(params)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"淘宝API调用失败: {e}")
        return None

    def search_items(self, q: str, page: int = 1) -> Optional[Dict]:
        """搜索淘宝商品"""
        params = {
            "app_key": self.app_key,
            "method": "taobao.items.search",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "format": "json",
            "v": "2.0",
            "q": q,
            "page_no": page,
            "page_size": 10
        }
        params["sign"] = self._generate_sign(params)

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"淘宝搜索API调用失败: {e}")
        return None


def demo():
    """演示模式 - 模拟输出"""
    print("=" * 60)
    print("德胧采购底价雷达 - 价格查询演示")
    print("=" * 60)
    print()
    print("📝 当前为演示模式，未配置真实API凭证")
    print("💡 请先申请京东/淘宝开放平台个人开发者账号")
    print("   - 京东: https://open.jd.com")
    print("   - 淘宝: https://open.taobao.com")
    print()
    print("-" * 60)
    print("模拟输出示例：")
    print("-" * 60)
    print()
    print("【京东商品搜索结果】关键词: 白菜")
    print("  1. 精选白菜 净菜 300g    ¥2.99   京东自营")
    print("  2. 有机白菜 500g        ¥4.50   京东生鲜")
    print("  3. 新鲜白菜 约1kg       ¥1.98   京东拼购")
    print()
    print("【淘宝商品搜索结果】关键词: 矿泉水")
    print("  1. 农夫山泉 550ml*24瓶  ¥29.9   淘宝精选")
    print("  2. 怡宝 555ml*24瓶      ¥32.0   淘宝超市")
    print()
    print("【价格分析建议】")
    print("  白菜参考采购价: ¥1.5-3.0/kg")
    print("  矿泉水参考价: ¥1.2-1.5/瓶 (24瓶装)")
    print()
    print("=" * 60)
    print("⚠️  以上为演示数据，实际价格请配置API后查询")
    print("=" * 60)


def main():
    """主函数"""
    # 检查是否配置了真实凭证
    if JD_APP_KEY == "your_jd_appkey" and TAOBAO_APP_KEY == "your_taobao_appkey":
        demo()
        return

    # 真实模式
    jd = JdPriceChecker(JD_APP_KEY, JD_APP_SECRET)
    tb = TaobaoPriceChecker(TAOBAO_APP_KEY, TAOBAO_APP_SECRET)

    # 示例：搜索商品
    if len(sys.argv) > 1:
        keyword = " ".join(sys.argv[1:])
        print(f"搜索关键词: {keyword}")
        print("-" * 40)

        # 京东搜索
        jd_result = jd.search_items(keyword)
        if jd_result:
            print("京东结果:", json.dumps(jd_result, ensure_ascii=False, indent=2))

        # 淘宝搜索
        tb_result = tb.search_items(keyword)
        if tb_result:
            print("淘宝结果:", json.dumps(tb_result, ensure_ascii=False, indent=2))
    else:
        print("用法: python ecommerce_price_checker.py <商品关键词>")


if __name__ == "__main__":
    main()
