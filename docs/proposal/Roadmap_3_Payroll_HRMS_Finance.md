# Roadmap 3 — Payroll + HRMS + Finance & Fund Control

**Project:** Assam Agricultural University (AAU) — Integrated University Management System
**Option:** 3 of 3 · *Close the full salary-to-treasury money loop*
**Prepared by:** Bohniman Systems Private Limited (BSPL)
**Version:** 0.1 (Draft) · **Date:** 12 June 2026

> **In one line:** Everything in Roadmap 2, plus **FOC (fund ceiling control)** and **Finance & Accounts** — so every salary rupee is traced from its fund source through the bill to the treasury, with automatic reconciliation for audit.

**Built on:** Spring Boot + React + PostgreSQL (Spring Security app-side RBAC, Flowable workflow, RabbitMQ, JasperReports, Redis), containerised on AAU's in-house servers. Full stack in the *Options Overview*.

---

## 1. What this adds over Roadmap 2

Roadmap 2 owns people and payroll; the money still depends on offline finance and manual fund control. Roadmap 3 brings the **financial backbone** in-house:

```
  Roadmap 2 scope  +  FOC (Fixation of Ceiling)  +  Finance & Accounts  +  full reconciliation
```

This is the complete administrative-financial core: fund source → ceiling → salary component → bill → treasury → ledger, all traceable end-to-end.

---

## 2. Goal — what the University gets

Everything in Roadmap 2, **plus**:

- **Fund control (FOC)** — fund-source intake (govt budget, ICAR/scheme grants, internal receipts, endowments), fund ↔ head ↔ sector and designation ↔ fund mapping, ceiling fixation, dispersal breakup, and **per-spend ceiling gating** so each fund is spent only on its sanctioned purpose.
- **Finance & Accounts** — general ledger + chart of accounts, fund accounting, accounts payable/receivable, treasury interface, postings intake (payroll, fee, store), bank reconciliation, budget tracking, financial statements.
- **End-to-end fund traceability** — the study's stated gap (tracing a fund's actual source) is closed: fund → head → spend is auditable.
- **Reconciliation by design** — **payroll-to-bill and fund-to-spend totals must agree**, producing AG/CAG and RTI audit evidence automatically.
- **The full money loop in one system** — salary computed, bill raised, ceiling checked at every hop, funds released, ledger posted, reconciled.
- **Standard report framework** (inherited from Roadmap 2) — *retiring in next 6/12/N months*, increment-due, contract-ending, appraisal-due lists — now extended with **fund/finance reports** (fund-utilisation, ceiling-breach, reconciliation statements).

---

## 3. Scope — modules built

All Roadmap 2 modules, **plus**:

| Group | Module | Build state |
|---|---|---|
| **Fund & Money** | FOC — Fixation of Ceiling (fund intake, mapping, ceiling fixation, gating) | Rebuild |
| | Finance & Accounts (GL, fund accounting, AP/AR, treasury, reconciliation, statements) | Build |

(Bill Tracking, already built in Roadmap 1, is now **gated by FOC** at each hop and **reconciled** by Finance. The native HRMS, Establishment and **digital Service Book + inter-DDO transfer** are inherited from Roadmap 2 — so the faculty service-book transfer pain point is solved here too.)

> **Employee onboarding & identity reconciliation (native, inherited from Roadmap 2).** PAN-complete payroll data seeds the native HRMS master; existing employees auto-matched (PAN → emp-ID → email+mobile → fuzzy) with admin match-review; payroll-only employees onboarded via prefilled HRMS registration; new joiners fill the HRMS form → admin approves → auto-propagates to payroll → foundation data created. All new records draft until maker-checker. Internal Employee ID = PK.

> **Input-boundary note (modules deferred to next phase).** Leave, Attendance and the full GPF/Loan ledgers remain next-phase, so **LWP/attendance is fed to payroll by periodic import/manual sheet** and **GPF/Loans run as deduction lines with minimal recovery-balance tracking** until those modules arrive. HRMS, FOC and Finance are all native here.

---

