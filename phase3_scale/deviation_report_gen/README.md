# App #13: Deviation Report Generation

**Phase:** 3 | **Timeline:** Week 15-19 | 2026-06-01 to 2026-06-29
**Effort:** 3-4 weeks | **Complexity:** Medium
**Dept:** QA / MFG
**Dependency Map ID:** `dev_report`

## Purpose
Not just search -- actual document generation using [[placeholder]] methodology. Template with placeholders for deviation description, root cause, impacted batches, CAPA, affected SOPs. AI drafts investigation narrative referencing past deviations. Human reviews and finalizes. Same architecture as Campaign Report Generator.

## Expected Files
- `amaran_report_generator_v1_3.py` -- Report generation engine
- `AmaranPlaceholderReplace_DoubleBracket.bas` -- VBA macro for Word template placeholder replacement
- Word templates with [[PLACEHOLDER]] fields
- Sample generated reports

## Dependencies
- Upstream: Deviation Investigation, SOP Content Search, CCS, Risk Assessment + CC Proc
- Downstream: None (terminal application node)
