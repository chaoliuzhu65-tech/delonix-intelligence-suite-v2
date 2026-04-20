#!/usr/bin/env python3
"""
德胧AI龙虾军团 - 图片理解工具（备用CLI接口）
推荐直接使用系统的 image_understanding 工具，此脚本为备用

用法:
  python3 image_understand.py --image <图片路径或URL> --prompt "描述需求"
"""

import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description="德胧AI龙虾军团图片理解工具（建议使用系统内置image_understanding工具）")
    parser.add_argument("--image", "-i", required=True, help="图片路径或URL")
    parser.add_argument("--prompt", "-p", default="请描述这张图片的内容", help="分析指令")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="text", help="输出格式")
    args = parser.parse_args()

    print("注意：建议直接使用系统内置的 image_understanding 工具，本脚本仅作为备用接口。")
    print(f"\n图片: {args.image}")
    print(f"指令: {args.prompt}")
    print(f"\n请调用系统的 image_understanding 工具获取AI分析结果。")

if __name__ == "__main__":
    main()
