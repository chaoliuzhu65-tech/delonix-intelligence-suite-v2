---
name: delonix-web-search
description: 德胧AI龙虾军团开源网络搜索技能。基于DuckDuckGo开源搜索库（ddgs），无需API Key，所有AI伙伴均可使用。触发词：搜索、网页搜索、搜一下、查一下、web search、搜索摘要、查资料、搜索引擎。
---

# Delonix Web Search（德胧网络搜索）

基于DuckDuckGo开源搜索库 `ddgs`，无需API Key，所有AI伙伴开箱即用。

## 依赖安装

```bash
pip3 install ddgs -q
```

## 命令

```bash
python3 <skill-path>/scripts/web_search.py "关键词" [选项]
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--num N` / `-n N` | 返回结果数量 | 10 |
| `--instruction TEXT` / `-i TEXT` | AI处理指令 | 无 |
| `--format json\|text` / `-f` | 输出格式 | text |
| `--news` | 搜索新闻 | 否 |

## 使用示例

```bash
# 基础搜索
python3 <skill-path>/scripts/web_search.py "天津瑞湾开元名都酒店"

# 搜索并限制数量
python3 <skill-path>/scripts/web_search.py "竞品动态" -n 5

# 搜索新闻
python3 <skill-path>/scripts/web_search.py "酒店行业新闻" --news

# JSON输出（程序调用）
python3 <skill-path>/scripts/web_search.py "德胧集团" -f json
```

## 决策树

```
用户需要网络信息
├─ 有具体URL → 使用 miaoda-web-fetch 抓取页面
├─ 无具体URL，需要搜索 → 使用本技能 delonix-web-search
└─ 先搜索再深入 → search获取URL → miaoda-web-fetch抓详情
```

## 依赖说明

- **Python包**: `ddgs`（DuckDuckGo开源搜索库）
- **无需API Key**，纯开源方案
- 所有AI伙伴均可独立安装使用
- 技能目录：`/home/gem/workspace/agent/workspace/skills/delonix-web-search`

## 已知限制

- DuckDuckGo在中国大陆访问不稳定，服务器环境可能需要代理
- 如搜索失败，检查网络连通性或配置代理
