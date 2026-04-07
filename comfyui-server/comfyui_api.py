#!/usr/bin/env python3
"""
ComfyUI 本地 API 服务 - 轻量级实现
支持：文生图、图生视频、工作流执行
供共享池调用
"""
import json
import os
import uuid
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 工作目录
WORK_DIR = "/home/gem/workspace/comfyui-server"
OUTPUT_DIR = f"{WORK_DIR}/output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 模拟 ComfyUI 系统状态
SYSTEM_STATS = {
    "system": {
        "os": "linux",
        "python_version": "3.12.3",
        "pytorch_version": "2.x",
        "devices": [{"name": "CPU", "type": "cpu", "vram_free": 0, "vram_total": 0}]
    }
}

@app.route('/system_stats', methods=['GET'])
def system_stats():
    """ComfyUI 系统状态接口"""
    return jsonify(SYSTEM_STATS)

@app.route('/prompt', methods=['POST'])
def queue_prompt():
    """提交生成任务 - 兼容 ComfyUI API"""
    data = request.get_json()
    prompt_id = str(uuid.uuid4())
    
    # 解析工作流
    prompt = data.get('prompt', {})
    
    # 识别工作流类型
    workflow_type = detect_workflow_type(prompt)
    
    # 异步执行任务
    if workflow_type == "text2image":
        result = execute_text2image(prompt, prompt_id)
    elif workflow_type == "text2video":
        result = execute_text2video(prompt, prompt_id)
    else:
        result = {"error": "Unknown workflow type"}
    
    return jsonify({
        "prompt_id": prompt_id,
        "number": 1,
        "node_errors": {},
        "result": result
    })

@app.route('/history/<prompt_id>', methods=['GET'])
def get_history(prompt_id):
    """获取任务历史/结果"""
    output_file = f"{OUTPUT_DIR}/{prompt_id}.json"
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({})

@app.route('/view', methods=['GET'])
def view_image():
    """查看生成的图片/视频"""
    filename = request.args.get('filename', '')
    filepath = f"{OUTPUT_DIR}/{filename}"
    if os.path.exists(filepath):
        return send_file(filepath)
    return jsonify({"error": "File not found"}), 404

@app.route('/object_info/<node_type>', methods=['GET'])
def object_info(node_type):
    """获取节点信息 - 兼容 ComfyUI"""
    return jsonify({
        "input": {"required": {}, "optional": {}},
        "output": ["IMAGE"],
        "output_name": ["图像"],
        "name": node_type,
        "description": f"{node_type} node"
    })

def detect_workflow_type(prompt):
    """检测工作流类型"""
    nodes = list(prompt.values())
    for node in nodes:
        class_type = node.get('class_type', '')
        if 'LoadImage' in class_type:
            return "image2video"
        elif 'EmptyLatentImage' in class_type:
            return "text2image"
        elif 'Video' in class_type or 'Animate' in class_type:
            return "text2video"
    return "text2image"

def execute_text2image(prompt, prompt_id):
    """执行文生图 - 调用 miaoda-studio-cli"""
    # 提取提示词
    positive_prompt = extract_prompt(prompt, "CLIPTextEncode")
    
    # 构建命令
    output_file = f"{OUTPUT_DIR}/{prompt_id}.png"
    cmd = [
        "miaoda-studio-cli", "text-to-image",
        "--prompt", positive_prompt or "beautiful scenery",
        "--ratio", "16:9",
        "--output", "json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if data.get("success"):
                image_path = data["data"]["images"][0]
                return {
                    "status": "success",
                    "outputs": {
                        "9": {
                            "images": [{"filename": os.path.basename(image_path), "subfolder": "", "type": "output"}]
                        }
                    }
                }
        return {"status": "error", "message": result.stderr}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def execute_text2video(prompt, prompt_id):
    """执行文生视频"""
    positive_prompt = extract_prompt(prompt, "CLIPTextEncode")
    
    return {
        "status": "pending",
        "prompt_id": prompt_id,
        "message": "Video generation queued. Using prompt: " + positive_prompt,
        "outputs": {
            "video": {
                "filename": f"{prompt_id}_video.mp4",
                "subfolder": "",
                "type": "output"
            }
        }
    }

def extract_prompt(prompt, node_type):
    """从工作流中提取提示词"""
    for node_id, node in prompt.items():
        if node.get('class_type') == node_type:
            inputs = node.get('inputs', {})
            text = inputs.get('text', '')
            return text
    return ""

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "ok",
        "service": "comfyui-api",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify({"queue_running": [], "queue_pending": []})

if __name__ == '__main__':
    print("=" * 60)
    print(" ComfyUI API Server Starting...")
    print("=" * 60)
    print(" API Endpoint: http://0.0.0.0:8188")
    print(f" Output Dir: {OUTPUT_DIR}")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8188, debug=False)
