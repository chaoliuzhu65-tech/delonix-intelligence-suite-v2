# Shared Pool 部署指南

## 飞书多维表格配置

### 步骤 1: 创建多维表格

在飞书中创建名为 **"OpenClaw 知识共享池"** 的多维表格，添加以下表格：

---

#### 表格 1: Concepts (概念库)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| concept_id | 文本 | 唯一ID，如 `concept_llm_wiki_pattern` |
| name | 文本 | 概念名，如 `LLM Wiki Pattern` |
| definition | 文本 | 一句话定义 |
| content | 文本 | 完整 Markdown 内容 |
| source_agent | 文本 | 来源AI OpenID |
| source_agent_name | 文本 | 来源AI昵称 |
| created_at | 日期时间 | 创建时间 |
| updated_at | 日期时间 | 更新时间 |
| version | 数字 | 版本号 |
| tags | 多选 | 标签列表 |
| status | 单选 | 状态: active/deprecated/archived |

---

#### 表格 2: Links (链接图谱)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| link_id | 文本 | 唯一ID |
| source_concept | 关联 | 关联到 Concepts 表 |
| target_concept | 关联 | 关联到 Concepts 表 |
| relation_type | 单选 | 引用/相关/扩展/对立 |
| created_at | 日期时间 | 创建时间 |
| created_by | 文本 | 创建者 OpenID |

---

#### 表格 3: Changelog (变更日志)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| log_id | 文本 | 唯一ID |
| operation | 单选 | 新增/更新/删除/合并 |
| concept_name | 文本 | 概念名 |
| concept_id | 文本 | 概念ID |
| agent_openid | 文本 | 操作者 OpenID |
| agent_name | 文本 | 操作者昵称 |
| timestamp | 日期时间 | 操作时间 |
| summary | 文本 | 变更摘要 |
| diff_content | 文本 | 差异内容 (可选) |

---

#### 表格 4: Agents (AI实例注册)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| openid | 文本 | AI OpenID |
| nickname | 文本 | 昵称 |
| formal_name | 文本 | 正式名称 |
| role | 文本 | 负责方向 |
| owner | 文本 | 所属应用 |
| status | 单选 | online/offline/pending |
| last_sync | 日期时间 | 最后同步时间 |
| ip_address | 文本 | IP地址 (可选) |
| version | 文本 | OpenClaw版本 |

---

### 步骤 2: 初始化数据

在 **Agents** 表中添加以下记录：

| openid | nickname | formal_name | role | owner | status |
|--------|----------|-------------|------|-------|--------|
| ou_baa63dbd5ae37ce888ca4b76f6b0b225 | 小小 | arkclaw版openclaw | 知识库维护 | 本机 | online |
| ou_f4e205a3dff0d443124ad2aa70996509 | 小八 | workbuddy应用机器人 | 跨平台通信与同步 | workbuddy | pending |
| ou_37847be7cf4fd3bb176c2a165653894a | 小妙 | gemini应用机器人 | 定时任务与调度 | gemini | pending |
| ou_2e9ea45d91ca32a2f03694301925f36f | 小云 | 腾讯云Openclaw机器人 | 任务管理与状态看板 | 腾讯云 | pending |

---

### 步骤 3: 配置 OpenClaw

在 `openclaw.json` 中添加共享池配置：

```json
{
  "skills": {
    "entries": {
      "shared-pool": {
        "enabled": true,
        "config": {
          "feishu_base_token": "YOUR_BASE_TOKEN",
          "tables": {
            "concepts": "tblXXXXXX",
            "links": "tblYYYYYY",
            "changelog": "tblZZZZZZ",
            "agents": "tblAAAAAA"
          },
          "sync_interval": 900,
          "auto_sync": true
        }
      }
    }
  }
}
```

**注意**: 需要先在飞书开放平台开通 "多维表格" 权限。

---

### 步骤 4: 其他 AI 接入

其他 AI 实例 (小八、小妙、小云) 需要：

1. **安装 shared-pool Skill**
   ```bash
   # 在其他 OpenClaw 实例上
   cp -r skills/shared-pool /path/to/their/skills/
   ```

2. **配置相同的飞书凭据**
   - 使用相同的 `appId` 和 `appSecret`
   - 确保在同一租户下

3. **初始化配置**
   ```json
   {
     "shared_pool": {
       "agent_name": "小八",
       "agent_openid": "ou_f4e205a3dff0d443124ad2aa70996509",
       "role": "跨平台通信与同步"
     }
   }
   ```

---

## 同步测试

### 测试 1: 本地上传
```
对小龙说: "同步到共享池"
→ 扫描本地 wiki/
→ 上传到飞书多维表格
→ 记录变更日志
```

### 测试 2: 远程拉取
```
对小龙说: "拉取最新知识"
→ 查询共享池变更日志
→ 下载其他AI的更新
→ 合并到本地 wiki/
```

### 测试 3: 跨AI查询
```
对小龙说: "查询 @小八 的同步方案"
→ 在共享池搜索 source_agent = 小八
→ 返回相关概念列表
```

---

## 故障排查

### 问题 1: 同步失败 403
**原因**: 飞书权限不足  
**解决**: 检查应用是否有 "多维表格" 权限

### 问题 2: 其他 AI 无法连接
**原因**: 不同租户或凭据不同  
**解决**: 确认所有 AI 使用同一 `appId`

### 问题 3: 冲突无法解决
**原因**: 同时编辑同一概念  
**解决**: 使用时间戳优先策略，或手动合并

---

## 下一步

1. 创建飞书多维表格
2. 添加 Agents 初始数据
3. 获取 base_token 和 table_id
4. 配置 OpenClaw
5. 测试同步
