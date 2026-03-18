#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
酒店竞争分析 SKILL - 环境检测脚本
检测当前环境可用能力，给出配置建议
"""

import sys
import os
import json
from pathlib import Path

class EnvChecker:
    def __init__(self):
        self.checks = {}
        self.score = 0
        self.missing_deps = []
        self.optional_deps = []
    
    def check_python(self):
        """检测 Python"""
        try:
            import sys
            version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            self.checks['python'] = {
                'status': '✅',
                'version': version,
                'message': f'Python {version}'
            }
            return True
        except:
            self.checks['python'] = {
                'status': '❌',
                'message': 'Python 未安装'
            }
            self.missing_deps.append('python3')
            return False
    
    def check_node(self):
        """检测 Node.js"""
        import subprocess
        try:
            result = subprocess.run(['node', '--version'], capture_output=True, text=True)
            version = result.stdout.strip()
            self.checks['node'] = {
                'status': '✅',
                'version': version,
                'message': f'Node.js {version}',
                'optional': True
            }
            return True
        except:
            self.checks['node'] = {
                'status': '⚠️',
                'message': 'Node.js 未安装（可选，用于官方高德 Skill）',
                'optional': True
            }
            self.optional_deps.append('nodejs')
            return False
    
    def check_amap_key(self):
        """检测高德 API Key"""
        config_paths = [
            'config/amap_key.json',
            'config.json',
            os.path.expanduser('~/.amap_key.json')
        ]
        
        for path in config_paths:
            if os.path.exists(path):
                try:
                    with open(path, 'r') as f:
                        config = json.load(f)
                    key = config.get('webServiceKey') or config.get('key') or config.get('amap_key')
                    if key:
                        self.checks['amap_key'] = {
                            'status': '✅',
                            'message': '高德 API Key 已配置',
                            'source': path
                        }
                        self.score += 40
                        return True
                except:
                    pass
        
        # 检查环境变量
        if os.environ.get('AMAP_KEY') or os.environ.get('AMAP_WEBSERVICE_KEY'):
            self.checks['amap_key'] = {
                'status': '✅',
                'message': '高德 API Key 已配置（环境变量）'
            }
            self.score += 40
            return True
        
        self.checks['amap_key'] = {
            'status': '❌',
            'message': '高德 API Key 未配置'
        }
        return False
    
    def check_scrapling(self):
        """检测 Scrapling"""
        try:
            import scrapling
            self.checks['scrapling'] = {
                'status': '✅',
                'message': 'Scrapling 已安装（可用于 OTA 价格抓取）',
                'optional': True
            }
            self.score += 30
            return True
        except ImportError:
            self.checks['scrapling'] = {
                'status': '⚠️',
                'message': 'Scrapling 未安装（可选，用于 OTA 价格抓取）',
                'optional': True
            }
            self.optional_deps.append('scrapling')
            return False
    
    def check_brave_api(self):
        """检测 Brave API"""
        if os.environ.get('BRAVE_API_KEY'):
            self.checks['brave_api'] = {
                'status': '✅',
                'message': 'Brave API 已配置（可用于网络搜索）',
                'optional': True
            }
            self.score += 30
            return True
        else:
            self.checks['brave_api'] = {
                'status': '❌',
                'message': 'Brave API 未配置',
                'optional': True
            }
            return False
    
    def check_feishu(self):
        """检测飞书集成"""
        feishu_files = [
            'skills/feishu-bitable',
            'skills/feishu-calendar',
            'skills/feishu-im-read'
        ]
        
        installed = sum(1 for f in feishu_files if os.path.exists(f))
        
        if installed > 0:
            self.checks['feishu'] = {
                'status': '✅',
                'message': f'飞书集成已安装 ({installed} 个技能)',
                'optional': True
            }
            self.score += 10
        else:
            self.checks['feishu'] = {
                'status': '⚠️',
                'message': '飞书集成未安装（可选，用于报告分享）',
                'optional': True
            }
    
    def run_all_checks(self):
        """运行所有检测"""
        print("======================================")
        print("🏨 酒店竞争分析 SKILL - 环境检测")
        print("======================================")
        print()
        
        self.check_python()
        self.check_node()
        self.check_amap_key()
        self.check_scrapling()
        self.check_brave_api()
        self.check_feishu()
        
        # 输出检测结果
        for key, check in self.checks.items():
            status = check['status']
            message = check['message']
            optional = check.get('optional', False)
            
            print(f"{status} {message}")
        
        print()
        print("======================================")
        print("📊 能力等级评估")
        print("======================================")
        print()
        
        # 评估能力等级
        if self.score >= 80:
            level = "进阶版"
            desc = "完整数据分析 + 实时价格 + 自动监控"
            mode = "advanced"
        elif self.score >= 40:
            level = "标准版"
            desc = "基础数据分析 + 地图可视化"
            mode = "standard"
        else:
            level = "兜底版"
            desc = "手动数据 + 基础报告"
            mode = "basic"
        
        print(f"🎯 能力等级：{level} (Score: {self.score}/100)")
        print(f"📊 可用功能：{desc}")
        print()
        
        # 给出建议
        print("======================================")
        print("💡 推荐配置方案")
        print("======================================")
        print()
        
        if mode == "advanced":
            print("✅ 当前配置已支持进阶版功能")
            print()
            print("建议配置（可选优化）:")
            print("  1. 配置携程 API（获取实时价格）")
            print("  2. 配置美团 API（获取网评数据）")
            print("  3. 设置定时任务（自动监控）")
        elif mode == "standard":
            print("⚠️  当前配置支持标准版功能")
            print()
            print("升级到进阶版:")
            print("  pip install scrapling")
            print("  export BRAVE_API_KEY=your_key")
            print()
            print("配置向导:")
            print("  ./scripts/setup_wizard.sh")
        else:
            print("📝 当前为兜底版配置")
            print()
            print("升级到标准版（推荐）:")
            print("  1. 获取高德 API Key: https://lbs.amap.com/")
            print("  2. 运行配置向导：./scripts/setup_wizard.sh")
            print("  3. 或使用一键配置：./scripts/quick_setup.sh amap")
            print()
            print("零成本使用:")
            print("  可以直接运行基础分析功能")
            print("  python3 scripts/hotel_analysis.py --hotel '酒店名称'")
        
        print()
        print("======================================")
        
        # 保存检测结果
        result = {
            'score': self.score,
            'mode': mode,
            'checks': self.checks,
            'missing_deps': self.missing_deps,
            'optional_deps': self.optional_deps
        }
        
        os.makedirs('config', exist_ok=True)
        with open('config/env_check_result.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return result

if __name__ == "__main__":
    checker = EnvChecker()
    checker.run_all_checks()
