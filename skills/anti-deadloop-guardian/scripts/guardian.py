#!/usr/bin/env python3
"""
Anti-Deadloop Guardian - 防死循环守护模块
核心实现：时间盒、迭代限制、检查点、降级策略
"""

import time
import json
import signal
import pickle
from dataclasses import dataclass, asdict
from typing import Any, Optional, Callable, Dict
from datetime import datetime
from pathlib import Path
import threading


@dataclass
class TaskConfig:
    """任务配置"""
    max_duration: int = 300        # 最大持续时间(秒)，默认5分钟
    max_iterations: int = 3        # 最大迭代次数
    checkpoint_interval: int = 60  # 检查点间隔(秒)
    quality_threshold: float = 0.8 # 质量阈值(0-1)
    confirm_on_threshold: bool = True  # 超阈值时是否询问
    degradation_enabled: bool = True   # 启用降级
    verbose: bool = True           # 详细输出
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TaskConfig':
        return cls(**data)


class GuardianState:
    """守护状态"""
    def __init__(self):
        self.start_time: float = 0
        self.iteration: int = 0
        self.checkpoints: list = []
        self.last_checkpoint_time: float = 0
        self.is_running: bool = False
        self.result: Any = None
        self.delivered: bool = False
        self.stop_requested: bool = False
        
    def to_dict(self) -> Dict:
        return {
            'start_time': self.start_time,
            'iteration': self.iteration,
            'checkpoint_count': len(self.checkpoints),
            'is_running': self.is_running,
            'delivered': self.delivered,
            'elapsed': time.time() - self.start_time if self.start_time else 0
        }


