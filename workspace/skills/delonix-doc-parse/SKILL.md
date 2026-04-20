---
name: delonix-doc-parse
description: 德胧AI龙虾军团开源文档解析技能。支持PDF/Word/Excel/PPT/TXT等格式转换为Markdown。触发词：文档解析、解析文档、解析PDF、解析Word、解析Excel、读取文档、提取文档内容、doc parse、文档转Markdown、读取PDF。
---

# Delonix Doc Parse（德胧文档解析）

支持多种文档格式转换为Markdown，纯本地解析，**无需上传到第三方**。

## 依赖安装

```bash
pip3 install pdfplumber python-docx python-pptx openpyxl trafilatura -q
```

## 命令

```bash
python3 <skill-path>/scripts/doc_parse.py --file <文件路径或URL> [选项]
```

## 支持格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| PDF | .pdf | 文本内容提取 |
| Word | .docx / .doc | 段落文本 |
| Excel | .xlsx / .xls | 表格数据 |
| PowerPoint | .pptx | 幻灯片文本 |
| 纯文本 | .txt / .md / .csv | 直接读取 |

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--file, -f` | 文档路径或URL | 必需 |
| `--sheet, -s` | Excel工作表索引 (0-based) | 全部 |
| `--format, -o` | 输出格式: json/text | text |
| `--url` | file参数是URL | false |

## 使用示例

```bash
# 解析本地PDF
python3 <skill-path>/scripts/doc_parse.py --file report.pdf

# 解析远程文档（通过URL）
python3 <skill-path>/scripts/doc_parse.py --file "https://example.com/doc.pdf" --url

# 解析Excel指定工作表
python3 <skill-path>/scripts/doc_parse.py --file data.xlsx --sheet 0

# JSON输出（程序调用）
python3 <skill-path>/scripts/doc_parse.py --file doc.docx -o json
```

## 决策树

```
需要文档内容
├─ 本地文件 → 直接解析
├─ 远程URL → --url参数下载解析
├─ 飞书云文档 → 使用feishu skill
└─ 网页内容 → 使用delonix-web-fetch
```

## 技术说明

- **本地解析**，文件不离开服务器
- **无需API Key**
- 技能目录: `/home/gem/workspace/agent/workspace/skills/delonix-doc-parse`
