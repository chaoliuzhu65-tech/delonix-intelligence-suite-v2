#!/usr/bin/env python3
"""
Guardian CLI - 命令行工具
"""

import sys
import argparse
import json
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from guardian import Guardian, TaskConfig, GuardedTask


def cmd_init(args):
    """初始化配置"""
    config_dir = Path.home() / ".guardian"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    config_file = config_dir / "config.json"
    default_config = {
        "max_duration": 300,
        "max_iterations": 3,
        "checkpoint_interval": 60,
        "quality_threshold": 0.8,
        "confirm_on_threshold": True,
        "degradation_enabled": True
    }
    
    with open(config_file, 'w') as f:
        json.dump(default_config, f, indent=2)
    
    print(f"✅ 配置已初始化: {config_file}")
    return 0


def cmd_start(args):
    """启动守护任务"""
    config = TaskConfig(
        max_duration=args.max_time,
        max_iterations=args.max_iter,
        quality_threshold=args.threshold,
        verbose=True
    )
    
    task_name = args.task or "guarded_task"
    
    print(f"🛡️  启动守护任务: {task_name}")
    print(f"   ⏱️  时间限制: {config.max_duration}s")
    print(f"   🔄 迭代限制: {config.max_iterations}")
    print(f"   📊 质量阈值: {config.quality_threshold}")
    print()
    print("任务正在运行... (按 Ctrl+C 停止)")
    
    try:
        # 这里可以执行实际的任务
        import time
        with Guardian(config, task_name) as guard:
            iteration = 0
            while guard.can_continue():
                iteration = guard.iteration_start()
                
                # 模拟工作
                time.sleep(1)
                
                # 保存检查点
                guard.checkpoint({"iteration": iteration, "status": "working"})
                
                # 模拟结果
                result = {"iteration": iteration, "quality": 0.8}
                
                if guard.meets_threshold(result):
                    guard.deliver(result, "quality_met")
                    break
                    
            if not guard.state.delivered:
                guard.deliver(result, "max_iterations")
                
    except KeyboardInterrupt:
        print("\n🛑 用户中断")
        return 1
    
    return 0


def cmd_status(args):
    """查看状态"""
    checkpoint_dir = Path.home() / ".guardian" / "checkpoints"
    
    if not checkpoint_dir.exists():
        print("❌ 没有检查点数据")
        return 1
    
    checkpoints = list(checkpoint_dir.glob("*.pkl"))
    
    print(f"📁 检查点目录: {checkpoint_dir}")
    print(f"📊 检查点数量: {len(checkpoints)}")
    
    if checkpoints:
        print("\n最近检查点:")
        for cp in sorted(checkpoints, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            import pickle
            try:
                with open(cp, 'rb') as f:
                    data = pickle.load(f)
                print(f"   - {cp.name}: {data.get('task', 'unknown')} @ {data.get('timestamp', 'unknown')}")
            except:
                print(f"   - {cp.name}: (无法读取)")
    
    return 0


def cmd_demo(args):
    """运行演示"""
    from guardian import demo
    demo()
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Anti-Deadloop Guardian - 防死循环守护工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  guardian init                           # 初始化配置
  guardian start -t "my_task" -T 300      # 启动5分钟任务
  guardian status                         # 查看状态
  guardian demo                           # 运行演示
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # init 命令
    init_parser = subparsers.add_parser('init', help='初始化配置')
    
    # start 命令
    start_parser = subparsers.add_parser('start', help='启动守护任务')
    start_parser.add_argument('-t', '--task', type=str, help='任务名称')
    start_parser.add_argument('-T', '--max-time', type=int, default=300, help='最大时间(秒)')
    start_parser.add_argument('-I', '--max-iter', type=int, default=3, help='最大迭代次数')
    start_parser.add_argument('-Q', '--threshold', type=float, default=0.8, help='质量阈值')
    
    # status 命令
    status_parser = subparsers.add_parser('status', help='查看状态')
    
    # demo 命令
    demo_parser = subparsers.add_parser('demo', help='运行演示')
    
    args = parser.parse_args()
    
    if args.command == 'init':
        return cmd_init(args)
    elif args.command == 'start':
        return cmd_start(args)
    elif args.command == 'status':
        return cmd_status(args)
    elif args.command == 'demo':
        return cmd_demo(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
