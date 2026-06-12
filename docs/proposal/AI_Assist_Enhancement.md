# AAU IUMS — AI Assist (Optional Enhancement)

**Project:** Assam Agricultural University (AAU) — Integrated University Management System
**Document type:** Optional enhancement — applies on top of any roadmap (1, 2 or 3)
**Prepared by:** Bohniman Systems Private Limited (BSPL)
**Version:** 0.1 (Draft) · **Date:** 12 June 2026

> **Positioning.** AI assist is **optional and à-la-carte** — not required for any roadmap to go live. It layers on once the chosen option's core data exists, and AAU can pick any subset. Because AAU hosts on-premise and the data includes PAN/Aadhaar, the default stance is **AI runs on-premise; sensitive data never leaves AAU servers.**

---

## 1. Where AI helps — by module

| Module | AI use-case | AI type | Data sensitivity |
|---|---|---|---|
| **Payroll** | Anomaly / fraud detection — salary jumps, duplicate pay, wrong deduction, pre-run ceiling breach | Classic ML | Low |
| | Arrears / fixation **"why did pay change" explainer** | LLM | Med |
| **Finance / FOC / Bill** | **Reconciliation assistant** — explain payroll-to-bill / fund-to-spend mismatches | LLM + rules | Low–Med |
| | **Fund-trace summariser** — natural-language fund → head → spend trace | LLM (RAG) | Low |
| | Duplicate / fraud bill detection; budget burn-rate forecast | Classic ML | Low |
| **HRMS / Establishment** | **Document & service-book extraction** — OCR old books, certificates, appraisal forms → structured data | OCR + LLM | **High** |
| | **Service-book gap detector** — missing verification entries, leave / GPF mismatch | ML + rules | High |
| | Promotion / CAS-MACP **eligibility explainer**; fuzzy duplicate-employee match | LLM / ML | High |
| | **Self-appraisal (APAR) draft assist** + summarise for reporting officer | LLM | High |
| **ESS** | **Employee chatbot** — "my GPF balance", "how to apply leave", policy Q&A | LLM (RAG) | High |
| **Admin / Monitoring portal** | **Natural-language query over dashboards** ("pending bills > 30 days in college X"); bottleneck detection; alert prioritisation | LLM + ML | Low–Med |
| **Reporting (any module)** | **NL → report** ("who retires in next 6 months in College X" → AI builds the filter, the **list stays a deterministic query**); **report briefing/summary**; proactive succession / pension-dossier alerts | LLM + rules | Low–Med |
| **EFMS / Workflow** | SLA-breach prediction, smart file routing, movement-bottleneck analytics | ML | Low |
| **Cross-cutting** | **RAG over HR / Finance manuals** ("which rule applies"); audit / RTI natural-language query; Assamese ↔ English translation | LLM (RAG) | Med |

**Earliest ROI:** classic-ML wins (payroll anomaly, reconciliation, forecast) — no LLM, no GPU, runs on CPU on-premise. Ship these first.
**Highest migration value:** document / service-book extraction — removes manual data-entry of legacy and physical records.

---

## 2. Deployment options

### A. On-premise local model (recommended default)
Open-weight model (Llama 3.x / Qwen2.5 / Mistral) served with **Ollama or vLLM** on a GPU node.

- ✅ Data **never leaves AAU premises** — PAN/Aadhaar safe; government-compliant
- ✅ No per-call cost; no internet dependency; full control
- ❌ Needs **GPU hardware** (capex, see §4) and in-house MLOps
- ❌ Lower ceiling than frontier cloud models; slower on very large models

### B. Cloud API (Claude / GPT / Gemini)
- ✅ Strongest reasoning; zero infra; fastest to ship; scales
- ❌ **Sensitive data leaves premises** → compliance/legal blocker for citizen PII
- ❌ Recurring per-token cost; internet dependency; data-residency concerns

> For a government university, sending raw PAN/Aadhaar/service-book data to external cloud is **likely not permitted** without anonymisation and legal clearance.

### C. Hybrid + anonymise (pragmatic middle path)
- Sensitive tasks (HR, ESS, service-book, payroll PII) → **on-premise local**
- Non-sensitive / aggregated / **anonymised** tasks (dashboard NL-query, manual RAG, public-notice translation) → cloud API allowed, **PII stripped first**
- RAG: documents + vector DB stay **on-premise**; only the anonymised prompt optionally goes to cloud

---

## 3. Recommendation matrix

