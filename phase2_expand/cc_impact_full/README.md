# App #2b: CC Impact Assessment (Full Matrix)

**Phase:** 2 | **Timeline:** Week 6-12 | 2026-03-30 to 2026-05-10
**Effort:** 4-6 weeks | **Complexity:** High
**Dept:** QA / Ops / Engineering
**Dependency Map ID:** `cc_full`

## Purpose
Phase B -- Impact matrix. Build structured dependency database: equipment-SOP mappings, material-supplier-qualification links, process-validation-regulatory links, customer notification rules. Every CC initiation queries: "Which CCS controls does this change touch?" This is institutional knowledge extraction from domain experts, not coding. The bottleneck.

## Expected Files
- Dependency database/mappings (structured format)
- System prompts for full matrix queries
- Expert interview notes/knowledge capture
- Validation results against real CC cases

## Dependencies
- Upstream: CC Basic, CCS, Deviation Investigation, Validation Cross-Ref, Equipment Doc, Risk Assessment + CC Proc
- Downstream: APQR Aggregation, Customer Service Bot
