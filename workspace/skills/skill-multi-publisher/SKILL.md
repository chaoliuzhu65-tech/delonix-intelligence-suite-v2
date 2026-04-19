# Skill Multi-Publisher - 多平台一键发布工具

> **功能**：一键将Skill发布到GitHub、ClawHub等多个 marketplaces

---

## 功能概述

- ✅ 验证SKILL.md格式
- ✅ 自动生成缺失文件
- ✅ 一键发布到GitHub
- ✅ 一键发布到ClawHub
- ✅ 发布后自动创建Release
- ✅ 支持GitHub Actions自动化

---

## 使用方法

### 方式1：本地CLI

```bash
# 克隆工具
git clone https://github.com/dongsheng123132/skill-multi-publisher.git
cd skill-multi-publisher

# 安装依赖
npm install

# 配置Token
export GITHUB_TOKEN="your_github_token"
export CLAWHUB_TOKEN="your_clawhub_token"

# 发布
./publish.sh --skill-path /path/to/your/skill --platform all
```

### 方式2：AI Agent直接调用

```markdown
请帮我把 /path/to/hotel-skill 发布到GitHub和ClawHub
```

---

## 支持平台

| 平台 | 状态 | 命令 |
|------|------|------|
| GitHub | ✅ | `--platform github` |
| ClawHub | ✅ | `--platform clawhub` |
| npm | 🔲 开发中 | `--platform npm` |

---

## 目录结构

```
skill-multi-publisher/
├── SKILL.md
├── publish.sh           # 主发布脚本
├── validate-skill.sh    # SKILL.md验证
├── generate-meta.sh     # 自动生成元数据
└── README.md
```

---

## 配置说明

### 环境变量

```bash
# GitHub Token (需要repo权限)
GITHUB_TOKEN=ghp_xxxx

# ClawHub Token
CLAWHUB_TOKEN=ch_xxxx
```

### GitHub CLI

```bash
# 安装
npm install -g gh

# 登录
gh auth login
```

### ClawHub CLI

```bash
# 安装
npm install -g clawhub

# 登录
clawhub login
```

---

## AI协作格式

### 发布前检查

```bash
# 验证SKILL.md
./validate-skill.sh /path/to/skill

# 检查结果
✅ name字段存在
✅ description字段存在
✅ triggers字段存在
✅ version字段存在
```

### 一键发布

```bash
# 完整发布
./publish.sh \
  --skill-path /path/to/skill \
  --platform all \
  --github-org chaoliuzhu65-tech \
  --message "Initial release"
```

---

## 错误处理

| 错误 | 解决方案 |
|------|----------|
| Token无效 | 重新生成GitHub/ClawHub Token |
| 仓库已存在 | 添加 `--force` 强制更新 |
| 网络超时 | 重试或检查代理设置 |
| 权限不足 | 检查Token是否有repo权限 |

---

## GitHub Actions自动发布

创建 `.github/workflows/publish.yml`：

```yaml
name: Publish Skill
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Publish to GitHub
        run: |
          gh release create ${{ github.event.release.tag_name }}
          --title "${{ github.event.release.name }}"
          --notes "${{ github.event.release.body }}"
      
      - name: Publish to ClawHub
        run: |
          npx -y clawhub publish . \
            --slug ${{ vars.CLAWHUB_SLUG }} \
            --version ${{ github.event.release.tag_name }}
        env:
          CLAWHUB_TOKEN: ${{ secrets.CLAWHUB_TOKEN }}
```

---

*本工具由德胧AI龙虾军团整合*
