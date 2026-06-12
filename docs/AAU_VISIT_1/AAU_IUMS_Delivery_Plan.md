# AAU IUMS — Revised Delivery Plan (Phase 1)

**Project:** Assam Agricultural University (AAU) — Integrated University Management System
**Document type:** Delivery Plan (working draft for internal discussion)
**Prepared by:** Pallab Handique · for BSPL Management (cost-estimation input)
**Version:** 0.2 (Draft) · **Date:** 11 June 2026
**Baseline:** Visit Closure Document v1.0 + HLD (8–9 June 2026 study), refined by scope discussion
**Phase 1 delivery window:** 24 months (client-agreed)

> This is a delivery/phasing plan, not a price. It defines what we build, in what order, over the agreed 24-month Phase 1. Management applies day-rate, overhead, margin and contingency to the effort figures in §8.

---

## 1. Engagement Understanding (corrected)

AAU already runs HRMS, Payroll, Academic, EFMS, FOC and Bill Tracking. The visit documents describe how those systems work **today**. The engagement, as refined in discussion:

1. **Rebuild the Payroll system** — the central ask.
2. Payroll cannot be rebuilt in isolation: it depends on the employee master (**HRMS**), the fund/ceiling logic (**FOC**), the salary bill chain (**Bill Tracking**), and the accounting backbone (**Finance & Accounts**). These are rebuilt with it.
3. Provide an **Admin / Monitoring Portal** for unified reporting and oversight across new and legacy systems.
4. Everything that **affects an employee's salary** is delivered inside Phase 1.

**Guiding rule for Phase 1 scope:** *if it touches the salary calculation, the salary bill, or the money that pays it — it is in Phase 1.*

---

## 2. Scope Model & Principles

- **Rebuild** — we replace the existing system with our own (HRMS, Payroll, FOC).
- **Build** — module does not exist today; we create it (Bill Tracking is built fresh as it is core to payroll; Finance & Accounts, GPF, Leave, Loans, ESS, Workflow engine, etc.).
- **Integrate / Monitor** — existing system kept as-is; we read it via API and surface it on the portal (Academic; legacy non-salary EFMS files).
- **Not quoted now** — one-by-one replacement of remaining legacy systems (former "Stage 3") is **out of this offer**, noted as future scope only.

**Identity principle:** PAN is the universal key. New HRMS becomes the single source of truth for "who is an employee"; all Phase-1 modules read from it, never re-key.

---

## 3. Module Classification

| System / Module | Today | Phase-1 action | Salary link |
|---|---|---|---|
| Masters & Rule Engine | partial | **Build (Foundation)** | drives all formulas/deductions |
| RBAC / User Management | partial | **Build (Foundation)** | access to pay data |
| Audit Ledger | — | **Build (Foundation)** | audit of pay changes |
| Notification Service | — | **Build (Foundation)** | approval/alert routing |
| Workflow / File-Movement Engine | EFMS exists | **Build (Foundation, payroll-domain scope)** | carries bill/leave/GPF approvals |
| HRMS | exists | **Rebuild** | employee master, designation→payscale |
| ESS Portal (self-register + self-service) | partial | **Build (with HRMS)** | seeds employee data; leave/attendance |
| Attendance | — | **Build** | LWP reduces pay |
| Leave | — | **Build** | LWP / absence affects pay |
| Payroll | exists | **Rebuild** | the core ask |
| GPF | — | **Build** | salary deduction + advances |
| Loans & Advances | — | **Build** | salary-deduction recovery |
| Establishment (core) — transfer, promotion, pay-fixation, increment, seniority | exists (manual) | **Build (Phase 1, W2.5)** | promotion/increment change pay |
| FOC (Fixation of Ceiling) | exists | **Rebuild** | salary drawn per fund; ceiling gates bill |
| Bill Tracking | exists | **Build (fresh)** | salary bill disbursement chain |
| Finance & Accounts (full suite) | offline | **Build (full)** | salary→GL, fund accounting, reconciliation |
| Admin / Monitoring Portal | — | **Build** | reports/oversight |
| Academic (admission, counselling, payment gateway, mark entry, grade card) | exists | **Integrate / Monitor only** | none |
| Legacy EFMS (non-salary admin files) | exists | **Integrate / Monitor (optional)** | none |
| Appraisal / APAR system (8 formats, faculty) | exists | **Integrate (Phase 1) → replace later** | feeds promotion eligibility |
| Pension, Claims/TA-DA, Asset & Estate, Store & Purchase, Budget Mgmt, deep Analytics | — | **Phase 2** | no immediate salary impact |
| Establishment appraisal automation (APAR 8 formats, CAS/MACP engine) | exists | **Replace later (targeted)** | promotion eligibility |
| Replacement of remaining legacy systems | exists | **Not quoted (future)** | — |

