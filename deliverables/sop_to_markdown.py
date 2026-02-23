"""
SOP to Markdown Converter
=========================
將 Word (.docx) 和 PDF 檔案轉為 AI-Ready Markdown + YAML Front Matter

使用方式：
  python sop_to_markdown.py input_folder/ output_folder/

安裝依賴：
  pip install mammoth markitdown pymupdf pyyaml

備註：
  - mammoth: Word -> HTML -> Markdown (表格支援好)
  - markitdown: 微軟出品，Word/PDF/PPT 都能轉 (簡單快速)
  - pymupdf: PDF 文字提取 (輕量，不需 OCR 的場景)
  - 如需高品質 PDF 轉換(含表格、圖片)，另裝 marker-pdf
"""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import datetime


# ============================================================
# 方法 1: mammoth (Word -> Markdown, 表格支援最好)
# ============================================================
def docx_to_md_mammoth(filepath: str) -> str:
    """用 mammoth 將 .docx 轉為 Markdown"""
    import mammoth

    with open(filepath, "rb") as f:
        result = mammoth.convert_to_markdown(f)
        return result.value


# ============================================================
# 方法 2: markitdown (微軟出品, 支援 Word/PDF/PPT/Excel)
# ============================================================
def file_to_md_markitdown(filepath: str) -> str:
    """用微軟 markitdown 轉換（最簡單的萬用方案）"""
    from markitdown import MarkItDown

    md = MarkItDown()
    result = md.convert(filepath)
    return result.text_content


# ============================================================
# 方法 3: PyMuPDF (PDF -> 文字, 輕量快速)
# ============================================================
def pdf_to_md_pymupdf(filepath: str, skip_first_page: bool = True) -> str:
    """用 PyMuPDF 提取 PDF 文字，加上基本 Markdown 格式"""
    import fitz  # PyMuPDF

    doc = fitz.open(filepath)
    pages = []

    for i, page in enumerate(doc):
        # Skip scanned cover/signature page (usually page 1)
        if skip_first_page and i == 0:
            continue
        text = page.get_text("text")
        # 簡單的標題偵測：全大寫或短行可能是標題
        lines = text.split("\n")
        formatted_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                formatted_lines.append("")
                continue
            # 偵測可能的章節標題 (例如 "1. PURPOSE", "2. SCOPE")
            if re.match(r'^\d+\.?\s+[A-Z\s]{4,}$', stripped):
                formatted_lines.append(f"## {stripped}")
            elif re.match(r'^\d+\.\d+\.?\s+', stripped):
                formatted_lines.append(f"### {stripped}")
            else:
                formatted_lines.append(stripped)
        pages.append("\n".join(formatted_lines))

    doc.close()
    return "\n\n---\n\n".join(pages)


# ============================================================
# Page 2 Header Parsing (Amaran SOP format)
# ============================================================
# Amaran SOP page 2 header pattern:
#   Page X of Y
#   中文標題
#   English Title
#   QP-0008.V08  (or similar doc code)
#   Effective Date: DD/MM/YY
#   CONFIDENTIAL
#   DO NOT COPY

# Lines to skip when looking for the English title
_HEADER_SKIP = re.compile(
    r'^(Page\s+\d+|CONFIDENTIAL|DO NOT COPY|Effective\s+Date)',
    re.IGNORECASE,
)

# SOP/doc number patterns:
#   SOPs: QP-0008.V08, GP-0012.V03, etc.
#   WIs:  WI-QA-001, WI-PRD-012.V02, etc.
_DOC_NUMBER = re.compile(
    r'^([A-Z]{2,4}-(?:[A-Z]{2,4}-)?\d{3,5}(?:\.V?\d+)?)$'
)

# Mostly-CJK line (Chinese title) — skip when looking for English title
_CJK_LINE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')


def parse_page2_header(content: str) -> dict:
    """Extract title, sop_number, effective_date from page 2 header lines."""
    result = {"title": "", "sop_number": "", "effective_date": ""}
    # Only inspect first 15 lines (header block)
    lines = [l.strip() for l in content.split("\n")[:15] if l.strip()]

    for line in lines:
        # SOP / document number
        m = _DOC_NUMBER.match(line)
        if m and not result["sop_number"]:
            result["sop_number"] = m.group(1)
            continue

        # Effective date
        m = re.match(r'Effective\s+Date\s*[:：]\s*(.+)', line, re.IGNORECASE)
        if m and not result["effective_date"]:
            result["effective_date"] = m.group(1).strip()
            continue

        # Skip non-title lines
        if _HEADER_SKIP.match(line):
            continue
        if _CJK_LINE.search(line):
            continue

        # English title: first remaining line that is long enough
        if not result["title"] and len(line) > 3:
            result["title"] = line

    return result


