# 德隆 AI Native 技能清单

> 生成时间：2026-04-05
> 目标：打造德隆 AI Native，多 AI 助手协同工作

---

## 一、飞书原生工具矩阵

### 1. 即时通讯 (IM)

| 工具名称 | 功能描述 | AI 协同价值 |
|---------|---------|------------|
| feishu_im_user_get_messages | 获取历史消息 | 上下文记忆、多轮对话 |
| feishu_im_user_get_thread_messages | 获取话题消息 | 群聊讨论串管理 |
| feishu_im_user_search_messages | 跨会话搜索 | 知识检索、历史追溯 |
| feishu_im_user_message (send/reply) | 发送/回复消息 | 主动触达、任务通知 |
| feishu_im_bot_image | 下载消息中的图片 | 附件处理 |

### 2. 日历与会议

| 工具名称 | 功能描述 | AI 协同价值 |
|---------|---------|------------|
| feishu_calendar_calendar | 日历管理 | 日程同步 |
| feishu_calendar_event | 日程创建/查询 | 自动约会议 |
| feishu_calendar_event_attendee | 参会人管理 | 邀请/移除成员 |
| feishu_calendar_freebusy | 忙闲查询 | 智能排时间 |

### 3. 文档与知识库

| 工具名称 | 功能描述 | AI 协同价值 |
|---------|---------|------------|
| feishu_fetch_doc | 获取文档内容 | 知识读取 |
| feishu_create_doc | 创建新文档 | 自动生成报告 |
| feishu_update_doc | 更新文档 | 内容追加/覆盖 |
| feishu_search_doc_wiki | 搜索文档/Wiki | 知识问答 |
| feishu_drive_file | 云空间文件管理 | 文件存取 |

### 4. 多维表格 (Bitable)

| 工具名称 | 功能描述 | AI 协同价值 |
|---------|---------|------------|
| feishu_bitable_app | 多维表格应用管理 | 数据聚合 |
| feishu_bitable_app_table | 数据表管理 | 表结构操作 |
| feishu_bitable_app_table_record | 记录 CRUD | 数据增删改查 |
| feishu_bitable_app_table_field | 字段管理 | 结构化数据 |
| feishu_bitable_app_table_view | 视图管理 | 数据筛选展示 |

### 5. 任务管理

| 工具名称 | 功能描述 | AI 协同价值 |
|---------|---------|------------|
| feishu_task_task | 任务创建/查询 | 待办管理 |
| feishu_task_tasklist | 任务清单 | 项目管理 |
| feishu_task_comment | 任务评论 | 协作沟通 |
| feishu_task_subtask | 子任务 | 任务分解 |

### 6. 组织与通讯录

| 工具名称 | 功能描述 | AI 协同价值 |
|---------|---------|------------|
| feishu_get_user | 获取用户信息 | 身份识别 |
| feishu_search_user | 搜索员工 | 找人/查岗 |
| feishu_chat | 群聊管理 | 群操作 |
| feishu_chat_members | 群成员列表 | 权限管理 |

---

## 二、妙搭 AI 技能 (Miaoda)

### 1. 内容理解

| 技能名称 | 功能描述 | 酒店场景 |
|---------|---------|---------|
| miaoda-image-understanding | 图片理解 | 房间照片分析、菜品识别 |
| miaoda-speech-to-text | 语音转文字 | 会议记录、客人语音留言 |
| miaoda-doc-parse | 文档解析 | 合同/报表提取 |

### 2. 内容生成

| 技能名称 | 功能描述 | 酒店场景 |
|---------|---------|---------|
| miaoda-text-gen-image | 文字生成图片 | 生成海报、配图 |
| miaoda-web-search | AI 搜索摘要 | 市场调研、竞品分析 |
| miaoda-web-fetch | 网页抓取 | 价格监控、舆情收集 |

### 3. 知识管理

| 技能名称 | 功能描述 | 酒店场景 |
|---------|---------|---------|
| notebook-lm | 播客/文档转知识库 | 培训材料、学习资料 |

---

## 三、德隆酒店专用技能

### 运营管理

| 技能名称 | 功能描述 |
|---------|---------|
| delong-duty-log | 值守日志 |
| delong-complaint-handler | 投诉处理 |
| delong-occupancy-rate-forecast | 入住率预测 |
| delong-quality-inspection | 质量检查 |
| delong-scheduling | 排班管理 |
| delong-emergency-plan | 应急预案 |
| delong-inspection | 巡检任务 |
| delong-guest-reminder | 客人提醒 |

---

## 四、系统级工具

| 工具名称 | 功能描述 |
|---------|---------|
| browser | 浏览器自动化 |
| canvas | UI 展示 |
| nodes | 设备控制 |
| cron | 定时任务 |
| sessions_spawn | 子代理生成 |
| memory_* | 记忆管理 |
| tts | 语音合成 |

---

## 五、AI 协同使用建议

### 场景 1：智能客服
- **输入**：客人消息 + 知识库搜索
- **处理**：LLM 理解意图 → 查FAQ → 生成回复
- **工具组合**：feishu_im + feishu_search_doc + NotebookLM

### 场景 2：会议纪要
- **输入**：会议录音
- **处理**：Speech-to-Text → LLM 摘要 → 存入文档
- **工具组合**：miaoda-speech-to-text + feishu_create_doc

### 场景 3：数据报表
- **输入**：多维表格数据
- **处理**：自动汇总 → 生成分析 → 推送
- **工具组合**：feishu_bitable + feishu_im_user_message

### 场景 4：巡检自动化
- **输入**：巡检计划
- **处理**：定时触发 → 任务下发 → 进度跟踪
- **工具组合**：cron + feishu_task + feishu_im

### 场景 5：智能问答
- **输入**：员工提问
- **处理**：意图识别 → 知识库检索 → 生成答案
- **工具组合**：feishu_search_doc + NotebookLM + feishu_im

---

## 六、快速部署指南

### 新 AI 助手接入飞书

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "你的appId",
      "appSecret": "你的appSecret"
    }
  }
}
```

### 启用德隆技能

在 openclaw.json 的 skills.entries 中添加：

```json
{
  "delong-duty-log": { "enabled": true },
  "delong-complaint-handler": { "enabled": true },
  "delong-occupancy-forecast": { "enabled": true }
}
```

---

*此清单由 AI 自动生成，可供其他 AI 助手一键学习部署*
