# Assam Agricultural University ERP — Clarifications Required (Next Visit)

> **Purpose:** This is the targeted question list for the **second visit (detailed
> requirement analysis)**. It is derived directly from the **initial-study notes**
> taken during visit 1, and isolates every point that was stated as *uncertain*,
> *contradictory*, or *unscoped*. Resolving these is what converts the initial
> budget figure into a defensible BRD.
>
> **Companion docs:** full method in `Requirement Gathering & Discovery Plan v2.md`;
> domain reference in `Assam_Govt_University_Payroll_Concepts.md`. This doc does
> **not** repeat those — it lists *only the open questions* and tags each to the
> phase that will close it.
>
> **How to use:** send Sections 1–12 as **interview pre-reads** to the relevant
> SME (see owner column) before the visit. Bring the **document checklist**
> (Section 14). Record every answer in the **Decision Log** (plan v2, §0.3).

---

## Legend

* **Owner** — who can answer (best guess; confirm in Phase 0 stakeholder map).
* **Why it matters** — the effort/architecture decision the answer unblocks.
* **Phase** — where in the discovery plan v2 this gets fully worked.
* **Priority** — 🔴 blocks budget/architecture · 🟡 blocks module design · 🟢 detail.

---

## 1. Fund Source & Disbursal Tracking 🔴

> **Biggest open item.** Notes say funds are mapped (fund→head→designation) **and**
> separately admit *"gap in tracking where the actual fund is coming from"* while
> *"the organisation is managing the fund seamlessly."* Mapping may be aspirational;
> real flow may be offline. Must resolve before fixed-pricing the fund/FOC scope.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 1.1 | **Enumerate every fund source** (State grant, ICAR, sponsored research grants, internal receipts/farm-lab revenue, others). | Comptroller / Accounts | FOC + fund mapping cannot be built without the list. |
| 1.2 | For a sample employee paid from a project: **how is the actual paying fund identified today** — system field, register, or clerk knowledge? | Salary Section + Project office | Determines if fund tracking is a build or a data-entry retro-fit. |
| 1.3 | Is the master fund→head→designation mapping **actually used to disburse**, or is it reference data while disbursal is decided manually on receipt? | Comptroller | Resolves the contradiction; sizes the FOC module. |
| 1.4 | FOC: confirm *"funds spent on specific purpose"* — is there a **hard block** (cannot pay from wrong fund) or a soft report? | Finance | Hard enforcement = validation engine; soft = report only. |
| 1.5 | Can a post/employee's funding source **change** (project closure/renewal) mid-year? | Project office | Drives effective-dated funding + arrear-on-source logic. |

*Phase: 1.3 (funding-source mapping), 6 (FOC / fund management).*

---

## 2. Salary Structure Model 🔴

> Notes contradict themselves: *"designation-wise salary structure **might** exist,
> confirmation needed"* vs *"salary structures maintained **pay-grade wise**."*
> These are different data models.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 2.1 | Is salary keyed to **pay grade / pay level** (employee inherits from level) or held **per designation**? | Salary Section | Picks the core payroll data model. |
| 2.2 | Confirm whether **both** a state matrix (non-teaching) **and** UGC academic scale (teaching) are in use simultaneously. | Establishment + Finance | Two pay authorities = two grids to hold. |
| 2.3 | Is there a **Pay Authority** concept (employee→authority→grid), or is the grid attached directly? | Salary Section | Affects how revisions/versions are modelled. |

*Phase: 4.1, 4.3 (pay matrix / pay authority).*

---

## 3. Calculation Formula Engine 🔴

> Notes: formulas in master, mapped to heads in "head assign"; deductions applied
> to all employees; increments via formulas; *"formulas are also changed
> accordingly."* Powerful but the governance is unspecified.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 3.1 | **Who authors/edits formulas** — IT, or finance super-user via UI? | IT + Finance | Decides config-UI scope + RBAC. |
| 3.2 | When a formula changes mid-year, does it apply **prospectively only**, or **recompute prior months** (arrears)? | Finance | Retroactive recompute is heavy; must be scoped. |
| 3.3 | Are formulas **versioned / effective-dated**, or overwritten in place? | IT | Overwrite-in-place breaks audit + arrears. |
| 3.4 | What variables can a formula reference (basic, DA%, attendance days, grade, custom)? Provide 2–3 **real formula samples**. | Finance | Defines the expression language needed. |

*Phase: 2.2 (legacy rule reverse-engineering), 4.1, 4.4.*

---

## 4. Attendance → Salary Integration 🟡

> Notes: *"salaries adjusted based on attendance."* Source undefined. A "Leave"
> module is listed separately — unclear if live.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 4.1 | **Source of attendance data** — biometric, the Leave module, or manual entry? | HR / IT | Defines an integration point or a manual screen. |
| 4.2 | Is the **Leave module live** today, or listed-but-unused? (Same question for GPF, Asset/Estate, Store, Budget Mgmt — notes say only **HRMS** "properly used".) | IT | Live vs stub changes migration vs build for each module. |
| 4.3 | What attendance counts as **on-duty** (tour, field visit, training, exam duty) and must *not* reduce pay? | HR | Agricultural university → frequent field duty; common error source. |
| 4.4 | Proration basis for mid-month join/leave — calendar days or working days? | Salary Section | Salary-engine input. |

