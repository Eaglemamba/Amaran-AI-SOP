#!/usr/bin/env python3
"""
Amaran PDF Redaction Tool v1.0
==============================
Removes confidential info (product name, sponsor, employee names) from
scanned or digital PDFs before uploading to Gemini for OCR extraction.

Workflow:
  1. Select PDF file
  2. Choose document type (BPR, Campaign Report, etc.)
  3. Tool converts pages to images, applies black-fill redactions
  4. Output: folder of redacted PNGs ready for Gemini upload

Dependencies:
  pip install pdf2image Pillow
  + Poppler binaries (see README)
"""

import json
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from datetime import datetime

try:
    from pdf2image import convert_from_path
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Missing dependencies. Run:")
    print("  pip install pdf2image Pillow")
    sys.exit(1)

VERSION = "1.0.0"
DEFAULT_DPI = 300
CONFIG_FILE = "redaction_config.json"


def load_config():
    """Load redaction zone config from JSON file."""
    config_path = Path(__file__).parent / CONFIG_FILE
    if not config_path.exists():
        # Also check current working directory
        config_path = Path(CONFIG_FILE)
    if not config_path.exists():
        messagebox.showerror("Config Missing",
            f"Cannot find {CONFIG_FILE}\n"
            f"Place it in the same folder as this script.")
        return None

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Remove metadata keys
    return {k: v for k, v in config.items() if not k.startswith("_")}


def redact_page(img, zones, is_cover=False, header_cfg=None, footer_cfg=None):
    """
    Apply black rectangles to a single page image.

    Args:
        img: PIL Image
        zones: list of cover page zones (applied only if is_cover=True)
        is_cover: whether this is the cover page
        header_cfg: {"enabled": bool, "height_px": int}
        footer_cfg: {"enabled": bool, "height_px": int}

    Returns:
        Modified PIL Image
    """
    draw = ImageDraw.Draw(img)
    w, h = img.size
    count = 0

    # Header redaction (every page)
    if header_cfg and header_cfg.get("enabled"):
        hh = header_cfg.get("height_px", 150)
        draw.rectangle([0, 0, w, hh], fill="black")
        count += 1

    # Footer redaction (every page)
    if footer_cfg and footer_cfg.get("enabled"):
        fh = footer_cfg.get("height_px", 100)
        draw.rectangle([0, h - fh, w, h], fill="black")
        count += 1

    # Cover page specific zones
    if is_cover and zones:
        for zone in zones:
            x = zone.get("x", 0)
            y = zone.get("y", 0)
            zw = zone.get("w", 500)
            zh = zone.get("h", 100)
            draw.rectangle([x, y, x + zw, y + zh], fill="black")
            count += 1

    return img, count


