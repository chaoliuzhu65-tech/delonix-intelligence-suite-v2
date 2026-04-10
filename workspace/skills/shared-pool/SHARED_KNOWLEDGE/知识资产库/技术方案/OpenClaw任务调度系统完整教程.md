# 7×24小时后台常驻任务调度系统 - 完整版教程

> 创建时间: 2026-03-30
> 来源: 晁留柱
> 文档链接: https://delonix.feishu.cn/docx/Ck5idhWfDoJe9fxrdwocryFCnCe
> 存入共享池时间: 2026-04-10

---

## 核心架构

```
飞书租户级授权层
        ↓
OpenClaw Gateway层（Cron调度 + WebSocket）
        ↓
任务执行层（Agent会话池 + 任务队列 + 异常重试）
        ↓
结果推送层（飞书消息/文档/日历）
```

---

## 核心组件

| 组件 | 功能 | 状态 |
|------|------|------|
| OpenClaw Gateway | 核心服务，常驻进程 | ✅ |
| Cron调度引擎 | 定时任务触发 | ✅ |
| 任务队列 | 任务缓冲，优先级管理 | ✅ |
| 异常重试 | 指数退避算法 | ✅ |
| 飞书推送 | 结果主动推送 | ✅ |

---

## Cron调度

### 常用表达式

| 表达式 | 说明 |
|--------|------|
| `0 9 * * *` | 每天09:00 |
| `0 10,12,14 * * *` | 每天10:00、12:00、14:00 |
| `30 22 * * *` | 每天22:30 |
| `0 9 * * 1` | 每周一09:00 |
| `0 9 1 * *` | 每月1日09:00 |
| `0 */2 * * *` | 每2小时 |

### 酒店业务场景示例

```bash
# 每日运营指标监控
openclaw cron add \
  --name "daily-operational-metrics" \
  --cron "0 9 * * *" \
  --message "【每日运营指标】请生成昨日酒店运营数据报告"

# 每2小时进度跟进
openclaw cron add \
  --name "progress-check-2h" \
  --cron "0 10,12,14,16,18,20 * * *" \
  --message "【进度跟进】请检查当前出租率、ADR等核心指标"

# 每日复盘
openclaw cron add \
  --name "daily-review" \
  --cron "30 22 * * *" \
  --message "【每日复盘】请汇总今日各项指标完成情况"
```

---

## 异常重试机制

**指数退避算法**：
- 第1次失败：等待1分钟后重试
- 第2次失败：等待5分钟后重试
- 第3次失败：等待15分钟后重试
- 超过3次：放弃执行

```python
from retry_manager import RetryManager, get_feishu_retry_policy

manager = RetryManager(get_feishu_retry_policy())
result = manager.execute_with_retry(unstable_function)
```

---

## 飞书租户级授权（关键！）

### vs 用户级授权

| 权限 | 用户级 | 租户级 |
|------|--------|--------|
| 私信其他AI | ❌ | ✅ |
| @任意用户 | ❌ | ✅ |
| 跨会话通信 | ❌ | ✅ |

### 必须申请的权限

```yaml
- im:message:send_as_user  # 最关键！
- contact:user:search
- doc:document
- calendar:event
- bitable:app
```

---

## 跨Agent通信

### AI助手注册表

```python
AI_AGENTS = {
    "claw_analyst": {
        "name": "claw分析官",
        "open_id": "ou_f7653f0ada5ad48a78ca303cc6f289f9",
        "session_key": "agent:main:main"
    },
    "workbuddy": {
        "name": "workbuddy应用机器人",
        "open_id": "ou_33f9f6bae7c6c490785443c7f4d3f442",
        "session_key": "agent:workbuddy:main"
    }
}
```

### 通信方式

1. **sessions_send**（推荐）- 直接发送消息到其他Agent会话
2. **飞书私信** - 使用租户级授权私信
3. **飞书群聊中介** - 通过协调群传递消息

---

## 常用命令

```bash
# Gateway管理
systemctl restart openclaw-gateway
systemctl status openclaw-gateway

# Cron任务
openclaw cron list
openclaw cron runs
openclaw cron run <job-id>

# 日志
journalctl -u openclaw-gateway -n 100 --no-pager
```

---

*本教程由晁留柱编写，已存入共享池*
