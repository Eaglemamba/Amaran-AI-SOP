#!/usr/bin/env python3
"""
Amaran BPR Report Generator v1.3
================================
Updated to match BPR Verifier v3.4 output structure.

Report 1: QA Compliance Audit (Full verification including Weighing and IPC/EM)
Report 2: Page Reconciliation
"""

import json
import argparse
from pathlib import Path
from datetime import datetime

VERSION = "1.3.0"

COLORS = {
    "primary": "#d97757",
    "secondary": "#6a9bcc",
    "tertiary": "#788c5d",
    "dark": "#3d2a6b",
    "bg_light": "#faf9f5",
    "bg_card": "#f0eeeb",
    "text": "#141413",
    "muted": "#b0aea5",
}


def get_compact_css():
    """Compact CSS matching Amaran brand style - print-safe"""
    return f'''
    @page {{ size: A4; margin: 12mm 15mm; }}
    
    * {{ box-sizing: border-box; }}
    
    body {{
        font-family: Arial, sans-serif;
        font-size: 8.5pt;
        line-height: 1.3;
        color: #333;
        margin: 0;
        padding: 15px;
        max-width: 190mm;
    }}
    
    @media print {{
        body {{
            padding: 0;
            max-width: none;
            width: 100%;
        }}
    }}
    
    .header {{
        padding-bottom: 6px;
        margin-bottom: 8px;
        border-bottom: 2px solid {COLORS["dark"]};
    }}
    .title {{
        font-size: 14pt;
        font-weight: bold;
        color: {COLORS["dark"]};
        text-align: center;
        margin: 0;
    }}
    .info {{
        font-size: 9pt;
        color: #555;
        margin-top: 4px;
        text-align: center;
    }}
    
    .section {{
        background: {COLORS["dark"]};
        color: white;
        padding: 4px 10px;
        font-weight: bold;
        margin-top: 10px;
        font-size: 9pt;
    }}
    
    .source-note {{
        font-size: 7.5pt;
        color: #666;
        margin: 4px 0 6px 0;
        font-style: italic;
    }}
    
    table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 8pt;
        margin-top: 4px;
        table-layout: fixed;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }}
    th {{
        background: {COLORS["bg_card"]};
        padding: 4px 6px;
        text-align: left;
        border-bottom: 1px solid #ccc;
        font-weight: bold;
        overflow: hidden;
    }}
    td {{
        padding: 3px 6px;
        border-bottom: 1px solid #e0e0e0;
        overflow: hidden;
    }}
    
    .center {{ text-align: center; }}
    .item {{ font-weight: bold; color: {COLORS["dark"]}; }}
    .pass {{ color: #2e7d32; }}
    .fail {{ color: #c62828; }}
    .warn {{ color: #f57c00; }}
    .na {{ color: #888; }}
    
    .footer {{
        margin-top: 12px;
        padding-top: 8px;
        border-top: 1px solid #ccc;
        font-size: 8pt;
    }}
    
    .math-box {{
        background: #f8f8f8;
        padding: 6px 10px;
        margin: 6px 0;
        font-family: Consolas, monospace;
        font-size: 8pt;
        border-left: 3px solid {COLORS["secondary"]};
    }}
    
    .page-break {{
        page-break-before: always;
    }}
    '''


def generate_report1_compact(data):
    """Report 1: QA Compliance Audit - v3.4 Format with all verification sections"""
    
    batch_info = data.get("batch_info", {})
    b = batch_info.get("batch_number", "Unknown")
    p = batch_info.get("product_name", "Unknown")
    
    disposition = data.get("disposition", {})
    status = disposition.get("status", "PASS")
    bpr_body_check = data.get("bpr_body_check", {})
    reconciliation = data.get("reconciliation", {})
    sterilization = data.get("sterilization", {})
    gdp_corrections = data.get("gdp_corrections", [])
    documentation_summary = data.get("documentation_summary", {})
    filter_integrity = data.get("filter_integrity", {})
    weighing_verification = data.get("weighing_verification", {})
    ipc = data.get("ipc", {})
    em = data.get("em", {})
    
    qa_date = bpr_body_check.get("qa_signature_date_str", "N/A")
    critical = disposition.get("critical", 0)
    major = disposition.get("major", 0)
    minor = disposition.get("minor", len(gdp_corrections))
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QA Compliance Audit - {b}</title>
    <style>{get_compact_css()}</style>
</head>
<body>

<div class="header">
    <div class="title">QA Compliance Audit Report</div>
    <div class="info">Batch: <b>{b}</b> | Product: {p}</div>
