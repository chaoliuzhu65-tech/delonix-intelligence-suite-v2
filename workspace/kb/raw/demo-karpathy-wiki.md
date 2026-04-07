# Andrej Karpathy's LLM Wiki Pattern

Source: Twitter/X Post, April 2026

## 核心问题

传统 RAG 的问题：每次查询都重新从原始文档中检索片段，没有知识积累。

> "Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored."

## 解决方案：LLM Wiki

三层架构：

### 1. raw/ - 原料库
- 论文、文章、代码仓库、图片
- 使用 Obsidian Web Clipper 一键转换
- LLM 读取但不修改

### 2. wiki/ - 知识库
- 纯 Markdown 文件
- LLM 自动生成和维护
- 包含摘要、反向链接、概念文章

### 3. schema/ - 指令集
- 指导 LLM 如何维护 Wiki
- 定义格式、链接规则、更新策略

## 关键洞察

1. **无需向量数据库** - 结构化 Markdown + 链接足够
2. **持久化积累** - Wiki 是复利资产，不是临时输出
3. **自动化维护** - LLM 处理重复性组织工作

## 工具链

- Obsidian - 编辑器
- Claude Code - AI 助手
- Git - 版本控制

## 与个人知识管理的区别

| 传统 PKM | LLM Wiki |
|---------|----------|
| 人工整理 | AI 自动维护 |
| 容易放弃 | 持续进化 |
| 线性笔记 | 网状知识图谱 |
