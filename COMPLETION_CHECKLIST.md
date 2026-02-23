# Completion Checklist

**Project:** AI SOP Knowledge Retrieval -- Amaran Biopharmaceutical CDMO
**Last Updated:** 2026-02-24
**Legend:** [x] = Done | [ ] = Not started

---

## Strategy & Planning Deliverables

- [x] Implementation Roadmap v2 (tabbed HTML, 16 apps + 6 infra) -- `deliverables/AI_SOP_Implementation_Roadmap_v2.html`
- [x] Application Dependency Map (22-node interactive SVG) -- `deliverables/AI_SOP_Application_Dependency_Map.html`
- [x] Strategic Brief Presentation (PPTX + PDF, fonts embedded) -- `deliverables/AI_SOP_Knowledge_Retrieval_Strategic_Brief.pptx`
- [x] Markdown-in-AI-Era Guide (bilingual HTML) -- `deliverables/markdown_ai_guide_20250213.html`
- [x] Markdown-DMS-RAG Architecture Doc -- `deliverables/markdown_dms_rag_architecture_20250213.html`
- [x] Dependency Map Master Prompt (reusable template) -- `deliverables/Dependency_Map_Master_Prompt.md`
- [x] Amaran PPTX SKILL.md (python-pptx generation skill) -- `deliverables/amaran_presentation_SKILL_v2.md`
- [x] CLAUDE.md project instructions -- `CLAUDE.md`
- [x] Repo README with handoff context -- `README.md`
- [x] Directory structure with scoped READMEs -- all `*/README.md` files

---

## Phase 0: Foundation Infrastructure (Week 1-4)

### App #1: SOP Content Search
- [x] SOP-to-Markdown conversion script -- `deliverables/sop_to_markdown.py`
- [ ] Convert 5-10 pilot SOPs to Markdown -- output to `sops_markdown/`
- [ ] Upload pilot SOPs to Gemini context window and test queries
- [ ] Validate citation accuracy (target: >80% on test suite)

### Infrastructure: Desensitization Script
- [x] Basic redaction rules in sop_to_markdown.py (`REDACT_RULES`, `desensitize()`)
- [x] Dedicated desensitization script with full rule set -- `phase0_foundation/desensitization/amaran_redact.py` + `redaction_config.json` (GUI + CLI, 4 doc types, zone-based PDF redaction)
- [ ] QA validation checklist (zero-leakage verification)

### Evaluation: Acceptance Test Suite
- [ ] Define 10-15 test queries with known correct answers -- `phase0_foundation/acceptance_tests/`
- [ ] RAG Triad metrics framework (context relevance, groundedness, answer relevance)
- [ ] Baseline scoring run on pilot SOPs

### GMP: System Inventory + AI Use Policy
- [ ] Add AI search tool to computerized system inventory -- `phase0_foundation/gmp_docs/`
- [ ] 1-page AI Use Policy (acceptable use, human oversight, data protection)

### Phase 0 Gate
- [ ] SOP Content Search accuracy >80%
- [ ] Zero data leakage confirmed by QA
- [ ] System Inventory + AI Use Policy approved

---

## Phase 1: Core Applications / Quick Wins (Week 3-8)

### App #2: CC Impact Assessment (Basic)
- [ ] System prompt for "which SOPs mention affected equipment/process" -- `phase1_core/cc_impact_basic/`
- [ ] Test with 3-5 recent change control cases
- [ ] Management demo completed

### App #3: Regulatory Gap Analysis
- [ ] Ingest regulatory text (PIC/S Annex 1, etc.) as Markdown
- [ ] System prompt for gap identification -- `phase1_core/regulatory_gap/`
- [ ] Test with real regulatory update scenario

### App #4: New Employee Training
- [ ] Training assistant system prompt -- `phase1_core/training/`
- [ ] Example Q&A pairs and quiz questions
- [ ] Test with a new hire scenario

### Phase 1 Gate
- [ ] CC Impact Basic demonstrated on 3-5 real CC cases
- [ ] Management demo completed
- [ ] All three apps tested against acceptance test suite

---

## Phase 2: Expand Knowledge Base + Specialize (Week 6-16)

### App #2b: CC Impact Assessment (Full Matrix)
- [ ] Equipment-SOP dependency mappings -- `phase2_expand/cc_impact_full/`
- [ ] Material-supplier-qualification links
- [ ] Process-validation-regulatory links
- [ ] Customer notification rules
- [ ] Domain expert knowledge extraction sessions

### App #5: Equipment Document Search
- [ ] Expand Markdown pipeline for equipment-specific formats -- `phase2_expand/equipment_doc/`
- [ ] Ingest equipment manuals, IQ/OQ/PQ protocols, maintenance SOPs

### App #6: Deviation Investigation Reference
- [ ] Desensitize deviation/CAPA records -- `phase2_expand/deviation_investigation/`
- [ ] "Show similar deviations and root causes" query interface