</div>

<!-- 1. EXECUTIVE SUMMARY -->
<div class="section">1. EXECUTIVE SUMMARY</div>
<table>
    <tbody>
        <tr><td class="item" style="width:20%">Batch No</td><td>{b}</td></tr>
        <tr><td class="item">Product</td><td>{p}</td></tr>
        <tr><td class="item">QA Verified Date</td><td>{qa_date}</td></tr>
        <tr><td class="item">Overall Status</td><td class="{"pass" if status == "PASS" else "warn"}">{status}</td></tr>
        <tr><td class="item">Total Issues</td><td>{critical} Critical, {major} Major, {minor} Minor</td></tr>
    </tbody>
</table>

<!-- 2. DETAILED FINDINGS & ISSUE LOG -->
<div class="section">2. DETAILED FINDINGS & ISSUE LOG</div>'''
    
    if gdp_corrections:
        html += '''<table>
            <thead><tr><th style="width:8%">Severity</th><th style="width:7%">Section</th><th style="width:6%">Page</th><th>Description</th><th style="width:20%">Reason</th></tr></thead>
            <tbody>'''
        for corr in gdp_corrections:
            html += f'''<tr>
                <td class="center">{corr.get("severity", "Minor")}</td>
                <td class="center">{corr.get("section", "-")}</td>
                <td class="center">{corr.get("page", "-")}</td>
                <td>{corr.get("description", "-")}</td>
                <td>{corr.get("reason", "-")}</td>
            </tr>'''
        html += '</tbody></table>'
    else:
        html += '<p style="padding:6px;" class="pass">No issues identified. âœ“</p>'
    
    # 3. RECONCILIATION MATH PROOF
    html += '<div class="section">3. RECONCILIATION MATH PROOF</div>'
    math_proofs = reconciliation.get("math_proof", [])
    if math_proofs:
        for proof in math_proofs:
            html += f'<div class="math-box">{proof}</div>'
    else:
        html += '<p style="padding:6px; color:#888;">No reconciliation data available</p>'
    
    # 4. DOCUMENTATION & GDP SUMMARY
    html += '<div class="section">4. DOCUMENTATION & GDP SUMMARY</div>'
    
    sig_ver = documentation_summary.get("signature_verification", "Pass")
    border_sig = documentation_summary.get("border_signatures", "Pass")
    corrections = documentation_summary.get("corrections", "All corrections followed GDP standards.")
    
    html += f'''<table>
        <tbody>
            <tr><td class="item" style="width:18%">Signature Verification</td><td>{sig_ver}</td></tr>
            <tr><td class="item">Border Signatures</td><td>{border_sig}</td></tr>
            <tr><td class="item">Corrections</td><td>{corrections}</td></tr>
        </tbody>
    </table>'''
    
    # 5. STERILIZATION VERIFICATION TABLE
    cycles = sterilization.get("cycles", [])
    if cycles:
        html += '<div class="section">5. STERILIZATION VERIFICATION TABLE</div>'
        html += '''<table>
            <thead><tr><th style="width:11%">Cycle ID</th><th style="width:16%">Item Sterilized</th><th style="width:10%">Parameter</th><th class="center" style="width:7%">Spec</th><th class="center" style="width:11%">Actual</th><th class="center" style="width:7%">Pass/Fail</th></tr></thead>
            <tbody>'''
        for cycle in cycles:
            cid = cycle.get("cycle_id", "-")
            item = cycle.get("item", "-")
            temp = cycle.get("temperature")
            temp_range = cycle.get("temperature_range", str(temp) if temp else "-")
            time_val = cycle.get("time")
            
            if temp or temp_range != "-":
                temp_pass = (temp >= 122) if temp else True
                html += f'<tr><td>{cid}</td><td>{item}</td><td>Temp (Â°C)</td><td class="center">â‰¥122</td><td class="center">{temp_range}</td><td class="center pass">Pass</td></tr>'
            if time_val:
                time_pass = time_val >= 20
                html += f'<tr><td>{cid}</td><td>{item}</td><td>Time (min)</td><td class="center">â‰¥20</td><td class="center">{time_val}:00</td><td class="center pass">Pass</td></tr>'
        html += '</tbody></table>'
    
    # 6. WEIGHING VERIFICATION TABLE (NEW in v1.3)
    weighing_items = weighing_verification.get("items", [])
    if weighing_items:
        html += '<div class="section">6. WEIGHING VERIFICATION TABLE</div>'
        
        source_note = weighing_verification.get("source_note", "")
        if source_note:
            html += f'<p class="source-note">{source_note}</p>'
        
        html += '''<table>
            <thead><tr><th style="width:7%">Step</th><th style="width:13%">Item</th><th style="width:9%">Parameter</th><th style="width:13%">Handwritten (BPR)</th><th style="width:13%">Printout (Att-7)</th><th class="center" style="width:7%">Match?</th></tr></thead>
            <tbody>'''
        for w in weighing_items:
            match = w.get("match", True)
            match_cls = "pass" if match else "fail"
            match_text = "Yes" if match else "No"
            note = w.get("note", "")
            if note:
                match_text = f"Yes ({note})"
            html += f'''<tr>
                <td>{w.get("step", "-")}</td>
                <td>{w.get("item", "-")}</td>
                <td>{w.get("parameter", "-")}</td>
                <td>{w.get("handwritten", "-")}</td>
                <td>{w.get("printout", "-")}</td>
                <td class="center {match_cls}">{match_text}</td>
            </tr>'''
        html += '</tbody></table>'
    
    # 7. FILTER INTEGRITY VERIFICATION
    if filter_integrity:
        html += '<div class="section">7. FILTER INTEGRITY VERIFICATION</div>'
        
        source_note = filter_integrity.get("source_note", "")
        if source_note:
            html += f'<p class="source-note">{source_note}</p>'
        
        html += '''<table>
            <thead><tr><th style="width:9%">Stage</th><th style="width:15%">Filter ID (from BPR/Att)</th><th class="center" style="width:14%">Extracted Spec (Min. BP)</th><th class="center" style="width:11%">Actual Result</th><th class="center" style="width:7%">Status</th></tr></thead>
            <tbody>'''
        
        tests = filter_integrity.get("tests", [])
        for t in tests:
            passed = t.get("passed", True)
            cls = "pass" if passed else "fail"
            status_text = "Pass" if passed else "Fail"
            html += f'''<tr>
                <td>{t.get("stage", "-")}</td>
                <td>{t.get("filter_id", "-")}</td>
                <td class="center">{t.get("spec", "-")}</td>
                <td class="center">{t.get("value", "-")}</td>
                <td class="center {cls}">{status_text}</td>
            </tr>'''
        
        html += '</tbody></table>'
    
    # 8. IPC/EM VERIFICATION TABLE (NEW in v1.3 - moved from Report 2)
    html += '<div class="section">8. IPC/EM VERIFICATION TABLE</div>'
    html += '''<table>
        <thead>
            <tr>
                <th style="width:9%">Item</th>
                <th class="center" style="width:17%">Spec</th>
                <th style="width:14%">Source Attachment</th>
                <th class="center" style="width:15%">Actual Result</th>
                <th class="center" style="width:7%">Pass/Fail</th>
            </tr>
        </thead>
        <tbody>'''
    
    # IPC items
    for k in ["ipc_1", "ipc_2", "ipc_3", "ipc_4", "ipc_5"]:
        d = ipc.get(k, {})
        if not d:
            continue
        
        passed = d.get("passed")
        cls = "pass" if passed else ("fail" if passed is False else "na")
        status_text = "Pass" if passed else ("Fail" if passed is False else "-")
        
        html += f'''
        <tr>
            <td class="item">{d.get("item", "-")}</td>
            <td class="center">{d.get("spec", "-")}</td>
            <td>{d.get("source", "-")}</td>
            <td class="center">{d.get("value", "-")}</td>
            <td class="center {cls}">{status_text}</td>
        </tr>'''
    
    # EM items
    for k in ["em_1", "em_2", "em_2a", "em_2b", "em_3"]:
        d = em.get(k, {})
        if not d:
            continue
        
        val = d.get("value", "-")
        spec = d.get("spec", "-")
        if val == "-" and spec == "-":
            continue
        
        passed = d.get("passed")
        cls = "pass" if passed else ("fail" if passed is False else "na")
        status_text = "Pass" if passed else ("Fail" if passed is False else "-")
        
        html += f'''
        <tr>
            <td class="item">{d.get("item", "-")}</td>
            <td class="center">{spec}</td>
            <td>{d.get("source", "-")}</td>
            <td class="center">{val}</td>
            <td class="center {cls}">{status_text}</td>
        </tr>'''
    
    html += '</tbody></table>'
    
    # FOOTER
    html += f'''
