# ComfyUI 本地 API 服务

## 服务状态

| 项目 | 状态 |
|------|------|
| 服务地址 | http://localhost:8188 |
| 运行状态 | ✅ 运行中 |
| 进程 PID | 274119 |
| 输出目录 | /home/gem/workspace/comfyui-server/output |

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 健康检查 |
| `/system_stats` | GET | 系统状态 |
| `/prompt` | POST | 提交生成任务 |
| `/history/<id>` | GET | 查询任务结果 |
| `/view` | GET | 查看生成文件 |
| `/queue` | GET | 队列状态 |

## 共享池调用方式

### 1. 日报生成场景

```bash
# 生成日报配图
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": {
      "3": {
        "class_type": "CLIPTextEncode",
        "inputs": {"text": "德胧集团酒店日报封面, 数据可视化, 商务风格"}
      }
    }
  }'
```

### 2. 数字人播报场景

```bash
# 生成播报背景
curl -X POST http://localhost:8188/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": {
      "3": {
        "class_type": "CLIPTextEncode", 
        "inputs": {"text": "数字人新闻播报背景, 科技感, 蓝色调, 专业"}
      }
    }
  }'
```

### 3. OpenClaw 集成

在 `openclaw.json` 中添加 ComfyUI Provider:

```json
{
  "models": {
    "providers": {
      "comfyui-local": {
        "type": "custom",
        "baseUrl": "http://localhost:8188",
        "models": ["text2image", "text2video"]
      }
    }
  }
}
```

## 工作流类型

| 类型 | 触发节点 | 说明 |
|------|----------|------|
| text2image | EmptyLatentImage | 文生图 |
| image2video | LoadImage | 图生视频（待实现）|
| text2video | Video/Animate | 文生视频（待实现）|

## 管理命令

```bash
# 查看服务状态
curl http://localhost:8188/health

# 查看队列
curl http://localhost:8188/queue

# 重启服务
pkill -f comfyui_api.py
nohup python3 /home/gem/workspace/comfyui-server/comfyui_api.py > /tmp/comfyui.log 2>&1 &
```
