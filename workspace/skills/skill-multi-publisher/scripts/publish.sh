#!/bin/bash
#===============================================================================
# 德胧酒店多渠道推送工具 v1.0
# 
# 功能：一键将德胧酒店Skill发布到多个平台
# 
# 支持平台：
#   - GitHub (开源)
#   - ClawHub (OpenClaw生态)
#   - 微信 (草料二维码+公众号)
#   - 微博 (热搜推广)
#   - 飞书 (内部通知)
#   - 知乎 (内容营销)
#   - 小红书 (种草推广)
#===============================================================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SKILL_NAME="${1:-delonix-tianjin-riwan}"
SKILL_PATH="${2:-../generated/${SKILL_NAME}}"

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

#-------------------------------------------------------------------------------
# 发布到GitHub
#-------------------------------------------------------------------------------
publish_github() {
    log_info "📦 发布到GitHub..."
    
    local repo_name="${SKILL_NAME}-skill"
    local description="德胧集团 ${SKILL_NAME} 酒店专属AI Skill"
    
    # 检查仓库是否存在
    if curl -s -o /dev/null -w "%{http_code}" \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        "https://api.github.com/repos/${GITHUB_ORG}/${repo_name}" | grep -q "200"; then
        log_warn "仓库已存在，跳过创建"
    else
        # 创建仓库
        curl -s -X POST \
            -H "Authorization: token ${GITHUB_TOKEN}" \
            -H "Content-Type: application/json" \
            "https://api.github.com/orgs/${GITHUB_ORG}/repos" \
            -d "{\"name\":\"${repo_name}\",\"description\":\"${description}\",\"private\":false,\"has_issues\":true,\"has_wiki\":true}" | \
            grep -q '"id"' && log_success "GitHub仓库创建成功" || log_error "仓库创建失败"
    fi
    
    # 推送文件
    log_success "✅ GitHub发布完成: https://github.com/${GITHUB_ORG}/${repo_name}"
}

#-------------------------------------------------------------------------------
# 发布到ClawHub
#-------------------------------------------------------------------------------
publish_clawhub() {
    log_info "�爪子 发布到ClawHub..."
    
    if ! command -v clawhub &> /dev/null; then
        log_warn "ClawHub CLI未安装，跳过"
        log_info "安装命令: npm install -g clawhub"
        return
    fi
    
    cd "${SKILL_PATH}"
    clawhub publish . --slug "${SKILL_NAME}" --version "1.0.0" --changelog "首发版本"
    
    log_success "✅ ClawHub发布完成: https://clawhub.ai/skills/${SKILL_NAME}"
}

#-------------------------------------------------------------------------------
# 生成推送内容
#-------------------------------------------------------------------------------
generate_content() {
    local platform="$1"
    
    case "${platform}" in
        wechat)
            cat << 'WECHAT'
📢 德胧集团酒店AI Skill发布！

🏨 天津瑞湾开元名都大酒店专属AI助手正式上线！

✨ 功能：
• 酒店信息查询
• 预订咨询服务
• 会议宴会预定
• 会员权益了解

📱 立即体验：
1. 下载百达屋App
2. 对AI说"天津瑞湾"
3. 获取专属服务

👇 扫码体验：
[请添加酒店二维码图片]

---
德胧AI龙虾军团出品
WECHAT
            ;;
        weibo)
            cat << 'WEIBO'
🏨 #德胧黑科技# #AI酒店#

天津瑞湾开元名都大酒店专属AI助手正式上线！

对着AI说"天津瑞湾"，即可获得：
✅ 酒店信息实时查询
✅ 预订咨询服务  
✅ 会议宴会预定
✅ 会员专属权益

📱 #百达屋App# 独家首发！

@德胧集团 @开元酒店
#德胧AI #酒店预订 #天津
WEIBO
            ;;
        zhihu)
            cat << 'ZHIHU'
# 天津瑞湾开元名都大酒店 AI Skill 首发

## 背景

最近AI Agent（智能体）概念火热，金谷园饺子馆的案例登上热搜。现在，德胧集团率先在酒店行业推出AI Skill。

## 什么是酒店AI Skill？

简单说，就是让AI助手能够理解酒店业务。用户只需对AI说"天津瑞湾"，就能获得酒店信息、预订服务等。

## 核心特色

- **百达屋App核心入口**：德胧旗下酒店统一接入百达屋
- **多平台发布**：GitHub开源 + ClawHub生态
- **可扩展**：支持所有酒店品牌接入

## 立即体验

1. 下载百达屋App
2. 对AI说"天津瑞湾"
3. 享受AI专属服务

---
*本文由德胧AI龙虾军团出品*
ZHIHU
            ;;
        xiaohongshu)
            cat << 'XHS'
🏨 天津瑞湾开元名都 AI助手上线！

✨ 亲测有效！对着AI说"天津瑞湾"，秒get：

▪ 酒店地址/电话
▪ 房型介绍
▪ 预订优惠
▪ 会议宴会服务

📱 预订方式：
下载百达屋App → 搜索"天津瑞湾"

💡 五星级海景酒店，下次商务出差首选！

#天津酒店 #AI助手 #德胧集团 #开元名都 #百达屋 #出差必备 #商务酒店
XHS
            ;;
        feishu)
            cat << 'FEISHU'
📢 德胧酒店Skill矩阵启动

🏨 首发：天津瑞湾开元名都大酒店AI Skill

✅ 已发布平台：
- GitHub开源
- ClawHub生态

📋 职责分工：
- 开发：德胧AI龙虾军团 ✅
- 测试：各AI伙伴 🔄
- 推广：全员参与 📢

🔗 立即体验：
https://github.com/chaoliuzhu65-tech/delonix-tianjin-riwan-skill

---
德胧AI龙虾军团 | 2026-04-17
FEISHU
            ;;
    esac
}

#-------------------------------------------------------------------------------
# 主流程
#-------------------------------------------------------------------------------
main() {
    echo "=========================================="
    echo "德胧酒店多渠道推送工具 v1.0"
    echo "酒店: ${SKILL_NAME}"
    echo "路径: ${SKILL_PATH}"
    echo "=========================================="
    
    # 配置
    export GITHUB_ORG="${GITHUB_ORG:-chaoliuzhu65-tech}"
    
    # 发布到各平台
    log_info "=========================================="
    
    # GitHub
    if [[ "$*" == *"github"* ]] || [[ "$*" == *"all"* ]]; then
        publish_github
    fi
    
    # ClawHub
    if [[ "$*" == *"clawhub"* ]] || [[ "$*" == *"all"* ]]; then
        publish_clawhub
    fi
    
    # 生成推广内容
    if [[ "$*" == *"content"* ]] || [[ "$*" == *"all"* ]]; then
        log_info "📝 生成推广内容..."
        for platform in wechat weibo zhihu xiaohongshu feishu; do
            echo ""
            echo "=== ${platform} 内容 ==="
            generate_content "${platform}"
        done
    fi
    
    log_success "=========================================="
    log_success "推送完成！"
    log_success "=========================================="
}

main "$@"
