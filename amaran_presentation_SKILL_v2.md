---
name: amaran-presentation
description: Create professional presentations using Amaran's company slide template. Use when building presentations, pitch decks, reports, or any slide-based content that should follow Amaran's visual identity and design standards.
---

# Amaran Presentation Skill

Create branded presentations using Amaran Biotech's official template (Widescreen 13.33" x 7.5").

## Quick Start

```python
from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree
import shutil

template_path = "/mnt/skills/user/amaran-presentation/assets/Amaran_PPT_Template.pptx"
output_path = "/home/claude/presentation.pptx"
shutil.copy(template_path, output_path)
prs = Presentation(output_path)

# ALWAYS remove all 23 demo slides before adding content
while len(prs.slides) > 0:
    rId = prs.slides._sldIdLst[0].rId
    prs.part.drop_rel(rId)
    prs.slides._sldIdLst.remove(prs.slides._sldIdLst[0])
```

## Critical: Template Dimensions and Safe Zones

```
Slide: 13.33" wide x 7.5" tall (widescreen)

┌─────────────────────────────────────────┐
│  Title placeholder area (0.4" - 1.3")   │  <- Title zone
│─────────────────────────────────────────│
│                                         │
│  SAFE CONTENT ZONE                      │  <- 1.4" to 5.7"
│  (Keep ALL content within this area)    │
│  Left margin: 0.5"   Right edge: 12.8" │
│  Full usable width: 12.3"              │
│                                         │
│─────────────────────────────────────────│
│  ██ Amaran Logo + Wave Graphic ██████   │  <- 6.0" to 7.5"
│  ██████████████████████████████████████  │     DO NOT place content here
└─────────────────────────────────────────┘
     ↑ 0.5" left margin           12.8" →  ↑ right edge
```

**HARD RULE: All content must stay ABOVE y = 5.7 inches.** The Amaran branded wave graphic and logo occupy the bottom ~1.5" of every slide (except Layout 0 title page which has a larger wave). Content placed below y=5.7" WILL be covered or clipped.

**Full-bleed layout constants:**
```python
LM = 0.5    # left margin
RM = 12.8   # right edge  
FW = 12.3   # full usable width
HW = 5.8    # half width (for two-column)
MID = 7.0   # midpoint x for right column
YMAX = 5.7  # max y before logo zone
```

## Template Layouts Reference

### Recommended Layouts

| Layout | Name | Use For | Placeholders |
|--------|------|---------|-------------|
| **0** | 標題投影片 (Title) | Cover/title slide only | PH14: title (0.6",0.5" / 12.2"x1.0"), PH12: subtitle (0.6",1.6" / 12.2"x0.6"), PH13: footer (0.6",6.5" / 2.4"x0.4") |
| **17** | 自訂版面配置 (Custom) | **ALL content slides** | PH11: title only (0.8",0.4" / 11.7"x0.9") + page number |

### Layouts to AVOID for Content

| Layout | Issue |
|--------|-------|
| 1-8 | Placeholders inherit master body style with auto-bullets, indent, and 28pt default font. Paragraphs added via `add_paragraph()` get unwanted numbered list formatting. |
| 9-12 | Two-column placeholders with same inherited bullet problem. Content extends too low into logo zone. |
| 13-16 | Multi-cell grid layouts - very rigid positioning, hard to control content. |

**Why Layout 17 is the safe choice:** It only has a title placeholder (PH11) and page number. All other content is built with free textboxes and shapes, giving full control over positioning, font size, bullets, and spacing.

## Critical Bug: Inherited Auto-Numbering

The slide master's `bodyStyle` enforces these properties on ALL body placeholders (Layouts 1-16):

```xml
<a:lvl1pPr marL="228600" indent="-228600">
  <a:buFont typeface="Arial"/>
  <a:buChar char="•"/>       <!-- forced bullet character -->
  <a:defRPr sz="2800"/>      <!-- forced 28pt font -->
  <a:spcBef><a:spcPts val="1000"/></a:spcBef>  <!-- 10pt spacing -->
</a:lvl1pPr>
```

**Effect:** Every `add_paragraph()` call in a placeholder inherits bullet characters, 28pt font, large margins, and wide spacing - regardless of what you set in python-pptx. The text appears as a numbered/bulleted list with huge spacing.

**The fix (if you must use Layouts 1-16):** Apply `kill_bullets()` to EVERY paragraph:

