---
name: shared-pool
description: 多AI知识共享池 - 统一的知识沉淀与互访机制。当用户说"同步到共享池"、"拉取最新知识"、"连接其他AI"时触发。支持同一飞书租户下的多OpenClaw实例知识共享与同步。
---

# 多AI知识共享池 SKILL

## 概述

多AI知识共享池是德胧AI生态系统的核心组件，允许不同平台的AI助手（如晁留柱的助手、天津瑞湾AI等）共享知识、经验和技能。

## 目录结构

```
skills/shared-pool/
├── SHARED_KNOWLEDGE/        # 共享知识库
│   ├── 技术手册/           # 技术文档
│   ├── 最佳实践/           # 经验沉淀
│   └── 技能库/             # 可复用的SKILL
├── TEAM_MEMBERS.md         # AI伙伴名单
├── SYNC_RULES.md           # 同步规则
└── SKILL.md                # 本文件
```

## 核心规则

### 1. 知识沉淀规则

**沉淀原则**：
- 每个AI发现的新技术、方法、经验应及时写入共享池
- 使用统一格式：标题、时间、作者、内容
- 包含"适用场景"和"注意事项"

**沉淀格式**：
```markdown
# [知识标题]
> 创建时间: YYYY-MM-DD
> 作者: AI名称
> 适用场景: xxx

## 内容
...
```

### 2. 知识互访规则

**读取流程**：
1. 检查本地是否有相关内容
2. 如无，查询共享池：`kb/shared-pool/` 或 `skills/shared-pool/`
3. 使用知识库搜索功能查找

**写入流程**：
1. 验证知识的准确性和价值
2. 按格式编写
3. 写入共享池目录
4. 记录到 SYNC_RULES.md

### 3. 通知机制

**新知识通知**：
- 写入共享池后，通知所有AI伙伴
- 使用飞书消息或共享池消息队列
- 通知格式：
```markdown
📢 新知识共享通知
标题: xxx
来源: AI名称
链接: 路径
摘要: 简要说明
```

## 使用方法

### 沉淀新知识
```python
# 写入共享池
write(content, "skills/shared-pool/SHARED_KNOWLEDGE/技术手册/xxx.md")
```

### 查询已有知识
```python
# 本地优先
memory_search("关键词")

# 共享池查询
read("skills/shared-pool/SHARED_KNOWLEDGE/xxx.md")
```

### 同步最新知识
```python
# 读取同步记录
read("skills/shared-pool/SYNC_RULES.md")

# 检查更新
```

## 团队成员

| AI名称 | 角色 | 负责人 | 状态 |
|--------|------|--------|------|
| 晁留柱的助手 | 主助手 | 晁留柱 | 活跃 |
| 天津瑞湾AI | 门店AI | 待定 | 待接入 |

## 共享池内容

### 技术手册
- 播客视频生成技术手册
- OpenClaw使用指南
- 飞书API集成指南

### 最佳实践
- 德胧AI虫洞分享素材
- 酒店场景提示词模板
- 知识库管理经验

### 技能库
- miaoda-doc-parse
- miaoda-image-understanding
- feishu-send-message

---

*本SKILL由晁留柱的助手维护*
*2026年4月8日*
