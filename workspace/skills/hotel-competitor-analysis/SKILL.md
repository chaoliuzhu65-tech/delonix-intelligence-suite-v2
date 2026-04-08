# 酒店竞品分析 & 价格监测 Skill

> 借助AI工具实现酒店竞品数据采集、实时价格监控、市场洞察的系统化方法。

## 核心能力矩阵

| 场景 | 推荐工具/方法 | 难度 | 自动化 |
|------|-------------|------|--------|
| OTA平台酒店价格抓取 | miaoda-studio-cli web-crawl | ⭐ | 可定时 |
| 携程/去哪儿/美团 | Python Scrapy + Playwright | ⭐⭐⭐ | ✅ |
| Google Hotels 价格 | Apify Google Hotels Scraper | ⭐⭐ | ✅ |
| 酒店评论/舆情分析 | 小红书/大众点评 + AI总结 | ⭐⭐ | 手动 |
| 竞品动态追踪 | 定时web-crawl + 飞书通知 | ⭐ | ✅ |
| 竞品官网价格 | miaoda-studio-cli web-crawl | ⭐ | ✅ |
| 行业报告/文章 | 头条/公众号抓取 | ⭐ | ✅ |

## 竞品分析核心指标

### 1. 价格指标
- **ADR**（平均房价）= 总收入 / 售出客房数
- **RevPAR**（每可用客房收入）= ADR × 入住率
- **动态价格差**：与竞品的价格差值追踪

### 2. 运营指标
- 入住率（Occupancy Rate）
- 评分（点评分数）
- 好评率 / 差评率
- 预订取消率

### 3. 市场指标
- 市场占有率（通过STR/HotStats）
- 渠道流量（SimilarWeb）
- 搜索引擎排名

## 工具链组合方案

### 方案A：轻量级（推荐德胧先试）
```
miaoda-studio-cli web-crawl
    ↓ 抓取携程/去哪儿/美团酒店页面
    ↓ 提取：价格、房型、评分
    ↓ 定时任务 cron 每日抓取
    ↓ 飞书卡片通知结果
```
**适合**：单店或少量竞品，简单高效

### 方案B：进阶方案
```
Python (Scrapy + Playwright)
    ↓ 多平台并发抓取
    ↓ 数据清洗 pandas
    ↓ MySQL/多维表格存储
    ↓ Tableau 可视化
```
**适合**：多店集团、需要长期数据积累

### 方案C：专业方案
```
Apify Google Hotels Scraper
SimilarWeb 市场分析
八爪鱼RPA（携程批量）
STR/HotStats 行业报告
```
**适合**：大型酒店集团、专业收益管理

## 数据来源优先级（国内）

| 优先级 | 平台 | 数据类型 | 抓取难度 |
|--------|------|---------|---------|
| 🥇 | 携程 | 价格、房型、评分、入住率 | ⭐⭐⭐ |
| 🥇 | 美团 | 价格、团购、点评 | ⭐⭐⭐ |
| 🥈 | 去哪儿 | 价格、返现、评分 | ⭐⭐⭐ |
| 🥈 | 飞猪 | 价格、会员价 | ⭐⭐⭐ |
| 🥉 | 大众点评 | 点评、团购、评分 | ⭐⭐ |
| 🥉 | 小红书 | 口碑、探店 | ⭐⭐ |

## 实施路线图（德胧版）

### Phase 1：建立竞品名单（第1周）
- 确定核心竞品（5-10家）
- 建立竞品列表多维表格
- 手动抓取基准数据

### Phase 2：自动化价格监测（第2-3周）
- 部署 miaoda-studio-cli 定时任务
- 每日自动抓取竞品价格
- 存入共享池多维表格

### Phase 3：价格预警（第4周）
- 设置价格阈值（如竞品低于我们10%）
- 触发飞书通知
- 生成价格对比日报

### Phase 4：智能分析（月度）
- AI分析价格趋势
- 生成竞品分析报告
- 建议调价策略

## 飞书通知示例（卡片格式）

```json
{
  "config": {"wide_screen_mode": true},
  "header": {
    "title": {"tag": "plain_text", "content": "📊 竞品价格日报 - 2026-04-08"},
    "template": "red"
  },
  "elements": [
    {"tag": "div", "text": {"tag": "lark_md", "content": "**今日竞品价格对比**"}},
    {"tag": "div", "text": {"tag": "lark_md", "content": "🏨 天津瑞湾开元名都：**¥580**"}},
    {"tag": "div", "text": {"tag": "lark_md", "content": "🏨 竞品A：**¥520**（低10.3%）⚠️"}},
    {"tag": "div", "text": {"tag": "lark_md", "content": "🏨 竞品B：**¥620**（高6.9%）✅"}},
    {"tag": "hr"},
    {"tag": "div", "text": {"tag": "lark_md", "content": "建议：考虑对周末价格进行下调5%促销"}}
  ]
}
```

## 参考资源

- 携程酒店爬虫：[Python携程价格抓取(CSDN)](https://blog.csdn.net/2503_91057718/article/details/156994698)
- 酒店竞品分析：[Hotel Competitor Analysis (EHL)](https://hospitalityinsights.ehl.edu/hotel-competitor-analysis)
- Google Hotels Scraper：[Apify](https://apify.com/dainty_screw/google-hotels-scraper-for-price-extraction)
- Thunderbit（无代码爬虫）：[财经头条报道](https://cj.sina.cn/articles/view/7879922979/1d5ae152301901k69e)

---

**版本**: v1.0  
**创建日期**: 2026-04-08  
**作者**: 晁留柱的助手（小柱）  
**状态**: 已验证方案可行性，待德胧落地实施
