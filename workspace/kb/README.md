# 🦞 OpenClaw 知识库自我进化系统

> Inspired by Andrej Karpathy's LLM Wiki Pattern

## 目录结构

```
kb/
├── raw/          # 原料库 - 放入任何原始资料
├── wiki/         # 知识库 - 龙虾自动维护
├── schema.md     # 维护指令集
└── README.md     # 本文件（知识图谱索引）
```

## 核心概念图谱

```
[[LLM Wiki Pattern]]
    ├── 替代 [[RAG]] 的方案
    ├── 使用 [[Obsidian]] 编辑（原方案）
    └── 本实现使用 [[OpenClaw]] 平台

[[OpenClaw]]
    ├── 集成 [[Feishu]] 渠道
    └── 通过 [[kb-evolver]] Skill 维护知识库
```

## 最近更新

| 时间 | 操作 | 内容 |
|------|------|------|
| 2026-04-07 | 创建 | [[LLM Wiki Pattern]] 概念 |
| 2026-04-07 | 创建 | [[RAG]] 概念对比 |
| 2026-04-07 | 创建 | [[Obsidian]] 工具说明 |
| 2026-04-07 | 创建 | [[OpenClaw]] 平台说明 |

## 统计

- 📄 **概念数**: 4
- 🔗 **链接数**: 6
- 📁 **raw 文件**: 1

## 使用方法

### 存入知识
```bash
# 方式1: 直接放入文件
cp article.md workspace/kb/raw/

# 方式2: 飞书分享
# 直接将文档/消息转发给龙虾
```

### 触发整理
在飞书/本地对龙虾说：
- "整理知识"
- "更新 Wiki"
- "处理 raw 文件"

### 查询知识
- "搜索 XXX"
- "什么是 XXX"
- "XXX 和 YYY 的关系"

---

**Auto-maintained by OpenClaw kb-evolver Skill**
