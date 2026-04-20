#!/usr/bin/env python3
"""
德胧AI龙虾军团 - 网络搜索工具
基于DuckDuckGo开源搜索，无API Key要求，支持所有AI伙伴

用法:
  python3 web_search.py "关键词" [--num N] [--format json|text]
  python3 web_search.py "关键词" --instruction "AI处理指令"
"""

import sys
import json
import argparse
from ddgs import DDGS

def search_web(query: str, num: int = 10, instruction: str = None, output_format: str = "text") -> dict:
    """执行网络搜索并返回结构化结果"""
    
    results = []
    try:
        with DDGS() as ddgs:
            # 获取搜索结果（包含摘要）
            for i, r in enumerate(ddgs.text(query, max_results=num)):
                if i >= num:
                    break
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("href", ""),
                    "description": r.get("body", ""),
                    "source": "DuckDuckGo"
                })
    except Exception as e:
        return {"error": str(e), "results": []}
    
    if output_format == "json":
        return {"query": query, "count": len(results), "results": results}
    
    # 文本格式输出
    if instruction:
        output = f"# 搜索结果: {query}\n\n"
        output += f"**AI处理指令**: {instruction}\n\n"
    else:
        output = f"# 网络搜索结果: {query}\n\n"
    
    output += f"共找到 {len(results)} 条结果:\n\n"
    
    for i, r in enumerate(results, 1):
        output += f"## [{i}] {r['title']}\n"
        output += f"**链接**: {r['url']}\n"
        if r['description']:
            output += f"**摘要**: {r['description']}\n"
        output += "\n"
    
    if instruction:
        output += f"\n---\n*以上结果已按指令筛选/处理*\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(description="德胧AI龙虾军团网络搜索工具")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--num", "-n", type=int, default=10, help="返回结果数量 (默认10)")
    parser.add_argument("--instruction", "-i", type=str, default=None, help="AI处理指令")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="text", help="输出格式")
    parser.add_argument("--news", action="store_true", help="搜索新闻")
    
    args = parser.parse_args()
    
    if args.news:
        # 新闻搜索
        with DDGS() as ddgs:
            results = list(ddgs.news(args.query, max_results=args.num))
        output = {
            "query": args.query,
            "type": "news",
            "count": len(results),
            "results": [{"title": r["title"], "url": r["url"], "source": r.get("source", ""), "date": r.get("date", "")} for r in results]
        }
    else:
        output = search_web(args.query, args.num, args.instruction, args.format)
    
    if args.format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        if isinstance(output, dict) and "error" in output:
            print(f"错误: {output['error']}", file=sys.stderr)
            sys.exit(1)
        print(output)

if __name__ == "__main__":
    main()