---

## 4. Phase 1 — Full Salary + Financial Backbone (24 months)

Phase 1 delivers the complete administrative-financial core. Grouped by function:

### Foundation
- **Masters & Rule Engine** — DDO, Designation, Grade, Fund Type, Budget Head, Discipline, Nature Type, Payscale; formula engine; deduction-breakup master; **effective-dated versioning** (past runs recompute on then-rules — vital for arrears/audit).
- **RBAC / User Management** — system-wide roles, 3 access levels, 6 user types, department/centre scoping.
- **Audit Ledger** — append-only who/what/when/why; AG-CAG & RTI ready.
- **Notification Service** — event → email/in-app; reporting-officer targeting.
- **Workflow / File-Movement Engine** — reusable maker-checker + file lifecycle rail, **scoped to payroll-domain flows** (bill, leave, GPF, loan, corrections). *Not* a replacement of the university-wide EFMS.

### Identity & HR
- **HRMS (rebuild)** — employee master, PAN key, JSON quals/employment/research consumed as-is, transfer history.
- **ESS Portal** — employee self-registration **verified against legacy payroll data**; self-service profile, payslip, leave, attendance, claims requests.
- **Attendance** — capture/import + reporting-officer/biometric verification; feeds LWP.
- **Leave** — apply → approve → balance; LWP detection → Payroll.

### Payroll
- **Payroll Engine (rebuild)** — gross (pay + allowances), deduction engine (IT, LIC, GIS, SSS, loans, GPF, license-fee), net per fund/budget-head, attendance-linked pay, batch corrections, formula increments, arrears, dynamic payslip, annual report, salary-difference/scrutiny report, bill + PDF.
- **GPF** — subscription deduction, advances/withdrawals, ledger, annual statement.
- **Loans & Advances** — grant, schedule, salary-deduction recovery, closure ledger.

### Career & Establishment
- **Establishment (core) — build (W2.5)** — transfer, promotion, pay-fixation on new payscale, increment workflow, basic seniority. Feeds Payroll directly, replacing the manual master-entry stopgap.
- **Appraisal / APAR — integrate (Phase 1)** — read the **existing appraisal system** (8 formats) via API to support promotion / CAS-MACP eligibility. We consume appraisal *results*; we do not rebuild appraisal now.
- *Targeted later:* **replace** the appraisal system natively (APAR 8 formats + CAS/MACP eligibility engine) once the core is stable — strangler pattern: integrate first, swallow later.

### Fund & Money
- **FOC (rebuild)** — fund-source intake, fund↔head↔sector + designation↔fund mapping, ceiling fixation, dispersal breakup, per-spend ceiling gating.
- **Bill Tracking (build)** — disbursement chain state machine (Accounts→DDO→Budget→Cashier→Treasury), per-hop FOC check, single live status.
- **Finance & Accounts — full suite (build)** — general ledger + chart of accounts, fund accounting, accounts payable / receivable, treasury interface, fee/store posting intake, bank reconciliation, budget tracking, financial statements, payroll-to-bill & fund-to-spend reconciliation.

### Oversight
- **Admin / Monitoring Portal** — live dashboards, alerts, file/bill lifecycle tracking, audit/compliance views, payroll/fund/HR analytics, over new modules natively and legacy systems via API.

### Integrate / Monitor (existing, kept as-is)
- **Academic** — read-only via API; surfaced on portal. No salary tie.
- **Legacy EFMS (non-salary files)** — optional monitoring via API.

---

## 5. Phase 1 Delivery Schedule (24-month wave plan)

Waves overlap. Calendar is governed by sub-phase rollout, parallel runs and client sign-off gates — not raw development capacity.

| Wave | Months | Delivers | Exit / acceptance |
|---|---|---|---|
| **W0 — Foundation** | M1–M5 | BRD close, legacy data + vendor handover; Masters & Rule Engine, RBAC, Audit, Notification, Workflow engine | A master setting drives a sample calc; a file moves end-to-end with full audit log |
| **W1 — HR & Identity** | M4–M11 | HRMS rebuild, ESS self-registration (verified vs legacy payroll), Attendance, Leave | Employee resolvable by PAN across modules; self-reg → maker-checker → active; LWP feeds pay |
| **W2 — Payroll core** | M8–M15 | Payroll engine, GPF, Loans & Advances; **parallel run begins ~M13** | Parallel run matches legacy payslip + treasury bill within tolerance |
| **W2.5 — Establishment (core)** | M14–M18 | Transfer, promotion, pay-fixation, increment, seniority; **integrate existing appraisal/APAR system** (API) for eligibility | Promotion/increment flows feed Payroll automatically; appraisal data read into eligibility |
| **W3 — Fund & Finance** | M15–M21 | FOC rebuild, Bill Tracking, Finance & Accounts (full suite) | Payroll-to-bill & fund-to-spend reconciliation totals agree |
| **W4 — Oversight & Integration** | M18–M23 | Admin/Monitoring Portal; Academic + legacy-EFMS API monitoring | Unified dashboards live; legacy data visible on portal |
| **W5 — Stabilise & Go-live** | M21–M24 | Full parallel run, UAT, data cutover, training, go-live, stabilization | Full salary cycle on new system; sign-off; legacy payroll retired |