## 4. Deployment plan

Seven overlapping waves over an indicative **15–18 month** window.

| Wave | Months | Delivers | Exit / acceptance |
|---|---|---|---|
| **W0 — Discovery & Foundation** | M1–M2 | Legacy reverse-engineering (payroll + HRMS + fund flow); Masters & Rule Engine, RBAC, Audit, Notification, Workflow rail | Master setting drives a sample calc; fund flow documented |
| **W1 — HRMS rebuild** | M2–M5 | Employee master (PAN), profiles, transfer history; HRMS migration | Employee resolvable by PAN across modules |
| **W2 — Payroll core** | M4–M7 | Payroll engine, deductions, corrections, increments, arrears, payslip & reports | Test month matches a real legacy payslip |
| **W3 — Establishment & Appraisal** | M6–M9 | Transfer/promotion/fixation/increment/seniority; appraisal + self-appraisal workflow | Promotion/increment feed payroll automatically |
| **W4 — Fund & Finance** | M9–M13 | FOC rebuild; Finance & Accounts (GL, fund accounting, AP/AR, treasury, statements) | A fund's source → head → spend is traceable |
| **W5 — Bill, reconciliation, platform** | M11–M15 | Bill tracking gated by FOC; payroll-to-bill & fund-to-spend reconciliation; Admin/Monitoring Portal; integrate remaining apps | Reconciliation totals agree; dashboards live |
| **W6 — Parallel run & go-live** | M13–M18 | Full parallel run, UAT, cutover, training, go-live, stabilisation | Full salary + finance cycle on new system; legacy retired |

**Parallel run begins ~M13.** An internal "salary runnable" checkpoint at ~M9 lets payroll be parallel-tested before Finance completes — de-risking the big-bang.

---

## 5. Man-days required

### Module build

| Module | Person-days |
|---|--:|
| *Roadmap 2 module subtotal (incl. Service Book + native onboarding)* | *422* |
| FOC — Fixation of Ceiling (rebuild) | 39 |
| Finance & Accounts (full suite) | 75 |
| **Module subtotal** | **536** |

### Programme-level

| Item | Person-days |
|---|--:|
| Project / delivery management (~12%) | 55 |
| Data migration (payroll + HRMS + **fund/opening balances, ledgers**) | 42 |
| External integrations (treasury, **PFMS**, bank, IT/TRACES) | 35 |
| System/integration testing + UAT + parallel run + **reconciliation** | 35 |
| Deployment, go-live, cutover | 18 |
| Training & documentation | 14 |
| **Programme subtotal** | **199** |

| | Person-days |
|---|--:|
| **Roadmap 3 total** | **~735** |

> Effort is build only — person-days, pre-BRD. Day-rate, overhead, margin and contingency are set by management to produce the commercial figure. Contingency (+15–25% recommended) should be weighted to the low-confidence Finance/FOC modules pending fund-flow clarification.

---

## 6. Requirements needed from client

All Roadmap 2 inputs (old-payroll analysis, API contracts, samples, HR policy, appraisal rules, people), **plus** the finance inputs below.

### 6.1 Finance policy & fund-handling rules
- **Finance policy manual / accounts manual** — accounting rules, posting policy, financial year handling.
- **Delegation of financial powers** — who sanctions what, at which ceiling.
- **Chart of accounts** and **fund-accounting rules** (per fund type/head/sector).
- **Reconciliation rules** — how payroll-to-bill and fund-to-spend totals are expected to tie out.
- **Treasury drawing procedure** — treasury-drawn vs university-drawn salary; depth of treasury/PFMS integration.

> **If no Financial manual exists.** FOC ceiling rules and Finance posting/reconciliation logic can only be built against a documented finance policy. If AAU has no Financial manual / delegation-of-powers / chart-of-accounts and asks BSPL to **author it**, we must engage a **finance/government-accounting domain specialist** to draft and validate it. This adds cost and time to Roadmap 3 and is **not included** in the effort above — it is sized separately once the gap is confirmed.

