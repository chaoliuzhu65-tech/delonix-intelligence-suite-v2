# CrewAI + MCP + AutoGen 德胧落地指南

> 来源：AI伙伴团队协作研究 | 状态：✅ 已确认执行

## 架构确认

| 层级 | 方案 | 德胧价值 |
|------|------|---------|
| 编排核心 | CrewAI | 角色化多Agent，开箱即用 |
| 互通标准 | MCP协议 | 跨平台无障碍通信 |
| 复杂补充 | AutoGen | 灵活协作场景 |

## CrewAI 核心概念

### 四大组件
1. **Agent（角色）** — 定义角色、目的、工具
2. **Task（任务）** — 具体工作单元
3. **Process（流程）** — Sequential（顺序）/ Hierarchical（层级）/ Crew（并行）
4. **Crew（团队）** — Agent+Task+Process的完整执行单元

### 德胧龙虾角色设计示例
```python
# 示例：德胧预订助手龙虾团队
booking_crew = Crew(
    agents=[
        Agent(role="预订信息提取员", goal="从文字提取结构化预订信息"),
        Agent(role="客户档案匹配员", goal="关联协议客户历史偏好"),
        Agent(role="PMS录入员", goal="生成PMS录入格式"),
    ],
    tasks=[extract_task, match_task, pms_task],
    process=Process.sequential
)
```

## MCP协议适配

### MCP Server设计（德胧版）
```json
{
  "name": "delonix-mcp-server",
  "tools": [
    "feishu_search_messages",  // 搜索群消息
    "feishu_create_task",       // 创建飞书任务
    "hotel_booking_extract",    // 预订信息提取
    "hotel_client_lookup"       // 客户档案查询
  ]
}
```

## 落地计划

- [ ] 2026-04-10：安装测试CrewAI（pip install crewai）
- [ ] 2026-04-11：设计德胧预订助手Crew
- [ ] 2026-04-12：对接飞书MCP Server
- [ ] 2026-04-13：多龙虾协作测试

## 参考文档

- CrewAI: github.com/crewAI/crewAI
- MCP: modelcontextprotocol.io
- AutoGen: github.com/microsoft/autogen
