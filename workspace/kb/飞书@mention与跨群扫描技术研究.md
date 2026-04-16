# 飞书 @mention 与跨群扫描技术研究

> 研究时间：2026-04-14
> 研究人：晁留柱的助手（子代理）

---

## 研究一：飞书 @mention 正确实现方式

### 1.1 核心问题诊断

**问题现象**：@mention 在消息中变成普通文本字符，无法真正激活阅读（对方收不到通知）。

**根本原因**：飞书 @mention 不是普通的文本内容，而是需要用 XML 标签格式嵌入消息内容，且发送时必须满足特定条件，否则只会被当作纯文本渲染。

---

### 1.2 text 类型消息中 @mention 的正确格式

飞书 text 类型消息完全支持 @mention，**但格式必须是 XML 标签**，不能是普通 @字符。

#### 正确格式

```json
// 发送给群组（chat_id）
{
  "receive_id_type": "chat_id",
  "receive_id": "oc_xxxxxxxxxxxxxxxxx",
  "msg_type": "text",
  "content": "{\"text\":\"<at user_id=\\\"ou_xxxxxxxx\\\">张三</at> 请查看今日数据\"}"
}

// 发送给个人（open_id）
{
  "receive_id_type": "open_id",
  "receive_id": "ou_xxxxxxxx",
  "msg_type": "text",
  "content": "{\"text\":\"<at user_id=\\\"ou_xxxxxxxx\\\">张三</at> 有新任务\"}"
}
```

#### @mention XML 标签格式

```xml
<!-- @ 单个用户 -->
<at user_id="ou_xxxxxxxx">用户名字</at>

<!-- @ 所有人 -->
<at user_id="all">所有人</at>
```

- `user_id` 支持三种 ID 类型：`open_id`、`union_id`、`user_id`，推荐使用 `open_id`（最稳定）
- 标签之间的文本是显示名（可随意填写，建议填真实名字）
- **content 是 JSON 字符串，整体需要 JSON 转义**，这是最常出错的地方

#### 错误写法（会导致 @变成普通文本）

```json
// ❌ 错误：直接把 @ 当成普通字符
"content": "{\"text\":\"@张三 请查看今日数据\"}"

// ❌ 错误：标签没有闭合
"content": "{\"text\":\"<at user_id=\\\"ou_xxx\\\">张三 请查看\"}"

// ❌ 错误：user_id 拼写错误
"content": "{\"text\":\"<at user_id=\\\"ou_xxx\\\">张三</at text\"}"
```

---

### 1.3 富文本（post）类型消息中的 @mention

post 类型支持更丰富的 @mention 写法，在 content 的富文本节点中使用：

```json
{
  "receive_id_type": "chat_id",
  "receive_id": "oc_xxxxxxxx",
  "msg_type": "post",
  "content": "{\"zh_cn\":{\"title\":\"任务通知\",\"content\":[[{\"tag\":\"text\",\"text\":\"<at user_id=\\\"ou_xxxxxxxx\\\">李四</at> 有一项新任务\"}]]}}"
}
```

post 类型中可以混合使用 `text`、`at`、`link` 等标签。

---

### 1.4 消息卡片（interactive）中的 @mention

在飞书卡片中，@mention 通过 Markdown 或原生标签实现：

#### 方式一：Markdown 格式（推荐）

```json
{
  "receive_id_type": "chat_id",
  "receive_id": "oc_xxxxxxxx",
  "msg_type": "interactive",
  "content": "{\"config\":{\"wide_screen_mode\":true},\"elements\":[{\"tag\":\"markdown\",\"content\":\"**任务提醒**\\n<at user_id=\\\"ou_xxxxxxxx\\\">王五</at> 请尽快处理\"}]}"
}
```

#### 方式二：原生标签

```json
{
  "msg_type": "interactive",
  "content": "{
    \"elements\": [{
      \"tag\": \"div\",
      \"text\": \"<at user_id=\\\"ou_xxxxxxxx\\\">赵六</at> 审批已通过\"
    }]
  }"
}
```