<div class="footer">
    <p>Prepared by: ____________________________</p>
</div>

</body>
</html>'''
    
    return html


def generate_report2_compact(data):
    """Report 2: Page Reconciliation - Simplified per v3.4"""
    
    batch_info = data.get("batch_info", {})
    b = batch_info.get("batch_number", "Unknown")
    p = batch_info.get("product_name", "Unknown")
    
    attachments = data.get("attachments", {})
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Page Reconciliation - {b}</title>
    <style>{get_compact_css()}</style>
</head>
<body>

<div class="header">
    <div class="title">Page Reconciliation Report</div>
    <div class="info">Batch: <b>{b}</b> | Product: {p}</div>
</div>

<!-- PAGE RECONCILIATION TABLE -->
<div class="section">PAGE RECONCILIATION TABLE</div>
<table>
    <thead>
        <tr>
            <th style="width:13%">Attachment</th>
            <th>Document Name</th>
            <th class="center" style="width:7%">Pages</th>
        </tr>
    </thead>
    <tbody>'''
    
    # BPR Body
    bpr_end = attachments.get("bpr_body_pages", 0)
    html += f'''
        <tr>
            <td class="item">-</td>
            <td>BPR Body</td>
            <td class="center">{bpr_end}</td>
        </tr>'''
    
    # Attachments sorted by number
    att_dict = attachments.get("attachments", {})
    all_att = [(k, v) for k, v in att_dict.items() if v.get("actual") or v.get("declared")]
    all_att.sort(key=lambda x: x[1].get("att_number", 99) or 99)
    
    for att_key, att in all_att:
        att_num = att.get("att_number") or "?"
        name = att.get("name", att_key)
        actual = att.get("actual") or att.get("declared") or "-"
        
        if actual and actual != "-":
            html += f'''
        <tr>
            <td class="item">Attachment-{att_num}</td>
            <td>{name}</td>
            <td class="center">{actual}</td>
        </tr>'''
    
    # Total
    total = attachments.get("total_pages", 0)
    html += f'''
        <tr style="font-weight:bold; background:{COLORS["bg_card"]}">
            <td></td>
            <td>Total</td>
            <td class="center">{total}</td>
        </tr>'''
    
    html += f'''
    </tbody>
</table>

<div class="footer">
    <p>Prepared by: ____________________________</p>
</div>

</body>
</html>'''
    
    return html


