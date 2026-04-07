# [[Feishu Tenant]]

## 一句话定义
飞书企业级部署单元，提供组织级的应用权限和数据隔离。

## 核心要点

### 在知识库中的作用
- 作为 **Shared Pool** 的权限边界
- 控制哪些 AI 可以访问共享知识
- 实现企业级数据安全

### 配置要点
1. **事件订阅** - WebSocket 长连接模式
2. **权限范围** - 租户内全员 or 指定部门
3. **加密配置** - Encrypt Key / Verification Token

### 当前问题
飞书 WebSocket 返回 400 错误，可能原因：
- Encrypt Key 配置错误
- 订阅方式未开启"长连接"
- IP 白名单限制

## 来源
- [[运营组周会纪要]](raw/my-meeting-2025-04-07.md)

## 相关概念
- [[Shared Pool]] - 依赖租户权限
- [[OpenClaw]] - 集成平台

---
Created: 2025-04-07
Updated: 2025-04-07
Tags: #feishu #enterprise #security