---

### 1.5 @mention 通知触发的条件

被 @ 的用户**能收到通知**必须同时满足：

| 条件 | 说明 |
|------|------|
| 机器人必须在群里 | 发送群消息时，机器人需要是群成员 |
| user_id 正确 | 必须是接收者真实的 open_id/union_id/user_id |
| 标签格式正确 | `<at user_id="ou_xxx">名字</at>` 完整闭合 |
| content 是正确转义的 JSON 字符串 | JSON 嵌套需要双重转义 |
| 机器人有发消息权限 | 群设置中允许机器人发言 |

**特别说明**：如果消息是卡片格式（interactive），飞书对 @mention 标签的解析可能有延迟，但通知通常能正常送达。如果 text 格式的 @mention 没有生效，首先检查 content 的 JSON 转义是否正确。

---

### 1.6 OpenClaw 中的 @mention 实践

在 OpenClaw 中通过飞书发送消息时，正确的 @mention 写法（直接用飞书原生格式）可以触发通知。问题通常出在：

1. **消息内容没有用 XML 标签包裹**：直接写 `@某人` 而非 `<at user_id="ou_xxx">某人</at>`
2. **JSON 转义问题**：content 中的 JSON 字符串需要正确转义
3. **ID 类型不匹配**：尽量使用 open_id

---

## 研究二：跨群消息扫描技术方案

### 2.1 核心问题

**问题**：OpenClaw 机器人不在某个群中，能否读取该群的消息？

**答案**：**不能**。根据飞书开放平台 API 文档：

```
错误码 230002: "The bot can not be outside the group."
机器人必须是被查询群组的成员，才能调用消息读取 API。
```

---

### 2.2 飞书消息 API 的权限要求

| API | 权限要求 | 机器人是否必须在群中 |
|-----|---------|---------------------|
| `im.v1.messages` (发送消息) | 机器人能力 + 在群中发言权限 | ✅ 是 |
| `im.v1.messages` (读取消息列表) | 机器人能力 + `im:message` 或 `im:message:readonly` | ✅ 是（对于群组消息） |
| `im.v1.messages/:message_id` (获取单条消息) | 机器人能力 + 在群中 | ✅ 是 |
| 消息事件订阅（Webhook） | 需要先加入群，接收 @机器人的消息 | ✅ 是（只能收 @机器人的消息） |

**关键限制**：飞书**没有**"管理员代持权限跨群读取所有消息"的 API。即使是应用管理员，也无法通过 API 读取机器人不在的群的消息。

---

### 2.3 跨群消息扫描的可行方案

#### 方案一：机器人加入所有目标群（推荐）

**原理**：将机器人 Agent 账号加入每一个需要监控的群，机器人即可读取该群消息（通过 `im.v1.messages` API）。

**优点**：实现简单，稳定可靠
**缺点**：需要人工将机器人添加到每个群；群多时管理复杂

**实现步骤**：
1. 在飞书开放平台应用管理中开启「机器人」能力
2. 将应用机器人添加到所有目标群
3. 通过 `im.v1.messages` API 按时间/关键词拉取消息
4. 结合事件订阅，实现实时监控

```python
# 伪代码：拉取群消息
GET https://open.feishu.cn/open-apis/im/v1/messages?container_id_type=chat&container_id=oc_xxx
Headers:
  Authorization: Bearer <tenant_access_token>

# 响应包含消息列表，每条消息有：
# - message_id: 消息唯一ID
# - msg_type: text/post/interactive等
# - content: 消息内容（需要解析）
# - sender: 发送者信息
# - create_time: 创建时间
```

---

#### 方案二：利用飞书「获取群组中所有消息」权限（管理员方案）

**条件**：应用需要申请 `im:message:readonly`（获取群组中所有消息）权限，且需要是**系统管理员**。

