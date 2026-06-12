# AAU IUMS — Three Roadmap Options (Overview & Comparison)

**Project:** Assam Agricultural University (AAU) — Integrated University Management System (IUMS)
**Prepared by:** Bohniman Systems Private Limited (BSPL)
**For:** AAU — decision on engagement scope
**Version:** 0.1 (Draft) · **Date:** 12 June 2026
**Baseline:** Visit Closure Document v1.0 + HLD (8–9 June 2026 study)

---

## Why three options

The University's most pressing problem is its **outsourced .NET payroll system** — old technology, high recurring cost, and **unable to integrate** with AAU's in-house applications. Every option below solves that core problem first. They differ only in **how much of the surrounding administrative-financial backbone** is rebuilt natively in the same engagement.

You choose **one** option as the starting engagement. Each is a complete, go-live deliverable. The options are **progressive supersets**:

```
  Roadmap 1  ─────────────▶  Roadmap 2  ─────────────▶  Roadmap 3
  Payroll + Admin +         + HRMS (native)            + FOC + Finance
  integrate existing apps   + Establishment            + fund control
                            + Appraisal                + reconciliation
```

Whatever option you pick, the **independent modules** (ESS portal, Attendance, Leave, Asset & Estate, Store & Purchase, GPF/Loans full ledgers, Pension, Deep Analytics/Warehouse, AI assists) are delivered as a **subsequent phase** — they do not block the first go-live.

---

## How to read these documents

Each roadmap document states four things, as requested:

1. **Goal** — what the University will actually be able to do once the system is live.
2. **Deployment plan** — the delivery waves, milestones and go-live approach.
3. **Man-days required** — build effort in person-days (module + programme).
4. **Requirements from client** — exactly what AAU must provide for that scope to be built.

> **Effort, not price.** Figures are **person-days, pre-BRD** — build effort only. Day-rate, overhead, margin and contingency (+15–25% recommended on low-confidence modules) are applied by management to produce the commercial figure. Excludes hardware, network and third-party licences.

> **Policy-document dependency.** Roadmap 2 needs a documented **HR policy / service & appraisal rules**; Roadmap 3 needs a documented **Financial manual / fund-handling rules**. If these do not exist and AAU asks BSPL to **author them**, we must engage a **domain specialist** (HR or finance) to draft and validate the policy — adding cost and time, sized separately and **not included** in the effort figures above.

---

## Side-by-side comparison

| Dimension | **Roadmap 1**<br>Payroll + Integration | **Roadmap 2**<br>+ HRMS | **Roadmap 3**<br>+ Finance & Fund |
|---|---|---|---|
| **Core idea** | Replace .NET payroll on a modern, integrable stack; one admin platform over existing apps | Also own HRMS natively (employee master, establishment, appraisal) | Also own the money backbone (fund control + finance) |
| **Payroll (new stack)** | ✅ rebuilt as-is | ✅ | ✅ |
| **Bill generation + tracking** | ✅ | ✅ | ✅ |
| **Admin / Monitoring portal** | ✅ | ✅ | ✅ |
| **Integrate existing in-house apps** | ✅ (read + report) | ✅ (HRMS now native) | ✅ |
| **Employee onboarding / identity reconciliation** | PAN-verification API + match-review (HRMS team maps) | Native registration + maker-checker onboarding | Native (inherited) |
| **HRMS rebuilt natively** | — (integrated only) | ✅ | ✅ |
| **Establishment + Appraisal** | — | ✅ | ✅ |
| **Service Book + inter-DDO transfer** | — (stays legacy/manual) | ✅ | ✅ |
| **FOC (fund ceiling control)** | — | — | ✅ |
| **Finance & Accounts** | — | — | ✅ |
| **Payroll-to-bill & fund-to-spend reconciliation** | partial (bill side) | partial | ✅ full |
| **Module build (pd)** | 317 | 422 | 536 |
| **Programme (pd)** | 144 | 169 | 199 |
| **Total effort (pd)** | **~461** | **~591** | **~735** |
| **Indicative delivery** | **7–9 months** | **11–13 months** | **15–18 months** |
| **Primary new inputs needed** | Old-payroll analysis + API contracts | + HR policy & appraisal rules | + Finance policy & fund rules |

---

## Which option fits when

- **Roadmap 1** — fastest exit from the costly .NET payroll. Choose if the priority is *stop the bleeding* and unify reporting now; HRMS/Finance stay as they are and are integrated.
- **Roadmap 2** — choose if AAU also wants to **stop depending on the existing HRMS** and own employee data, establishment workflows and appraisal natively alongside payroll. **Also solves the faculty service-book transfer pain point** — the full digital service book moves between colleges/KVKs/DDOs as a custody change, no physical book, no re-keying.
- **Roadmap 3** — choose if AAU wants the **complete salary-to-treasury money loop** closed in one engagement: fund control, finance ledger, and automatic reconciliation for AG/CAG and RTI audit.

---

## Common foundation (in every option)

All three share the same reusable core, **built once and never reworked**:

- **Masters & Rule Engine** — effective-dated, formula-driven (no hard-coded salary logic).
- **RBAC / User Management** — role-based access, maker–checker.
- **Audit Ledger** — append-only, AG/CAG & RTI ready.
- **Notification Service** — event-driven alerts to reporting officers.
- **Workflow / File-movement rail** — reusable approval engine.
- **PAN = universal identity key** — no duplicated employee masters.

