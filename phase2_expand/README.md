# Phase 2: Expand Knowledge Base + Specialize

**Timeline:** Week 6-16 | 2026-03-30 to 2026-06-14
**Scope:** 6 applications + 1 GMP deliverable + CCS (promoted from P3)
**Status:** Pending (requires Phase 1 completion)

Ingest new document types (equipment, deviations, validation), build specialized query interfaces,
and extract institutional knowledge. GMP Risk Assessment enables team-wide rollout.

Note: Contamination Control Strategy (CCS) was promoted to Phase 2 in the dependency map
because it serves as an upstream reference framework for every CC impact assessment.

## Contents

### `cc_impact_full/`
**App #2b: CC Impact Assessment (Full Matrix)** | 4-6 weeks | High complexity
- Structured dependency database: equipment-SOP mappings, material-supplier-qualification links
- Process-validation-regulatory links, customer notification rules
- Institutional knowledge extraction from domain experts -- this is the bottleneck

### `equipment_doc/`
**App #5: Equipment Document Search** | 2-3 weeks | Medium complexity
- Ingest equipment manuals, IQ/OQ/PQ protocols, maintenance SOPs
- Expand Markdown pipeline for equipment-specific formats

### `deviation_investigation/`
**App #6: Deviation Investigation Reference** | 2-3 weeks | Medium complexity
- Add deviation/CAPA records
- "Show similar deviations and root causes"
- Heavier desensitization (batch-specific data)

### `validation_xref/`
**App #7: Validation Cross-Reference** | 2-3 weeks | Medium complexity
- "Which validation protocols reference this equipment SOP?"
- Revalidation triggers from change controls

### `audit_prep/`
**App #8: Customer Audit Preparation** | 1-2 weeks | Low complexity
- Combine SOP + validation + training + gap analysis
- "What is our compliance status for [audit topic]?"

### `bd_client_qa/`
**App #9: BD Client Technical Q&A** | 2 weeks | Medium complexity
- BD-facing queries shared externally
- May need separate, more restricted knowledge base with extra desensitization

### `contamination_control/`
**App #12: Contamination Control Strategy (CCS)** | 3-4 weeks | Medium complexity
- Cross-reference cleaning SOPs, EM monitoring, gowning against PIC/S Annex 1 CCS requirements
- Builds contamination risk-control mapping
- UPSTREAM REFERENCE for every CC impact assessment

### `gmp_docs/`
**GMP: Risk Assessment + Change Control Scope** | 3-5 days | GMP Doc
- Simple risk assessment (human always verifies = low risk)
- CC tiers: minor (prompt tweak), moderate (new fields), major (model upgrade)
- Enables team-wide rollout in Phase 3

## Phase Gate Criteria
- Equipment and deviation docs ingested and searchable
- CCS gap mapping complete for PIC/S Annex 1
- Risk Assessment approved by QA
- Full CC Impact Matrix validated with domain experts