### 6.2 Fund-source data (closes the study's biggest gap)
- **Complete fund-source list** (govt budget, ICAR/scheme grants, internal receipts, endowments, others).
- **One project's full funding-to-disbursal paper trail** — to model the real fund → head → spend flow.
- Fund ↔ head ↔ sector and designation ↔ fund mapping definitions.
- Ceiling-fixation and dispersal-breakup rules on receipt.

### 6.3 Integration specs
- Treasury and **PFMS** interface specifications.
- Bank (NEFT/RTGS) and IT/TRACES specs (shared with payroll).

### 6.4 People & access
- Finance / Budget / DDO SMEs in addition to HR, Payroll and IT.
- Decision authority for finance-policy sign-off.

### 6.5 System scale & environment
- **Scale figures** — employee, pensioner, department and KVK/centre counts, and monthly payroll/transaction volume.
- **In-house server & infrastructure** — AAU-provided host environment, OS/DB access and deployment credentials.

---

## 7. Support, warranty & ownership

- **Source-code ownership** — AAU owns the full source code, database schema and documentation on final acceptance. No vendor lock-in.
- **Warranty** — defect-fix warranty (indicatively 6 months) post go-live at no extra cost.
- **Support / AMC** — optional Annual Maintenance Contract after warranty; priced separately by management.
- **Knowledge transfer** — handover, source walkthrough and runbooks so AAU IT can run and extend the system.
- **Hosting** — deployed on AAU's in-house server and infrastructure; BSPL handles deployment, containerisation and configuration.

---

## 8. Modules developed after go-live (next phase)

Independent modules delivered as one or more waves **after** the Roadmap 3 go-live — none block it. Estimated build effort (person-days, indicative, pre-BRD):

| Module | Est. person-days |
|---|--:|
| ESS Portal (self-service: profile, payslip, leave, claims) | 24 |
| Attendance | 18 |
| Leave | 20 |
| GPF — full ledger | 20 |
| Loans & Advances — full lifecycle | 20 |
| Pension & Retirement | 37 |
| Asset & Estate | 25 |
| Store & Purchase | 32 |
| Deep Analytics / Warehouse | 25 |
| AI assists (optional starter bundle — see `AI_Assist_Enhancement.md`) | 38 |
| **Module subtotal** | **259** |
| **Programme-level (~20%: PM, testing, deployment, training)** | **51** |
| **Next-phase total** | **~310** |

**Notes**
- **GPF / Loans** figures are the **delta** over the deduction-line already built in Roadmap 3.
- **Pension** reuses the native HRMS service history (efficient, as in Roadmap 2).
- With **Finance live**, Store & Purchase and Asset & Estate integrate especially cleanly — AP postings and license-fee deductions already supported.
- **AI assists** is optional / à-la-carte; the 38 pd is the no-GPU classic-ML starter bundle. Full menu (~87 pd) + deployment options in `AI_Assist_Enhancement.md`.
- Sequence into smaller waves by priority; effort is scale-dependent.

---

## 9. Risks, assumptions, exclusions

- **Risk:** **fund-source tracing** is the stated study gap — FOC effort can swing on the real flow; confirming it early is essential.
- **Risk:** legacy handover (payroll + HRMS) and finance-rule clarity — combined #1 schedule risk.
- **Risk:** treasury/PFMS integration depth is variable until confirmed.
- **Risk:** effort assumes a mid-size establishment — scale figures (above) may adjust it.
- **Assumption (onboarding effort):** BSPL builds the reconciliation **tools** (match-review screen, prefilled registration + maker-checker onboarding); the **manual data-matching and cleanup labour** — resolving low-confidence mismatches, filling missing PANs, verifying records — is **AAU-side effort**, not in the build figures above.
- **Assumption:** hosting on AAU's in-house server/infra; finance policy and fund rules documented; AAU provides a real funding-to-disbursal trail; PAN unique per employee.
- **Excludes:** hardware, network, third-party licences; next-phase modules above.

---

*Indicative, pre-BRD. Subject to BRD confirmation, legacy-code access and fund-flow clarification. Not a price or commitment.*
