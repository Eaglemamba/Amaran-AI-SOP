# Phase 0: Foundation Infrastructure

**Timeline:** Week 1-4 | 2026-02-23 to 2026-03-22
**Scope:** 1 application + 3 supporting deliverables
**Status:** Active

The critical foundation. Everything downstream depends on this phase.
If SOP Content Search accuracy is below 80%, stop and fix before proceeding.

## Contents

### `desensitization/`
**Desensitization Script + QA Validation** | 3-5 days | Low complexity
- Python script to strip client names, product codes, batch numbers, pricing from SOPs before upload
- QA verifies zero leakage
- Runs as pre-processing step before every upload
- Dependencies: None (root node)

### `sop_conversion/`
**SOP Content Search Pipeline** | 2-3 weeks + 1 week testing | Medium complexity
- SOP-to-Markdown conversion pipeline (Word/PDF to .md)
- Upload to Gemini context window / Claude Project
- Natural language query interface
- Citation accuracy validation
- Dependencies: Desensitization Script, Acceptance Tests

### `acceptance_tests/`
**Acceptance Test Suite** | 2-3 days (one-time + reuse) | Eval
- 10-15 test queries with known correct answers
- Run at each phase gate
- Metrics: context relevance, groundedness, answer relevance (RAG Triad)

### `gmp_docs/`
**System Inventory + AI Use Policy** | 2-3 days | GMP Doc
- Add AI search tool to computerized system inventory (existing format)
- 1-page AI Use Policy: acceptable use, human oversight, data protection
- Extends existing QMS -- no GAMP-specific framework needed

## Phase Gate Criteria
- SOP Content Search accuracy >80% on test suite
- Zero data leakage confirmed by QA
- System Inventory + AI Use Policy approved