### App #7: Validation Cross-Reference
- [ ] Ingest validation protocols and reports -- `phase2_expand/validation_xref/`
- [ ] "Which validation protocols reference this equipment SOP?" queries

### App #8: Customer Audit Preparation
- [ ] Combined query across SOP + validation + training + gap analysis -- `phase2_expand/audit_prep/`
- [ ] "What is our compliance status for [audit topic]?" prompt

### App #9: BD Client Technical Q&A
- [ ] Restricted knowledge base with extra desensitization -- `phase2_expand/bd_client_qa/`
- [ ] Safe prompt templates for externally-shared answers

### App #12: Contamination Control Strategy (CCS)
- [ ] Cross-reference cleaning/EM/gowning SOPs against PIC/S Annex 1 -- `phase2_expand/contamination_control/`
- [ ] Contamination risk-control gap mapping
- [ ] CCS as upstream input to CC Impact assessments

### GMP: Risk Assessment + Change Control Scope
- [ ] Simple risk assessment document -- `phase2_expand/gmp_docs/`
- [ ] Change control tiers (minor/moderate/major)

### Phase 2 Gate
- [ ] Equipment and deviation docs ingested and searchable
- [ ] CCS gap mapping complete for PIC/S Annex 1
- [ ] Risk Assessment approved by QA
- [ ] Full CC Impact Matrix validated with domain experts

---

## Phase 3: Scale, Integrate & Aggregate (Week 14-22)

### App #10: Tech Transfer Knowledge Base
- [ ] Consolidate validation + training + process SOPs -- `phase3_scale/tech_transfer/`
- [ ] Structured output for client onboarding queries

### App #11: APQR Data Aggregation
- [ ] Deviation trends + CC history + audit findings -- `phase3_scale/apqr_aggregation/`
- [ ] APQR summary report templates

### App #13: Deviation Report Generation
- [x] [[Placeholder]] replacement engine (VBA macro) -- `phase3_scale/deviation_report_gen/AmaranPlaceholderReplace_DoubleBracket.bas`
- [x] BPR report generator (QA Compliance Audit + Page Reconciliation from JSON) -- `phase3_scale/deviation_report_gen/amaran_report_generator_v1_3.py`
- [ ] Deviation report .docx template with [[placeholders]] -- `templates/`
- [ ] Human review workflow

### App #14: Meeting Minutes Search
- [ ] Standardized minute-taking format defined -- `phase3_scale/meeting_minutes/`
- [ ] Meeting minutes ingestion pipeline

### Architecture Decision Gate
- [ ] Evaluate: >500 docs? Multi-user? Accuracy degrading? -- `phase3_scale/architecture_gate/`
- [ ] Decision: stay Markdown+LLM or migrate to vector DB

### GMP: Validation Summary + Periodic Review
- [ ] Testing results summary -- `phase3_scale/gmp_docs/`
- [ ] Quarterly review process (accuracy, incidents, feedback)
- [ ] Supplier assessment for API providers (Anthropic, Google)

### Phase 3 Gate
- [ ] [[Placeholder]] methodology validated on deviation reports (VBA macro + report generator ready; pending .docx template + end-to-end test)
- [ ] Architecture Decision Gate assessment completed
- [ ] APQR aggregation functional with real data
- [ ] Validation Summary approved by QA

---

## Future: Separate Evaluation (Month 6+)

### App #16: Customer Service Bot
- [ ] IT security review -- `future/customer_service_bot/`
- [ ] Legal approval
- [ ] Separate infrastructure design
- [ ] Formal governance (possibly full GAMP)

---

## Cross-Cutting / Shared

### Governance
- [x] IP and compliance summaries -- `phase0_foundation/gmp_docs/Amaran_AI_Document_Automation_IP_Compliance_Summary.md`
- [ ] Data protection policies
- [ ] Vendor/supplier assessments

### Tools
- [ ] Shared conversion utilities -- `tools/`
- [ ] Common helper scripts

### Templates
- [ ] Deviation report template with [[placeholders]] -- `templates/`
- [ ] CAPA template
- [ ] Other GMP document templates

---

## Summary

| Category | Done | Total | % |
|----------|------|-------|---|
| Strategy & Planning | 10 | 10 | 100% |
| Phase 0 -- Foundation | 3 | 11 | 27% |
| Phase 1 -- Quick Wins | 0 | 10 | 0% |
| Phase 2 -- Expand | 0 | 16 | 0% |
| Phase 3 -- Scale | 2 | 13 | 15% |
| Future | 0 | 4 | 0% |
| Cross-Cutting | 1 | 6 | 17% |
| **Total** | **16** | **70** | **23%** |

**Next priorities:**
1. ~~Build dedicated desensitization script~~ -- DONE (`amaran_redact.py`)
2. Convert 5-10 pilot SOPs to Markdown
3. Define 10-15 acceptance test queries
4. Draft 1-page AI Use Policy
5. Test SOP Content Search accuracy in Gemini
6. Create deviation report .docx template with [[placeholders]]
