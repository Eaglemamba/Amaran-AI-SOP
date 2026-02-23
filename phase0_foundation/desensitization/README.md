# Desensitization Script + QA Validation

**Phase:** 0 | **Timeline:** Week 1-2 | 2026-02-23 to 2026-03-08
**Effort:** 3-5 days | **Complexity:** Low
**Dept:** Operations + QA
**Dependency Map ID:** `desensitize`

## Purpose
Python script to strip client names, product codes, batch numbers, and pricing from SOPs before upload to any LLM. QA verifies zero leakage. Hard blocker for any SOP upload.

## Expected Files
- `amaran_redact.py` -- Main redaction script
- `redaction_config.json` -- Configurable redaction rules
- Validation SOP or checklist for QA sign-off

## Dependencies
- Upstream: None (root node)
- Downstream: SOP Content Search (hard blocker)
