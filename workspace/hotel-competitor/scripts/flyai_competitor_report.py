#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
天津瑞湾竞品价格监控报告生成
使用FlyAI CLI获取实时价格数据

使用方法:
  python3 flyai_competitor_report.py [--checkin YYYY-MM-DD] [--checkout YYYY-MM-DD]
"""

import subprocess
import json
import sys
from datetime import datetime, timedelta

FLYAI_CLI = "/home/gem/.npm-global/lib/node_modules/@fly-ai/flyai-cli/dist/flyai-bundle.cjs"

def search_hotels(dest_name, checkin, checkout):
    """调用FlyAI搜索酒店"""
    cmd = [
        FLYAI_CLI, "search-hotel",
        "--dest-name", dest_name,
        "--check-in-date", checkin,
        "--check-out-date", checkout
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except:
        return None

def format_report(hotel_name, data, checkin, checkout):
    """生成Markdown报告"""
    hotels = data['data']['itemList'][:20]
    
    report = []
    report.append(f"# 天津瑞湾开元名都酒店 · 竞品价格监控报告")
    report.append(f"")
    report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"**监控日期**: {checkin} → {checkout}")
    report.append(f"**数据来源**: 飞猪FlyAI实时查询")
    report.append(f"")
    report.append(f"---")
    report.append(f"")
    report.append(f"## 竞品价格一览（按价格升序）")
    report.append(f"")
    
    # 解析价格（处理 ¥153 格式）
    def parse_price(p):
        if not p:
            return None
        s = str(p).replace('¥', '').strip()
        try:
            return int(s)
        except:
            return None

    # 按价格排序
    sorted_hotels = sorted(hotels, key=lambda x: parse_price(x.get('price')) or 9999)
    
    for i, h in enumerate(sorted_hotels, 1):
        price = h.get('price', 'N/A')
        star = h.get('star', '未知')
        name = h.get('name', '未知')
        address = h.get('address', '未知')
        brand = h.get('brandName') or '无'
        
        report.append(f"{i}. **{name}**")
        report.append(f"   - 星级: {star} | 价格: {price} | 品牌: {brand}")
        report.append(f"   - 地址: {address}")
        report.append(f"")
    
    # 价格分布统计
    prices = [parse_price(h.get('price')) for h in hotels if parse_price(h.get('price'))]
    if prices:
        report.append(f"---")
        report.append(f"")
        report.append(f"## 价格分析")
        report.append(f"")
        report.append(f"| 指标 | 数值 |")
        report.append(f"|------|------|")
        report.append(f"| 最低价 | ¥{min(prices)} |")
        report.append(f"| 最高价 | ¥{max(prices)} |")
        report.append(f"| 平均价 | ¥{sum(prices)//len(prices)} |")
        report.append(f"| 监控数量 | {len(prices)}家 |")
        report.append(f"")
        
        # 天津瑞湾参考价对比
        report.append(f"## 天津瑞湾开元名都酒店参考")
        report.append(f"")
        report.append(f"| 房型 | 协议价 | 说明 |")
        report.append(f"|------|--------|------|")
        report.append(f"| 豪华海河大床 | ¥350 | 散客/协议价 |")
        report.append(f"| 高级大床 | ¥240 | 散客价 |")
        report.append(f"| 套房 | ¥480 | 套房价 |")
    
    return "\n".join(report)

if __name__ == "__main__":
    # 默认明后天
    checkin = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    checkout = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
    
    if len(sys.argv) > 1:
        checkin = sys.argv[1]
    if len(sys.argv) > 2:
        checkout = sys.argv[2]
    
    print(f"正在查询天津滨海新区 {checkin} → {checkout} 酒店价格...", file=sys.stderr)
    
    data = search_hotels("天津滨海新区", checkin, checkout)
    
    if not data:
        print("❌ 查询失败，请检查FlyAI配置", file=sys.stderr)
        sys.exit(1)
    
    report = format_report("天津瑞湾开元名都酒店", data, checkin, checkout)
    print(report)
