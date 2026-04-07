# 🔥 Shared Pool 演示场景

## 场景 1: 小小发现新知识，全员同步

### 时序图

```
用户@小小:
"我发现了一篇关于 Multi-Agent 架构的好文章"
[上传文章到 raw/]

小小:
1. 读取文章
2. 提取概念: [[Multi-Agent Architecture]]
3. 生成 wiki/ 条目
4. 同步到共享池
5. 广播给其他 AI

共享池:
→ 记录 Concepts: Multi-Agent Architecture (by 小小)
→ 记录 Changelog: 新增概念
→ 触发 webhook

小八 🎱 (收到通知):
"小小新增了一个概念: Multi-Agent Architecture
与我负责的跨平台通信相关，已自动下载"
[更新本地 wiki/]

小妙 ⏰ (收到通知):
"已记录，将在下次定时任务中检查关联性"

小云 ☁️ (收到通知):
"已同步到知识看板"
```

---

## 场景 2: 小八优化同步协议，知识回流

```
小八 🎱 (分析小小上传的内容):
"发现 Multi-Agent Architecture 中的通信部分可以优化
我设计了一个新的 Cross-Agent Protocol"

小八:
1. 创建 [[Cross-Agent Protocol]]
2. 关联到 [[Multi-Agent Architecture]]
3. 同步到共享池

小小 🦞 (收到通知):
"小八基于我的概念扩展了新协议，已自动下载"
[更新本地: Multi-Agent Architecture 添加新链接]

用户@小小:
"查询 Multi-Agent 相关内容"

小小:
"找到以下内容:
- [[Multi-Agent Architecture]] (我创建的)
- [[Cross-Agent Protocol]] (小八贡献的，与我相关)"
```

---

## 场景 3: 用户跨 AI 协作完成任务

```
用户@小云:
"帮我创建一个项目看板"

小云 ☁️:
"已创建项目看板，已同步到共享池"
[创建 [[Project Board: Knowledge Base]]]

用户@小妙:
"每天提醒团队更新知识库"

小妙 ⏰:
"已设置定时任务，关联到小云的项目看板"
[创建 [[Cron Job: Daily Knowledge Sync]]]
[链接到 [[Project Board: Knowledge Base]]]

用户@小八:
"把这个看板同步到企业微信"

小八 🎱:
"已建立跨平台同步通道"
[创建 [[Cross-Platform Sync: WeChat]]]
[链接到 [[Project Board: Knowledge Base]]]

用户@小小:
"总结下这个项目的知识图谱"

小小 🦞:
"该项目涉及以下概念:
- [[Project Board: Knowledge Base]] (看板, 小云)
- [[Cron Job: Daily Knowledge Sync]] (定时任务, 小妙)
- [[Cross-Platform Sync: WeChat]] (同步通道, 小八)

知识网络: 看板 ← 定时任务 + 同步通道"
```

---

## 当前部署状态

| 组件 | 状态 | 说明 |
|------|------|------|
| 小小 (本机) | ✅ 已部署 | 知识库维护 Skill |
| 共享池架构 | ✅ 已设计 | 飞书多维表格方案 |
| 小八连接 | 🟡 待配置 | 需要对方 OpenClaw 配置 |
| 小妙连接 | 🟡 待配置 | 需要对方 OpenClaw 配置 |
| 小云连接 | 🟡 待配置 | 需要对方 OpenClaw 配置 |
| 飞书多维表格 | 🟡 待创建 | 需要飞书后台操作 |

---

## 下一步行动

1. **创建飞书多维表格** (需要您操作)
   - 登录飞书 → 创建多维表格
   - 按 setup-guide.md 配置表格结构

2. **获取 Token** (需要飞书开发者后台)
   - 开通"多维表格"权限
   - 获取 base_token 和 table_id

3. **配置其他 AI** (需要各 AI 负责人)
   - 发送 shared-pool Skill 给对方
   - 配置相同的飞书凭据
   - 注册到共享池

4. **测试同步**
   - 小小上传概念
   - 验证其他 AI 收到通知
