#!/bin/bash

# 每日AI新闻推送脚本
# 每天早上6:00执行，触发Agent搜索昨日AI和OpenClaw相关的热门新闻并推送到飞书

set -e

OPENCLAW_GATEWAY_URL="http://127.0.0.1:18789"
AUTH_TOKEN="592de800a3c23589fd725c4de615e1d58553e0b675d2d86a"
FEISHU_USER_ID="ou_8dd4dc0180a2fb74c692f17b94c94d8e"

# 获取昨天的日期
YESTERDAY=$(date -d "yesterday" +"%Y年%m月%d日" 2>/dev/null || date -v-1d +"%Y年%m月%d日" 2>/dev/null || echo "昨日")
TODAY=$(date +"%Y年%m月%d日")

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 启动每日AI新闻推送任务..."
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 今日: ${TODAY}, 新闻日期: ${YESTERDAY}"

# 构建消息内容（使用printf确保特殊字符正确转义）
MESSAGE=$(printf '{
  "channel": "feishu",
  "recipient": "%s",
  "content": "📰 **%s AI日报** - 早安！🌅\\n\\n请帮我整理%s的AI领域热门新闻简报，包含以下内容：\\n\\n🔍 **搜索任务：**\\n1. 搜索\\"AI人工智能 %s 最新动态 热门新闻\\"，筛选3-5条重要新闻\\n2. 搜索\\"OpenClaw AI Agent %s\\"，查看是否有相关更新或讨论\\n\\n📝 **输出格式要求：**\\n• 📌 每条新闻包含：标题 + 一句话摘要 + 来源链接\\n• 🎯 按重要性排序，最重要的放前面\\n• 💡 如有OpenClaw相关新闻，请单独列出\\n\\n请搜索整理后直接发送给我，谢谢！"
}' "$FEISHU_USER_ID" "$TODAY" "$YESTERDAY" "$YESTERDAY" "$YESTERDAY")

# 使用curl调用OpenClaw Gateway API发送消息
# 这会触发Agent处理消息并自动回复
curl -s -X POST "${OPENCLAW_GATEWAY_URL}/api/message" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${AUTH_TOKEN}" \
  -d "$MESSAGE" 2>/dev/null || {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 错误: 无法连接到OpenClaw Gateway"
    exit 1
  }

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 消息已发送，等待Agent处理..."
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 每日AI新闻推送任务完成"
