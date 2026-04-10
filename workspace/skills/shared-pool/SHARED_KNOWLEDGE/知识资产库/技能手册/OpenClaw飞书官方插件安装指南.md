# OpenClaw飞书官方插件接入安装指南

> 创建时间: 2026-03-16
> 来源: 飞书官方文档
> 文档链接: https://delonix.feishu.cn/docx/I3vEdhVbooeDN1xlvSdcHVeVnyb
> 存入共享池时间: 2026-04-10

---

## 插件能力

| 业务模块 | 支持能力 |
|----------|----------|
| 💬 消息 | 读取群聊/单聊历史、搜索消息、发送消息/卡片、下载图片文件 |
| 📄 文档 | 创建云文档、读取内容、更新文档 |
| 📊 多维表格 | 创建/管理数据表、增删改查记录、管理字段和视图 |
| 📊 电子表格 | 创建、编辑、查看表格内容 |
| 📅 日历 | 创建日程、查询忙闲、管理参会人、删除日程 |
| ✅ 任务 | 创建/更新任务、管理清单、添加子任务和评论 |

---

## 安装步骤

```bash
# 1. 安装命令
npx -y @larksuite/openclaw-lark-tools install

# 2. 完成后发送 /feishu auth 完成权限授权
# 3. 发送 /feishu start 验证安装
```

---

## 推荐配置

```bash
# 流式输出
openclaw config set channels.feishu.streaming true
openclaw config set channels.feishu.footer.elapsed true
openclaw config set channels.feishu.footer.status true

# 话题独立上下文（群聊推荐）
openclaw config set channels.feishu.threadSession true

# 群聊回复方式（默认@才回复）
openclaw config set channels.feishu.requireMention true
```

---

## 诊断命令

| 命令 | 作用 |
|------|------|
| `/feishu start` | 检查安装是否成功 |
| `/feishu doctor` | 自动检查配置异常 |
| `/feishu auth` | 一键完成所有权限批量授权 |

```bash
# 命令行诊断
npx @larksuite/openclaw-lark-tools doctor --fix
```

---

## 安全提示

⚠️ **重要**：
1. 先拿个人账号安全地「玩」起来
2. 接入工作环境前确认符合企业数据安全要求
3. 重要操作务必「先预览，再确认」，不要让AI完全脱离人工干预

---

## 官方资源

- 完整官方指南: https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh
- GitHub: https://github.com/larksuite/openclaw-lark
- 一键创建多机器人: https://open.feishu.cn/page/openclaw?form=multiAgent

---

*由方源兵分享，已存入共享池*
