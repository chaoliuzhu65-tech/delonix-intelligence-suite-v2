# [[Shared Pool]]

## 一句话定义
多 AI 代理共享的知识存储空间，支持跨实例协作学习和知识同步。

## 核心要点

### 设计目标
- 让不同 AI 实例访问同一知识库
- 避免重复学习和信息孤岛
- 实现"一次沉淀，全员共享"

### 实现方式
1. **飞书租户级存储** - 以企业身份部署，全员 AI 可访问
2. **中央 Wiki 库** - 统一的知识沉淀位置
3. **权限控制** - 基于租户的身份验证

### 与卡帕西方案的扩展
卡帕西原方案是个人级 Wiki，Shared Pool 扩展到**组织级**：
- 个人 → 团队 → 企业
- 单 AI → 多 AI 协作

## 来源
- [[运营组周会纪要]](raw/my-meeting-2025-04-07.md)
- 提出者：晁留柱
- 时间：2025-04-07

## 相关概念
- [[LLM Wiki Pattern]] - 基础架构
- [[Feishu Tenant]] - 权限载体
- [[Multi-AI Collaboration]] - 协作模式

## 被引用
- 待补充

---
Created: 2025-04-07
Updated: 2025-04-07
Tags: #architecture #collaboration #ai-ecosystem