> **Upgrading between options is additive at the core — with one exception: HRMS.** Roadmap 1 integrates the legacy HRMS read-only; Roadmaps 2 and 3 replace it natively. So a later Roadmap 1 → 2 upgrade **swaps the HRMS read-connector for the native HRMS module** (re-migration of HR data + a fresh HR-side parallel run) — re-integration at the HRMS boundary only, not a full rebuild. Picking the target option up front avoids this.

---

## Technology stack

Built on a modern, open, integrable stack — the opposite of the closed .NET system being replaced. No recurring third-party licence cost; runs on AAU's in-house servers.

| Layer | Choice |
|---|---|
| **Backend** | Java 21 + **Spring Boot** (modular REST services) |
| **Frontend** | **React** + TypeScript (role-based portal UI) |
| **Database** | **PostgreSQL** (OLTP; effective-dated masters, append-only audit) |
| **Security / authZ** | **Spring Security** with **app-side RBAC in PostgreSQL** (one role per user, permissions, temporary/delegated grants, dept scoping, maker-checker). Custom React login UI — full branding control. *Keycloak optional, only if external SSO / Active Directory / state-govt-SSO federation is later required — and even then for authentication only, never authorization.* |
| **Workflow** | **Flowable / Camunda** engine for the EFMS file rail, maker–checker and bill chain |
| **Eventing / notifications** | **RabbitMQ** (or Kafka) event bus — activity feed + module decoupling |
| **Reporting / PDF** | **JasperReports** — payslips, treasury bills, statements (govt formats) |
| **Caching** | **Redis** (sessions, performance) |
| **Reporting / warehouse** | PostgreSQL read-replica + materialized views (dedicated OLAP in a later phase) |
| **Packaging / deploy** | **Docker** containers on AAU's in-house servers |

> Core (Spring Boot + React + PostgreSQL) confirmed by AAU. A workflow engine, an event bus, JasperReports and Redis are the recommended supporting components — all open-source and on-prem-friendly. **Authorization is built app-side** (no Keycloak by default): keeps temporary/delegated permissions and dept scoping in the app, and avoids Keycloak's login-UI theming constraints. Keycloak is held in reserve only for external/AD/state-SSO federation.

> **AI assists (next phase):** because PAN/Aadhaar data stays on AAU's in-house servers, AI features use **on-prem / open-weight models or strict anonymisation** — no sensitive data leaves the premises.

---

## Engagement terms (all options)

- **Source-code ownership** — AAU owns the full source code, database schema and documentation on final acceptance. **No vendor lock-in** — the core reason for this replacement.
- **Warranty** — defect-fix warranty (indicatively 6 months) post go-live at no extra cost; bugs in delivered scope fixed free.
- **Support / AMC** — optional Annual Maintenance Contract after warranty (tiered: defect fix, minor enhancements, helpdesk), priced separately by management.
- **Knowledge transfer** — technical + admin handover, source walkthrough and runbooks so AAU IT can operate and extend the system independently.
- **Hosting** — deployed on AAU's **in-house server and infrastructure (AAU-provided)**; BSPL provides deployment, containerisation and configuration.
- **Scale to confirm** — effort assumes a mid-size establishment; final employee/pensioner/department/KVK counts and transaction volume are a required input (below) and may adjust effort.

---

## Next phase (applies to all three options)

Delivered after the chosen option's go-live, as one or more independent waves. **Indicative effort** (person-days, build only) — sized like the roadmap modules; confirmed at the BRD for that phase.

| Module | Indicative pd | Why deferred |
|---|--:|---|
| **ESS Portal** (self-service profile, payslip, leave, claims) | 24 | Not on the salary-critical path; large UI surface |
| **Attendance** | 18 | Feeds LWP but runs from imports initially |
| **Leave** | 20 | Deduction impact handled as manual input until then |
| **GPF — full ledger** | 20 | Deduction *line* already in payroll; full ledger/passbook/statement later |
| **Loans & Advances — full** | 20 | Deduction *line* already in payroll; full lifecycle later |
| **Pension & Retirement** | 37 | No immediate salary impact; leans on HRMS service history (R2/R3) |
| **Asset & Estate** | 25 | License-fee deduction already a payroll master line |
| **Store & Purchase** | 32 | Currently offline; finance can post bills meanwhile |
| **Deep Analytics / Warehouse** | 25 | Beyond the in-build Admin/Monitoring portal |
| **AI assists** (payroll anomaly detection, document extraction, ESS chatbot, fund-trace summaries) | 38* | On-prem / open-weight models; layered on once core data exists |
| **Module subtotal** | **259** | |
| **Programme-level (~20%)** | **51** | PM, integration testing, deployment, training |
| **Next-phase indicative total** | **~310** | |

> Indicative and scale-dependent. Modules can be sequenced into smaller waves by priority. GPF/Loans figures are the **delta** over the deduction-line already built in the chosen option. Pension is most efficient on Roadmaps 2/3 (native HRMS history); on Roadmap 1 it needs extra HRMS-data work.

> \* **AI assists is an optional à-la-carte enhancement** — the 38 pd shown is the no-GPU classic-ML starter bundle. Full use-case menu, deployment options (on-prem vs cloud) and the GPU-infra decision are in **`AI_Assist_Enhancement.md`** (full menu ~87 pd).

---

*Working draft for discussion. Effort and phasing are indicative, subject to BRD confirmation and access to the incumbent vendor's legacy code. Not a price or commitment.*