**Internal delivery checkpoint at ~M15:** "salary runnable" — payroll can be computed end-to-end and parallel-tested before Finance and Portal complete. De-risks the big-bang.

> **Schedule note:** inserting W2.5 pushes W3–W5 right by ~1 month each; overlaps absorb it but the back end (M18–M24) is tighter. W2.5 also brings the **payscale-model decision** (designation- vs grade-wise) forward to ~M14, since pay-fixation depends on it.

---

## 6. Phase 2 — Non-Existing Modules (post Phase 1, separate scope)

No immediate salary impact; deferred so Phase 1 stays focused on the salary-finance core.

- **Pension & Retirement** — computation from service history + GPF; NPS-CRA / Jeevan Pramaan / AG interfaces.
- **Claims (incl. TA/DA)** — outside the salary engine.
- **Asset & Estate** — register, allocation, quarters. *(License-fee deduction already a Phase-1 master line.)*
- **Store & Purchase** — requisition → purchase → receipt → issue (currently offline). *(Phase-1 Finance AP can post manual purchase bills meanwhile.)*
- **Budget Management** — if confirmed distinct from FOC.
- **Reports / Warehouse / Deep Analytics** — beyond the Phase-1 portal.

> **Note on Establishment:** the *core* (transfer, promotion, pay-fixation, increment, seniority) is delivered in **Phase 1 (W2.5)**, not here. Only the appraisal *automation* is deferred — and that is a **targeted replacement** (§7), not a Phase-2 build, because the existing appraisal system is integrated in Phase 1.

---

## 7. Targeted-Later & Not-Quoted Scope

**Targeted later (planned, not yet quoted):**
- **Replace the appraisal / APAR system** — build APAR 8 formats + CAS/MACP eligibility engine natively to swallow the system we integrate in Phase 1. Strangler pattern: integrate first (Phase 1), replace once core is stable.

**Not part of this offer:**
- One-by-one replacement of the remaining legacy systems (Academic, legacy EFMS, etc.) — recorded as future scope only, discussed separately if desired.

---

## 8. Indicative Effort Summary (person-days)

Build effort only — excludes day-rate, leave, margin (management adds those). Numbers are **indicative, pre-BRD**; low-confidence items depend on Closure §6 open points and legacy-code access.

### Module build

| Group | Modules | Person-days |
|---|---:|---:|
| Foundation | Masters 51, RBAC 21, Audit 16, Notify 11, Workflow engine 35 | 134 |
| Identity & HR | HRMS 45, ESS 30, Attendance 18, Leave 20 | 113 |
| Payroll | Payroll 73, GPF 25, Loans 25 | 123 |
| Career & Establishment | Establishment core 20, Appraisal/APAR integration connector 8 | 28 |
| Fund & Money | FOC 39, Bill Tracking 25, Finance (full) 95 | 159 |
| Oversight | Admin/Monitoring Portal | 40 |
| Legacy integration | Academic + EFMS API connectors | 20 |
| **Module subtotal** | | **617** |

### Program-level

| Item | Person-days |
|---|---:|
| Project / delivery management (~12%) | 80 |
| Data migration (legacy payroll → HRMS, opening balances, GPF/loan/fund balances, history) | 40 |
| External integrations (treasury, PFMS, banks, NPS-CRA, IT/TRACES, payment gateway) | 45 |
| System/integration testing + UAT + parallel run | 35 |
| Deployment, go-live, wave cutovers | 25 |
| Training & documentation | 20 |
| **Program subtotal** | **245** |

| | Person-days |
|---|---:|
| **Phase 1 indicative total** | **862** |

> **For management:** apply day-rate, overhead and margin. Recommend a contingency band of **+15% to +25%**, weighted to low-confidence rebuilds (Masters/Rule engine, Payroll, FOC, Finance). These are lower-bound build figures; the 24-month calendar absorbs parallel runs, government sign-off cycles and stabilization.

---

## 9. Integration Approach

