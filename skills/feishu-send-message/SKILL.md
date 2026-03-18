---
name: feishu-send-message
description: 向指定飞书群聊或用户发送卡片消息。触发词：发送消息、飞书发消息、发送卡片、群发消息、feishu send message
override-tools:
  - feishu_send_message
---

# 飞书发送消息

向指定的飞书群聊或用户发送卡片消息。

## Quick Reference

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| chat_id | 群聊ID (oc_xxx格式) 或用户open_id (ou_xxx格式) | 是 | - |
| title | 消息卡片标题 | 是 | - |
| content | 消息卡片正文内容（支持Markdown） | 是 | - |

## 使用示例

```bash
# 使用完整路径执行
/home/gem/workspace/agent/skills/feishu-send-message/scripts/send-message.sh \
  --chat_id "oc_xxx" \
  --title "标题" \
  --content "正文内容"

# 或者创建软链接后直接执行
ln -sf /home/gem/workspace/agent/skills/feishu-send-message/scripts/send-message.sh /usr/local/bin/feishu-send-message
feishu-send-message --chat_id "oc_xxx" --title "标题" --content "正文内容"
```

## 消息格式

支持 Markdown 格式的消息内容，可以包含：
- 加粗文本：**text**
- 斜体文本：*text*
- 链接：[text](url)
- 换行：\n

## 错误处理

| 错误码 | 说明 |
|--------|------|
| 99991663 | 应用凭证无效 |
| 99991642 | API 权限不足 |
| 99991681 | 群聊不存在 |

## 配置

技能脚本位置：`skills/feishu-send-message/scripts/send-message.sh`

如需修改飞书应用凭证，请编辑脚本中的 APP_ID 和 APP_SECRET 变量。
