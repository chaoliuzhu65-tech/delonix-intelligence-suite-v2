---
name: anti-deadloop-guardian
description: |
  防死循环守护技能。当执行可能长时间运行或迭代优化的任务时自动激活。
  提供时间盒管理、迭代次数限制、检查点保存、自动降级、用户确认等机制。
  触发词：死循环、超时控制、迭代限制、检查点、时间盒、任务边界
---

# Anti-Deadloop Guardian - 防死循环守护

## 核心功能

防止 AI 在执行任务时陷入无限循环或过度优化的防护系统。

### 防护机制

| 机制 | 说明 | 触发条件 |
|------|------|---------|
| **时间盒** | 强制时间限制 | 任务超时 |
| **迭代上限** | 最大迭代次数 | 超过设定轮次 |
| **检查点** | 定期保存进度 | 按时间/轮次间隔 |
| **质量阈值** | 足够好的标准 | 达到预设质量 |
| **用户确认** | 超限需确认 | 超过边界时 |
| **自动降级** | 简化方案 | 主方案失败/超时 |

---

## 使用方式

### 方式1: 装饰器模式 (推荐)

```python
from guardian import GuardedTask, TaskConfig

config = TaskConfig(
    max_duration=300,      # 5分钟上限
    max_iterations=3,      # 最多3轮优化
    checkpoint_interval=60, # 每60秒保存
    quality_threshold=0.85  # 质量阈值
)

@GuardedTask(config)
def generate_podcast():
    # 任务逻辑
    pass
```

### 方式2: 上下文管理器

```python
from guardian import GuardianContext

with GuardianContext(max_time=300, max_iter=3) as guard:
    while guard.can_continue():
        result = do_work()
        if guard.meets_threshold(result):
            break
    guard.deliver(result)
```

### 方式3: CLI 命令

```bash
# 启动守护模式
guardian start --task="生成播客" --max-time=300 --max-iter=3

# 报告进度
guardian status

# 强制终止
guardian stop
```

---

## 配置参数

### 默认配置

```yaml
# ~/.guardian/config.yaml
defaults:
  max_duration: 300        # 5分钟 (秒)
  max_iterations: 3        # 最多3轮
  checkpoint_interval: 60  # 60秒保存一次
  quality_threshold: 0.8   # 80分算合格
  
  # 用户确认阈值
  confirm_threshold:
    time: 180             # 3分钟时询问
    iteration: 2          # 第2轮后询问
    
  # 降级策略
  degradation:
    enabled: true
    levels:
      - level: 1
        trigger: "time > 50%"
        action: "简化流程"
      - level: 2
        trigger: "time > 80%"
        action: "MVP交付"
```

### 任务类型预设

```yaml
presets:
  content_generation:  # 内容生成
    max_duration: 600
    max_iterations: 5
    
  data_processing:     # 数据处理
    max_duration: 300
    max_iterations: 2
    
  code_generation:     # 代码生成
    max_duration: 900
    max_iterations: 4
    
  optimization:        # 优化任务
    max_duration: 300
    max_iterations: 3
    quality_threshold: 0.85
```

---

## 工作机制

### 1. 任务启动阶段

```
初始化 Guardian
    ↓
记录开始时间
    ↓
设置定时器 (超时检测)
    ↓
创建第一个检查点
    ↓
开始执行
```

### 2. 迭代监控阶段

```
每轮迭代开始
    ↓
检查时间是否超限 → 是 → 触发超时处理
    ↓ 否
检查迭代次数 → 超限 → 强制交付
    ↓ 否
执行迭代
    ↓
评估质量 → 达标 → 交付
    ↓ 否
是否到达检查点 → 是 → 保存状态
    ↓
下一迭代
```

### 3. 超时处理阶段

```
时间盒触发
    ↓
保存当前检查点
    ↓
评估当前结果质量
    ↓
├─ 质量可接受 → 立即交付
├─ 有降级方案 → 执行降级
└─ 质量不达标 → 询问用户
         ↓
用户选择继续/交付/取消
```

---

## API 参考

### Python API

```python
class Guardian:
    def __init__(self, config: TaskConfig):
        """初始化守护器"""
        pass
    
    def start(self) -> None:
        """启动任务监控"""
        pass
    
    def checkpoint(self, data: Any) -> None:
        """保存检查点"""
        pass
    
    def can_continue(self) -> bool:
        """检查是否可以继续"""
        pass
    
    def meets_threshold(self, result: Any) -> bool:
        """检查是否达到质量阈值"""
        pass
    
    def deliver(self, result: Any, reason: str) -> None:
        """交付结果"""
        pass
    
    def degrade(self, level: int) -> Any:
        """执行降级方案"""
        pass

class TaskConfig:
    max_duration: int        # 最大持续时间(秒)
    max_iterations: int      # 最大迭代次数
    checkpoint_interval: int # 检查点间隔(秒)
    quality_threshold: float # 质量阈值(0-1)
    confirm_on_threshold: bool # 超阈值时确认
    degradation_enabled: bool  # 启用降级
```

