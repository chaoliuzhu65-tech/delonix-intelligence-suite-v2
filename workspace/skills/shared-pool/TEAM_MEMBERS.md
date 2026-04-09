# 团队成员名单

> 最后更新: 2026-04-09 | 来源：飞书AI协作群(oc_36d47adad05d3ca8e93164ebc8bfca40)

## AI伙伴完整名单

| ID | 名称 | 昵称 | Open ID | Bot App ID | 平台 | 状态 | 备注 |
|----|------|------|---------|------------|------|------|------|
| 1 | 晁留柱的助手 | 小柱 | ou_8dd4dc0180a2fb74c692f17b94c94d8e | cli_a948e1a790b8dcdd | OpenClaw/妙搭 | 🟢 活跃 | 本实例 |
| 2 | arkclaw版openclaw | ArkClaw | ou_3ccf1eaae932cf5330813ef82cdfba83 | — | 火山引擎 | 🟢 活跃 | 知识库维护 |
| 3 | QclawAI助手 | Qclaw | ou_8b317f48061dc791c64546264c34db4a | — | Qclaw平台 | 🟢 活跃 | 跨平台通信 |
| 4 | 腾讯云Openclaw机器人 | 腾讯云Openclaw | ou_7ffafa7fc8ca551da1bc0c97c186ad89 | — | 腾讯云 | 🟢 活跃 | 定时任务调度 |
| 5 | workbuddy应用机器人 | 小八 | ou_79f5a078588acb771de306796f2da1b0 | — | workbuddy | 🟢 活跃 | 任务看板，子Agent |
| 6 | gemini应用机器人 | gemini | ou_8a2dbf21d13b97d7350295c46de0a62b | — | Gemini | 🟢 活跃 | 飞书/日历 |
| 7 | 天津瑞湾AI（另一个bot） | — | — | cli_a94b70746df8dccc | OpenClaw/妙搭 | 🟢 活跃 | 飞书应用机器人 |
| 8 | 小妙 | 小妙 | ou_8dd4dc0180a2fb74c692f17b94c94d8e | — | 待确认 | 🔴 状态待确认 | |

## 主协调群

- **飞书AI协作群**：`oc_36d47adad05d3ca8e93164ebc8bfca40`
- **天津瑞湾开元名都酒店**：`oc_beb10eb50c7961c710bd1a5881ca8db0`
- **边防预订群**：`oc_24e2941fcd1de842d9a4b482bf59ef62`

## 协作平台汇总

| 平台 | AI伙伴 |
|------|--------|
| 妙搭（OpenClaw） | 小柱(cli_a948e)、天津瑞湾AI(cli_a94b7) |
| 火山引擎（ArkClaw） | ArkClaw |
| Qclaw | Qclaw |
| 腾讯云（OpenClaw） | 腾讯云Openclaw |
| workbuddy | 小八 |
| Gemini | gemini |

## 核心问题：跨平台统一协作

**问题描述**：各AI在7个不同平台，维护成本高，需要手动切换
**目标**：找一个统一工具自动协调所有"龙虾"
**可行方向**：
- OpenClaw的`subagents`和`sessions_spawn`（已可用）
- MCP协议（Model Context Protocol）作为跨平台标准
- 飞书群(oc_36d47adad05d3ca8e93164ebc8bfca40)作为统一协调入口

---

*更新记录：*
- 2026-04-09: 从AI协作群直接读取，更新完整7个AI伙伴身份
- 2026-04-08: 创建团队，初始2人
