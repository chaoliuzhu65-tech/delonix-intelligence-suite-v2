# 德胧AI技能库 - 完整版

> **创建时间**: 2026-04-08
> **整理者**: 晁留柱的助手
> **用途**: 供所有AI伙伴学习、复用、反馈

---

## 📚 技能库目录

### 一、妙搭内置技能（ miaoda-* ）

| 技能名称 | 文件位置 | 功能说明 |
|----------|----------|----------|
| **文档解析** | miaoda-doc-parse | PDF/Word/Excel/PPT转Markdown |
| **图片理解** | miaoda-image-understanding | 图片内容识别分析 |
| **语音转文字** | miaoda-speech-to-text | 音频/会议录音转文字 |
| **文字生成图片** | miaoda-text-gen-image | AI生成配图、封面 |
| **网页搜索** | miaoda-web-search | 关键词搜索+AI摘要 |
| **网页抓取** | miaoda-web-fetch | 抓取URL内容并总结 |

### 二、飞书集成技能（ feishu-* ）

| 技能名称 | 功能说明 |
|----------|----------|
| **飞书消息** | 发送卡片/文本消息到群或个人 |
| **飞书日历** | 创建/查询/管理日程会议 |
| **飞书任务** | 任务创建、分配、跟踪 |
| **飞书多维表格** | Bitable数据管理 |
| **飞书文档** | 云文档创建/读取/更新 |
| **飞书知识库** | Wiki知识库管理 |

### 三、德胧专属技能（ delong-* ）

| 技能名称 | 功能说明 |
|----------|----------|
| **值班日志** | delong-duty-log | 自动生成酒店值班日志 |
| **客诉处理** | delong-complaint-handler | 客诉自动分类处理 |
| **入住率预测** | delong-occupancy-forecast | 数据预测 |
| **竞品分析** | hotel-competitor-analysis | 酒店竞品数据监控 |
| **排班管理** | delong-scheduling | 智能排班建议 |
| **质检巡检** | delong-quality-inspection | 数字化巡检 |
| **宾客提醒** | delong-guest-reminder | 自动提醒服务 |
| **应急方案** | delong-emergency-plan | 应急处理指南 |
| **入住检查** | delong-inspection | 入住全流程检查 |

### 四、自建/实验技能

| 技能名称 | 功能说明 |
|----------|----------|
| **播客生成** | ai-podcast | TTS+ffmpeg视频播客 |
| **微信公众号** | wechat-mp-reader | 读取公众号文章 |
| **头条抓取** | toutiao-fetch | 头条数据获取 |
| **AI协作协议** | ai-partner-protocol | 多AI协同工作 |
| **知识共享池** | shared-pool | 统一知识沉淀机制 |

### 五、第三方集成

| 技能名称 | 功能说明 |
|----------|----------|
| **NotebookLM** | notebook-lm | AI播客/视频生成 |
| **每日AI新闻** | ai-news-daily | 定时推送AI新闻 |
| **知识进化** | kb-evolver | 知识库自动整理 |

---

## 🎯 使用方法

### 读取技能详情
```python
# 直接读取SKILL.md文件
read("skills/技能名/SKILL.md")
```

### 应用技能
```python
# 根据SKILL.md中的指引调用对应工具
```

---

## 📊 技能分类统计

| 类别 | 数量 |
|------|------|
| 妙搭内置 | 6 |
| 飞书集成 | 6 |
| 德胧专属 | 9 |
| 自建技能 | 5 |
| 第三方 | 3 |
| **合计** | **29** |

---

## 🔄 技能更新记录

### 2026-04-19 新增
- ✅ **德胧舆情采集龙虾工具**（delonix-web-intelligence）
  - 整合 miaoda-web-search + AutoCLI + 飞书卡片
  - 路径：`skills/delonix-web-intelligence/SKILL.md`
  - 触发词：舆情、情报、网情、监控、行业动态

### 2026-04-08 新增
- ✅ 播客视频生成技术手册
- ✅ 多AI知识共享池
- ✅ AI协作协议

---

## 📝 反馈机制

请各AI伙伴：
1. **学习** - 阅读感兴趣的技能
2. **应用** - 在实际工作中使用
3. **反馈** - 将使用心得写入共享池

格式：
```markdown
## 技能反馈：[技能名称]
- 使用场景：xxx
- 效果评价：xxx
- 改进建议：xxx
```

---

*本技能库由晁留柱的助手维护*
*持续更新中...*

### 2026-04-19 新增（v3.0通用版）
- ✅ **hotel-intelligence-suite**（酒店舆情情报综合工具箱 v3.0通用版）
  - 通用版，支持任意酒店集团复用，无硬编码
  - 整合：miaoda搜索 + BettaFish(17k Stars) + 抖音监控 + 飞书卡片 + AI风险分析
  - GitHub: chaoliuzhu65-tech/hotel-intelligence-suite
  - 触发词：舆情、情报、网情、监控、风险分析、酒店日报

### 2026-04-20 新增（妙搭fork开源版）
- ✅ **delonix-web-search**（德胧开源网络搜索）
  - 基于DuckDuckGo开源库ddgs，**无需API Key**
  - 所有AI伙伴均可独立安装使用
  - 触发词：搜索、网页搜索、搜一下、查资料
- ✅ **delonix-web-fetch**（德胧开源网页抓取）
  - 基于trafilatura开源库，**无需API Key**
  - 所有AI伙伴均可独立安装使用
  - 触发词：网页抓取、提取网页内容、web crawl
- ✅ **delonix-doc-parse**（德胧开源文档解析）
  - 基于pdfplumber/python-docx，**纯本地解析无需上传**
  - 支持PDF/Word/Excel/PPT/TXT
  - 触发词：文档解析、解析PDF、解析Word
- ✅ **delonix-image-understanding**（德胧开源图片理解）
  - 封装系统内置图片理解能力
  - 触发词：图片理解、图片分析、图片描述

**安装包位置**（可直接安装）：
- `~/.npm-global/lib/node_modules/openclaw/skills/` 下skills目录
- GitHub: chaoliuzhu65-tech/delonix-intelligence-suite-v2

**Python依赖**：
```bash
pip3 install ddgs trafilatura pdfplumber python-docx python-pptx openpyxl -q
```

### 2026-04-19 v3.1 两层架构更新
- ✅ **hotel-intelligence-suite v3.1**（两层架构版）
  - 舆情风险层：每2小时快捷扫描，黑猫/微博/抖音全覆盖
  - 差评维度层：每日10点采集，12维度OTA分类管理
  - 支持交互调整：调频率/增竞品/改推送/暂停任务等
  - 飞书多维表格：Jx5Ibjc3WaJVgwsUOzQcHq56nyc
  - GitHub: chaoliuzhu65-tech/hotel-intelligence-suite
  - 触发词：舆情、情报、网情、监控、风险分析、酒店日报、差评管理
