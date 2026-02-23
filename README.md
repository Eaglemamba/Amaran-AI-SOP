# AI SOP Knowledge Retrieval Project - Handoff Package
## For Claude Code Continuation

**Project Owner:** David, Operations Excellence Lead, Amaran Biopharmaceutical CDMO (Taiwan)
**Date Packaged:** 2026-02-23
**Source:** Claude.ai Project conversations (Feb 13-23, 2026)

---

## What This Project Is

An AI-powered SOP (Standard Operating Procedure) knowledge retrieval system for a clinical-phase sterile fill-finish CDMO. The system enables natural language queries across company SOPs, with applications spanning change control impact assessment, regulatory gap analysis, deviation investigation, and more.

Architecture: Markdown + Gemini 1M token context window (not vector DB/RAG at current scale).

---

## Package Contents

### /deliverables/ (11 files)
Final output files from all sessions:

| File | Description |
|------|-------------|
| `AI_SOP_Implementation_Roadmap_v2.html` | **Primary deliverable.** Tabbed roadmap with 16 apps + 6 supporting deliverables across 5 phases. Gantt chart, metrics, architecture decision. |
| `AI_SOP_Application_Dependency_Map.html` | Interactive SVG dependency map (22 nodes). Click any node to see upstream/downstream. Right panel shows details. 3 node types: app (rect), infra (pill), decision gate (dashed). |
| `AI_SOP_Knowledge_Retrieval_Strategic_Brief.pptx` | 10-slide executive presentation using Amaran template. Poppins fonts embedded. |
| `AI_SOP_Knowledge_Retrieval_Strategic_Brief.pdf` | PDF export of above for mobile viewing. |
| `AI_SOP_Strategic_Brief_v7.pptx` | Earlier version (same content, earlier iteration). |
| `AI_SOP_Strategic_Brief_v7.pdf` | PDF of above. |
| `markdown_ai_guide_20250213.html` | Educational guide: "Markdown in the AI Era" - bilingual, covers GMP compliance. |
| `markdown_dms_rag_architecture_20250213.html` | Technical architecture: Markdown-DMS dual-track integration for RAG. |
| `sop_to_markdown.py` | Python script for SOP-to-Markdown conversion pipeline. |
| `Dependency_Map_Master_Prompt.md` | Reusable prompt template for generating dependency maps. |
| `amaran_presentation_SKILL_v2.md` | SKILL.md for Amaran PPTX template generation (python-pptx). |

### /transcripts/ (12 files)
Complete conversation transcripts, chronological:

| Transcript | Topic |
|-----------|-------|
| `journal.txt` | **Index file** - summaries of all sessions |
| `2026-02-13-09-05-17-*` | Markdown in AI era + GMP compliance guide |
| `2026-02-13-09-39-27-*` | Markdown-DMS-RAG architecture for CDMO (13 apps identified) |
| `2026-02-13-10-37-46-*` | CCS + Change Control as RAG use case |
| `2026-02-13-23-53-01-*` | Strategic brief presentation creation |
| `2026-02-14-00-38-48-*` | PPTX template debugging (auto-numbering fix) |
| `2026-02-14-15-49-31-*` | PPTX shape rendering fix (cross-platform) |
| `2026-02-14-16-38-08-*` | Font embedding fix (Poppins in PPTX) |
| `2026-02-14-16-38-48-*` | Font embedding (duplicate session) |
| `2026-02-14-16-50-19-*` | Full-bleed layout optimization |
| `2026-02-14-18-07-32-*` | Dependency map + implementation roadmap |
| `2026-02-14-18-38-30-*` | Roadmap v2: governance, architecture, gap analysis |

### /context/ (this file + CLAUDE.md)
- `README.md` - This file
- `CLAUDE.md` - Instructions for Claude Code

---

## Key Decisions Made

1. **Architecture:** Markdown + Gemini context window, NOT vector DB. Re-evaluate at Phase 2 end if >500 docs.
2. **Governance:** Proportionate to risk. Internal advisory tool = 1-page AI Use Policy + system inventory. NOT full GAMP. Exception: Customer Service Bot (external-facing).
3. **CC Impact split:** Basic (Phase 1, 1-2 wks, prompt engineering) vs Full Matrix (Phase 2, 4-6 wks, knowledge extraction). Don't conflate.
4. **CCS as upstream to CC:** Contamination Control Strategy should be consulted during every Change Control initiation for impact assessment.
5. **Tool selection:** Gemini for OCR/vision, Claude for document generation/reasoning.
6. **Bus factor mitigation:** All documentation, SKILL.md files, and governance docs serve dual purpose (compliance + knowledge transfer).

---

## Current Status (as of 2026-02-23)

- Roadmap v2 with tabbed UI: COMPLETE
- Dependency Map v4 (22 nodes, 3 types): COMPLETE
- Strategic Brief presentation: COMPLETE
- SOP-to-Markdown conversion script: COMPLETE
- Amaran PPTX SKILL.md: COMPLETE

**Not yet started:** Actual SOP conversion, desensitization script, acceptance test suite, AI Use Policy draft.

---

## Continuation Priorities for Claude Code

1. Build the desensitization Python script (strip client names, product codes, batch numbers, pricing)
2. Convert 5-10 pilot SOPs to Markdown using sop_to_markdown.py
3. Define 10-15 acceptance test queries with known correct answers
4. Draft 1-page AI Use Policy
5. Test SOP Content Search accuracy with pilot SOPs in Gemini

---

## Related Amaran Projects (not in this package)

These are separate but connected workstreams David is developing:
- **BPR Verifier v5.5.0** - Automated batch record verification (93.3% accuracy)
- **Campaign Report Generator** - [[placeholder]] methodology for document automation
- **Report Generator v1.3** - HTML/PDF report output from BPR Verifier JSON
- **OpEx Roadmap** - Closing 120M NTD revenue gap (separate from AI SOP project)
