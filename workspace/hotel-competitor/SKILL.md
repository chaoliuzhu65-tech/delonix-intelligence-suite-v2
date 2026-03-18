---
name: hotel-competitor
description: "酒店竞争分析工具。用于分析目标酒店周边的竞争对手情况，生成竞争分析报告。支持三种模式：兜底版（手动输入/公开数据）、标准版（高德地图API）、进阶版（OTA价格抓取+网评分析）。适用场景：(1) 生成竞争对手调研报告 (2) 分析酒店周边竞争态势 (3) 竞品价格对比 (4) 市场占有率评估"
---

# 酒店竞争分析 Skill

用于分析酒店周边竞争对手情况，生成专业的竞争分析报告。

## 支持的能力等级

| 模式 | 数据源 | 功能 | 适用场景 |
|-----|-------|------|---------|
| **兜底版** | 手动输入/公开数据 | 基础分析、报告生成 | 零预算、快速验证 |
| **标准版** | 高德地图 API | 自动搜索、距离计算、地图可视化 | 单体酒店、区域管理 |
| **进阶版** | 高德 + 携程 + 美团 | OTA价格抓取、网评分析、自动监控 | 酒店集团、专业分析 |

## 快速使用

### 兜底版（无需 API Key）

```bash
# 手动输入竞争对手
python3 scripts/hotel_analysis.py --mode basic --hotel "天津瑞湾开元名都酒店" --competitors "天津瑞湾开元大酒店,今天国际酒店,全季酒店"

# 使用公开数据
python3 scripts/hotel_analysis.py --mode basic --hotel "天津瑞湾开元名都酒店" --auto-fetch
```

### 标准版（需要高德 API Key）

```bash
# 基础搜索（3公里）
python3 scripts/hotel_analysis.py --mode standard --hotel "天津瑞湾开元名都酒店" --location "117.709941,39.001039"

# 自定义范围（5公里）
python3 scripts/hotel_analysis.py --mode standard --hotel "天津瑞湾开元名都酒店" --location "117.709941,39.001039" --radius 5000
```

### 进阶版（需要多个 API）

```bash
# 完整分析
python3 scripts/hotel_analysis.py --mode advanced --hotel "天津瑞湾开元名都酒店" --location "117.709941,39.001039" --radius 5000 --fetch-ota-prices --analyze-reviews
```

## 配置 API

### 高德 API Key 申请

1. 访问 https://lbs.amap.com/
2. 注册/登录账号
3. 进入控制台 → 应用管理 → 创建应用
4. 创建 Key，选择「Web 服务」类型
5. 每日免费 5000 次调用

### 配置保存

```bash
mkdir -p config
echo '{"webServiceKey": "your_amap_key"}' > config/amap_key.json
```

## 输出报告

报告包含：
- 目标酒店基本信息
- 竞争对手列表（距离、评分、价格）
- 竞争分析（市场定位、价格区间）
- 建议（定价策略、服务提升）

---
*酒店竞争分析 SKILL - 让每一家酒店都拥有专业的竞争分析能力*
