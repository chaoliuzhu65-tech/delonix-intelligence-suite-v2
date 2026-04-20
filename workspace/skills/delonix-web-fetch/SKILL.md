---
name: delonix-web-fetch
description: 德胧AI龙虾军团开源网页抓取技能。基于trafilatura开源库抓取网页正文，支持AI指令提取。触发词：网页抓取、抓取网页、提取网页内容、web crawl、爬取、fetch url、总结网页、读取网页。
---

# Delonix Web Fetch（德胧网页抓取）

基于 `trafilatura` 开源库抓取网页正文内容，支持结构化提取。

## 依赖安装

```bash
pip3 install trafilatura -q
```

## 命令

```bash
python3 <skill-path>/scripts/web_fetch.py --url "URL" [选项]
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url, -u` | 目标网页URL | 必需 |
| `--instruction, -i` | AI处理指令 | 无 |
| `--format, -f` | 输出格式: json/text | text |

## 使用示例

```bash
# 抓取网页
python3 <skill-path>/scripts/web_fetch.py --url "https://example.com"

# 抓取并指定提取指令
python3 <skill-path>/scripts/web_fetch.py --url "https://ctrip.com/hotel/484448" -i "提取酒店名称、地址、价格"

# JSON输出
python3 <skill-path>/scripts/web_fetch.py --url "https://news.example.com" -f json
```

## 决策树

```
需要网页内容
├─ 有具体URL → delonix-web-fetch（抓取提取）
├─ 无URL需搜索 → delonix-web-search（搜索找URL）
└─ 深入抓取 → search找到URL → fetch提取详情
```

## 技术说明

- **底层库**: trafilatura（Python开源网页正文提取）
- **无需API Key**，完全自主可控
- 技能目录: `/home/gem/workspace/agent/workspace/skills/delonix-web-fetch`

## 已知限制

- JS动态渲染页面可能提取失败（fallback到原始HTML）
- 大页面自动截断到5000字符
