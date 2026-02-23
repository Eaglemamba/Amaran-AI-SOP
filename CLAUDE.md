# CLAUDE.md - Project Instructions for Claude Code

## Project Context
This is the AI SOP Knowledge Retrieval project for Amaran Biopharmaceutical CDMO (Taiwan). 
Owner: David (Operations Excellence). 
Industry: Clinical-phase sterile fill-finish pharmaceutical manufacturing.

## Key Files
- `deliverables/AI_SOP_Implementation_Roadmap_v2.html` - Master roadmap (tabbed UI, 16 apps + 6 infra)
- `deliverables/AI_SOP_Application_Dependency_Map.html` - Interactive dependency graph (22 nodes)
- `deliverables/sop_to_markdown.py` - SOP conversion pipeline
- `deliverables/amaran_presentation_SKILL_v2.md` - PPTX generation skill
- `transcripts/journal.txt` - Index of all conversation transcripts

## Architecture Decisions
- Markdown files + Gemini 1M context window (NOT vector DB/RAG)
- Claude for document generation/reasoning, Gemini for OCR/vision
- Proportionate GMP governance (not full GAMP for internal advisory tools)
- [[placeholder]] methodology for document automation (e.g., [[BATCH_NO]], [[IPC1_B1]])

## Style Preferences
- Direct, consulting tone. No emojis.
- Segment answers into categories when possible.
- Simple language, actionable advice.
- Brief and concise.
- HTML deliverables use Poppins + Noto Sans TC fonts, Amaran brand colors (#482A77 primary).

## Regulatory Context
- PIC/S GMP, TFDA compliance required
- 21 CFR Part 11 for electronic records
- ICH Q9(R1) for risk assessments
- ISPE GAMP for AI validation guidance (proportionate application)

## Document Naming Conventions
- SOPs: `QP-XXXX` (Quality Procedures) or `GP-XXXX` (General Procedures) — 4-digit suffix
- WIs: `WI-XXX-YYY` or `WI-XX-YYY` — XXX/XX is department abbreviation (e.g., QA, QC, PRD), YYY is sequence number

## Current Phase
Pre-Phase 0. Roadmap and strategy complete. Next: build desensitization script, convert pilot SOPs, define test queries.
