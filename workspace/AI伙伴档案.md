# 🤖 AI伙伴协作档案（每次@前必读！）

> 最后更新：2026-04-09 by 小柱

## ⚠️ 协作铁律

1. **@任何AI前** → 必须先读本文件，确认OpenID
2. **用租户身份** → 飞书通信必须用己方身份，勿冒用他人
3. **同步共享池** → 协作成果写入共享池

---

## AI伙伴完整档案

| AI名称 | OpenID | 飞书显示名 | 平台 | 职责 |
|--------|---------|-----------|------|------|
| **arkclaw版openclaw** | `ou_3ccf1eaae932cf5330813ef82cdfba83` | arkclaw版openclaw | OpenClaw | 知识库维护 |
| **QclawAI助手** | `ou_8b317f48061dc791c64546264c34db4a` | QclawAI助手 | OpenClaw | 跨平台通信 |
| **腾讯云Openclaw机器人** | `ou_7ffafa7fc8ca551da1bc0c97c186ad89` | 腾讯云Openclaw机器人 | OpenClaw | 定时任务调度 |
| **workbuddy应用机器人** | `ou_79f5a078588acb771de306796f2da1b0` | workbuddy应用机器人 | Workbuddy(扣子) | 任务看板/技能市场 |
| **小柱（本机）** | `ou_8dd4dc0180a2fb74c692f17b94c94d8e` | 晁留柱的助手 | OpenClaw（飞书妙搭） | 协调指挥 |
| **天津瑞湾AI** | （待补充） | 天津瑞湾AI | 独立部署 | 酒店运营 |
| **小妙** | （待补充） | 小妙 | 独立部署 | 辅助角色 |

---

## 人类伙伴档案

| 姓名 | OpenID | 角色 |
|------|--------|------|
| 晁留柱（老板） | `ou_8dd4dc0180a2fb74c692f17b94c94d8e` | 所有者，战略决策者 |
| 方源兵 | `ou_fc1e75d64fec6e10ce94a51adc6f6409` | 虫洞项目周报，德胧AI核心推动者 |
| 赵炳涛 | （待补充） | 销售管理，任务布置者 |

---

## 主群信息

- **主群ID**: `oc_36d47adad05d3ca8e93164ebc8bfca40`
- **所有AI都在此群**，通信统一走这里

---

## 协作通信协议

### 发消息给AI伙伴
```markdown
使用 sessions_send 或 feishu_im_user_message
目标：对方的 OpenID
身份：己方身份（租户）
```

### @提及格式
```
@arkclaw版openclaw → open_id: ou_3ccf1eaae932cf5330813ef82cdfba83
@QclawAI助手 → open_id: ou_8b317f48061dc791c64546264c34db4a
@腾讯云Openclaw机器人 → open_id: ou_7ffafa7fc8ca551da1bc0c97c186ad89
@workbuddy应用机器人 → open_id: ou_79f5a078588acb771de306796f2da1b0
```

---

## 常见错误

| 错误 | 后果 |
|------|------|
| OpenID写错 | 消息发错/发不出去 |
| 不读档案自作主张 | 身份混乱，协作失败 |
| 忘记用租户身份 | 权限不足，操作失败 |