```python
def kill_bullets(paragraph):
    """Remove inherited bullet/numbering from a paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('marL', '0')
    pPr.set('indent', '0')
    buNone = pPr.find(qn('a:buNone'))
    if buNone is None:
        etree.SubElement(pPr, qn('a:buNone'))
    for tag in ['a:buChar', 'a:buAutoNum', 'a:buFont']:
        el = pPr.find(qn(tag))
        if el is not None:
            pPr.remove(el)
```

**Better approach: Use Layout 17 + free textboxes.** This avoids the inheritance problem entirely.

## Critical: AVOID Shape Elements (Rounded Rectangles, Cards, Color Bars)

**Problem discovered:** Shapes created with `add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, ...)` render correctly in LibreOffice PDF export but **misrender in PowerPoint and mobile viewers**. The shapes appear as oversized opaque blocks that cover surrounding text.

This affects:
- KPI cards with colored top bars
- Roadmap phase header bars  
- Background boxes behind content
- Any `MSO_SHAPE.ROUNDED_RECTANGLE` or `MSO_SHAPE.RECTANGLE` used decoratively

**Root cause:** Shape positioning/sizing interprets EMU values differently across renderers. LibreOffice shows them at intended size; PowerPoint and mobile expand them.

**Solution: Use PURE TEXT for all content.** Replace visual cards with:
- Bold colored text headers instead of colored shape bars
- Unicode line characters (`\u2500`) for separators instead of shape borders  
- Manual bullet characters (`\u2022`) instead of shape-based lists
- Large bold colored numbers for KPI display instead of card backgrounds

**The only safe shape usage** is the template's built-in backgrounds and logos (which are part of the slide master, not added programmatically).

## Brand Colors (from Amaran Brand Guide)

```python
# ── Primary Palette ──
PURPLE    = RGBColor(0x48, 0x2A, 0x77)  # Pantone 7679C - PRIMARY brand color
GRAY      = RGBColor(0x5A, 0x55, 0x55)  # Pantone Cool Gray 10C
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
BLACK     = RGBColor(0x00, 0x00, 0x00)

# ── Purple Tints (innovation column) ──
PURPLE_MD = RGBColor(0x79, 0x62, 0x9B)  # Pantone 2101C - mid-tone purple
PURPLE_LT = RGBColor(0xD4, 0xCC, 0xE0)  # Pantone 270C - light purple tint

# ── Secondary Color Palette ──
PINK      = RGBColor(0xE6, 0x76, 0xA7)  # Pantone 237C (gentle)
GREEN     = RGBColor(0x83, 0xBB, 0x70)  # Pantone 2255C (organic)
ORANGE    = RGBColor(0xF1, 0x82, 0x36)  # Pantone 3588C (vitality)

# ── Functional Colors (not in brand guide, but needed) ──
POSITIVE  = RGBColor(0x2E, 0x7D, 0x32)  # Green for success/improvement
NEGATIVE  = RGBColor(0xC6, 0x28, 0x28)  # Red for problems/warnings
MUTED     = RGBColor(0x8C, 0x85, 0x85)  # Light gray for captions

# ── Text Hierarchy ──
# Headings: PURPLE (#482A77)
# Body text: GRAY (#5A5555) 
# Captions/footnotes: MUTED
# Labels on dark backgrounds: WHITE
```

