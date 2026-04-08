# 头条文章抓取 Skill

> 通过 `miaoda-studio-cli web-crawl` 绕过头条反爬，提取任意头条文章的结构化内容。

## 验证有效 ✅
- 日期：2026-04-08
- 工具：miaoda-studio-cli web-crawl
- 状态：可绕过头条反爬，返回完整可读文本

## 使用方法

```bash
miaoda-studio-cli web-crawl --url "https://m.toutiao.com/is/ToE5a3QmvQM/" -o text
```

## 适用场景
- 抓取头条文章（今日头条、抖音头条号）
- 提取文章标题、作者、正文、发布时间
- 支持各类头条分享链接格式

## 注意事项
- 头条文章链接通常为 `https://m.toutiao.com/is/{id}/`
- 移动版和 PC 版链接均可使用
- 直接用 web_fetch 可能失败，必须用 miaoda-studio-cli
