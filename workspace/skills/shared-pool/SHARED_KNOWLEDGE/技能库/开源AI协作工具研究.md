

---

## 18:10 开源优先原则 + 三大成熟方案发现

### 底层规则写入（已完成）

**新增核心原则 #1：开源优先，不造轮子**
写入文件：`skills/ai-partner-protocol/SKILL.md`
内容：德胧AI Native的80%已有成熟开源方案，每个AI伙伴必须先搜索、先学习、先复用，禁止闷头自研。

### 三大开源方案发现

#### 1. MCP（Model Context Protocol）⭐⭐⭐ 最高优先级
- **定位**：AI的"USB-C接口"——连接AI与外部系统的开放标准
- **官网**：modelcontextprotocol.io
- **现状**：Anthropic Claude、OpenAI、VS Code、Cursor等已全面支持
- **德胧价值**：统一连接妙搭/火山引擎/腾讯云/Workbuddy/Gemini的数据和工具
- **立即可用**：已有 OpenClaw MCP 支持！

#### 2. MCP Jam
- **定位**：多Agent编排框架，共享状态+MCP工具
- **官网**：docs.mcpjam.com
- **特点**：Build multi-agent applications by composing agents with shared state and MCP tools
- **德胧价值**：多"龙虾"共享上下文、协同任务分配

#### 3. AutoGen（Microsoft）
- **定位**：微软开源的多Agent对话框架
- **官网**：github.com/microsoft/autogen
- **特点**：enable next generation of LLM applications，Agent间对话协作
- **德胧价值**：直接可部署的多Agent框架

#### 4. CrewAI
- **定位**：Role-based AI agent框架
- **特点**：类似德胧的"各司其职"龙虾体系
- **德胧价值**：参考角色分工设计

### 立即行动计划

- [ ] 研究 OpenClaw 的 MCP 支持（skills/里已有clawhub）
- [ ] 研究 MCP Jam 作为多龙虾协调层
- [ ] 优先部署 MCP，打通妙搭+火山引擎+腾讯云+Workbuddy的连接

### 参考：ClawHub技能市场
clawhub.ai — OpenClaw的技能市场，已有大量可安装技能