### CLI 命令

```bash
# 基础命令
guardian init                    # 初始化配置
guardian start [options]         # 启动守护任务
guardian status                  # 查看状态
guardian checkpoint [data]       # 手动保存检查点
guardian deliver [result]        # 手动交付
guardian stop                    # 强制停止
guardian logs                    # 查看日志

# 选项
--task, -t          # 任务名称
--max-time, -T      # 最大时间(秒)
--max-iter, -I      # 最大迭代次数
--threshold, -Q     # 质量阈值
--preset, -p        # 使用预设配置
--degradation, -d   # 启用降级策略
```

---

## 使用场景示例

### 场景1: 播客生成

```python
from guardian import GuardedTask, TaskConfig

config = TaskConfig(
    max_duration=600,      # 10分钟
    max_iterations=3,      # 最多3轮
    quality_threshold=0.85,
    degradation_enabled=True
)

@GuardedTask(config)
def generate_podcast(topic: str):
    """
    第1轮: 生成基础脚本
    第2轮: 优化对话流畅度
    第3轮: 最终润色
    超时: 交付当前最佳版本
    """
    script = generate_script(topic)
    
    for i in range(config.max_iterations):
        if i > 0:
            script = optimize_script(script)
        
        quality = evaluate_script(script)
        if quality >= config.quality_threshold:
            return script
    
    return script
```

### 场景2: 数据分析

```python
config = TaskConfig(
    max_duration=300,
    max_iterations=2,    # 数据分析不需要多轮
    checkpoint_interval=30
)

@GuardedTask(config)
def analyze_data(dataset):
    """
    第1轮: 基础分析
    第2轮: 深度洞察 (可选)
    """
    result = basic_analysis(dataset)
    
    if can_continue():
        result = deep_insights(result)
    
    return result
```

### 场景3: 代码生成

```python
config = TaskConfig(
    max_duration=900,
    max_iterations=4,
    quality_threshold=0.9
)

@GuardedTask(config)
def generate_code(requirements):
    """
    第1轮: 框架代码
    第2轮: 核心功能
    第3轮: 异常处理
    第4轮: 优化重构
    """
    code = generate_skeleton(requirements)
    
    for i in range(1, config.max_iterations):
        code = refine_code(code, iteration=i)
        
        if test_pass_rate(code) >= config.quality_threshold:
            break
    
    return code
```

---

## 最佳实践

### Do's

- ✅ **始终设置时间盒** - 即使预估很快也要设上限
- ✅ **定义"完成"标准** - 质量阈值要具体可测量
- ✅ **频繁保存检查点** - 便于中断恢复
- ✅ **准备降级方案** - 主方案失败时有备选
- ✅ **超限必须询问** - 不要擅自延长

### Don'ts

- ❌ **不要追求完美** - 80分就交付，剩余20分留给下次
- ❌ **不要黑箱执行** - 每轮都要向用户展示进度
- ❌ **不要忽视警告** - 系统提示超限时立即停止
- ❌ **不要无限重试** - 失败3次就降级或询问

---

## 故障排除

### 问题: 任务被过早终止

**原因**: 时间盒设置过短

**解决**: 
```python
config = TaskConfig(
    max_duration=estimate_time() * 1.5  # 预估的1.5倍
)
```

### 问题: 迭代次数不够用

**原因**: 质量阈值过高或任务本身复杂

**解决**:
```python
# 方案1: 提高阈值
config.quality_threshold = 0.75

# 方案2: 增加迭代
config.max_iterations = 5

# 方案3: 分阶段执行
phase1 = GuardedTask(config_phase1)
phase2 = GuardedTask(config_phase2)
```

### 问题: 检查点恢复失败

**原因**: 检查点数据不完整

**解决**:
```python
# 确保检查点包含完整状态
guardian.checkpoint({
    'iteration': current_iter,
    'data': full_data,  # 不是增量
    'metadata': {...}
})
```

---

## 相关资源

- [[experience_deadloop_analysis_20250408]] - 死循环复盘
- [[experience_self_iteration_best_practices]] - 自我迭代经验
- [[timebox-timer]] - 时间盒工具
- [[checkpoint-manager]] - 检查点管理

---

**版本**: 1.0.0  
**作者**: MiaoDa  
**创建日期**: 2026-04-08  
**标签**: #防死循环 #任务管理 #时间盒 #质量阈值 #检查点
