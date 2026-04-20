#!/usr/bin/env python3
"""
德胧AI龙虾军团 - 文档解析工具
支持PDF/Word/Excel/PPT/TXT等格式转换为Markdown

用法:
  python3 doc_parse.py --file document.pdf [选项]
  python3 doc_parse.py --file document.xlsx --sheet 0
"""

import sys
import json
import argparse
import os


def parse_pdf(file_path: str) -> str:
    """解析PDF文件"""
    import pdfplumber
    text_parts = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
    return "\n\n".join(text_parts)


def parse_docx(file_path: str) -> str:
    """解析Word文档"""
    from docx import Document
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def parse_pptx(file_path: str) -> str:
    """解析PowerPoint"""
    from pptx import Presentation
    prs = Presentation(file_path)
    slides_text = []
    for i, slide in enumerate(prs.slides, 1):
        slide_text = [shape.text for shape in slide.shapes if hasattr(shape, "text")]
        if any(s.strip() for s in slide_text):
            slides_text.append(f"## 幻灯片 {i}\n\n" + "\n".join(s.strip() for s in slide_text if s.strip()))
    return "\n\n".join(slides_text)


def parse_xlsx(file_path: str, sheet_index: int = 0) -> str:
    """解析Excel文件"""
    import openpyxl
    wb = openpyxl.load_workbook(file_path, data_only=True)
    sheets_text = []
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            continue
        # 转换为Markdown表格
        header = rows[0] if rows else []
        if sheet_index is not None:
            sheet_data = rows
        else:
            sheet_data = rows
        md_rows = []
        for row in sheet_data[:100]:  # 限制100行
            md_rows.append("| " + " | ".join(str(c) if c is not None else "" for c in row) + " |")
        header_md = "| " + " | ".join(str(h) if h else "" for h in header) + " |" if header else ""
        sep = "| " + " | ".join("---" for _ in (header or [1])) + " |"
        table = "\n".join([header_md, sep] + md_rows)
        sheets_text.append(f"### 工作表: {sheet_name}\n\n{table}\n")
    return "\n\n".join(sheets_text)


def parse_txt(file_path: str) -> str:
    """解析纯文本"""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_document(file_path: str, sheet: int = None, output_format: str = "text") -> dict:
    """根据文件类型自动解析"""
    ext = os.path.splitext(file_path)[1].lower()

    parsers = {
        ".pdf": parse_pdf,
        ".docx": parse_docx,
        ".doc": parse_docx,
        ".pptx": parse_pptx,
        ".xlsx": parse_xlsx,
        ".xls": parse_xlsx,
        ".txt": parse_txt,
        ".md": parse_txt,
        ".csv": parse_txt,
    }

    if ext not in parsers:
        return {"error": f"不支持的格式: {ext}，支持: {list(parsers.keys())}"}

    try:
        if ext == ".xlsx" and sheet is not None:
            content = parse_xlsx(file_path, sheet)
        else:
            parser_func = parsers[ext]
            if ext == ".xlsx":
                content = parser_func(file_path)
            else:
                content = parser_func(file_path)
    except Exception as e:
        return {"error": f"解析失败: {str(e)}"}

    if output_format == "json":
        return {"file": file_path, "format": ext, "content": content[:8000] if content else ""}

    output = f"# 文档解析结果\n\n**文件**: {file_path}\n**格式**: {ext}\n\n## 内容\n\n{content}\n"
    return output


def main():
    parser = argparse.ArgumentParser(description="德胧AI龙虾军团文档解析工具")
    parser.add_argument("--file", "-f", required=True, help="文档路径或URL")
    parser.add_argument("--sheet", "-s", type=int, default=None, help="Excel工作表索引 (0-based)")
    parser.add_argument("--format", "-o", choices=["json", "text"], default="text", help="输出格式")
    parser.add_argument("--url", action="store_true", help="file参数是URL而非本地路径")

    args = parser.parse_args()

    # 如果是URL，先下载
    if args.url or args.file.startswith("http"):
        import urllib.request
        import tempfile
        try:
            req = urllib.request.Request(args.file, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            suffix = os.path.splitext(args.file.split("?")[0])[1] or ".pdf"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                with urllib.request.urlopen(req, timeout=30) as response:
                    tmp.write(response.read())
                tmp_path = tmp.name
            result = parse_document(tmp_path, args.sheet, args.format)
            os.unlink(tmp_path)
        except Exception as e:
            print(f"下载失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if not os.path.exists(args.file):
            print(f"文件不存在: {args.file}", file=sys.stderr)
            sys.exit(1)
        result = parse_document(args.file, args.sheet, args.format)

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if isinstance(result, dict) and "error" in result:
            print(f"错误: {result['error']}", file=sys.stderr)
            sys.exit(1)
        print(result)


if __name__ == "__main__":
    main()
