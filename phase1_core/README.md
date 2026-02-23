# Phase 1: Core Applications (Quick Wins)

**Timeline:** Week 3-8 | 2026-03-09 to 2026-04-19
**Scope:** 3 applications, all run in parallel
**Status:** Pending (requires Phase 0 completion)

Same search engine, different prompts. These are essentially free once SOP Content Search works.
Management demo: CC Impact (Basic) -- show it working on a real change control.

## Contents

### `cc_impact_basic/`
**App #2: CC Impact Assessment (Basic)** | 1-2 weeks | Low complexity
- "Which SOPs mention the affected equipment/process?"
- Prompt engineering on existing knowledge base
- Test with 3-5 recent CC cases
- This is the management demo

### `regulatory_gap/`
**App #3: Regulatory Gap Analysis** | 1-2 weeks | Low complexity
- Upload regulatory text (PIC/S Annex 1, etc.) alongside SOPs
- "Which SOPs don't meet the updated requirement in Section X?"
- Same engine, different query pattern

### `training/`
**App #4: New Employee Training** | 1 week | Low complexity
- Training assistant system prompt
- Answers questions, explains procedures, quizzes on SOP content
- Existing knowledge base, minimal effort

## Phase Gate Criteria
- CC Impact Basic demonstrated on 3-5 real CC cases
- Management demo completed
- All three apps tested against acceptance test suite