class Guardian:
    """防死循环守护器"""
    
    def __init__(self, config: TaskConfig = None, task_name: str = "task"):
        self.config = config or TaskConfig()
        self.task_name = task_name
        self.state = GuardianState()
        self._checkpoint_dir = Path.home() / ".guardian" / "checkpoints"
        self._checkpoint_dir.mkdir(parents=True, exist_ok=True)
        self._timer = None
        self._lock = threading.Lock()
        
    def start(self) -> 'Guardian':
        """启动守护"""
        self.state.start_time = time.time()
        self.state.is_running = True
        self._setup_timeout_handler()
        self.checkpoint({"status": "started", "task": self.task_name})
        
        if self.config.verbose:
            print(f"🛡️  Guardian 启动: {self.task_name}")
            print(f"   ⏱️  时间限制: {self.config.max_duration}s")
            print(f"   🔄 迭代限制: {self.config.max_iterations}")
            print(f"   📊 质量阈值: {self.config.quality_threshold}")
            
        return self
    
    def _setup_timeout_handler(self):
        """设置超时处理器"""
        def timeout_handler(signum, frame):
            self._handle_timeout()
            
        # 使用定时器线程而不是 signal（更兼容）
        self._timer = threading.Timer(self.config.max_duration, self._handle_timeout)
        self._timer.daemon = True
        self._timer.start()
    
    def _handle_timeout(self):
        """处理超时"""
        with self._lock:
            if not self.state.is_running or self.state.delivered:
                return
                
            print(f"\n⚠️  任务超时 ({self.config.max_duration}s)")
            
            if self.state.result is not None:
                print("📦 交付当前最佳结果...")
                self.deliver(self.state.result, reason="timeout")
            else:
                print("❌ 无可用结果，任务终止")
                self.state.is_running = False
    
    def can_continue(self) -> bool:
        """检查是否可以继续"""
        with self._lock:
            if not self.state.is_running:
                return False
                
            elapsed = time.time() - self.state.start_time
            
            # 检查时间
            if elapsed >= self.config.max_duration:
                return False
                
            # 检查迭代次数
            if self.state.iteration >= self.config.max_iterations:
                return False
                
            # 检查停止请求
            if self.state.stop_requested:
                return False
                
            return True
    
    def iteration_start(self) -> int:
        """开始新一轮迭代"""
        with self._lock:
            self.state.iteration += 1
            current = self.state.iteration
            
        elapsed = time.time() - self.state.start_time
        remaining = self.config.max_duration - elapsed
        
        if self.config.verbose:
            print(f"\n🔄 迭代 {current}/{self.config.max_iterations} | 剩余时间: {remaining:.0f}s")
            
        return current
    
    def checkpoint(self, data: Any = None) -> str:
        """保存检查点"""
        with self._lock:
            checkpoint_id = f"{self.task_name}_{int(time.time())}"
            checkpoint_data = {
                'id': checkpoint_id,
                'timestamp': time.time(),
                'iteration': self.state.iteration,
                'elapsed': time.time() - self.state.start_time,
                'data': data
            }
            
            self.state.checkpoints.append(checkpoint_data)
            self.state.last_checkpoint_time = time.time()
            
            # 保存到文件
            checkpoint_file = self._checkpoint_dir / f"{checkpoint_id}.pkl"
            try:
                with open(checkpoint_file, 'wb') as f:
                    pickle.dump(checkpoint_data, f)
            except Exception as e:
                if self.config.verbose:
                    print(f"   ⚠️  检查点保存警告: {e}")
            
            return checkpoint_id
    
    def meets_threshold(self, result: Any, evaluator: Callable = None) -> bool:
        """检查是否达到质量阈值"""
        if evaluator:
            quality = evaluator(result)
        elif isinstance(result, dict) and 'quality' in result:
            quality = result['quality']
        elif isinstance(result, (int, float)):
            quality = result
        else:
            # 默认假设达标（避免无限等待）
            quality = 0.5
            
        meets = quality >= self.config.quality_threshold
        
        if self.config.verbose:
            status = "✅" if meets else "❌"
            print(f"   {status} 质量评估: {quality:.2f} / {self.config.quality_threshold}")
            
        return meets
    
    def deliver(self, result: Any, reason: str = "completed") -> Dict:
        """交付结果"""
        with self._lock:
            self.state.result = result
            self.state.delivered = True
            self.state.is_running = False
            
            elapsed = time.time() - self.state.start_time
            
            delivery_info = {
                'task': self.task_name,
                'status': 'delivered',
                'reason': reason,
                'iterations': self.state.iteration,
                'elapsed_time': elapsed,
                'checkpoints': len(self.state.checkpoints),
                'timestamp': datetime.now().isoformat()
            }
            
            if self.config.verbose:
                print(f"\n📦 任务交付")
                print(f"   原因: {reason}")
                print(f"   迭代: {self.state.iteration}/{self.config.max_iterations}")
                print(f"   用时: {elapsed:.1f}s / {self.config.max_duration}s")
                print(f"   检查点: {len(self.state.checkpoints)}")
                
            # 取消定时器
            if self._timer:
                self._timer.cancel()
                
            return delivery_info
    
    def get_progress(self) -> Dict:
        """获取进度"""
        elapsed = time.time() - self.state.start_time if self.state.start_time else 0
        
        return {
            'task': self.task_name,
            'is_running': self.state.is_running,
            'iteration': self.state.iteration,
            'max_iterations': self.config.max_iterations,
            'elapsed': elapsed,
            'max_duration': self.config.max_duration,
            'progress_pct': min(100, (elapsed / self.config.max_duration) * 100),
            'iteration_pct': min(100, (self.state.iteration / self.config.max_iterations) * 100),
            'checkpoints': len(self.state.checkpoints)
        }
    
    def report_progress(self):
        """报告进度"""
        progress = self.get_progress()
        
        print(f"\n📊 任务进度: {self.task_name}")
        print(f"   时间: {progress['elapsed']:.0f}s / {progress['max_duration']}s ({progress['progress_pct']:.0f}%)")
        print(f"   迭代: {progress['iteration']} / {progress['max_iterations']} ({progress['iteration_pct']:.0f}%)")
        print(f"   状态: {'运行中' if progress['is_running'] else '已停止'}")
        
        return progress
    
    def stop(self):
        """停止任务"""
        with self._lock:
            self.state.stop_requested = True
            self.state.is_running = False
            
        if self._timer:
            self._timer.cancel()
            
        if self.config.verbose:
            print("\n🛑 任务被手动停止")
    
    def __enter__(self):
        """上下文管理器入口"""
        return self.start()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器退出"""
        if not self.state.delivered and self.state.is_running:
            if self.state.result is not None:
                self.deliver(self.state.result, reason="context_exit")
            else:
                self.state.is_running = False
                
        if self._timer:
            self._timer.cancel()


class GuardedTask:
    """任务装饰器"""
    
    def __init__(self, config: TaskConfig = None, task_name: str = None):
        self.config = config or TaskConfig()
        self.task_name = task_name
        
    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            task_name = self.task_name or func.__name__
            
            with Guardian(self.config, task_name) as guard:
                result = func(guard, *args, **kwargs)
                
                if not guard.state.delivered:
                    guard.deliver(result, reason="function_completed")
                    
                return result
                
        return wrapper


def demo():
    """演示用法"""
    print("=" * 50)
    print("Anti-Deadloop Guardian 演示")
    print("=" * 50)
    
    # 配置
    config = TaskConfig(
        max_duration=10,       # 10秒上限
        max_iterations=3,      # 最多3轮
        checkpoint_interval=3, # 每3秒检查点
        quality_threshold=0.85,
        verbose=True
    )
    
    # 使用上下文管理器
    with Guardian(config, "demo_task") as guard:
        while guard.can_continue():
            iter_num = guard.iteration_start()
            
            # 模拟工作
            print(f"   执行迭代 {iter_num} 的工作...")
            time.sleep(2)
            
            # 模拟质量评估
            quality = 0.7 + iter_num * 0.1  # 每轮提升
            result = {"iteration": iter_num, "quality": quality, "data": f"result_{iter_num}"}
            
            # 保存检查点
            guard.checkpoint(result)
            
            # 检查是否达标
            if guard.meets_threshold(result):
                guard.deliver(result, reason="quality_threshold_met")
                break
                
            # 每轮后报告进度
            guard.report_progress()
    
    print("\n✅ 演示完成")


if __name__ == "__main__":
    demo()
