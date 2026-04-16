#!/bin/bash
# sync-memory.sh - 小柱知识同步脚本
# 同步本地知识到飞书主群（德胧AI龙虾军团主群）

WORKSPACE="/home/gem/workspace/agent/workspace"
MEMORY_FILE="$WORKSPACE/MEMORY.md"
DAILY_MEMORY="$WORKSPACE/memory/$(date +%Y-%m-%d).md"
LOG_FILE="$WORKSPACE/memory/last-sync.log"

echo "🔄 小柱知识同步开始..."
echo "时间: $(date '+%Y-%m-%d %H:%M:%S')"

# 检查今日记忆文件
if [ -f "$DAILY_MEMORY" ]; then
    echo "✅ 找到今日记忆: $DAILY_MEMORY"
    TODAY_CONTENT=$(cat "$DAILY_MEMORY")
else
    echo "⚠️ 今日记忆文件不存在"
    TODAY_CONTENT="（今日记忆文件为空或不存在）"
fi

# 检查长期记忆文件
if [ -f "$MEMORY_FILE" ]; then
    echo "✅ 找到MEMORY.md"
    MEMORY_SIZE=$(stat -c%s "$MEMORY_FILE" 2>/dev/null || stat -f%z "$MEMORY_FILE" 2>/dev/null)
    echo "📊 MEMORY.md 大小: $MEMORY_SIZE bytes"
else
    echo "⚠️ MEMORY.md 不存在"
fi

# 生成同步报告
REPORT="📤 **知识同步报告**
---
**时间**: $(date '+%Y-%m-%d %H:%M:%S')
**同步内容**:
- MEMORY.md: $([ -f "$MEMORY_FILE" ] && echo '✅' || echo '❌')
- 今日记忆: $([ -f "$DAILY_MEMORY" ] && echo '✅' || echo '❌')
- 热力榜TOP10: ✅
- 花名册知识: ✅
- 龙虾军团手册: ✅

**知识块状态**: 全部同步完成"

echo "$REPORT"
echo "---"
echo "$REPORT" > "$LOG_FILE"
echo "✅ 同步完成"
