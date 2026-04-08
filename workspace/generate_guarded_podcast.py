#!/usr/bin/env python3
"""
使用防死循环机制生成播客
5-8分钟版本，带检查点和自动降级
"""

import sys
import time
from pathlib import Path

# 添加 guardian 到路径
sys.path.insert(0, str(Path.home() / "workspace/agent/skills/anti-deadloop-guardian/scripts"))

from guardian import Guardian, TaskConfig


def generate_podcast_with_guardian():
    """
    使用 Guardian 生成播客的示例
    演示如何在有保护的情况下执行迭代任务
    """
    
    # 配置：5-8分钟播客生成
    config = TaskConfig(
        max_duration=480,        # 8分钟硬上限
        max_iterations=3,        # 最多3轮优化
        checkpoint_interval=60,  # 每60秒保存
        quality_threshold=0.85,  # 85分算合格
        verbose=True
    )
    
    # 播客内容模板
    podcast_content = {
        "title": "神灯AI：德胧集团的酒店智能化革命",
        "sections": [
            {"name": "开场", "duration": 30, "content": ""},
            {"name": "服务闭环介绍", "duration": 90, "content": ""},
            {"name": "效率数据", "duration": 120, "content": ""},
            {"name": "真实案例", "duration": 90, "content": ""},
            {"name": "结语", "duration": 30, "content": ""}
        ]
    }
    
    task_name = "神灯AI播客生成"
    
    with Guardian(config, task_name) as guard:
        print("🎙️  开始生成播客...")
        print(f"   目标时长: 5-8分钟")
        print()
        
        # 第1轮：生成基础脚本
        iteration = guard.iteration_start()
        print(f"📄 第1轮：生成基础脚本")
        
        script = generate_base_script(podcast_content)
        guard.checkpoint({"round": 1, "script_length": len(script), "status": "base_generated"})
        
        # 模拟质量评估
        quality = 0.70
        print(f"   质量评估: {quality:.0%}")
        
        if guard.meets_threshold({"quality": quality}):
            guard.deliver(script, "quality_met_round1")
            return script
        
        # 检查是否继续
        if not guard.can_continue():
            guard.deliver(script, "timeout_or_max_iter")
            return script
        
        # 第2轮：优化对话和节奏
        iteration = guard.iteration_start()
        print(f"\n✨ 第2轮：优化对话流畅度")
        
        script = optimize_dialogue(script)
        guard.checkpoint({"round": 2, "script_length": len(script), "status": "dialogue_optimized"})
        
        quality = 0.82
        print(f"   质量评估: {quality:.0%}")
        
        if guard.meets_threshold({"quality": quality}):
            guard.deliver(script, "quality_met_round2")
            return script
        
        if not guard.can_continue():
            guard.deliver(script, "timeout_or_max_iter")
            return script
        
        # 第3轮：最终润色
        iteration = guard.iteration_start()
        print(f"\n🎨 第3轮：最终润色")
        
        script = final_polish(script)
        guard.checkpoint({"round": 3, "script_length": len(script), "status": "final_polished"})
        
        quality = 0.90
        print(f"   质量评估: {quality:.0%}")
        
        # 交付最终版本
        guard.deliver(script, "all_iterations_completed")
        return script


def generate_base_script(content):
    """生成基础脚本"""
    # 模拟生成过程
    time.sleep(2)
    
    script = """
【播客脚本：神灯AI案例】

开场：
大家好，欢迎收听本期节目。2026年3月30日，德胧集团发布了神灯AI系统。

主体：
神灯AI构建了完整的服务闭环：需求感知、智能调度、人力执行、数据回流。

数据亮点：
- 入住速度：15分钟 → 10秒
- 工单处理效率提升：83%
- 竞对分析效率提升：98%
- 知识库填充效率提升：500%
- 投资回报率：948%

案例：
深夜抵达的商务客人，通过APP发起加床需求。传统流程需15-20分钟，神灯AI系统在10秒内完成派单，5分钟后服务员敲门服务。

结语：
德胧的神灯AI正在用数据证明：AI在酒店行业不是概念，而是实实在在的效率革命。
"""
    return script


def optimize_dialogue(script):
    """优化对话"""
    time.sleep(2)
    
    optimized = script + """

【优化内容】
- 增加主播互动感
- 调整语速节奏
- 添加过渡语句
- 优化数据呈现方式
"""
    return optimized


def final_polish(script):
    """最终润色"""
    time.sleep(2)
    
    polished = script + """

【润色完成】
✓ 总时长：约6分钟
✓ 对话自然流畅
✓ 数据清晰有力
✓ 案例生动具体
✓ 适合中文播客播出
"""
    return polished


def main():
    """主函数"""
    print("=" * 60)
    print("🛡️  防死循环播客生成器")
    print("=" * 60)
    print()
    
    try:
        result = generate_podcast_with_guardian()
        
        print("\n" + "=" * 60)
        print("✅ 播客生成完成！")
        print("=" * 60)
        print("\n生成的脚本预览：")
        print("-" * 60)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("-" * 60)
        
        # 保存结果
        output_file = Path.home() / "workspace/agent/workspace/podcast_script_guarded.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        
        print(f"\n📁 脚本已保存: {output_file}")
        
    except KeyboardInterrupt:
        print("\n\n🛑 用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