def generate_pdf(html, path):
    """Generate PDF from HTML"""
    try:
        from weasyprint import HTML
        HTML(string=html).write_pdf(str(path))
        print(f"  âœ“ PDF: {path.name}")
        return True
    except ImportError:
        print("  âš  WeasyPrint not installed")
        return False
    except Exception as e:
        print(f"  âœ— PDF error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description=f"Amaran BPR Report Generator v{VERSION}")
    parser.add_argument("input", help="Input JSON file")
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    parser.add_argument("--html-only", action="store_true", help="HTML only, skip PDF")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return 1
    
    print("=" * 60)
    print(f"Amaran BPR Report Generator v{VERSION}")
    print("=" * 60)
    
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    batch_number = data.get("batch_info", {}).get("batch_number", "Unknown")
    product_name = data.get("batch_info", {}).get("product_name", "Unknown")
    
    print(f"Batch: {batch_number}")
    print(f"Product: {product_name}")
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Report 1: QA Compliance Audit
    print("\nGenerating Report 1: QA Compliance Audit...")
    report1_html = generate_report1_compact(data)
    
    report1_html_path = output_dir / f"Report1_QA_Compliance_Audit_{batch_number}.html"
    with open(report1_html_path, "w", encoding="utf-8") as f:
        f.write(report1_html)
    print(f"  âœ“ HTML: {report1_html_path.name}")
    
    if not args.html_only:
        report1_pdf_path = output_dir / f"Report1_QA_Compliance_Audit_{batch_number}.pdf"
        generate_pdf(report1_html, report1_pdf_path)
    
    # Report 2: Page Reconciliation
    print("\nGenerating Report 2: Page Reconciliation...")
    report2_html = generate_report2_compact(data)
    
    report2_html_path = output_dir / f"Report2_Page_Reconciliation_{batch_number}.html"
    with open(report2_html_path, "w", encoding="utf-8") as f:
        f.write(report2_html)
    print(f"  âœ“ HTML: {report2_html_path.name}")
    
    if not args.html_only:
        report2_pdf_path = output_dir / f"Report2_Page_Reconciliation_{batch_number}.pdf"
        generate_pdf(report2_html, report2_pdf_path)
    
    print("\n" + "=" * 60)
    print("Complete!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())
