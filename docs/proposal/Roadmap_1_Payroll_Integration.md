# Roadmap 1 — Payroll Replacement + Integration Platform

**Project:** Assam Agricultural University (AAU) — Integrated University Management System
**Option:** 1 of 3 · *Fastest delivery — solve the payroll problem first*
**Prepared by:** Bohniman Systems Private Limited (BSPL)
**Version:** 0.1 (Draft) · **Date:** 12 June 2026

> **In one line:** Rebuild the existing payroll *exactly as it works today* on a modern, integrable technology stack, add a single Admin/Monitoring platform, and connect all existing in-house applications into it for unified reporting — in the shortest possible time.

**Built on:** Spring Boot + React + PostgreSQL (Spring Security app-side RBAC, Flowable workflow, RabbitMQ, JasperReports, Redis), containerised on AAU's in-house servers. Full stack in the *Options Overview*.

---

## 1. The problem this solves

AAU runs its payroll on an **outsourced .NET system** that is:
- built on **old technology**,
- **expensive** to keep running, and
- **cannot integrate** with AAU's in-house applications.

Roadmap 1 replaces only that payroll — like-for-like in function — on a new stack that **integrates cleanly**, and puts a control platform over everything AAU already has. No re-design of payroll rules, so delivery is fast and risk is contained.

---

## 2. Goal — what the University gets

When Roadmap 1 is live, AAU will be able to:

- **Run the full monthly salary cycle** on the new system — gross (pay + allowances), all deductions (IT, LIC, GIS, SSS, loans, GPF, license-fee), net per fund/budget-head, batch corrections, formula increments, arrears.
- Produce **dynamic payslips, the annual employee report, and the salary-difference/scrutiny report** — matching today's outputs.
- Generate the **treasury salary bill (PDF)** and **track it end-to-end** through the disbursement chain (Accounts → DDO → Budget → Cashier → Treasury), with a single live status per bill.
- **Stop paying the existing .NET payroll vendor** — the new payroll is owned by AAU and built to integrate.
- See **one Admin / Monitoring portal** with live dashboards, alerts, file/bill lifecycle tracking, audit views and payroll analytics.
- View **all existing in-house applications in one place** — HRMS, Recruitment, Academic, Exam, Fee Collection, Employee Portal, User Management, EFMS, Notices — surfaced read-only with reports, linked by **PAN (with email/mobile fallback)**.
- Give the HRMS team a **PAN-keyed employee verification API** to map and cleanse their records against the authoritative, PAN-complete payroll data (see onboarding note below).
- Pull **standard parameterised reports** — *employees retiring in next 6 / 12 / N months*, increment-due, probation/contract-ending lists — filtered by college/dept/cadre, exported to PDF/Excel, scheduled. *(Retirement/cadre reports depend on the legacy HRMS exposing DOB + retirement-age via API; reliable natively from Roadmap 2.)*
- Rely on **government-grade auditability** — append-only audit log, effective-dated rules, AG/CAG & RTI-ready exports.

**Explicitly *not* in Roadmap 1** (kept as-is and integrated): HRMS rebuild, FOC fund control, Finance & Accounts. These are integrated for reporting only — see Roadmaps 2 and 3 to own them natively.

> **Service-book transfer pain point — not solved in Roadmap 1.** Because HRMS stays legacy (read-only), the **faculty service book and its inter-DDO transfer** remain in the existing system — still effectively manual. This is solved from **Roadmap 2** onward, where HRMS + Establishment are native and the service book transfers as a digital custody change.

---

## 3. Scope — modules built

| Group | Module | Build state |
|---|---|---|
| **Foundation** | Masters & Rule Engine (DDO, designation, grade, fund type, budget head, payscale, formulas — effective-dated) | Build |
| | RBAC / User Management — **app-side** (one role per user, permissions, **temporary/delegated grants with expiry** = delegation-of-powers, dept/centre scoping, maker-checker; custom React login) | Build |
| | Audit Ledger | Build |
| | Notification Service | Build |
| | Workflow / File-movement rail | Build |
| **Payroll** | Payroll engine (rebuilt as-is on new stack) | Rebuild |
| | Bill Tracking (generation + disbursement-chain state machine) | Build |
| **Platform** | Admin / Monitoring Portal (dashboards, alerts, **parameterised report framework** — retirement-due / increment-due / contract-ending and similar "due in next N months" lists) | Build |
| **Integration** | Read-only connectors to all existing in-house apps + report surfacing | Integrate |

