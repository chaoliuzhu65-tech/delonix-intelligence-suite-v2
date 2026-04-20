---
name: delonix-image-understanding
description: 德胧AI龙虾军团图片理解技能。分析图片内容、提取文字、描述场景。支持图片URL和本地文件路径。触发词：图片理解、图片分析、图片描述、识别图片、看图、图片识别、image understanding。
---

# Delonix Image Understanding（德胧图片理解）

分析图片内容，支持描述、OCR提取、场景理解等多种任务。

## 依赖

**方案A（推荐）：使用OpenClaw内置图片理解**
系统已内置 `image_understanding` 工具，无需额外安装。

**方案B：使用MiniMax多模态API**
```bash
# 已在miaoda-image-understanding skill中实现
# 调用时使用对应工具
```

## 使用方式

### 方式1：使用内置工具（推荐）

直接调用系统的 `image_understanding` 工具处理图片URL或本地路径：

- 图片URL: 直接传入URL
- 本地文件: 传入文件路径

### 方式2：命令行脚本（备选）

```bash
python3 <skill-path>/scripts/image_understand.py --image <图片路径或URL> --prompt "分析需求"
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--image, -i` | 图片路径或URL | 必需 |
| `--prompt, -p` | 分析指令 | "描述图片内容" |
| `--format, -f` | 输出格式 | text |

## 使用示例

```bash
# 描述图片内容
python3 <skill-path>/scripts/image_understand.py --image screenshot.png

# 提取图片中的文字
python3 <skill-path>/scripts/image_understand.py --image scan.jpg --prompt "提取图片中所有文字"

# 分析图片风格
python3 <skill-path>/scripts/image_understand.py --image photo.jpg --prompt "分析这张图片的色彩风格和构图"
```

## 常见场景

| 场景 | prompt 示例 |
|------|------------|
| 基础描述 | "请详细描述这张图片的内容" |
| OCR提取 | "提取图片中所有文字内容" |
| 场景分析 | "分析这张图片的场景、人物、氛围" |
| 风格解读 | "分析图片的设计风格和色调" |
| 物体识别 | "识别图片中的所有物体" |

## 决策树

```
需要理解图片
├─ 有图片URL/路径 → 直接使用image_understanding工具
├─ 需要OCR → prompt指定"提取文字"
└─ 批量处理 → 循环调用image_understanding
```
