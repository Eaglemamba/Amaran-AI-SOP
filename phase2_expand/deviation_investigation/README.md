# App #6: Deviation Investigation Reference

**Phase:** 2 | **Timeline:** Week 8-11 | 2026-04-13 to 2026-05-03
**Effort:** 2-3 weeks | **Complexity:** Medium
**Dept:** QA / MFG
**Dependency Map ID:** `deviation`

## Purpose
"Show similar deviations and root causes." Add deviation/CAPA records. Requires desensitizing deviation records (heavier than SOPs -- batch-specific data) and linking to SOP references.

## Expected Files
- Deviation record conversion/desensitization pipeline
- System prompts for deviation investigation queries
- CAPA cross-reference logic

## Dependencies
- Upstream: SOP Content Search, CC Impact Basic
- Downstream: BD Client Q&A, APQR, Deviation Report Gen, CC Impact Full, CCS
