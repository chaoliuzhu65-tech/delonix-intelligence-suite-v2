#!/usr/bin/env python3
"""
德胧AI龙虾军团 - 网页抓取工具
基于trafilatura开源库，提取网页正文内容，支持AI总结

用法:
  python3 web_fetch.py --url "https://example.com" [选项]
  python3 web_fetch.py --url "https://example.com" --instruction "提取关键信息"
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
import ssl
import trafilatura


def fetch_url(url: str, instruction: str = None, output_format: str = "text") -> dict:
    """抓取网页并提取正文"""

    # 创建SSL上下文（处理证书问题）
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        # 使用trafilatura下载并提取正文
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            # trafilatura失败，尝试直接下载
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
                html_content = response.read().decode('utf-8', errors='ignore')

            # 提取正文
            result = trafilatura.extract(html_content, url=url)
            if result:
                content = result
            else:
                # 降级：简单HTML标签去除
                import re
                content = re.sub(r'<[^>]+>', ' ', html_content)
                content = re.sub(r'\s+', ' ', content).strip()
        else:
            content = downloaded

    except Exception as e:
        return {"error": f"抓取失败: {str(e)}", "url": url, "content": ""}

    if output_format == "json":
        return {
            "url": url,
            "content": content[:5000] if content else "",
            "instruction": instruction,
            "source": "trafilatura"
        }

    # 文本格式
    output = f"# 网页内容抓取\n\n**URL**: {url}\n\n"
    if instruction:
        output += f"**处理指令**: {instruction}\n\n"

    if not content:
        return {"error": "无法提取网页内容", "url": url}

    output += f"## 正文内容\n\n{content}\n"

    if instruction:
        output += f"\n---\n*请根据指令「{instruction}」提取/分析上述内容*\n"

    return output


def main():
    parser = argparse.ArgumentParser(description="德胧AI龙虾军团网页抓取工具")
    parser.add_argument("--url", "-u", required=True, help="目标网页URL")
    parser.add_argument("--instruction", "-i", type=str, default=None, help="AI处理指令")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="text", help="输出格式")

    args = parser.parse_args()

    result = fetch_url(args.url, args.instruction, args.format)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if isinstance(result, dict) and "error" in result:
            print(f"错误: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(result)


if __name__ == "__main__":
    main()
