#!/usr/bin/env python3
"""
德胧AI Native - CrewAI 预订助手 Demo
基于开源CrewAI框架（github.com/crewAI/crewAI）

本文件为概念验证，实际部署需在本地环境运行：
  pip install crewai
  pip install 'crewai[tools]'

角色设计：
- 信息提取员：从自然语言提取预订结构化信息
- 档案匹配员：关联协议客户历史记录
- PMS录入员：生成PMS录入格式
"""

from crewai import Agent, Task, Crew, Process
from textwrap import dedent

# === Agent 定义 ===

info_extractor = Agent(
    role="预订信息提取员",
    goal="从文字提取结构化预订信息（客户名/电话/房型/天数/价格/特殊要求）",
    backstory="你是在德胧集团酒店工作5年的预订专员，擅长从各种描述中快速提取关键信息。",
    verbose=True
)

client_matcher = Agent(
    role="客户档案匹配员", 
    goal="关联协议客户历史偏好（价格/房型/礼遇/联系人）",
    backstory="你掌握德胧集团18个核心协议客户的详细信息，能快速匹配新订单。",
    verbose=True
)

pms_recorder = Agent(
    role="PMS录入员",
    goal="生成PMS系统标准录入格式，发给前台确认",
    backstory="你是天津瑞湾开元名都的前台主管，熟悉PMS系统所有录入规范。", 
    verbose=True
)

# === Task 定义 ===

extract_task = Task(
    description="从以下预订文字提取信息：'{booking_text}'",
    agent=info_extractor,
    expected_output="JSON格式：{客户名,电话,房型,天数,入住日期,价格,付费方式,特殊要求}"
)

match_task = Task(
    description="根据提取的客户名'{client_name}'查询客户档案，返回历史偏好和对应协议价",
    agent=client_matcher,
    expected_output="JSON格式：{客户类型,协议价,折扣,礼遇,联系人}"
)

pms_task = Task(
    description="根据提取信息和档案匹配结果，生成标准PMS录入格式",
    agent=pms_recorder,
    expected_output="飞书卡片格式，包含所有预订字段，@前台确认"
)

# === Crew 执行 ===

booking_crew = Crew(
    agents=[info_extractor, client_matcher, pms_recorder],
    tasks=[extract_task, match_task, pms_task],
    process=Process.sequential,  # 顺序执行
    verbose=True
)

# === 运行示例 ===

if __name__ == "__main__":
    result = booking_crew.kickoff(
        inputs={
            "booking_text": "朱辉 SLCDDX公司，2间大床，350元，住3天，4月15到18，公付挂账"
        }
    )
    print(result)
