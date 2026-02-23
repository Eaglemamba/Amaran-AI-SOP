# SOP Content Search -- Conversion Pipeline

**Phase:** 0 | **Timeline:** Week 1-4 | 2026-02-23 to 2026-03-22
**Effort:** 2-3 weeks + 1 week testing | **Complexity:** Medium
**Dept:** All Depts
**Dependency Map ID:** `sop_search`

## Purpose
The critical path. Build SOP-to-Markdown conversion pipeline, run desensitization, upload 5-10 pilot SOPs to Gemini. Test natural language queries. Validate citation accuracy against pre-defined test queries.

## Expected Files
- Conversion scripts (Word/PDF to Markdown)
- System prompts for SOP search queries
- Pilot SOP test results

## Dependencies
- Upstream: Desensitization Script, Acceptance Test Suite, AI Use Policy
- Downstream: ALL Phase 1-3 applications (every app depends on this)