def add_redaction_stamp(img, page_num, doc_type):
    """Add small stamp at bottom-right indicating redaction was applied."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    stamp = f"REDACTED | {doc_type} | p.{page_num} | {datetime.now().strftime('%Y-%m-%d')}"

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Semi-transparent stamp area
    bbox = draw.textbbox((0, 0), stamp, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    margin = 10
    draw.rectangle(
        [w - tw - margin * 2, h - th - margin * 2, w, h],
        fill="white"
    )
    draw.text(
        (w - tw - margin, h - th - margin),
        stamp, fill="gray", font=font
    )
    return img


def process_pdf(pdf_path, doc_type, config, output_dir=None,
                page_range=None, dpi=DEFAULT_DPI, add_stamp=True,
                progress_callback=None):
    """
    Main processing function.

    Args:
        pdf_path: Path to input PDF
        doc_type: Key in config (e.g., "BPR", "Campaign_Report")
        config: Loaded config dict
        output_dir: Output directory (default: same folder as PDF)
        page_range: Tuple (start, end) 1-indexed, or None for all
        dpi: Resolution for conversion
        add_stamp: Whether to add redaction stamp
        progress_callback: Function(current, total, message) for GUI updates

    Returns:
        (output_path, stats_dict)
    """
    pdf_path = Path(pdf_path)
    doc_cfg = config.get(doc_type, {})

    header_cfg = doc_cfg.get("header", {"enabled": False})
    footer_cfg = doc_cfg.get("footer", {"enabled": False})
    cover_zones = doc_cfg.get("cover_page_zones", [])
    skip_pages = set(doc_cfg.get("skip_pages", []))

    # Create output directory
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_redacted"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert PDF to images
    if progress_callback:
        progress_callback(0, 1, "Converting PDF to images...")

    convert_kwargs = {"dpi": dpi, "fmt": "png"}
    if page_range:
        convert_kwargs["first_page"] = page_range[0]
        convert_kwargs["last_page"] = page_range[1]

    try:
        images = convert_from_path(str(pdf_path), **convert_kwargs)
    except Exception as e:
        raise RuntimeError(
            f"PDF conversion failed: {e}\n\n"
            f"If Poppler is not installed:\n"
            f"  Windows: Download from github.com/osber/poppler/releases\n"
            f"           Extract, add bin/ folder to system PATH\n"
            f"  Mac: brew install poppler\n"
            f"  Linux: apt install poppler-utils"
        )

    total_pages = len(images)
    start_page = page_range[0] if page_range else 1

    stats = {
        "total_pages": total_pages,
        "redacted_pages": 0,
        "skipped_pages": 0,
        "total_zones_applied": 0,
        "output_files": []
    }

    for i, img in enumerate(images):
        page_num = start_page + i

        if progress_callback:
            progress_callback(i + 1, total_pages,
                            f"Processing page {page_num}...")

        # Skip excluded pages (e.g., signature log)
        if page_num in skip_pages:
            stats["skipped_pages"] += 1
            continue

        # Apply redactions
        is_cover = (page_num == 1)
        img, zone_count = redact_page(
            img,
            zones=cover_zones,
            is_cover=is_cover,
            header_cfg=header_cfg,
            footer_cfg=footer_cfg
        )

        if add_stamp and zone_count > 0:
            img = add_redaction_stamp(img, page_num, doc_type)

        # Save
        filename = f"p{page_num:03d}.png"
        out_path = output_dir / filename
        img.save(str(out_path), "PNG", optimize=True)

        stats["redacted_pages"] += 1
        stats["total_zones_applied"] += zone_count
        stats["output_files"].append(str(out_path))

    # Save processing log
    log = {
        "source_file": str(pdf_path),
        "document_type": doc_type,
        "processed_at": datetime.now().isoformat(),
        "dpi": dpi,
        "config_used": doc_cfg,
        "stats": stats
    }
    log_path = output_dir / "redaction_log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    return output_dir, stats


# ================================================================
# GUI
# ================================================================

class RedactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Amaran PDF Redaction Tool v{VERSION}")
        self.root.geometry("620x520")
        self.root.resizable(False, False)

        self.config = load_config()
        if not self.config:
            root.destroy()
            return

        self.pdf_path = tk.StringVar()
        self.doc_type = tk.StringVar()
        self.page_start = tk.StringVar(value="")
        self.page_end = tk.StringVar(value="")
        self.add_stamp = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self):
        # --- File Selection ---
        frame_file = ttk.LabelFrame(self.root, text="1. Select PDF", padding=10)
        frame_file.pack(fill="x", padx=10, pady=(10, 5))

        ttk.Entry(frame_file, textvariable=self.pdf_path, width=55).pack(
            side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(frame_file, text="Browse...", command=self.browse_file).pack(
            side="right")

        # --- Document Type ---
        frame_type = ttk.LabelFrame(self.root, text="2. Document Type", padding=10)
        frame_type.pack(fill="x", padx=10, pady=5)

        doc_types = list(self.config.keys())
        self.doc_type.set(doc_types[0] if doc_types else "")

        for dtype in doc_types:
            desc = self.config[dtype].get("description", dtype)
            ttk.Radiobutton(
                frame_type, text=f"{dtype}  ({desc})",
                variable=self.doc_type, value=dtype
            ).pack(anchor="w")

        # --- Options ---
        frame_opts = ttk.LabelFrame(self.root, text="3. Options", padding=10)
        frame_opts.pack(fill="x", padx=10, pady=5)

        # Page range
        page_frame = ttk.Frame(frame_opts)
        page_frame.pack(fill="x")
        ttk.Label(page_frame, text="Page range (blank = all):").pack(side="left")
        ttk.Entry(page_frame, textvariable=self.page_start, width=6).pack(
            side="left", padx=(10, 2))
        ttk.Label(page_frame, text="to").pack(side="left", padx=2)
        ttk.Entry(page_frame, textvariable=self.page_end, width=6).pack(
            side="left", padx=(2, 10))

        ttk.Checkbutton(
            frame_opts, text="Add redaction stamp on processed pages",
            variable=self.add_stamp
        ).pack(anchor="w", pady=(5, 0))

        # --- Redaction Preview ---
        frame_preview = ttk.LabelFrame(self.root, text="4. What Will Be Redacted", padding=10)
        frame_preview.pack(fill="x", padx=10, pady=5)

        self.preview_text = tk.Text(frame_preview, height=5, width=70,
                                     state="disabled", bg="#f5f5f5",
                                     font=("Consolas", 9))
        self.preview_text.pack(fill="x")

        # Update preview when doc type changes
        self.doc_type.trace_add("write", lambda *_: self.update_preview())
        self.update_preview()

        # --- Progress ---
        self.progress_var = tk.DoubleVar()
        self.progress_label = ttk.Label(self.root, text="Ready")
        self.progress_label.pack(padx=10, anchor="w")
        self.progress_bar = ttk.Progressbar(
            self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", padx=10, pady=(2, 5))

        # --- Run Button ---
        ttk.Button(
            self.root, text="Run Redaction",
            command=self.run_redaction
        ).pack(pady=10)

    def update_preview(self):
        dtype = self.doc_type.get()
        cfg = self.config.get(dtype, {})

        lines = []
        header = cfg.get("header", {})
        if header.get("enabled"):
            lines.append(f"  Header: black-fill top {header.get('height_px', 0)}px on every page")

        cover = cfg.get("cover_page_zones", [])
        for zone in cover:
            lines.append(f"  Cover: {zone.get('label', 'zone')} "
                        f"(x={zone['x']}, y={zone['y']}, "
                        f"{zone['w']}x{zone['h']}px)")

        skip = cfg.get("skip_pages", [])
        if skip:
            lines.append(f"  Skip pages: {skip} (excluded from output)")

        if not lines:
            lines.append("  No redaction rules defined for this type.")

        self.preview_text.config(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", "\n".join(lines))
        self.preview_text.config(state="disabled")

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Select PDF to redact",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if path:
            self.pdf_path.set(path)

    def run_redaction(self):
        pdf = self.pdf_path.get().strip()
        if not pdf or not Path(pdf).exists():
            messagebox.showwarning("No File", "Please select a valid PDF file.")
            return

        dtype = self.doc_type.get()
        if not dtype:
            messagebox.showwarning("No Type", "Please select a document type.")
            return

        # Parse page range
        page_range = None
        ps = self.page_start.get().strip()
        pe = self.page_end.get().strip()
        if ps and pe:
            try:
                page_range = (int(ps), int(pe))
            except ValueError:
                messagebox.showwarning("Invalid Range",
                    "Page range must be numbers.")
                return

        def progress_cb(current, total, msg):
            pct = (current / total * 100) if total > 0 else 0
            self.progress_var.set(pct)
            self.progress_label.config(text=msg)
            self.root.update_idletasks()

        try:
            self.progress_label.config(text="Processing...")
            self.root.update_idletasks()

            output_dir, stats = process_pdf(
                pdf_path=pdf,
                doc_type=dtype,
                config=self.config,
                page_range=page_range,
                add_stamp=self.add_stamp.get(),
                progress_callback=progress_cb
            )

            self.progress_var.set(100)
            self.progress_label.config(text="Complete!")

            msg = (
                f"Redaction complete!\n\n"
                f"Pages processed: {stats['redacted_pages']}\n"
                f"Pages skipped: {stats['skipped_pages']}\n"
                f"Zones applied: {stats['total_zones_applied']}\n\n"
                f"Output: {output_dir}\n\n"
                f"Open output folder?"
            )
            if messagebox.askyesno("Done", msg):
                os.startfile(str(output_dir))

        except RuntimeError as e:
            messagebox.showerror("Error", str(e))
            self.progress_label.config(text="Failed")
        except Exception as e:
            messagebox.showerror("Unexpected Error", str(e))
            self.progress_label.config(text="Failed")


# ================================================================
# CLI MODE (for scripting / automation)
# ================================================================

def cli_mode():
    import argparse
    parser = argparse.ArgumentParser(
        description=f"Amaran PDF Redaction Tool v{VERSION}")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument("--type", "-t", required=True,
                       help="Document type (BPR, Campaign_Report, etc.)")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--pages", "-p", help="Page range, e.g. 1-10")
    parser.add_argument("--dpi", type=int, default=DEFAULT_DPI)
    parser.add_argument("--no-stamp", action="store_true")
    args = parser.parse_args()

    config = {}
    config_path = Path(__file__).parent / CONFIG_FILE
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
            config = {k: v for k, v in raw.items() if not k.startswith("_")}

    if args.type not in config:
        print(f"Error: Unknown document type '{args.type}'")
        print(f"Available: {', '.join(config.keys())}")
        sys.exit(1)

    page_range = None
    if args.pages:
        parts = args.pages.split("-")
        page_range = (int(parts[0]), int(parts[1]))

    def progress(cur, total, msg):
        print(f"  [{cur}/{total}] {msg}")

    print(f"Amaran PDF Redaction Tool v{VERSION}")
    print(f"Input:  {args.pdf}")
    print(f"Type:   {args.type}")
    print()

    output_dir, stats = process_pdf(
        pdf_path=args.pdf,
        doc_type=args.type,
        config=config,
        output_dir=args.output,
        page_range=page_range,
        dpi=args.dpi,
        add_stamp=not args.no_stamp,
        progress_callback=progress
    )

    print()
    print(f"Done! Output: {output_dir}")
    print(f"  Pages processed: {stats['redacted_pages']}")
    print(f"  Pages skipped:   {stats['skipped_pages']}")
    print(f"  Zones applied:   {stats['total_zones_applied']}")


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI mode: python redact.py input.pdf --type BPR
        cli_mode()
    else:
        # GUI mode: double-click to run
        root = tk.Tk()
        app = RedactionApp(root)
        root.mainloop()
