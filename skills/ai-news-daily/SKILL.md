---
name: ai-news-daily
description: 每天早上自动搜索AI和OpenClaw相关的热门新闻，并推送到飞书。触发词：AI新闻推送、OpenClaw新闻、每日新闻、定时新闻
---

# AI新闻每日推送

## 功能

每天早上6:00（北京时间）自动搜索前一天AI领域和OpenClaw相关的热门新闻，整理后发送到指定的飞书账号。

## 配置信息

| 配置项 | 值 |
|--------|-----|
| 执行时间 | 每天 06:00 (Asia/Shanghai) |
| 目标用户 | 晁留柱 (ou_8dd4dc0180a2fb74c692f17b94c94d8e) |
| 搜索内容 | AI人工智能动态 + OpenClaw相关新闻 |

## 工作流程

1. 🕕 每天早上6:00，cron任务触发执行脚本
2. 📨 脚本向OpenClaw Gateway发送消息请求
3. 🤖 Agent收到消息后，自动执行以下任务：
   - 搜索昨日AI人工智能热门新闻
   - 搜索OpenClaw相关动态
   - 整理3-5条重要新闻，包含标题、摘要和来源
4. 📲 Agent将整理好的新闻简报发送到飞书

## 文件结构

```
skills/ai-news-daily/
├── SKILL.md                          # 本文件
└── scripts/
    └── send-daily-news.sh            # 定时任务执行脚本
```

## Cron配置

定时任务配置位于：`cron/jobs.json`

```json
{
  "id": "daily-ai-news-push",
  "schedule": "0 6 * * *",
  "timezone": "Asia/Shanghai"
}
```

## 手动测试

如需手动测试定时任务，可以执行：

```bash
bash skills/ai-news-daily/scripts/send-daily-news.sh
```

## 修改配置

### 修改发送时间

编辑 `cron/jobs.json`，修改 `expression` 字段：

```json
"expression": "0 6 * * *"    // 每天6:00
"expression": "0 8 * * *"    // 每天8:00
"expression": "0 */6 * * *"  // 每6小时
```

### 修改目标用户

编辑 `skills/ai-news-daily/scripts/send-daily-news.sh`，修改：

```bash
FEISHU_USER_ID="ou_8dd4dc0180a2fb74c692f17b94c94d8e"
```

## 依赖

- OpenClaw Gateway 必须运行（默认端口18789）
- 飞书插件必须已安装并启用
- 飞书用户ID必须在 `channels.feishu.allowFrom` 白名单中

## 故障排查

### 任务未执行

1. 检查OpenClaw服务状态：`ps aux | grep openclaw`
2. 检查cron配置是否正确加载
3. 手动执行脚本查看错误信息

### 消息未收到

1. 检查飞书用户ID是否正确
2. 检查用户是否在 `allowFrom` 白名单中
3. 检查飞书插件配置是否正确
