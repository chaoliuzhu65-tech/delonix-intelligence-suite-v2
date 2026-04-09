# 通用商旅出行规划技能

## 来源
GitHub: https://github.com/chaoliuzhu65-tech/universal-travel-planner-skill

## 技能概述
一站式AI商旅出行规划 + 全平台酒店比价 + 精美HTML报告生成

## 核心功能
- 🚄 实时交通：12306 MCP 实时查票 + 高德路径规划 + 航班搜索
- 🏨 全平台酒店比价：携程/飞猪/去哪儿/Booking/Agoda
- 📊 智能预算：经济/舒适/商务三档标准
- 📱 HTML报告生成
- 🗺️ 高德地图集成
- 📋 出行清单

## 安装路径
`skills/universal-travel-planner/SKILL.md`

## 环境变量
- AMAP_WEB_KEY（可选）
- AMAP_JSAPI_KEY（可选）
- AMAP_SECURITY_CODE（可选）

## MCP配置
```json
{
  "mcpServers": {
    "12306-mcp": {
      "command": "npx",
      "args": ["-y", "12306-mcp"]
    }
  }
}
```

## 发布者
小八(workbuddy) via 方源兵
## 添加时间
2026-04-09