# ============================================================
# YAML Front Matter 生成
# ============================================================
def generate_front_matter(filepath: str, content: str) -> str:
    """從檔名和內容自動生成 YAML Front Matter"""
    filename = Path(filepath).stem
    ext = Path(filepath).suffix.lower()

    # Parse structured header from page 2 (works best with pymupdf + skip_first_page)
    header = parse_page2_header(content)

    # SOP number: prefer header parse, then filename, then content regex
    sop_number = header.get("sop_number", "")
    if not sop_number:
        sop_match = re.search(r'([A-Z]{2,4}-(?:[A-Z]{2,4}-)?\d{3,5}(?:\.V?\d+)?)', filename)
        if not sop_match:
            sop_match = re.search(r'([A-Z]{2,4}-(?:[A-Z]{2,4}-)?\d{3,5}(?:\.V?\d+)?)', content[:500])
        if sop_match:
            sop_number = sop_match.group(1)

    # Title: prefer header parse, then filename fallback
    title = header.get("title", "") or filename

    # Effective date (optional, informational)
    effective_date = header.get("effective_date", "")

    metadata = {
        "title": title,
        "sop_number": sop_number or "TBD",
        "doc_type": "WI" if sop_number.startswith("WI-") else "SOP",
        "source_format": ext.replace(".", ""),
        "source_file": Path(filepath).name,
        "converted_date": datetime.now().strftime("%Y-%m-%d"),
        "department": "TBD",           # 手動填寫
        "equipment": [],               # 手動填寫
        "classification": "Internal",
        "tags": [],                     # 手動填寫
    }
    if effective_date:
        metadata["effective_date"] = effective_date

    yaml_str = yaml.dump(
        metadata,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )

    return f"---\n{yaml_str}---\n\n"


# ============================================================
# 脫敏處理 (可選)
# ============================================================
# 定義脫敏規則 - 根據你的實際需求調整
REDACT_RULES = [
    # (pattern, replacement, description)
    (r'(?i)(client|customer|sponsor)\s*[:：]\s*\S+', r'\1: [REDACTED]', "客戶名稱"),
    (r'(?i)(product|drug\s*product)\s*[:：]\s*\S+', r'\1: [REDACTED]', "產品名稱"),
    (r'(?i)batch\s*#?\s*[:：]?\s*[A-Z0-9-]{4,}', 'Batch: [REDACTED]', "批號"),
    (r'(?i)(lot\s*#?|lot\s*number)\s*[:：]?\s*[A-Z0-9-]{4,}', r'\1: [REDACTED]', "批號"),
]

# 白名單：這些不會被脫敏
KEEP_PATTERNS = [
    r'21\s*CFR\s*Part\s*\d+',
    r'PIC/S',
    r'ICH\s*Q\d+',
    r'EU\s*GMP',
    r'USP\s*<\d+>',
]


def desensitize(content: str) -> str:
    """對內容進行脫敏處理"""
    result = content
    for pattern, replacement, desc in REDACT_RULES:
        result = re.sub(pattern, replacement, result)
    return result


# ============================================================
# 品質清理
# ============================================================
def clean_markdown(content: str) -> str:
    """清理轉換後的 Markdown，改善品質"""
    # 移除連續多個空行 (保留最多2個)
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # 移除行尾多餘空格
    content = re.sub(r'[ \t]+$', '', content, flags=re.MULTILINE)

    # 確保標題前有空行
    content = re.sub(r'([^\n])\n(#{1,4}\s)', r'\1\n\n\2', content)

    # 確保標題後有空行
    content = re.sub(r'(#{1,4}\s[^\n]+)\n([^#\n])', r'\1\n\n\2', content)

    return content.strip() + "\n"


