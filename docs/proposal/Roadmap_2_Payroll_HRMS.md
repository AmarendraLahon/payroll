# Roadmap 2 — Payroll + Native HRMS + Admin Platform

**Project:** Assam Agricultural University (AAU) — Integrated University Management System
**Option:** 2 of 3 · *Own your people data, not just payroll*
**Prepared by:** Bohniman Systems Private Limited (BSPL)
**Version:** 0.1 (Draft) · **Date:** 12 June 2026

> **In one line:** Everything in Roadmap 1, plus a **natively rebuilt HRMS** — employee master, establishment (transfer/promotion/pay-fixation/increment) and appraisal — so AAU owns its people data end-to-end and feeds payroll directly.

**Built on:** Spring Boot + React + PostgreSQL (Spring Security app-side RBAC, Flowable workflow, RabbitMQ, JasperReports, Redis), containerised on AAU's in-house servers. Full stack in the *Options Overview*.

---

## 1. What this adds over Roadmap 1

Roadmap 1 integrates the existing HRMS read-only. Roadmap 2 **rebuilds HRMS natively** on the new stack and makes it the single source of truth for "who is an employee". That removes dependence on the legacy HRMS, brings establishment workflows online, and lets promotions/increments feed payroll automatically instead of being keyed in by hand.

```
  Roadmap 1 scope  +  HRMS (rebuild)  +  Establishment  +  Appraisal integration
```

---

## 2. Goal — what the University gets

Everything in Roadmap 1, **plus**:

