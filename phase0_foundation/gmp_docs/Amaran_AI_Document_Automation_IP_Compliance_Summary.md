# Amaran AI Document Automation: IP Protection & Compliance Summary

**Date:** 2026-02-10
**Context:** Evaluating desktop vs cloud approaches for [[placeholder]] document automation while maintaining customer IP protection and Information Sensitivity Policy compliance.

---

## 1. Architecture Decision

### The Question
Can Claude handle [[placeholder]] replacement directly on the user's desktop, avoiding cloud upload of customer data?

### The Answer
**VBA macros in Microsoft Word already solve this.** No AI needed for the replacement step.

| Component | Approach | Location |
|---|---|---|
| Template (.docx) with [[placeholders]] | Stays on desktop | Local |
| Data source (JSON/CSV) | Excel form, CSV, or OCR output | Local |
| Replacement engine | VBA macro (Find & Replace) | Local |
| QA verification | Gemini OCR + Claude audit | Cloud |

### Two Separate Pipelines

**Forward (Document Generation):** Fully local, zero cloud exposure.
> Human fills Excel → CSV/JSON → VBA replaces [[placeholders]] in Word → Done

**Backward (QA Verification):** Cloud-based, requires compliance controls.
> Scanned BPR → Gemini OCR → JSON → Claude audit → HTML report

---

## 2. IP Protection by Design

### JSON as Universal API
The [[placeholder]] schema acts as middleware. Any data source can produce a JSON file matching the schema. The VBA macro doesn't care where the data came from.

Three decoupled layers:
1. **Data extraction** — varies by source, IP decision happens here
2. **JSON** — the contract between layers, always the same structure
3. **Document generation** — always local, always VBA, always zero IP risk

### Cloud Exposure Assessment

| AI Tool | Plan Type | Trains on Data? | Data Retention | Adequate for BPR? |
|---|---|---|---|---|
| Gemini Enterprise (Workspace) | Commercial | No | Per Google CDPA | Yes, with controls |
| Claude Free/Pro/Max | Consumer | Opt-out required | 30 days (or 5 years if opted in) | Not recommended |
| Claude Team/Enterprise | Commercial | No by default | 30 days (customizable) | Yes, with controls |
| Claude API with ZDR | Commercial | No | Zero (after abuse check) | Best option |

**Recommendation:** Use Gemini Enterprise for OCR (already in place). Keep document generation local via VBA.

---

## 3. Information Sensitivity Policy Compliance

### Data Classification for BPR Content

| BPR Section | Data Examples | Classification | Upload to AI? |
|---|---|---|---|
| Cover page | Sponsor name, product name, batch number | Third Party Confidential | Requires sponsor approval |
| Page 3 (Signature log) | Employee names, initials, departments | More Sensitive (personnel) | Redact names |
| Section 2 (Equipment) | Equipment ID, model | Minimal | OK |
| Section 7 (Compounding) | Weights, temperatures | More Sensitive | OK with controls |
| Section 9 (Reconciliation) | Fill quantities, accept/reject counts | More Sensitive | OK with controls |
| Attachments (Vanrx, CCIT) | Analytical results, serial numbers | Third Party Confidential | Requires sponsor approval |

### Policy Requirements Mapped to AI Uploads (Section 3.2 / 3.3)

| Policy Requirement | Concrete Measure |
|---|---|
| Signed NDA with non-employee | Confirm Google Workspace CDPA is on file; archive a copy |
| Encrypted transmission | Gemini Enterprise uses TLS 1.2+; document in SOP |
| No training on your data | Archive Google's enterprise data governance page as evidence |
| Individual access controls | Only designated operators have Gemini access; maintain access list |
| Approved recipients only | Gemini workspace restricted to Amaran domain |

---

## 4. BPR OCR Compliance Measures

### What to Redact vs Keep

