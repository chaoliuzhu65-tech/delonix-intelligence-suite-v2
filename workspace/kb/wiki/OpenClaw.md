# [[OpenClaw]]

## 一句话定义
开源 AI Agent & 自动化平台，支持多渠道接入（飞书/Slack/Discord等），通过 Skills 执行复杂任务。

## 核心要点

### 架构特点
- **Channels** - 飞书、Slack、Discord 等消息渠道
- **Skills** - 可复用的任务模块（Markdown 定义）
- **Agents** - 会话管理和任务协调
- **Memory** - 跨会话持久化记忆

### 在本方案中的作用
替代卡帕西原方案中的 **Claude Code + Obsidian** 组合：

| 原方案 | OpenClaw 替代 |
|--------|--------------|
| Claude Code | OpenClaw Agent |
| Obsidian 编辑器 | workspace/kb/ 目录 |
| 手动触发 | Skill 自动检测 |
| 单一会话 | 跨会话记忆 |

### 优势
- ✅ 飞书原生集成（消息/文档自动入库）
- ✅ Cron 定时任务（自动整理）
- ✅ 多 Agent 协作（不同知识领域）
- ✅ 无需额外付费（Claude Code $20/月）

## 相关概念
- [[LLM Wiki Pattern]] - 本实现的知识管理模式
- [[Feishu]] - 主要集成渠道
- [[Skill]] - 任务模块化机制

## 被引用
- [[kb-evolver]] - 知识库进化 Skill

---
Created: 2026-04-07
Updated: 2026-04-07
Tags: #platform #agent #automation