*Phase: 3.3, 3.4 (leave/attendance), 2.1.1 (unused-features).*

---

## 5. Approval / Bill Workflow vs EFMS 🔴

> Two workflow systems described: the **payroll bill chain**
> (employee → accounts → DDO → budget → funds → cashier) **and** **EFMS**
> (6 user types, 3 access levels, full log). Unclear if they are one engine or two.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 5.1 | Is the salary-bill approval flow **the same EFMS engine**, or a separate parallel flow? | IT / Accounts | Reuse = one workflow build; separate = double. |
| 5.2 | EFMS **6 user types and 3 access levels** — list them; map to payroll roles (DDO, accounts, budget, cashier, employee). | IT | Builds the unified RBAC matrix. |
| 5.3 | At each hop, what triggers the **reporting-officer notification** (notes mention it)? | IT | Notification rules. |
| 5.4 | Is EFMS in **Phase 1 scope**, or a later integration? | Steering Committee | Scope/phasing decision. |

*Phase: 7 (workflows, RBAC, ESS).*

---

## 6. Income Tax / Statutory Scope 🟡

> Notes: *"income tax deductions done monthly."* Unclear if deduction-only or full
> compliance.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 6.1 | Tax scope = **monthly TDS deduction only**, or full compliance (**Form 16, 24Q, 12BB, 10E**)? | Finance | Compliance outputs are a large sub-scope. |
| 6.2 | Old vs new **tax regime** — does the system let employees choose? | Finance | Slab/declaration logic. |
| 6.3 | Which other statutory returns are expected in-system — **PT return, NPS upload, GPF statement**? | Finance | Each is a mandated (non-droppable) requirement. |

*Phase: 4.9 (statutory outputs).*

---

## 7. Deductions: LIC / GIS / SSS / Loans 🟡

> Notes list LIC, GIS, SSS deductions **and** *"loan facilities are provided."*
> Loan management is a mini-subsystem if full-lifecycle.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 7.1 | **Loan** = full lifecycle (sanction, amortisation schedule, interest, foreclosure, exit recovery) or just a **deduction line item**? | Finance | Large effort delta. |
| 7.2 | Can multiple loans **coexist**? Recovery priority + max-recovery cap? | Finance | Negative-net / deduction-priority rule. |
| 7.3 | LIC/GIS/SSS — fixed master amounts, slab-based, or employee-entered? | Salary Section | Deduction master design. |
| 7.4 | Confirm OPS **GPF** vs **NPS** split — which cohorts, and the NPS cut-off date for AAU. | Finance | Scheme-determination fork. |

*Phase: 4.1, 4.2, 4.8.*

---

## 8. Retirement & Pension Boundary 🟡

> Notes: *"retirement age varies"*; retirement marked in system → **forwarded to
> pension dept**. Unclear if pension is integrated or handoff-only.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 8.1 | Retirement age **varies by what** — cadre, teaching vs non-teaching, designation? | Establishment | Drives auto-flagging of retirement. |
| 8.2 | Is **pension processing** (gratuity, commutation, family pension) **in scope**, or does the system only hand off to a separate pension dept? | Comptroller | Pension is a full phase if in scope. |
| 8.3 | Terminal recoveries (outstanding loan, overpayment) settled from benefits — in scope? | Finance | Links loan + pension. |

*Phase: 5 (pension & retirement).*

---

## 9. Module Phasing — what's real vs aspirational 🔴

> 12 modules named: Asset & Estate, Employee Portal, GPF, Leave, Store & Purchase,
> Bill Tracking, Establishment, HRMS, Pension, User Management, Budget Management,
> Finance & Accounts. **Only HRMS "properly used."** Inventory is **offline today.**

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 9.1 | For **each** of the 12 modules: **live / partially used / unused / offline**? | IT | Separates migrate vs build vs Phase-2. |
| 9.2 | Which modules are **Phase 1 must-have** vs deferrable? (Recommend Phase 1 = Payroll core; defer Asset/Estate, Store/Purchase, FOC.) | Steering Committee | Locks the quoted scope. |
| 9.3 | **Inventory/Store** is offline — is it in *this* engagement at all, or explicitly excluded? | Comptroller | Exclude in writing if out. |

*Phase: 0.9 (prioritization), 2.1.1.*

---

## 10. Existing Data: JSON Profiles & Appraisals 🟡