> **Access control note.** Authorization is built **app-side** (Spring Security + RBAC tables in PostgreSQL), not in Keycloak. One role per user; **temporary permissions** are time-bound grant rows (`valid_from`/`valid_to`) that auto-expire and are logged to the Audit Ledger — the digital form of *delegation of powers*. This keeps full control of the login UI and avoids Keycloak's theming limits. Keycloak is added later only if external/AD/state-SSO federation is required (authentication only).

> **Employee onboarding & identity reconciliation.** Our migrated payroll master is **PAN-complete** — taken from the existing payroll DB at deployment. The legacy HRMS is the incomplete side (some employees missing, some without PAN), and the in-house apps link by **email/mobile**, not PAN. Approach for Roadmap 1 (HRMS stays legacy, we don't change its UI):
> - **We expose a PAN-keyed employee verification / lookup API** (fallback keys: email + mobile, legacy employee-ID). The HRMS team uses it to map and cleanse their records and fill missing PANs against our authoritative payroll data.
> - **Existing employees** — matched on a key hierarchy (**PAN → legacy emp-ID → email+mobile → fuzzy name+DOB**); low-confidence matches go to an **admin match-review screen** for manual rectification.
> - **In payroll, not in HRMS** — kept in our payroll master; the HRMS team onboards them on their side via the API.
> - **New joiner** — admin creates in our payroll (PAN captured); legacy HRMS onboarding stays their process. Record is **draft, not payable until verified** (maker-checker).
> - Internal **Employee ID is the primary key**; PAN / email / mobile / legacy-IDs are alternate identifiers. "PAN-pending" applies only to HRMS-only records and blocks statutory/pension actions only — **never monthly pay** (payroll PAN is complete).

> **Input-boundary note (modules deferred to next phase).** Since Leave, Attendance and the full GPF/Loan ledgers come later, payroll is fed exactly as the old system is fed today:
> - **Leave / Attendance / LWP** — supplied to payroll as a **periodic import or manual sheet** until the live modules land.
> - **GPF / Loans** — payroll holds the **deduction line plus the minimal recovery schedule / running balance** needed to deduct (loan EMI schedule, GPF subscription). The full ledger, passbook, annual statement and advance workflow arrive in the next phase and take over balance ownership.

---

## 4. Deployment plan

Five overlapping waves over an indicative **7–9 month** window. Calendar is governed by legacy reverse-engineering, parallel run and sign-off gates — not raw coding speed.

| Wave | Months | Delivers | Exit / acceptance |
|---|---|---|---|
| **W0 — Discovery & Foundation** | M1–M2 | Reverse-engineer old .NET payroll (schema, stored procs, batch jobs, report SQL); Masters & Rule Engine, RBAC, Audit, Notification, Workflow rail | A master setting drives a sample calc; legacy salary logic catalogued |
| **W1 — Payroll core** | M2–M4 | Payroll engine (gross, deductions, net, corrections, increments, arrears, payslip, annual & scrutiny reports) | A test month computes to match a real legacy payslip |
| **W2 — Bill & external interfaces** | M3–M5 | Bill generation (treasury PDF) + Bill Tracking chain; treasury / bank / IT-TRACES interfaces | A salary bill flows Accounts→…→Treasury with live status |
| **W3 — Platform & integration** | M4–M6 | Admin/Monitoring Portal; read-only connectors to all existing in-house apps; reports/dashboards | Existing apps visible on one portal; payroll dashboards live |
| **W4 — Parallel run & go-live** | M5–M9 | Full parallel run, UAT, data cutover, training, go-live, stabilisation | A full salary cycle on the new system matches legacy within tolerance; old .NET payroll retired |

**Parallel run begins ~M5** — new and old payroll run side by side until totals agree, then cutover. This de-risks the switch.

---

## 5. Man-days required

Build effort only — excludes day-rate, leave and margin (management adds those).

### Module build

| Module | Person-days |
|---|--:|
| Masters & Rule Engine | 51 |
| RBAC / User Management | 21 |
| Audit Ledger | 16 |
| Notification Service | 11 |
| Workflow / File-movement rail | 35 |
| Payroll engine (as-is rebuild) | 73 |
| Bill Tracking (gen + chain) | 25 |
| Admin / Monitoring Portal | 40 |
| Integration connectors (all existing apps + reports) | 35 |
| Employee onboarding & identity reconciliation (PAN-verification API + match-review + admin-create) | 10 |
| **Module subtotal** | **317** |

### Programme-level

| Item | Person-days |
|---|--:|
| Project / delivery management (~12%) | 37 |
| Data migration (legacy payroll → new; opening balances; deduction/loan balances) | 30 |
| External integrations (treasury, bank/NEFT-RTGS, IT/TRACES) | 25 |
| System/integration testing + UAT + parallel run | 25 |
| Deployment, go-live, cutover | 15 |
| Training & documentation | 12 |
| **Programme subtotal** | **144** |

| | Person-days |
|---|--:|
| **Roadmap 1 total** | **~461** |

> Effort is build only — person-days, pre-BRD. Day-rate, overhead, margin and contingency (+15–25% recommended) are set by management to produce the commercial figure.

---

## 6. Requirements needed from client

Roadmap 1 is fast *only if* these are provided early. The single biggest schedule risk is delayed legacy-code handover.

### 6.1 Old payroll system — full analysis (time-critical)
Formal instruction to the **incumbent .NET vendor** to release:
- Database schema / ER diagrams
- Stored procedures and scheduled/batch jobs
- Report SQL and calculation logic
- Integration specifications

> The genuine salary rules (rounding, arrears, fixation) live in this code, not in manuals. Securing it early is essential.

### 6.2 API contracts of existing in-house apps
For every app to be integrated (HRMS, Recruitment, Academic, Exam, Fee, Employee Portal, User Management, EFMS, Notices):
- API documentation / contracts / endpoint specs, **or** read-replica / export access where no API exists
- Authentication method and data schema

### 6.3 Real samples (filled, not blank templates)
- A real payslip and a real treasury salary/pay bill
- 2–3 real calculation-formula definitions from the master
- Master-table list (DDO, designation, grade, fund type, budget head, payscale, deduction breakup)
- GIS / LIC / SSS deduction sheets; a sample loan schedule
- A sample arrear / salary-correction case

### 6.4 Decisions to confirm
- **Payscale model** — designation-wise vs pay-grade-wise (Closure §6).
- Income-tax handling — deduction-only vs full statutory compliance.
- Salary treasury-drawn vs university-drawn (depth of treasury integration).

### 6.5 People & access
- SMEs for Payroll, Accounts/DDO and IT for clarification sessions.
- A decision-making authority empowered to sign off scope.
- Secure transfer method + NDA for sensitive data (PAN/Aadhaar).

### 6.6 System scale & environment
- **Scale figures** — employee, pensioner, department and KVK/centre counts, and monthly payroll/transaction volume (sizes effort, performance and training).
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

Independent modules delivered as one or more waves **after** the Roadmap 1 go-live — none block it. Estimated build effort (person-days, indicative, pre-BRD):

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
- **GPF / Loans** figures are the **delta** over the deduction-line already built in Roadmap 1.
- **Roadmap 1 only:** Pension needs **extra HRMS-data work** (no native HRMS) — the figure may rise; it is native and cheaper from Roadmap 2.
- **AI assists** is optional / à-la-carte; the 38 pd is the no-GPU classic-ML starter bundle. Full menu (~87 pd) + deployment options in `AI_Assist_Enhancement.md`.
- Sequence into smaller waves by priority; effort is scale-dependent.

---

## 9. Risks, assumptions, exclusions

- **Risk:** incumbent-vendor handover delay is the #1 schedule risk — blocks payroll reverse-engineering.
- **Risk:** existing apps may lack clean APIs — sizing of integration depends on API maturity.
- **Risk:** effort assumes a mid-size establishment — scale figures (above) may adjust it.
- **Assumption (onboarding effort):** BSPL builds the reconciliation **tools** (PAN-verification API, match-review screen, admin-create form); the **manual data-matching and cleanup labour** — resolving low-confidence mismatches, filling missing PANs in the legacy HRMS, verifying records — is **AAU-side effort**, not in the build figures above.
- **Assumption:** hosting on AAU's in-house server/infra; legacy payroll data usable for parallel-run validation; PAN unique per employee; AAU provides data, SMEs and decision authority on time.
- **Excludes:** HRMS rebuild, FOC, Finance (integrated only — see Roadmaps 2/3); hardware, network, third-party licences; next-phase modules above.

---

*Indicative, pre-BRD. Subject to BRD confirmation and legacy-code access. Not a price or commitment.*