# ============================================================
# 主轉換函數
# ============================================================
def convert_file(
    filepath: str,
    method: str = "auto",
    add_front_matter: bool = True,
    do_desensitize: bool = False,
) -> str:
    """
    轉換單一檔案為 Markdown

    Args:
        filepath: 輸入檔案路徑
        method: 轉換方法 ("mammoth", "markitdown", "pymupdf", "auto")
        add_front_matter: 是否加上 YAML Front Matter
        do_desensitize: 是否執行脫敏

    Returns:
        轉換後的 Markdown 字串
    """
    ext = Path(filepath).suffix.lower()

    # 自動選擇方法
    if method == "auto":
        if ext == ".docx":
            method = "mammoth"
        elif ext == ".pdf":
            method = "markitdown"  # markitdown 也能處理 PDF
        else:
            method = "markitdown"  # 萬用方案

    # 執行轉換
    print(f"  Converting: {Path(filepath).name} (method: {method})")

    try:
        if method == "mammoth":
            content = docx_to_md_mammoth(filepath)
        elif method == "markitdown":
            content = file_to_md_markitdown(filepath)
        elif method == "pymupdf":
            content = pdf_to_md_pymupdf(filepath)
        else:
            raise ValueError(f"Unknown method: {method}")
    except ImportError as e:
        print(f"  ERROR: Missing package - {e}")
        print(f"  Install with: pip install {method}")
        return ""
    except Exception as e:
        print(f"  ERROR converting {filepath}: {e}")
        return ""

    # 清理
    content = clean_markdown(content)

    # 脫敏
    if do_desensitize:
        content = desensitize(content)

    # 加 Front Matter
    if add_front_matter:
        front_matter = generate_front_matter(filepath, content)
        content = front_matter + content

    return content


# ============================================================
# 批次轉換
# ============================================================
def batch_convert(
    input_dir: str,
    output_dir: str,
    method: str = "auto",
    do_desensitize: bool = False,
):
    """批次轉換整個資料夾"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 支援的格式
    supported = {".docx", ".pdf", ".doc", ".pptx", ".xlsx"}
    files = [
        f for f in input_path.iterdir()
        if f.suffix.lower() in supported and not f.name.startswith("~")
    ]

    if not files:
        print(f"No supported files found in {input_dir}")
        print(f"Supported formats: {supported}")
        return

    print(f"\n{'='*50}")
    print(f"SOP to Markdown Converter")
    print(f"{'='*50}")
    print(f"Input:  {input_dir} ({len(files)} files)")
    print(f"Output: {output_dir}")
    print(f"Method: {method}")
    print(f"Desensitize: {do_desensitize}")
    print(f"{'='*50}\n")

    success = 0
    failed = 0
    total_size = 0

    for f in sorted(files):
        md_content = convert_file(
            str(f),
            method=method,
            add_front_matter=True,
            do_desensitize=do_desensitize,
        )

        if md_content:
            # 輸出檔名: 保持原名但改副檔名為 .md
            out_file = output_path / f"{f.stem}.md"
            out_file.write_text(md_content, encoding="utf-8")

            size_kb = len(md_content.encode("utf-8")) / 1024
            total_size += size_kb
            print(f"  -> Saved: {out_file.name} ({size_kb:.1f} KB)")
            success += 1
        else:
            failed += 1

    print(f"\n{'='*50}")
    print(f"Done! {success} converted, {failed} failed")
    print(f"Total output: {total_size:.1f} KB ({total_size/1024:.2f} MB)")
    print(f"{'='*50}")


# ============================================================
# CLI Entry Point
# ============================================================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("""
Usage:
  python sop_to_markdown.py <input_folder> <output_folder> [options]

Options:
  --method mammoth|markitdown|pymupdf|auto  (default: auto)
  --desensitize                              Enable desensitization

Examples:
  # 基本轉換
  python sop_to_markdown.py ./sops/ ./markdown_sops/

  # 帶脫敏
  python sop_to_markdown.py ./sops/ ./markdown_sops/ --desensitize

  # 指定方法
  python sop_to_markdown.py ./sops/ ./markdown_sops/ --method markitdown
        """)
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    method = "auto"
    do_desensitize = False

    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == "--method" and i + 1 < len(sys.argv):
            method = sys.argv[i + 1]
        if arg == "--desensitize":
            do_desensitize = True

    batch_convert(input_dir, output_dir, method, do_desensitize)