- A **native HRMS** — employee master keyed on PAN, qualifications/employment/research consumed as-is, transfer history, the single source of truth all modules read from.
- **Establishment workflows online** — transfer, promotion, pay-fixation on the new payscale, increment workflow, basic seniority — feeding payroll **automatically** (no manual re-entry).
- **Appraisal integration** — the existing 8 appraisal formats and a **self-appraisal (APAR) workflow** drive promotion / CAS-MACP eligibility.
- **Retirement auto-listing** — employees due for retirement (age varies by cadre) are surfaced automatically.
- **Standard report framework** — *employees retiring in next 6 / 12 / N months*, increment-due, probation/contract-ending, appraisal-due lists — parameterised by college/dept/cadre, scheduled, exportable. Native HRMS owns DOB + cadre rules, so these are **exact** (no dependency on legacy systems).
- **Digital Service Book + one-click transfer** — each employee's complete service history (postings, promotions, fixations, increments, leave, GPF, verification entries) is a live record. When faculty transfer between AAU's colleges / KVKs / DDOs, the **whole service book moves as a custody change** — no physical book, no re-keying, balances preserved. *(This solves the client's stated transfer pain point.)*
- **One identity across HR and payroll** — PAN-based de-duplication; a promotion changes pay with a full audit trail.

**Still integrated read-only (not rebuilt here):** FOC fund control and Finance & Accounts — see Roadmap 3 to own these.

---

## 3. Scope — modules built

All Roadmap 1 modules, **plus**:

| Group | Module | Build state |
|---|---|---|
| **Identity & HR** | HRMS (employee master, PAN key, JSON profiles, transfer history) | Rebuild |
| **Career** | Establishment (transfer, promotion, pay-fixation, increment, seniority) | Build |
| | **Service Book** — complete service-history record + **inter-DDO service-book transfer** | Build |
| | Appraisal — 8 formats + self-appraisal (APAR) workflow, CAS/MACP eligibility feed | Build |

> **Employee onboarding & identity reconciliation (native).** With HRMS native, the **PAN-complete payroll data (from the legacy payroll DB) seeds the HRMS employee master directly** — no external verification API needed.
> - **Existing employees** — auto-matched on the key hierarchy (PAN → legacy emp-ID → email+mobile → fuzzy name+DOB); low-confidence → **admin match-review**.
> - **In payroll, not in HRMS** — **HRMS registration form prefilled from payroll data → HRMS admin verifies → onboarded**.
> - **New joiner** — fills the HRMS form (no autofill, no prior data) → HRMS admin verifies/approves → record **auto-propagates to payroll** → the respective user creates foundation data (payscale mapping, etc.).
> - Every new / auto-created record is **draft, not payable until maker-checker approval**. Internal **Employee ID is the primary key**; PAN mandatory at onboarding; email/mobile retained to bridge the legacy in-house apps.

> **Input-boundary note (modules deferred to next phase).** Leave, Attendance and the full GPF/Loan ledgers still come later, so — as in Roadmap 1 — **LWP/attendance is fed to payroll by periodic import/manual sheet**, and **GPF/Loans run as deduction lines with minimal recovery-balance tracking** until the full ledger modules arrive. (HRMS itself is now native, so employee data is no longer a manual feed.)

---

## 4. Deployment plan

Six overlapping waves over an indicative **11–13 month** window.

| Wave | Months | Delivers | Exit / acceptance |
|---|---|---|---|
| **W0 — Discovery & Foundation** | M1–M2 | Legacy reverse-engineering (payroll + HRMS); Masters & Rule Engine, RBAC, Audit, Notification, Workflow rail | Master setting drives a sample calc; legacy logic catalogued |
| **W1 — HRMS rebuild** | M2–M5 | Employee master (PAN), JSON profiles, transfer history; HRMS data migration | Every employee resolvable by PAN across modules |
| **W2 — Payroll core** | M4–M7 | Payroll engine, deductions, corrections, increments, arrears, payslip & reports | Test month matches a real legacy payslip |
| **W3 — Establishment & Appraisal** | M6–M9 | Transfer/promotion/pay-fixation/increment/seniority; appraisal + self-appraisal workflow, eligibility feed | Promotion/increment flows feed payroll automatically |
| **W4 — Bill, platform & integration** | M7–M10 | Bill generation + tracking; treasury/bank/IT interfaces; Admin/Monitoring Portal; integrate remaining existing apps | Salary bill flows to treasury; existing apps on one portal |
| **W5 — Parallel run & go-live** | M9–M13 | Full parallel run, UAT, cutover, training, go-live, stabilisation | Full salary cycle matches legacy; old payroll + HRMS dependence retired |

**Parallel run begins ~M9.**

---

## 5. Man-days required

### Module build

| Module | Person-days |
|---|--:|
| *Roadmap 1 module subtotal (incl. onboarding/reconciliation)* | *317* |
| HRMS (rebuild) — incl. **native registration + maker-checker onboarding** | 50 |
| Establishment (transfer, promotion, fixation, increment, seniority) + **Service Book & inter-DDO transfer** | 40 |
| Appraisal (8 formats + self-appraisal workflow) | 15 |
| **Module subtotal** | **422** |

### Programme-level

| Item | Person-days |
|---|--:|
| Project / delivery management (~12%) | 45 |
| Data migration (payroll + **HRMS master & history**; opening balances) | 42 |
| External integrations (treasury, bank, IT/TRACES) | 25 |
| System/integration testing + UAT + parallel run | 30 |
| Deployment, go-live, cutover | 15 |
| Training & documentation | 12 |
| **Programme subtotal** | **169** |

| | Person-days |
|---|--:|
| **Roadmap 2 total** | **~591** |

> Effort is build only — person-days, pre-BRD. Day-rate, overhead, margin and contingency (+15–25% recommended) are set by management to produce the commercial figure.

---

## 6. Requirements needed from client

All Roadmap 1 inputs (§6 there: old-payroll analysis, API contracts, samples, decisions, people), **plus** the HR inputs below.

### 6.1 HR policy & service rules
- **HR policy manual / service rules** — recruitment, confirmation, seniority, cadre structure.
- **Transfer & posting policy** — who can be transferred where, approval chain.
- **Promotion & pay-fixation rules** — including **CAS / MACP** eligibility criteria and the pay-fixation method on the new payscale.
- **Designation → payscale mapping rules** (resolves the designation-vs-grade open point).
- **Retirement-age rules by cadre/designation.**

> **If no HR manual exists.** Establishment and appraisal workflows can only be built against documented rules. If AAU has no consolidated HR policy / service rules / appraisal rubric and asks BSPL to **author it**, we must engage an **HR domain specialist** to draft and validate the policy. This adds cost and time to Roadmap 2 and is **not included** in the effort above — it is sized separately once the gap is confirmed.

### 6.2 Appraisal / self-appraisal (suggested set)
Since AAU's appraisal drives promotion eligibility, we need the rules to build the workflow:
- The **8 existing appraisal formats** (filled examples).
- **Self-appraisal (APAR) rules** — who self-appraises, the reporting/reviewing-officer chain, scoring/grading rubric, and the cycle (annual, mid-year).
- **Eligibility logic** — how appraisal scores + service translate to CAS/MACP/promotion eligibility.
- Any **API to the existing appraisal system**, if it is to be consumed rather than fully rebuilt.

### 6.3 HRMS data
- **JSON schema dumps** (qualification, employment, research profiles).
- Department ↔ faculty shared-ID mapping and transfer-history extract.
- Employee master extract for migration + PAN de-duplication.
- **Service Book** — existing format/fields, the **service-verification rules** (who attests, how often), and the **inter-DDO transfer procedure** (who hands over, who accepts). The service book is the pension foundation, so completeness of the migrated history matters.

### 6.4 People & access
- HR SMEs and Establishment SMEs in addition to Payroll/Accounts/IT.
- Decision authority for HR-policy sign-off.

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

Independent modules delivered as one or more waves **after** the Roadmap 2 go-live — none block it. Estimated build effort (person-days, indicative, pre-BRD):

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
- **GPF / Loans** figures are the **delta** over the deduction-line already built in Roadmap 2.
- **Pension** is most efficient here — it reuses the **native HRMS service history** built in this roadmap (no extra HRMS-data work, unlike Roadmap 1).
- **AI assists** is optional / à-la-carte; the 38 pd is the no-GPU classic-ML starter bundle. Full menu (~87 pd) + deployment options in `AI_Assist_Enhancement.md`.
- Sequence into smaller waves by priority; effort is scale-dependent.

---

## 9. Risks, assumptions, exclusions

- **Risk:** legacy handover (payroll **and** HRMS) — #1 schedule risk.
- **Risk:** appraisal scope — the 8 formats can vary in complexity; eligibility rules must be confirmed before build.
- **Risk:** HRMS data quality — migration and de-duplication effort depends on it.
- **Risk:** effort assumes a mid-size establishment — scale figures (above) may adjust it.
- **Assumption (onboarding effort):** BSPL builds the reconciliation **tools** (match-review screen, prefilled registration + maker-checker onboarding); the **manual data-matching and cleanup labour** — resolving low-confidence mismatches, filling missing PANs, verifying records — is **AAU-side effort**, not in the build figures above.
- **Assumption:** hosting on AAU's in-house server/infra; HR policy and appraisal rules documented and available; PAN unique per employee.
- **Excludes:** FOC and Finance (integrated only — see Roadmap 3); hardware, network, third-party licences; next-phase modules.

---

*Indicative, pre-BRD. Subject to BRD confirmation and legacy-code access. Not a price or commitment.*