| Use-case | Recommended deployment |
|---|---|
| Payroll anomaly / fraud / forecast | **On-prem, classic ML** (no GPU) |
| Service-book / document extraction | **On-prem local** (PII) |
| ESS chatbot + policy RAG | **On-prem local** (8B–14B model sufficient) |
| Self-appraisal assist, eligibility explainer | **On-prem local** |
| NL dashboard query, report summarise | On-prem; cloud OK only if anonymised aggregates |
| Assamese ↔ English public notices | Local or cloud (non-PII) |

---

## 4. Hardware / infrastructure requirement

AAU provides the in-house server — but **LLM features need a GPU; classic ML does not.**

| Workload | Hardware |
|---|---|
| Classic ML (anomaly / forecast / reconciliation) | **CPU server — no extra hardware** |
| Local LLM 8B–14B (RAG, chatbot, extraction) | **1× GPU 24 GB** (e.g. RTX 4090 / A5000) |
| Local LLM ~32B | 1× GPU 48 GB (A6000) |
| Local LLM ~70B | Multi-GPU node |

> **Decision point for AAU:** a GPU node is **extra infrastructure beyond the standard application server** and must be provisioned or budgeted. All classic-ML AI features work without it. Hardware cost is AAU's (outside BSPL software scope).

**Supporting AI stack (on-prem, open-source):** Ollama / vLLM (serving), a vector DB (pgvector on the existing PostgreSQL, or Qdrant) for RAG, OCR (PaddleOCR / Tesseract) for extraction, and an **anonymisation/guardrail layer** that strips PII before any optional cloud call.

---

## 5. Data privacy & guardrails

- **PII never to external APIs** by default; on-prem for all sensitive tasks.
- **Anonymisation layer** mandatory on any cloud path — strip PAN/Aadhaar/names/account numbers first.
- **Human-in-the-loop** — AI output is advisory; pay, fixation, eligibility and bill decisions stay with maker–checker, logged in the Audit Ledger.
- **No autonomous money/HR actions** — AI explains, drafts, flags; it does not approve.
- **RAG grounding** — answers cite the source rule/record to prevent hallucinated policy.

---

## 6. Indicative effort (à-la-carte menu)

Build effort only (person-days), pre-BRD. Pick any subset; each is independent.

| AI feature | Person-days | Needs GPU? |
|---|--:|:--:|
| AI platform setup (model serving, vector DB, anonymisation/guardrails) | 12 | — / yes for LLM |
| Payroll anomaly / fraud detection (classic ML) | 12 | No |
| Reconciliation assistant | 8 | No |
| Budget / burn-rate forecast | 6 | No |
| Document & service-book extraction (OCR + LLM) | 15 | Yes |
| ESS chatbot + policy RAG | 14 | Yes |
| NL dashboard query (Admin portal) | 8 | Yes |
| Self-appraisal assist + eligibility explainer | 8 | Yes |
| Assamese ↔ English translation | 4 | Optional |
| **Full menu** | **~87** | |

> **Starter bundle (~38 pd, no GPU):** platform setup (12) + payroll anomaly (12) + reconciliation (8) + forecast (6) — the classic-ML wins that need no GPU and give the fastest ROI. This matches the indicative "AI assists" line in the *Options Overview* next-phase table; the table above breaks out the full menu so AAU can choose.

---

## 7. Requirements from client

- **Use-case selection** — which features from §6 AAU wants (drives effort and whether a GPU is needed).
- **GPU infrastructure decision** — provision a GPU node, or stay CPU-only (classic ML only).
- **Cloud-vs-on-prem policy** — confirm whether any anonymised cloud use is permitted, or strictly on-prem.
- **Source documents for RAG / extraction** — HR & Finance manuals, service-book samples, appraisal formats (already requested for Roadmaps 2/3).
- **Labelled samples** — for anomaly/fraud detection, examples of known good/bad cases to train against.
- **Legal / data-privacy sign-off** for any cloud path involving (even anonymised) data.

---

## 8. Phasing

1. **Classic-ML wins** — anomaly, reconciliation, forecast. On-prem CPU, cheap, high ROI. No GPU.
2. **RAG chatbot + document extraction** — provision GPU node, deploy local model.
3. **Optional cloud** — non-sensitive / anonymised heavy reasoning, only after legal sign-off.

---

## 9. Assumptions & exclusions

- **Optional enhancement** — not required for any roadmap go-live; delivered after core data exists.
- **Assumption:** on-premise hosting; sensitive data stays on AAU servers; AAU provisions any GPU.
- **Excludes:** GPU/hardware cost (AAU's); cloud-API subscription cost if option B/C chosen; external legal/compliance clearance.

---

*Indicative, pre-BRD. Effort is build only — day-rate, overhead and margin applied by management. Not a price or commitment.*