| Data on BPR Page | Gemini Needs It? | Redact? |
|---|---|---|
| Sponsor name / logo | No | Yes |
| Product name | Could use code instead | Yes if possible |
| Batch number | Yes, for matching | Keep or use internal code |
| Employee full names | No | Yes |
| Signatures / initials | Only department matters | Black out names, keep initials |
| Equipment IDs | Yes | Keep |
| Weights / temperatures | Yes | Keep |
| Reconciliation numbers | Yes | Keep |
| Analytical results | Yes | Keep |
| Deviation numbers (NOE/DEV) | Yes | Keep |

**Principle:** Redact identifiers (who and for whom). Keep process data (what happened).

### Three Redaction Approaches

**A. Manual redaction in PDF (simplest)**
- Scan BPR → PDF editor → draw black boxes over sponsor/employee names → upload
- ~5 minutes per batch. At 10 batches/year, trivial effort.

**B. Automated redaction script (scalable)**
- Python script blacks out predefined zones on each page template
- BPR template is consistent → redaction zones are the same every batch
- One-time setup, runs in seconds

**C. Selective page upload (recommended)**
- Only upload sections Gemini needs, skip the rest

| Upload These | Content | Why |
|---|---|---|
| Section 7 (Compounding) | Weights, temps | Process data only |
| Section 9 (Reconciliation) | Counts, quantities | Process data only |
| Attachment 7 (Weighing printouts) | Thermal printout numbers | Zero sensitivity |
| Attachment 8/9 (Filter integrity) | Bubble point results | Zero sensitivity |

| Skip These | Why |
|---|---|
| Cover page | Sponsor info |
| Page 3 (Signature log) | Personnel data |
| Attachment 1 (Vanrx report) | May contain sponsor-proprietary data |

**Recommendation: C + A combined** — selective upload + quick manual redaction on uploaded pages.

---

## 5. Per-Batch Compliance Workflow

### One-Time Setup
1. Classify BPR as "More Sensitive" + "Third Party Confidential" in document register
2. Add AI processing clause to sponsor Quality Agreement / CDA
3. Get sponsor sign-off (or blanket approval)
4. Create authorized user list for Gemini BPR processing
5. Archive Google's CDPA and data governance documentation

### Per Batch

| Step | Action | Record |
|---|---|---|
| 1 | Confirm operator is on authorized user list | Access log |
| 2 | Select only needed BPR sections for upload | Page list |
| 3 | Redact sponsor name, employee names on selected pages | Before/after (optional) |
| 4 | Upload to Gemini Enterprise only (not personal account) | Domain verification |
| 5 | Extract JSON output, save locally | JSON file with timestamp |
| 6 | Delete conversation in Gemini after extraction | Confirmation |
| 7 | Log the upload | AI Processing Log |

### AI Processing Log Template

| Field | Example |
|---|---|
| Date | 2026-02-10 |
| Batch | 80015-0001 |
| Operator | D. Chen |
| AI Tool | Google Gemini Enterprise (Workspace) |
| Pages Uploaded | BPR pp. 30-55 (Sections 7-9) |
| Redactions Applied | Sponsor name (cover), employee names (p.3) |
| Purpose | OCR extraction for QA verification |
| Data Deleted from AI | Yes, conversation cleared |
| JSON Saved Locally | /data/80015-0001_bpr_extract.json |

---

## 6. Key Takeaways

1. **VBA + local JSON solves the document generation problem** without any cloud exposure
2. **OCR is only needed for the QA verification pipeline** (backward direction)
3. **Gemini Enterprise is commercially safe** but requires procedural controls per Amaran's Information Sensitivity Policy
4. **Selective page upload + manual redaction** is the practical compliance approach at 10 batches/year
5. **Sponsor awareness is mandatory** — add an AI processing clause to Quality Agreements
6. **Log everything** — the AI Processing Log is your PIC/S audit defense

---

*Amaran Biopharmaceutical CDMO | Operations Excellence Initiative*