**IMPORTANT:** The previous SKILL.md used incorrect navy blue (#2D2E72) and teal (#009688) colors. The actual Amaran brand color is **purple #482A77** (Pantone 7679C). Always use PURPLE for headings and primary UI elements.

## Brand Fonts (from Amaran Brand Guide)

```python
FONT_EN = 'Poppins'         # Primary English typeface (SemiBold, Medium, Regular)
FONT_TC = 'Noto Sans TC'    # Primary Chinese typeface (Bold, SemiBold, Medium, Regular)
# General Sans is the official secondary typeface but is NOT a standard system font.
# Use Poppins for ALL text to avoid Times New Roman fallback on devices without General Sans.
```

**Critical: Font Embedding Required**

Poppins is NOT installed on most devices (phones, Windows PCs). Without embedding, PowerPoint falls back to **Times New Roman**. You MUST embed fonts after generating the PPTX.

**Usage rules:**
- Use **Poppins** for ALL English text (headings, body, captions) to keep it simple and embeddable
- Use **Noto Sans TC** for Chinese content (available on most CJK-capable systems)
- **Never use General Sans** in generated PPTX - it's not available for embedding and will fall back to Times New Roman
- **Never use Calibri** - it was the previous incorrect default
- After all content is built, run `embed_fonts()` before saving final output

**Font embedding process** (add to every script):

```python
import zipfile, shutil, os
from lxml import etree

def embed_fonts(pptx_path, output_path=None):
    """Embed Poppins fonts into PPTX so they render on any device."""
    if output_path is None:
        output_path = pptx_path
    
    FONTS = {
        'Poppins-Regular': '/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf',
        'Poppins-Bold': '/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf',
        'Poppins-Medium': '/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf',
        'Poppins-Italic': '/usr/share/fonts/truetype/google-fonts/Poppins-Italic.ttf',
    }
    
    extract_dir = '/home/claude/_font_embed_tmp'
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    
    # Extract
    with zipfile.ZipFile(pptx_path, 'r') as z:
        z.extractall(extract_dir)
    
    # Copy font files
    fonts_dir = os.path.join(extract_dir, 'ppt', 'fonts')
    os.makedirs(fonts_dir, exist_ok=True)
    font_parts = {}
    for i, (name, path) in enumerate(FONTS.items(), 1):
        fname = f'font{i}.fntdata'
        shutil.copy(path, os.path.join(fonts_dir, fname))
        font_parts[name] = (f'fonts/{fname}', f'rId{900+i}')
    
    # Add relationships
    rels_ns = 'http://schemas.openxmlformats.org/package/2006/relationships'
    font_rel_type = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/font'
    rels_path = os.path.join(extract_dir, 'ppt', '_rels', 'presentation.xml.rels')
    rels_tree = etree.parse(rels_path)
    for name, (target, rid) in font_parts.items():
        rel = etree.SubElement(rels_tree.getroot(), f'{{{rels_ns}}}Relationship')
        rel.set('Id', rid); rel.set('Type', font_rel_type); rel.set('Target', target)
    rels_tree.write(rels_path, xml_declaration=True, encoding='UTF-8', standalone=True)
    
    # Add embeddedFontLst to presentation.xml
    p_ns = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    a_ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    r_ns = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
    pres_path = os.path.join(extract_dir, 'ppt', 'presentation.xml')
    pres_tree = etree.parse(pres_path)
    pres_root = pres_tree.getroot()
    
    font_lst = etree.SubElement(pres_root, f'{{{p_ns}}}embeddedFontLst')
    emb = etree.SubElement(font_lst, f'{{{p_ns}}}embeddedFont')
    desc = etree.SubElement(emb, f'{{{a_ns}}}font')
    desc.set('typeface', 'Poppins')
    
    for style, key in [('regular','Poppins-Regular'),('bold','Poppins-Bold'),('italic','Poppins-Italic')]:
        elem = etree.SubElement(emb, f'{{{p_ns}}}{style}')
        elem.set(f'{{{r_ns}}}id', font_parts[key][1])
    
    # Position after sldMasterIdLst
    master = pres_root.find(f'{{{p_ns}}}sldMasterIdLst')
    if master is not None:
        idx = list(pres_root).index(master)
        pres_root.remove(font_lst)
        pres_root.insert(idx + 1, font_lst)
    pres_tree.write(pres_path, xml_declaration=True, encoding='UTF-8', standalone=True)
    
    # Add content type
    ct_ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
    ct_path = os.path.join(extract_dir, '[Content_Types].xml')
    ct_tree = etree.parse(ct_path)
    if not any(e.get('Extension') == 'fntdata' for e in ct_tree.getroot()):
        d = etree.SubElement(ct_tree.getroot(), f'{{{ct_ns}}}Default')
        d.set('Extension', 'fntdata'); d.set('ContentType', 'application/x-fontdata')
    ct_tree.write(ct_path, xml_declaration=True, encoding='UTF-8', standalone=True)
    
    # Repackage
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zout:
        for root, dirs, files in os.walk(extract_dir):
            for f in files:
                fp = os.path.join(root, f)
                zout.write(fp, os.path.relpath(fp, extract_dir))
    shutil.rmtree(extract_dir)

# Usage at end of every script:
# prs.save('/home/claude/output.pptx')
# embed_fonts('/home/claude/output.pptx', '/mnt/user-data/outputs/final.pptx')
```

## Helper Functions (Copy These Into Every Script)

```python
def emu(inches):
    """Convert inches to EMU."""
    return int(inches * 914400)

def kill_bullets(paragraph):
    """Remove inherited bullet/numbering from a paragraph."""
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('marL', '0')
    pPr.set('indent', '0')
    buNone = pPr.find(qn('a:buNone'))
    if buNone is None:
        etree.SubElement(pPr, qn('a:buNone'))
    for tag in ['a:buChar', 'a:buAutoNum', 'a:buFont']:
        el = pPr.find(qn(tag))
        if el is not None:
            pPr.remove(el)

def set_spacing(paragraph, before_pt=0, after_pt=0, line_pct=100):
    """Set paragraph spacing explicitly."""
    pPr = paragraph._p.get_or_add_pPr()
    if before_pt > 0:
        spcBef = etree.SubElement(pPr, qn('a:spcBef'))
        etree.SubElement(spcBef, qn('a:spcPts')).set('val', str(int(before_pt * 100)))
    if after_pt > 0:
        spcAft = etree.SubElement(pPr, qn('a:spcAft'))
        etree.SubElement(spcAft, qn('a:spcPts')).set('val', str(int(after_pt * 100)))
    if line_pct != 100:
        lnSpc = etree.SubElement(pPr, qn('a:lnSpc'))
        etree.SubElement(lnSpc, qn('a:spcPct')).set('val', str(int(line_pct * 1000)))

def add_text(slide, left, top, width, height, text, size=14, bold=False,
             color=GRAY, align=PP_ALIGN.LEFT, font='Poppins', italic=False):
    """Add a text box with NO inherited bullets."""
    txBox = slide.shapes.add_textbox(emu(left), emu(top), emu(width), emu(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font
    p.font.italic = italic
    p.alignment = align
    kill_bullets(p)
    return txBox

def add_bullet_list(slide, left, top, width, height, items, size=11,
                    color=GRAY, bullet_char="\u2022", spacing=3, font='Poppins'):
    """Add a list with manual bullet characters (bypasses template inheritance)."""
    txBox = slide.shapes.add_textbox(emu(left), emu(top), emu(width), emu(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{bullet_char} {item}"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.name = font
        kill_bullets(p)
        set_spacing(p, before_pt=spacing)
    return txBox

def fill_placeholder(slide, ph_idx, text, size=28, bold=True, color=PURPLE):
    """Fill a layout placeholder and remove inherited bullets."""
    for ph in slide.placeholders:
        if ph.placeholder_format.idx == ph_idx:
            ph.text = text
            for para in ph.text_frame.paragraphs:
                para.font.size = Pt(size)
                para.font.bold = bold
                para.font.color.rgb = color
                para.font.name = 'Poppins'
                kill_bullets(para)
            return ph
```

**WARNING: Do NOT use `add_shape()` or `add_rounded_box()` for decorative elements.** Shapes render inconsistently across PowerPoint, mobile, and LibreOffice. Stick to textboxes only.

## Standard Slide Patterns

### Pattern 1: Title Slide (Layout 0)

```python
slide = prs.slides.add_slide(prs.slide_layouts[0])
fill_placeholder(slide, 14, "Main Title Here", size=36, color=PURPLE)
fill_placeholder(slide, 12, "Subtitle or description", size=16, bold=False, color=GRAY)
fill_placeholder(slide, 13, "Department  |  Date", size=10, bold=False, color=MUTED)
```

### Pattern 2: Two-Column Content (Layout 17 + Textboxes)

```python
slide = prs.slides.add_slide(prs.slide_layouts[17])
fill_placeholder(slide, 11, "Slide Title", size=28, color=PURPLE)

# Left column (0.5" to ~6.2")
add_text(slide, 0.5, 1.5, 6.0, 0.35, "Left Header", size=16, bold=True, color=PURPLE)
add_bullet_list(slide, 0.5, 2.0, 6.0, 3.5, [
    "First point with enough detail to fill the line width",
    "Second point with more detail for visual weight",
    "Third point",
], size=12, spacing=6)

# Right column (7.0" to ~12.8")
add_text(slide, 7.0, 1.5, 6.0, 0.35, "Right Header", size=16, bold=True, color=PURPLE)
# ... right column content, also using 6.0" width
```

### Pattern 3: KPI Display (Pure Text - No Cards)

```python
# Big colored numbers spread across full width - no background shapes
kpis = [("80%", "Label", "Detail", GREEN), ...]
for i, (num, label, desc, clr) in enumerate(kpis):
    x = 0.5 + i * 3.1
    add_text(slide, x, 1.4, 2.9, 0.6, num, size=42, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_text(slide, x, 2.2, 2.9, 0.5, label, size=12, bold=True, color=PURPLE, align=PP_ALIGN.CENTER)
    add_text(slide, x, 2.85, 2.9, 0.45, desc, size=10, color=MUTED, align=PP_ALIGN.CENTER)
```

### Pattern 4: Phase/Roadmap (Pure Text Columns)

```python
# Side-by-side columns with colored headers - no shape bars
pw = 3.9  # phase column width
for i, (title, sub, clr, items, cost) in enumerate(phases):
    x = 0.5 + i * 4.1
    add_text(slide, x, 1.5, pw, 0.3, title, size=15, bold=True, color=clr)
    add_text(slide, x, 1.85, pw, 0.22, sub, size=11, color=MUTED)
    add_text(slide, x, 2.1, pw, 0.08, "\u2500" * 45, size=5, color=clr)  # separator
    add_bullet_list(slide, x, 2.3, pw, 2.5, items, size=12, spacing=5)
    add_text(slide, x, 5.0, pw, 0.25, cost, size=11, bold=True, color=clr)
```

### Pattern 5: Application Grid (3-Column Text List)

```python
# Three-column layout for maximum coverage
cols = 3
for i, (title, dept, phase) in enumerate(items):
    col = i % cols
    row = i // cols
    x = 0.5 + col * 4.1
    y = 1.5 + row * 0.82
    add_text(slide, x, y, 0.6, 0.22, phase_tag, size=9, bold=True, color=phase_color)
    add_text(slide, x + 0.7, y, 3.2, 0.22, title, size=12, bold=True, color=PURPLE)
    add_text(slide, x + 0.7, y + 0.25, 3.2, 0.2, dept, size=10, color=MUTED)
```

## Font Sizes Reference (Full-Bleed Layout)

| Element | Size | Weight | Color |
|---------|------|--------|-------|
| Cover title | 34-36pt | Bold | PURPLE |
| Slide title (PH11) | 26-30pt | Bold | PURPLE |
| Section header | 14-16pt | Bold | PURPLE or functional color |
| Body text / bullets | 11-12pt | Regular | GRAY |
| Detail / footnote | 9-10pt | Regular | MUTED |
| KPI number | 36-42pt | Bold | Functional color |
| Phase/tag label | 9-10pt | Bold | Functional color |

**Design principle:** Fill the slide. Use larger fonts, wider spacing between items, and spread content across full 12.3" width. Two-column layouts should use both columns fully (LM to ~6.2" left, MID to ~12.8" right).

## Checklist Before Saving

1. **All demo slides removed** (template ships with 23)
2. **Content above y=5.7"** (nothing in logo/wave zone)
3. **`kill_bullets()` on every paragraph** in any placeholder (or use textboxes)
4. **Font = Poppins everywhere** (no General Sans, no Calibri)
5. **Full-bleed layout**: left margin 0.5", content extends to 12.8"
6. **Content fills the slide** - no large empty areas; use larger fonts and wider spacing
7. **`embed_fonts()` called** as final step before delivering PPTX
8. **PDF exported** for mobile viewing (`soffice --headless --convert-to pdf`)

## QA Process

```bash
# 1. Embed fonts (REQUIRED - without this, Poppins falls back to Times New Roman)
# Call embed_fonts() in your Python script before saving

# 2. Convert and inspect
soffice --headless --convert-to pdf presentation.pptx
pdftoppm -jpeg -r 200 presentation.pdf slide_qa

# 3. Check each image for:
# - Text clipped by wave graphic at bottom
# - Unwanted bullet numbers (1. 2. 3.)
# - Text overflow beyond slide edges
# - Empty space (content should fill the slide)
# - Font rendering (should be Poppins, not Times New Roman)

# 4. Always deliver BOTH files:
# - .pptx (with embedded fonts) for desktop editing
# - .pdf for mobile viewing (fonts baked in)
```

## Common Mistakes and Fixes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| **Not embedding fonts** | All text shows as Times New Roman on phones/PCs | Call `embed_fonts()` as final step; deliver PDF alongside PPTX |
| **Using General Sans or Calibri** | Font fallback to Times New Roman | Use Poppins for ALL text |
| **Sparse layout (0.8" margins, small fonts)** | Slide looks empty with large whitespace | Use 0.5" margins, 12pt body, 42pt KPIs; fill to y=5.5" |
| **Using shapes for visual cards/bars** | Shapes render as oversized opaque blocks in PowerPoint/mobile | Use PURE TEXT only: bold headers, Unicode separators, large numbers |
| Using Layout 1-16 without `kill_bullets()` | Paragraphs show as "1. 2. 3." numbered list | Apply `kill_bullets()` to every paragraph, or use Layout 17 |
| Content placed below y=5.7" | Text hidden behind Amaran logo wave | Move all content above y=5.7" |
| Using `add_paragraph()` in placeholder | Inherits 28pt font, wide spacing, bullets | Set explicit font size, call `kill_bullets()`, call `set_spacing()` |
| Setting font only on first paragraph | Subsequent paragraphs revert to 28pt | Loop through ALL paragraphs, set font on each |
| Not removing demo slides | 23 template slides appear before your content | Remove all slides before adding new ones |