> Notes: faculty qualification, employment history, research details held in **JSON**;
> **8 appraisal formats** exist; previous jobs in masters but "not maintained."

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 10.1 | Provide the **JSON schemas** (qualification, employment, research) — stable, or free-form? | IT | Decides migration vs reuse vs re-model. |
| 10.2 | Are the **8 appraisal formats** in payroll scope (promotion/increment input), or HR-only — ignore for payroll? | Establishment | Likely ignore for pay; confirm. |
| 10.3 | Qualification data used for **promotion** — does it feed CAS/MACP automation, or stay informational? | Establishment | Automation scope. |
| 10.4 | Confirm "previous jobs not maintained" — safe to **drop from migration**? | Establishment | Reduces migration effort. |

*Phase: 9 (migration), 3.2 (service book).*

---

## 11. Identifiers & External APIs 🟡

> Notes: **PAN + email** used as the cross-system link; *"external APIs can use PAN
> as unique identifier."*

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 11.1 | Which **external APIs** are involved (treasury, bank, NPS/CRA, govt budget portal)? What data each way? | IT / Finance | Integration scope + effort. |
| 11.2 | Is **PAN** truly unique and present for **all** employees (incl. contractual/project/guest)? Fallback key? | Establishment | PAN-as-key fails if nulls/dupes exist. |
| 11.3 | Is **email** reliably populated and unique for notifications? | IT | Notification reliability. |

*Phase: 8 (integrations).*

---

## 12. Operations: Corrections, Increments, Bills 🟡

> Notes: salary correction **in batches**; increments via formula; salary **difference
> reports** drive scrutiny; bill PDF upload → accounts.

| # | Question | Owner | Why it matters |
|---|---|---|---|
| 12.1 | **Batch salary correction** — does it recompute + regenerate bills, or adjust next month? Audit trail per correction? | Salary Section | Reprocessing + lock design. |
| 12.2 | **Difference report** — diff against what baseline (prior month, expected)? Tolerance? | Finance | Scrutiny + parallel-run validation logic. |
| 12.3 | Bill generation — is the **PDF** system-generated or manually uploaded? Format/template fixed by treasury? | Accounts | Report engine vs upload field. |
| 12.4 | Transfer/promotion *"by an entry in a form"* — does that **auto-trigger** pay re-fixation + arrears, or is it data-only? | Establishment | Fixation automation scope. |
| 12.5 | **TA/DA applied manually, not in salary** — confirm it stays **out of payroll scope** (separate claims, if any)? | Finance | Excludes TA/DA from pay engine. |

*Phase: 4.4, 4.5, 4.6, 10 (reports).*

---

## 13. Contradictions Register (resolve explicitly)

These are the **direct conflicts** in the visit-1 notes — each needs a one-line ruling in the Decision Log:

| # | Statement A | Statement B | Resolution needed |
|---|---|---|---|
| C1 | Fund source→head→designation is mapped | "Gap in tracking where actual fund comes from" | Is mapping real or aspirational? (§1) |
| C2 | Salary "designation-wise (might exist)" | Salary "maintained pay-grade wise" | One model. (§2) |
| C3 | Many modules listed as features | Only HRMS "properly used" | Live vs stub per module. (§9) |
| C4 | Formulas drive everything | Formula governance unstated | Authoring/versioning/recompute rules. (§3) |

---

## 14. Documents / Samples to Collect Next Visit

Bring back **real, filled** examples (one real sample > one interview hour):

- [ ] A real **payslip** (with all earnings + deductions populated)
- [ ] A real **salary bill / pay bill** as sent to treasury
- [ ] 2–3 real **calculation formula** definitions from master
- [ ] **Fund-source list** + one project's funding→disbursal paper trail
- [ ] **JSON schema** dumps: qualification, employment, research
- [ ] The **8 appraisal formats**
- [ ] **EFMS** role/access-level definition (6 types, 3 levels)
- [ ] Sample **loan** schedule + GIS/LIC/SSS deduction sheet
- [ ] One **arrear** / salary-correction example
- [ ] **Master-table list** (DDO, designation, grade, fund type, budget head, discipline, nature type, payscale, deduction breakup)
- [ ] Retirement-age rules (by cadre/designation)
- [ ] Module **usage status** sheet (live / partial / unused / offline) for all 12

---

## 15. Priority Summary (what to nail first)

| Rank | Topic | Section |
|---|---|---|
| 1 | Fund source & real disbursal path | §1, §13-C1 |
| 2 | Salary model (grade vs designation) | §2, §13-C2 |
| 3 | Module phasing — real vs aspirational | §9, §13-C3 |
| 4 | EFMS vs bill-workflow reuse | §5 |
| 5 | Formula engine governance | §3, §13-C4 |
| 6 | Scope boundaries: tax, loan, pension, TA/DA | §6, §7, §8, §12.5 |

> **For the budget report now:** quote **Phase 1 = Payroll core** (masters, calc,
> deductions, payslip, bill generation) at confidence; mark **EFMS, FOC/fund
> reconciliation, pension, and offline modules** as *dependent on the above
> clarifications* and price them as a range or a separate phase. State the
> assumptions in §13 explicitly so the estimate has cover.