- **New ↔ new:** internal APIs + shared masters; no duplicated employee/fund masters.
- **New ↔ legacy (monitor):** read-only API connectors to Academic and legacy EFMS; data surfaced on the portal. Where a clean API is absent, fallback is read-replica / export — **API maturity is an open point** (Closure §6.5) that sizes this work.
- **New Establishment → existing appraisal (consume):** Phase-1 Establishment reads appraisal/APAR *results* via API to drive promotion / CAS-MACP eligibility. Two-way write deferred to the later appraisal-replacement (§7). Connector effort depends on the appraisal system's API maturity.
- **New Payroll → legacy disbursement:** not required — Bill Tracking is built in Phase 1, so the salary bill flows inside our system.
- **Reconciliation by design:** payroll-to-bill and fund-to-spend totals must agree, giving audit evidence automatically.

---

## 10. Data Migration & ESS Self-Registration

- **Self-registration as migration:** employees self-register through ESS; each record is **validated against the legacy payroll master** (PAN / employee-ID match). This seeds clean HRMS data and performs de-duplication and cleansing as a by-product.
- **Maker-checker activation:** a self-registered record is **not payable** until Establishment/admin verifies and activates it. Identity proofing is mandatory because the record drives money.
- **Opening balances vs history:** live system starts from opening balances (current pay, leave, GPF/loan, fund balances); full history (service, increments, ledgers, multi-year financials) loads to archive/warehouse for arrears, audit and future pension.

---

## 11. Key Design Guardrails

1. **Workflow engine ≠ EFMS replacement.** Build the payroll-domain workflow rail only; the university-wide EFMS stays. Prevents silent scope creep into all administrative files.
2. **ESS maker-checker.** Self-registration never creates a payable employee directly.
3. **Attendance proofing.** Pay-affecting attendance is reporting-officer-approved or biometric/department-fed — never self-certified.
4. **Finance suite scope.** "Full" = GL, AP/AR, fund accounting, treasury, postings, reconciliation, financial statements. Module-level store/asset *operations* remain Phase 2; Finance posts their bills meanwhile.
5. **Effective-dated masters.** Mandatory so arrears and audits recompute on the rules that applied then.

---

## 12. Dependencies & Sequencing

- Foundation (Masters, Workflow, RBAC, Audit) gates everything.
- HRMS + ESS precede Payroll (employee data).
- Leave / Attendance / GPF / Loans precede or run with Payroll (deduction & LWP inputs).
- Establishment (core) follows Payroll (needs payscale model) and feeds it back (promotion/pay-fixation); integrates the existing appraisal system for eligibility.
- FOC precedes Bill Tracking (ceiling gating) and feeds Finance.
- Finance & Bill Tracking close the money loop after Payroll.
- Portal comes after the modules it monitors exist.

---

## 13. Risks, Assumptions & Exclusions

**Risks (effort/schedule):**
- Incumbent-vendor handover (DB schema, stored procs, batch jobs) is the #1 schedule risk — real salary/fixation/arrears logic lives in legacy code, not manuals (Closure §7.2). Delay blocks Payroll/Finance/FOC.
- Payscale model unresolved — Closure says pay-grade-wise, HLD says designation-wise. Reshapes Masters + Payroll.
- Legacy API maturity unknown — sizes monitoring & migration effort.
- Fund-source tracing is the stated study gap — FOC rebuild depends on confirming the real flow.

**Assumptions (Closure §5):** legacy payroll data usable for self-reg validation; PAN unique per employee; AAU provides data, SMEs, decision authority and legacy-code access on time.

**Exclusions:** Phase-2 modules above; replacement of remaining legacy systems; hardware, network/connectivity, third-party licences.

---

## 14. Open Points to Confirm

1. Payscale model — designation-wise vs pay-grade-wise.
2. Complete fund-source list and one project's funding-to-disbursal trail.
3. Salary treasury-drawn vs university-drawn (depth of treasury integration).
4. Legacy API maturity for Academic / EFMS monitoring.
5. Attendance source — biometric, departmental, or ESS-with-approval.
6. Budget Management distinct from FOC, or same scope.
7. Scope of income-tax handling — deduction-only vs full statutory compliance.
8. Appraisal/APAR system — API maturity for Phase-1 integration, and the 8-format scope for the later native replacement.

---

## 15. Next Steps

1. Internal review of this plan; adjust phasing/scope as needed.
2. Management applies rate, overhead, margin, contingency → format cost estimate.
3. Collect Closure §7 inputs; issue formal vendor-handover instruction (time-critical).
4. Close §14 open points in SME workshops; lock scope into the BRD.

---

*Working draft for discussion. Effort and phasing are indicative, subject to BRD confirmation and legacy-code access. Not a price or commitment.*
