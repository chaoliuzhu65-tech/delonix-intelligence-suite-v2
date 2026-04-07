# [[LLM Wiki Pattern]]

## 一句话定义
由 Andrej Karpathy 提出的一种知识管理架构，让 LLM 自动维护结构化的 Markdown Wiki，替代传统的 RAG 检索方式。

## 核心要点

### 1. 问题意识
传统 RAG 的缺陷：**无知识积累**
- 每次查询都重新从原始文档检索片段
- LLM 每次都要"重新发现"知识
- 无法处理需要综合多篇文档的复杂问题

### 2. 三层架构
| 层级 | 内容 | 维护者 |
|------|------|--------|
| **raw/** | 原始资料（论文、文章、代码） | 用户存入 |
| **wiki/** | 结构化知识库（Markdown） | LLM 自动生成 |
| **schema/** | 维护指令集 | 用户定义规则 |

### 3. 关键洞察
> "Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored."

- 人类放弃 Wiki 因为维护负担 > 价值
- LLM 不知疲倦，可持续维护

### 4. 技术优势
- ✅ 无需向量数据库（纯 Markdown + 链接）
- ✅ 知识复利（一次处理，永久可用）
- ✅ 网状结构（概念间自动链接）

## 来源
- [[Karpathy's Original Post]](raw/demo-karpathy-wiki.md)
- Andrej Karpathy (前 OpenAI/Tesla AI Director)
- 发布时间：2026年4月

## 相关概念
- [[RAG]] - 被替代的传统方案
- [[Obsidian]] - 推荐的编辑器工具
- [[Claude Code]] - 原方案使用的 AI 助手
- [[Knowledge Graph]] - 网状知识结构
- [[PKM]] - 个人知识管理

## 被引用
- [[OpenClaw]] - 本实现的基础平台

## OpenClaw 实现差异

| 特性 | 原方案 (Claude Code) | OpenClaw 方案 |
|------|---------------------|---------------|
| 触发方式 | 手动选择文件 | Skill 自动检测 + 指令触发 |
| 会话记忆 | 单次对话 | 跨会话持久化 |
| 渠道集成 | 仅本地 | 飞书/本地双通道 |
| 自动化 | 需 AI 常驻 | Cron 定时 + 事件驱动 |

---
Created: 2026-04-07
Updated: 2026-04-07
Tags: #knowledge-management #ai-pattern #rag-alternative