**重要提示**：这个权限需要用户在飞书管理后台授权，且申请理由需要说明用途。普通应用基本无法获得此权限（飞书对此管控严格）。

---

#### 方案三：WebSocket 事件订阅（实时监控）

**原理**：通过事件订阅机制，实时接收群消息事件。

**限制**：
- 默认情况下，**只能接收用户 @机器人 的消息**
- 如果申请了「接收群组中所有消息」事件（`im.message.receive_v1`），可以接收所有消息，但机器人仍然必须在群中

**实现**：
```json
// 事件订阅配置
{
  "Event_types": [
    "im.message.receive_v1"  // 接收消息事件
  ]
}
```

**注意**：这个方案中，机器人同样需要先加入群。但一旦加入，可以实时接收所有消息，而不需要轮询拉取。

---

#### 方案四：多机器人 + 消息汇总（多 OpenClaw 实例方案）

**原理**：在不同群中部署不同的机器人实例，通过共享存储（如多维表格）汇总消息。

**架构**：
```
群A → OpenClaw实例A → 写入共享 Bitable
群B → OpenClaw实例B → 写入共享 Bitable
群C → OpenClaw实例C → 写入共享 Bitable
```

**优点**：天然解决跨群问题，每个实例只管自己所在的群
**缺点**：多实例运维成本高

---

#### 方案五：用户代取消息（Webhook 中转方案）

**原理**：
1. 在每个群中添加一个「飞书自建应用」作为群成员
2. 该应用通过 WebSocket 接收用户 @它 的消息
3. 用户 @应用 时，触发应用调用 `im.v1.messages` API 读取该群最近消息
4. 应用处理消息后，再将结果 @回传给用户

**本质**：通过用户主动 @应用 触发消息读取，而不是应用主动扫描。

---

### 2.4 OpenClaw 跨群实现建议

基于以上研究，对于 OpenClaw 部署，推荐方案如下：

#### 短期方案：机器人加群 + 定时轮询

```yaml
# OpenClaw 配置伪例
plugins:
  entries:
    - name: feishu
      config:
        # 机器人自动加入以下群
        auto_join_groups:
          - oc_group_1  # 美誉度群
          - oc_group_2  # 人资财务群
          - oc_group_3  # 预订产量群
          - oc_group_4  # OTA群
        # 定时拉取消息间隔（秒）
        poll_interval: 60
```

#### 中期方案：事件订阅 + 实时处理

通过 WebSocket 事件订阅实时接收消息，对每条消息进行实时分析和处理，减少轮询开销。

#### 长期方案：多 OpenClaw 实例 + 知识共享池

每个关键群部署独立 OpenClaw 实例，通过共享 Bitable 知识库实现信息互通。

---

## 附录：飞书 @mention 速查表

| 消息类型 | @格式 | 是否触发通知 |
|---------|-------|------------|
| text | `<at user_id="ou_xxx">名字</at>` | ✅ 是 |
| post（富文本） | 同上，嵌套在 content 中 | ✅ 是 |
| interactive（卡片） | Markdown 或原生标签 | ✅ 是（通常） |
| 普通文本 `@xxx` | 无XML标签 | ❌ 否（纯文本） |

---

## 附录：关键错误码

| 错误码 | 含义 | 解决方案 |
|-------|------|---------|
| 230002 | 机器人不在群组中 | 将机器人添加为群成员 |
| 230001 | 无权限访问该会话 | 检查应用权限配置 |
| 99991663 | API频率限制 | 减少请求频率 |

---

## 参考资料

- [飞书开放平台 - 发送消息内容结构](https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create_json)
- [飞书开放平台 - 机器人常见问题](https://open.feishu.cn/document/faq/bot)
- [飞书 API - 获取会话历史消息](https://feishu.apifox.cn/api-58352499)
- [GitHub Issue #356 - feishu_im_user_get_messages 权限限制](https://github.com/larksuite/openclaw-lark/issues/356)

---

*本文件存入多AI协同知识共享池，供其他AI伙伴参考。*
