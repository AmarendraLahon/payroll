# Assam Agricultural University ERP Replacement Project

## Requirement Gathering & Discovery Plan — v2

> **Version:** 2.0  ·  **Supersedes:** v1 (`Requirement Gathering & Discovery Plan.md`)
> **Basis:** v1 plan + gap analysis against the documented domain in
> `Assam_Govt_University_Payroll_Concepts.md` and `docs/learning/01–19`.
>
> **What changed in v2 (summary):** v1 was a sound skeleton but missed whole
> scope areas that materially affect effort estimation. v2 adds: the **OPS/GPF
> and Pension** path, a **Claims & Reimbursements** module, a **Pension &
> Retirement** phase, the **revenue/receipts** side of Finance, **ESS + RBAC**
> as a first-class workstream, **effective-dated master data**, **period-lock /
> processing states**, expanded **integrations** and **non-functional
> requirements**, a deeper **data-migration** method (opening balances +
> parallel run), and discovery **governance** (stakeholders, timeline, risks,
> prioritization, success criteria). New/expanded items are tagged **[NEW]** or
> **[EXPANDED]**. A concept-to-phase coverage matrix is in Appendix A.

---

### Project Objective

Replace the existing systems currently used by Assam Agricultural University (AAU):

1. Existing HRMS (Native PHP)
2. Existing Payroll System (Third-Party Vendor)
3. Existing Finance Management Processes

Build a unified, web-based ERP platform covering:

* Human Resource Management
* Payroll Management (serving staff **and** pensioners)
* **Pension & Retirement Settlement** **[NEW]**
* **Claims & Reimbursements** **[NEW]**
* Finance & Accounting (expenditure **and** receipts) **[EXPANDED]**
* Budget, Fund & Grant Management (incl. project/grant costing) **[EXPANDED]**
* Approval Workflows + Role-Based Access Control + Employee Self-Service **[EXPANDED]**
* Reporting, Statutory Compliance & Analytics **[EXPANDED]**
* Integration with External Systems

> **AAU-specific scope note [NEW]:** AAU is an agricultural university with
> **Constituent Colleges, Regional Research Stations, Krishi Vigyan Kendras
> (KVKs), ICAR-funded schemes, sponsored research projects, and farms/labs that
> earn revenue**. The domain reference docs are currently written for a generic
> "Assam Government University"; during discovery they must be reconciled to
> AAU's reality (vacation-department teachers, ICAR pay rules where applicable,
> project-staff funded from grants, farm/lab receipts). See Appendix B.

---

# Phase 0: Discovery Governance & Approach **[NEW]**

## Goal

Run discovery as a controlled workstream with named owners, a schedule, and
sign-off — not an open-ended collection exercise. **The single most important
output of Phase 0 is not requirements — it is agreement on *who can approve
requirements*.** Once decision authority is fixed, the remaining phases run
smoother and scope disputes largely disappear.

> **Why Phase 0 matters most:** ERP projects rarely fail on technology. They
> fail because nobody owns requirements, departments give conflicting
> requirements, scope keeps changing, and no formal sign-off exists. For a
> university-scale ERP, Phase 0 is arguably more important than every technical
> phase combined.

---

### 0.1 Stakeholder Map

Identify and confirm every stakeholder group before interviews begin. For AAU:

**Executive**
* Vice Chancellor
* Registrar
* Comptroller / Finance Officer

**HR**
* Establishment Branch
* Service Book Section
* Pension Cell

**Payroll**
* Salary Section
* Bill Preparation Team
* DDO (Drawing & Disbursing Officer)

**Finance**
* Budget Section
* Accounts Section
* Internal Audit

**Technical**
* IT Cell
* **Existing software vendors — current HR vendor + current payroll vendor [important]**

**End Users**
* Faculty
* Non-teaching staff
* Retired employees / pensioners
* Contractual & project employees

> **Do not skip the incumbent vendors.** They hold the undocumented truth —
> hidden workflows, stored procedures, batch jobs, reconciliation logic. Many
> real requirements live in their code, not in any manual.
>
> **Vendor-handover guardrail:** a vendor being *replaced* has an incentive to
> withhold or mislead. They will often hand over a **database dump** but not the
> **business logic** — which is where the real complexity lives. Secure, through
> a **contract or exit clause** (not goodwill), and **before any migration
> discussion begins**:
> * ER diagrams
> * Database schemas
> * Stored procedures
> * Scheduler / batch jobs
> * Report SQL
> * Integration specifications
> * Deployment architecture
>
> Treat all vendor input as *needs-verification*.

---

### 0.1.1 System Inventory Register **[NEW]**

Before interviews begin, catalogue every existing system — feeds migration and
integration planning later.

| System | Purpose | Owner | Vendor | DB | Users |
|---|---|---|---|---|---|
| HRMS | Employee Mgmt | Establishment | Vendor A | MySQL | 250 |
| Payroll | Salary | Finance | Vendor B | SQL Server | 15 |
| Finance | Accounting | Accounts | (in-house/manual) | — | — |

---

### 0.2 RACI Matrix

Produce a **RACI matrix** for each discovery deliverable — who is Responsible,
Accountable, Consulted, Informed.

---

### 0.3 Decision Authority Matrix **[NEW — highest-value control]**

RACI says who *works on* a deliverable. The Decision Authority Matrix says who
makes the **final call** on each topic — this is what prevents "HR approves a
workflow, Finance later rejects it."

| Topic | Final Decision Maker |
|---|---|
| HR Rules | Registrar |
| Payroll Rules | Comptroller / Finance Officer |
| Budget Rules | Finance Officer |
| Accounting Rules | Accounts Department |
| Infrastructure | IT Cell |
| Project Scope | Steering Committee |

**Cross-domain decisions (joint sign-off required).** Many decisions straddle
owners and must not be decided unilaterally:

| Cross-domain topic | Joint owners |
|---|---|
| Employer-NPS 14% funding/accounting head | Payroll + Finance |
| Leave → pay reduction (half/nil pay) | HR + Payroll |
| Salary component → accounting object head mapping | Payroll + Accounts |
| Project-staff salary charged to grant fund | Payroll + Finance + Project office |

* **Escalation tiebreaker:** any unresolved or cross-domain conflict escalates to
  the **Steering Committee**.

**Decision Log (mandatory companion artifact).** The matrix says *who may
decide*; the **Decision Log** records *what was decided*. Without it, settled
decisions get re-litigated months later. Pairs with the matrix exactly as the
audit trail pairs with RBAC. Required columns:

| ID | Date | Topic | Decision | Decided By | Reason | Affected Requirements |
|---|---|---|---|---|---|---|
| DEC-014 | 12-Jul-2026 | NPS employer contribution | 14% | Finance Officer | Govt rule | PAY-024 |

---

### 0.4 Conflict-Resolution Process **[NEW]**

A named procedure, not an implied one:

```text
Department A and B disagree on a requirement
   ↓
Route to the topic's Decision Authority owner (0.3)
   ↓
If cross-domain → joint owners; if still unresolved → Steering Committee tiebreaker
   ↓
Decision recorded in the Decision Log (0.3) with rationale
   ↓
Requirement backlog item updated + re-baselined
```

---

### 0.5 Discovery Methodology

* Structured interviews + **process walkthroughs** (observe a real monthly run).
* **Document collection** — and specifically **real, filled samples** (an actual
  payslip, a real arrear bill, a real pension calculation), **not blank
  templates**. One real example surfaces more undocumented rules than an hour of
  interview.
* **Interview pre-reads** — send the question set ahead of each session so SMEs
  arrive prepared. This roughly halves cycles where SME time is the bottleneck.

Process-mapping flow (expanded):

```text
As-Is Process
   ↓
Pain Points
   ↓
Gap Analysis
   ↓
To-Be Process
   ↓
Future Enhancements   → routed to the Parking Lot (0.7), NOT the main backlog
```

Ask every department three questions — the answers become immediate wins:

1. **What takes the most time?**
2. **What causes the most errors?**
3. **What is still done manually?**

---

### 0.6 Requirement Backlog

Every requirement gets a unique ID, module, priority, and source — **no
requirement without an ID**, traceable to BRD/SRS.

| ID | Module | Requirement | Priority | Compliance | Source | Risk |
|---|---|---|---|---|---|---|
| HR-001 | HRMS | Employee Master | Must | No | Establishment | Low |
| PAY-001 | Payroll | DA Calculation | Must | No | Finance | Medium |
| PAY-014 | Payroll | NPS monthly upload | Must | **Yes (law)** | Finance | **High** |
| FIN-001 | Finance | Budget Allocation | Must | No | Accounts | Medium |

The **Risk** field flags requirements with high implementation/complexity risk
early, so estimation and sequencing account for them.

---

### 0.7 Parking Lot (Deferred / Phase-2 Register) **[NEW]**

Captures "future enhancements" and out-of-scope ideas **separately** from the
main backlog, so they don't dilute MoSCoW discipline. Reviewed at scope/roadmap
checkpoints, not built by default.

---

### 0.8 Timeline & Sequencing

Indicative schedule — **a target, not a contract.** It must stay **elastic to
SME availability** (see Knowledge-Concentration risk, 0.10), which is the real
binding constraint, not the calendar.

| Window | Focus |
|---|---|
| Week 1 | Organization · Current systems · Document collection |
| Week 2 | HRMS · Service Book · Leave · Attendance |
| Week 3 | Payroll · Salary structure · Arrears · Claims · Loans |
| Week 4 | **Pension · Retirement · NPS · GPF · GIS · Loans & Recoveries** (terminal benefits + recoveries share data and formulas — keep together) |
| Week 5 | Finance · Budget · Accounting · Fund/Grant management |
| Week 6 | Integrations · Migration · Reports · NFR |
| Week 7 | **Buffer** · Validation · Gap closure · BRD sign-off |

> Org + existing-system assessment run first; integrations and NFRs can run in
> parallel once modules are understood. Define interview slots and
> document-submission deadlines per process owner.

---

### 0.9 Prioritization & Phasing

Universities default to *"everything is critical."* Do not accept it. Use two
**independent** axes:

**MoSCoW (business value):**

| Priority | Meaning |
|---|---|
| Must | System cannot go live without it |
| Should | Required soon after go-live |
| Could | Nice to have |
| Won't Now | Future phase (→ Parking Lot) |

**Compliance flag (separate axis):** *Mandated by law?* A legally-mandatory item
(NPS upload, Form 16, Form 24Q, PT return) can **never** be "Won't Now",
regardless of business priority. Keep it as its own column (see backlog 0.6) so
it cannot be traded away in scope negotiations.

| Requirement | Mandatory by law? |
|---|---|
| NPS Upload | Yes |
| Form 16 / 24Q | Yes |
| Employee Self-Service | No |

**Rollout phasing:** decide and record the rationale (e.g. HR+Payroll first,
Finance next; or college-by-college).

---

### 0.10 Risks, Assumptions, Constraints

Maintain a **risk register**, **assumption register**, and **constraint
register**. AAU-specific risks to seed:

* **Data-migration risk** — employee/service history may span **20–30 years**;
  legacy quality and completeness are uncertain.
* **Pay-rule coexistence risk** — UGC rules, state-government rules, and
  project-staff rules apply simultaneously to different cohorts.
* **Financial-year risk** — **never go live during March closing or the salary-
  processing week.**
* **Parallel-run risk** — replacing payroll means running **old + new payroll
  together for 2–3 salary cycles**; differences *will* appear. Plan **Parallel
  Payroll Validation** as an explicit activity (not an afterthought) with a
  defined comparison + tolerance + sign-off (links Phase 9).
* **Knowledge-concentration risk** — often **one senior clerk knows everything**;
  if unavailable, discovery stalls. **Mitigation:** shadow them early, record
  walkthroughs (screen/video), and convert their undocumented rules into backlog
  items immediately.
* Treasury-integration readiness; change resistance; statutory deadlines.

Constraints to record: budget, go-live window tied to the financial year,
mandated govt-cloud hosting, etc.

---

### 0.11 Success Criteria (measurable KPIs)

Each KPI carries a **baseline, target, measurement method, and target date** —
otherwise it is unfalsifiable at UAT.

| Area | Current (baseline) | Target | How measured |
|---|---|---|---|
| Payroll run | ~5 days | 1 day | cycle time per monthly run |
| Leave approval | manual file movement | 100% digital | % approvals via ESS |
| Budget tracking | Excel | real-time utilization | live head-wise vs allotment |
| Audit reports | manual compilation | one-click | report generation time |
| Reconciliation | manual | zero mismatches | schedule-vs-bill tie-out |

**Data-migration KPIs:**

| Area | Target |
|---|---|
| Employee Master | 100% migrated |
| Service History | 100% verified |
| Salary History | ≥ 99.5% matched |

**Payroll-accuracy KPI:**

| Area | Target |
|---|---|
| Salary calculation variance (parallel run) | ≤ 0.1% |

Also define the **acceptance / sign-off** process for each discovery deliverable.

---

### 0.12 Glossary & Master Data Dictionary **[NEW]**

Build during discovery — not just acronyms but the **canonical definition of each
master-data term**, because these definitions drive formulas and disputes (e.g.
exactly what counts as *qualifying service* or *emoluments* for pension). A
living document. Seed terms: DDO, UC, GIA, CPF, NPS, GPF, GIS, LWP, EL, HPL,
Commuted Leave, MACP, CAS, DR, PRAN, LPC, dies-non, fitment factor.

---

### 0.13 Discovery Repository & Evidence Management **[NEW]**

Discovery generates a flood of documents. Without a controlled repository, by
Week 5 nobody knows which payslip sample is current. Maintain a structured store:

```text
/Discovery
    /HR
    /Payroll
    /Finance
    /Reports
    /Integrations
    /Decisions
    /Samples
```

Every artifact is registered with version control:

| ID | Name | Version | Owner |
|---|---|---|---|
| DOC-031 | Sample salary slip (June) | v2 | Salary Section |

---

### 0.14 Baseline Capture **[NEW]**

Before redesigning anything, capture the **current-state metrics** — these become
the baseline against which ERP success is later judged. Without a baseline,
"success" is subjective.

* Payroll processing time
* Leave approval time
* Number of reports generated monthly
* Number of manual Excel sheets in use
* Number of reconciliation issues per cycle

(Feeds the KPI sheet in 0.11.)

---

### Phase 0 Deliverables

1. Stakeholder Map
2. **System Inventory Register**
3. RACI Matrix
4. **Decision Authority Matrix** (incl. cross-domain joint-owner rows + escalation)
5. **Decision Log** (mandatory)
6. **Conflict-Resolution Process**
7. Discovery Schedule (elastic, buffer week included)
8. Requirement Backlog (template + IDs + compliance + risk flag)
9. **Parking Lot / Deferred register**
10. Risk Register (incl. parallel-run risk)
11. Assumption Register
12. Constraint Register
13. Rollout / Prioritization Strategy (MoSCoW + compliance axis)
14. KPI Sheet (baseline + target + method, incl. migration & accuracy KPIs)
15. **Glossary & Master Data Dictionary**
16. **Discovery Repository & Evidence Register**
17. **Baseline Metrics Capture**
18. Discovery Sign-Off Document

---

# Phase 1: Organization Discovery **[EXPANDED]**

## Goal

This is where **actual business discovery** begins — learning how AAU operates,
not how discovery is managed. The common mistake is treating *organization chart
= Phase 1 complete*. For an ERP, Phase 1 is really the discovery of the
**authority structure, financial-control structure, employee-ownership
structure, and reporting boundaries.**

By the end of Phase 1 you must be able to answer:

```text
Who owns employees?
Who owns money?
Who owns approvals?
Who owns budgets?
Who owns grants?
Who owns pensioners?
```

Everything in HR, Payroll, Pension and Finance depends on those answers.

---

### 1.1 University Structure

Map the full hierarchy:

* Headquarters
* Constituent Colleges
* Regional Research Stations
* Krishi Vigyan Kendras (KVKs)
* Regional Offices
* Project Offices
* Farms / labs / testing units that incur cost or earn revenue

**Why it matters** — the structure determines data visibility, budget ownership,
payroll ownership, and approval chains. Universities typically nest as:

```text
University → College → Department → Employee
```

and sometimes:

```text
University → Research Station → Project → Employee
```

**Question — autonomous units:** are there units (e.g. a research centre) that
maintain a **separate budget / grant / payroll**? Autonomous units change the
architecture significantly (separate scoping, bills, and approval chains).

---

### 1.2 Establishment & Posts

Salary attaches to a **post**, not directly to an employee — the employee
*inherits* pay from the post. Without post management, promotion, vacancy,
recruitment, and the reservation roster all become hard later.

Collect sanctioned posts by cadre:

* **Teaching** — Professor, Associate Professor, Assistant Professor
* **Non-teaching** — Registrar, Superintendent, Clerk, Technician, …
* **Contractual**
* **Project staff**

For each: **sanctioned strength vs filled vs vacancy**, and the
**designation → pay level** mapping (teaching and non-teaching).

```text
Assistant Professor → Pay Level 10   (employee inherits from the post)
```

**Cadre rules** — capture the promotion ladder per cadre; it drives promotion
workflows:

```text
Assistant Professor → Associate Professor → Professor
```

---

### 1.3 Funding-Source Mapping

Two employees can share a **designation** but differ in **funding source**, which
changes budget, accounting, and reporting:

* **State-funded** — salary from state grants
* **ICAR-funded** — salary from project funds
* **Research-grant-funded** — salary charged to a grant account

Capture, per post/employee, which source pays — and whether a post can switch
source (project closure/renewal).

---

### 1.4 Employee & Pensioner Counts

Counts drive sizing, licence estimates, and migration effort. Collect by
category:

| Category | Count |
|---|---|
| Teaching | |
| Non-teaching | |
| Contractual | |
| Project | |
| Daily wage | |
| Pensioners | |
| Family pensioners | |

---

### 1.5 Payroll Control Structure

Centralized vs decentralized changes the whole architecture:

* **Scenario A — HQ payroll:** all salaries processed centrally (simpler).
* **Scenario B — College payroll:** each college processes its own (different
  scoping, bills, and roles).

Questions:

1. Is payroll centralized or decentralized?
2. Which offices act as **DDO** / prepare salary bills?
3. Who **sanctions** vs **approves** bills?
4. **Number of payroll operators per unit** (e.g. HQ = 5, College A = 2,
   College B = 1) — feeds role design.
5. **How many distinct payroll streams exist, and who owns each?** **[NEW]** —
   regular monthly, daily-wage, project payroll, pension payroll. Capture the
   *existence + ownership* of each stream (it determines how many payroll
   engines/roles are needed); processing mechanics belong to Phase 2/4.

---

### 1.6 Treasury & Payment Structure

How money actually leaves — determines integrations, approval chains, and finance
workflows. Identify per unit whether payment is via:

```text
Treasury   |   Bank   |   Grant account
```

---

### 1.7 Data Partitioning (scoping)

A frequently-skipped question that causes ERP failures. Establish visibility
boundaries:

* Can College A see College B's employees? (usually no)
* Can HQ see all colleges? (usually yes)

This directly determines the **role model, access control, and reporting scope**
(feeds Phase 7 RBAC).

---

### 1.8 Financial Responsibility Centres **[NEW]**

Also called cost centres / budget units / accounting units. Capture the cost-
centre structure and, for each, the **budget owner**, **fund owner**, and
**spending (sanctioning) authority** — these are **not always the same person**.
"Budget exists" does not mean "this person can spend it."

| Cost Centre | Budget Owner | Spending Authority |
|---|---|---|
| College of Agriculture | Dean | Dean |
| Research Project X | PI | PI |
| University HQ | Registrar | Finance Officer |

Makes Finance discovery (Phase 6) far easier.

---

### 1.9 Document-Flow Ownership **[NEW]**

For each key document, capture initiate → verify → approve → submit ownership —
this seeds Phases 3–6:

* **Leave application** — who initiates / approves?
* **Salary bill** — who prepares / verifies / sanctions / submits?
* **Pension case** — who starts / verifies / finalizes?

---

### 1.10 Academic Structure **[NEW]**

AAU is fundamentally a university; academic hierarchy drives leave sanction, CAS,
promotion, and academic allowances. Colleges/departments (1.1), posts (1.2), and
document flow (1.9) are already captured — so here collect only the **academic
authority dimension** not covered there:

* **Academic approval authority** — do HoD, Dean, Director hold *different*
  sanction powers (e.g. who approves a faculty member's leave / CAS / duty leave)?
* **Academic vs administrative post mapping** — are academic positions mapped on a
  different pay authority (UGC academic levels) and promotion path (CAS) than
  administrative posts (state matrix, MACP)? (links 1.2 + Phase 4.3/4.4)

*(Skip deep academic-council/committee governance detail — not payroll-relevant.)*

---

### 1.11 Project & Grant Ownership **[NEW]**

Funding sources (1.3) and cost centres (1.8) are captured; this adds the
**ownership/authority layer** on top:

* Who **owns** a project — PI / Co-PI?
* Who **approves** project expenditure?
* Can project staff belong to **multiple projects**?
* Can one employee draw salary from **multiple grants** simultaneously?

These are control-structure questions and decide Payroll + Finance behaviour.
*(Cost-allocation %, UC generation mechanics → Phase 6.)*

---

### 1.12 Legal Entity / Registration Structure **[NEW]**

Fundamentally shapes accounting, audit, fund management, and the data model
(single-entity vs multi-entity):

* Is AAU a **single legal entity**?
* Do any units maintain **separate accounts**?
* Do projects maintain **separate bank accounts**?

---

### 1.13 Operational Reality (flag only) **[NEW]**

A light flag here; the architecture/NFR substance lives in **Phase 11**:

* Which units are geographically remote (research stations, KVKs)?
* Which units currently operate on **paper / offline** due to connectivity?

Capture the *fact* of distribution + offline units (affects decentralization and
approval feasibility). **Connectivity, bandwidth, offline-sync, and hosting
requirements are gathered in Phase 11**, not here.

---

### Deliverables

* Organization Hierarchy Diagram
* Approval Hierarchy Diagram (per document type)
* **DDO / treasury mapping**
* **Sanctioned-post register** (sanctioned/filled/vacancy + cadre rules)
* **Funding-Source Matrix** (unit → source)
* **Cost-Centre Hierarchy** (AAU → College → Department → Project)
* **Authority & Control Matrix** (operational domain → owner)
* Academic-authority + academic-vs-admin post-mapping note
* Project-ownership / multi-grant note
* Legal-entity / separate-accounts note
* Employee & pensioner count sheet (by category)
* Document-flow ownership map
* User Role Matrix input (finalized in Phase 7)

**Authority & Control Matrix (template)** — *a discovered fact: who owns each
operational domain at AAU. Distinct from the Phase 0.3 Decision Authority Matrix,
which governs who decides project requirements.*

| Operational domain | Owner |
|---|---|
| Employees | Establishment |
| Payroll | Finance |
| Pension | Pension Cell |
| Budget | Accounts |
| Grants | Project Office |

**Funding-Source Matrix (template):**

| Unit | Funding Source |
|---|---|
| HQ | State |
| Project A | ICAR |
| Project B | Grant |

---

### Phase 1 success test

**Interview tip:** don't open with *"how many employees?"* Open with *"can you
draw the AAU organizational structure for me?"* then drill: *who owns / approves
/ pays / funds this unit?* Structure → Funding → Approvals → Employees → Payroll
ownership emerges naturally.

Phase 1 is complete not when you have an org chart, but when you can answer,
without notes:

1. Who owns employees?
2. Who owns payroll?
3. Who owns pensioners?
4. Who owns budgets?
5. Who owns grants?
6. Which unit prepares bills?
7. Which unit approves bills?
8. Which unit releases payments?
9. Which units can see each other's data?
10. Which funding source pays each employee category?

If you can answer those confidently — and draw
`AAU → Posts → Employees → Funding → Approvals → Treasury/DDO` from memory —
Phase 1 has succeeded and you're ready for Phase 2.

---

# Phase 2: Existing System Assessment **[EXPANDED]**

## Goal

Understand how the current **HRMS, Payroll, and Finance** actually work — and,
above all, **recover the undocumented business logic** buried in the legacy code
and in people's heads. This is *technical archaeology*: the real payroll rules
(DA rounding, leave accrual, arrear logic, fixation edge cases) live in stored
procedures, batch jobs, and one senior clerk's memory, not in any manual.
Reverse-engineering them is one of the highest-value activities of this phase and
a common point of replacement-project failure. (For a finance-heavy replacement,
the pain-points and shadow-systems findings can matter equally.)

> **Scope & de-duplication.** To avoid repeating other phases, Phase 2 does *not*
> re-collect: the **System Inventory Register** (see **0.1.1**), the **vendor
> schema / stored-proc / batch-job artifacts** (secured via the **0.1** vendor
> guardrail), **source DB / record counts / history span** (**Phase 9**),
> **current integrations** (**Phase 8**), or the **current report inventory**
> (**Phase 10**). Phase 2 *consumes* those and focuses on the five items below.

---

### 2.1 As-Is Functional & Technical Maps (per legacy system) **[EXPANDED]**

Produce an As-Is map for **each** legacy system — including **Finance**, which v1
treated as "processes" and likely runs on Tally / Excel / manual registers.

**HRMS** — modules present (Employee Master, Service Book, Leave, Transfer,
Promotion, Increment, Retirement, Recruitment): which are **actively used /
unused / need improvement**.

**Payroll** — observe an **actual monthly run** end to end: Salary Processing →
Approval → Bill Generation → Payment → Reports, *plus* arrears, claims, loans,
pension/retirement settlement, statutory returns. Capture who initiates, data
sources, and hand-offs.

**Finance (As-Is) [NEW]** — what exists today: Tally / Excel / standalone app /
manual? Budget, expenditure, fund/grant ledgers, receipts, accounting close —
how each is done now, and by whom.

Each map records: actors, inputs, outputs, hand-offs, and the technical
substrate (app / DB / spreadsheet / register).

**2.1.1 Unused-features analysis.** Formalize "used vs unused" — users often say
"keep everything", but half the legacy system may never be used. Drives scope
control (feeds MoSCoW, 0.9):

| Feature | Exists | Used |
|---|---|---|
| Leave | Yes | Yes |
| Recruitment | Yes | No |
| Transfer | Yes | No |

**2.1.2 Dependency mapping (internal, as-is).** Document how the legacy systems
*actually* feed each other today — including Excel-in-the-middle flows. This is
the **as-is** internal data flow; designing the *new* external integrations is
**Phase 8** (cross-ref, don't re-collect):

| Source | Target | Purpose |
|---|---|---|
| HRMS | Payroll | Employee data |
| Payroll | Finance | Salary journal |
| Payroll | Excel → Treasury | NPS / bank upload |

---

### 2.2 Legacy Business-Rule Reverse-Engineering **[NEW — marquee activity]**

Extract the rules the system actually applies, from code + SME shadowing — not
from manuals (which are usually stale or absent). Target:

* **Salary engine:** per-component base, rate source, formula, **rounding rule**,
  effective-date handling.
* **Leave:** accrual/credit logic, caps, carry-forward, and the **leave → pay
  reduction** (full/half/nil) actually computed.
* **Arrears:** how a past month is recomputed; deduction top-ups; rounding (per-
  month vs on-total).
* **Increment / fixation:** increment-date assignment, 6-month rule, fixation /
  MACP / CAS landing-cell logic, option-form handling.
* **Deductions:** OPS vs NPS branching, **GPF** handling, PT/GIS slabs, recovery
  priority, negative-net handling.
* **Pension:** qualifying-service, commutation, gratuity, encashment formulas if
  any exist in the legacy system.

Method: read **stored procedures, scheduler/batch jobs, report SQL** (from the
0.1 vendor artifacts); **shadow the senior clerk**; validate each extracted rule
against **real filled samples** (Phase 0.5). Log every rule in the **Legacy
Business-Rule Register** below.

> The classic failure: the vendor hands over a **database dump** but not the
> **business logic**. The dump tells you *what* the numbers are; only the logic
> tells you *why* — and the "why" is what the new system must reproduce exactly.

**Legacy Business-Rule Register** — every extracted rule carries its **source**,
a **confidence level** (not all sources are equally trustworthy), and a
**customization flag** (post-go-live customizations are often the most important
requirements — someone paid to add them):

| Rule | Source | Confidence | Customization? |
|---|---|---|---|
| DA formula | Government order | High | No |
| Arrear logic | Stored procedure | High | No |
| Leave accrual | Clerk memory | Medium | No |
| Special DA rule | Stored procedure | High | **Yes (post-go-live)** |
| Pension rule | Assumption | Low | No |

Low/medium-confidence rules flag what still needs validation; **Yes** in the
customization column flags a deliberately-added requirement to carry forward.

#### 2.2.1 Calculation Validation Samples (Golden Test Cases) **[NEW]**

For every critical calculation, collect **input → expected-output** pairs from
the legacy system. These become the **oracle** for the Phase 9 parallel run and
the ≤0.1% accuracy KPI (0.11) — distinct from the "real filled samples" of 0.5
(which are evidence; these are validation pairs).

* **Payroll:** normal salary · increment-month · promotion-month · LWP-month · arrear
* **Pension:** normal retirement · voluntary retirement · family pension
* **Finance:** budget allocation · expenditure booking

```text
Employee A · Basic 56,100 · DA 55% · …
Expected Net Salary = 82,433
   → Old system 82,433  ==  New system 82,433  ✓  (proves the implementation)
```

---

### 2.3 "Why Replace?" — Known-Issues & Pain-Points Register **[NEW]**

Capture the business case + must-fix sources. For each current system, record:

* **Pain points** — what takes the most time, causes the most errors, is most
  manual (the Phase 0.5 questions, applied to the legacy tools).
* **Known issues / failure modes** — where it breaks today (reconciliation
  mismatches, recomputation gaps, missing audit trail, reporting limits).
* **Limitations driving the replacement** — what the current systems *cannot* do.
* **Compliance-gap assessment [NEW]** — which statutory activities are **manual or
  missing today** (NPS upload, Form 16 / 24Q, PT return, audit trail). Ask:
  *"which compliance activities are done by hand today?"* These are immediate
  improvement candidates. This is an **as-is gap check** — the outputs are
  *designed* in Phase 4.9 / reported in Phase 10 (cross-ref, don't redesign here).

These directly seed must-fix requirements and anchor MoSCoW (Phase 0.9).

---

### 2.4 Shadow Systems & Workarounds **[NEW]**

Inventory the **Excel sheets, side databases, and manual registers** that
compensate for system gaps. These are hidden requirements — anything done
outside the official system is functionality the new ERP must absorb or
consciously drop. Record: what, who maintains it, why it exists, what it feeds.

---

### 2.5 Data-Quality Observations (hand-off to Phase 9) **[NEW]**

While reading the legacy data, note quality signals — missing mandatory fields,
duplicates, inconsistent codes, opening-balance gaps (GPF/loan/leave). These are
**observations, not the migration plan**; route them to **Phase 9** for the full
data-quality assessment and parallel-run design.

---

### Documents Required

* HRMS + Payroll user manuals (if they exist)
* Sample salary slip, salary register, pay bill — **real, filled** (per 0.5)
* Sample GPF/NPS/GIS/IT schedules, arrear bill, pension papers, claim bills
* Finance As-Is artifacts (current ledgers, budget sheets, UC samples)
* *(Schemas / stored procs / batch jobs come via the 0.1 vendor guardrail)*

### Deliverables

* As-Is process maps (HRMS, Payroll, **Finance**)
* **Unused-features matrix** (exists vs used → scope control)
* **Internal dependency map** (as-is legacy data flows → feeds Phase 8)
* **Legacy business-rule register** (rule + source + **confidence** + **customization flag**)
* **Golden test cases** (input → expected-output, for parallel-run validation → Phase 9)
* **Known-issues / pain-points register** (the replacement business case)
* **Compliance-gap assessment** (manual/missing statutory activities)
* **Shadow-systems & workarounds inventory**
* Data-quality observations log (→ Phase 9)

---

# Phase 3: HRMS Detailed Study **[EXPANDED]**

## 3.1 Employee Categories

Teaching (Professor / Associate / Assistant); Non-teaching (Registrar, Accounts,
Admin, Technical); Other (Contractual, Project, Daily-wage, **Guest Faculty**).

**Employment Nature Matrix [NEW]** — capture which rules apply per category;
universities often apply completely different rules:

| Category | Payroll | Leave | Pension |
|---|---|---|---|
| Regular | Yes | Yes | Yes |
| Contractual | Yes | Limited | No |
| Project | Yes | Maybe | No |
| Guest Faculty | Honorarium | No | No |

### Questions

1. Are payroll, service, and leave rules different per category?
2. **Which categories are "vacation department" (reduced EL)? [NEW]**
3. **How are project/contractual staff funded and paid (grant-charged)? [NEW]**
4. **How is Guest Faculty paid — remuneration master, non-salary TDS? [NEW]**
5. **Can an employee move between categories (e.g. contractual → regular)? [NEW]**
   — affects seniority, service book, leave, and pension.

## 3.2 Service Book Management

### Events to Capture

Appointment, Confirmation, Promotion, Transfer, Increment, **Pay Fixation**,
Pay Revision, **Leave Without Pay / dies-non**, Suspension, **Reinstatement**,
**Deputation**, **Pay Protection**, **Stepping-Up**, Retirement. **[EXPANDED]**

### Questions

1. Digital vs physical service book; which records are mandatory; attestation rule?
2. **Is the service book append-only (corrections via new event + order ref)? [NEW]**
3. **How is the Employee Master kept consistent with service events? [NEW]**
4. **Transfer → is a Last Pay Certificate (LPC) issued; do leave/loan balances carry? [NEW]**
5. **Can past service-book entries be edited — if so, by whom? (audit) [NEW]**

**Service Event → Supporting Document [NEW].** Government HRMS is order-driven —
events rarely exist without an order. Map each event to the document that creates it:

| Event | Document |
|---|---|
| Appointment | Appointment Order |
| Confirmation | Confirmation Order |
| Promotion | Promotion Order |
| Transfer | Transfer Order |
| Increment | Increment Order |

**Seniority Management [NEW].** How is seniority maintained (seniority list, inter-se
seniority on category change)? Promotion, MACP and CAS depend on it.

**HR document/order inventory [NEW].** Where do orders physically live today —
paper / PDF / file system / DMS? (Light as-is inventory; the **DMS requirement**
itself is gathered in **Phase 11 / integrations**, not here.)

## 3.3 Leave Management **[EXPANDED]**

### Leave Types (confirm AAU figures)

Casual (CL), Earned (EL), Half Pay Leave (HPL), **Commuted Leave**, Medical,
Maternity, Paternity, Child Care (CCL), Extraordinary (EOL/LWP), **Study Leave**,
**Duty Leave**, **Special Casual Leave (SCL)**, **Compensatory Off**,
**Restricted Holidays (RH)**. **[EXPANDED]**

### Questions

1. Accrual / credit frequency / advance credit, accumulation caps, carry-forward, encashment.
2. **Pay effect per type (full / half / 80% / nil) — the salary-engine input. [NEW]**
3. **EOL = dies-non? Effect on increment date and qualifying service. [NEW]**
4. **Commuted-leave 2× HPL debit; no-debit special leaves (Mat/Pat/CCL/SCL). [NEW]**
5. **Vacation-department reduced EL for teachers. [NEW]**
6. Leave approval hierarchy (Employee → HOD → Registrar?).
7. **Leave year — calendar / financial / academic? [NEW]** (many accruals depend on it).
8. **Leave encashment events — in-service / during LTC / retirement only? [NEW]**
   (feeds pension & settlement, Phase 5).

## 3.4 Attendance & Holiday Calendar **[NEW]**

### Questions

1. Attendance capture method (manual / biometric / face) and devices?
2. Holiday Calendar master — gazetted, restricted, weekly-off; per-college local holidays?
3. Working-day basis for **proration** and comp-off eligibility?
4. **Attendance exceptions (on-duty) — tour, training, duty leave, exam duty,
   field visit? [NEW]** (common at an agricultural university; must not count as absence).

## 3.5 Recruitment & Transfer **[EXPANDED]**

### Recruitment

1. Is Recruitment in ERP scope? If so, capture the workflow (vacancy → selection → appointment → service book).
2. **Reservation rules — SC / ST / OBC / EWS / PwD roster? [NEW]** *(only if
   recruitment is in scope; ties to sanctioned posts, Phase 1.2).*

### Transfer

1. Transfer process between colleges/units and the LPC handover.
2. **Inter-unit (College A → College B) vs inter-cadre (Admin ↔ Academic wing)
   transfer — different implications for seniority/service. [NEW]**

## 3.6 Employee Self-Service (pointer only) **[NEW]**

Not detailed here to avoid duplication: **as-is** employee-facing functions
(current leave application, salary-slip download, etc.) are captured in
**Phase 2**; the **to-be ESS scope** is designed in **Phase 7 (Approval
Workflows, RBAC & ESS)**.

---

### Deliverables

* **Employee Category Matrix** (employment-nature: payroll/leave/pension per category)
* **Service Event Catalogue** (event → supporting document)
* **Seniority-management note**
* **Leave Rule Matrix** (type, accrual, pay-effect, leave year, encashment)
* **Attendance Rule Matrix** (capture method, holiday calendar, on-duty exceptions)
* **Recruitment & Transfer workflow** (incl. reservation roster if in scope)
* **HR document/order inventory** (→ DMS requirement to Phase 11)
* **Service Book data-model draft**

> **Phase 3 success test:** you can answer — how does an employee join, get
> confirmed, get promoted, maintain seniority; how does leave affect salary; how
> does transfer affect service records; how does retirement start; and **what
> document supports each event**. If yes, Phase 3 is complete — and you stop at
> the HR/Payroll boundary (formulas belong to Phase 4).

---

# Phase 4: Payroll Deep Dive **[EXPANDED]**

## 4.1 Salary Structure

### Earnings

Basic, DA, HRA, TA, Medical, Academic, Special, Research **+ DA-on-TA rule**. **[EXPANDED]**

### Deductions

**GPF (OPS)**, NPS (post-cutoff), GIS, Professional Tax, Income Tax (TDS),
Loan/Advance recovery, **Overpayment recovery, Court attachment/Garnishee,
Quarter licence fee**, Misc recovery. **[EXPANDED]**

### Questions

1. **For each component: base, rate source, formula, rounding, effective date. [NEW]**
2. **Government-quarter flag → HRA withdrawn + licence-fee recovery coupling. [NEW]**

## 4.2 Pension-Scheme Determination (OPS vs NPS) **[NEW]**

### Questions

1. NPS cut-off date for AAU staff (State Finance notification)?
2. How is scheme derived from Date of Joining vs cut-off?
3. NPS contribution rates (employee 10%, employer 14% of Basic+DA) — and is the
   **employer 14% reported as expenditure + on the NPS schedule**?
4. GPF subscription min/max, interest schedule, advances/withdrawals.

## 4.3 Pay Matrix **[EXPANDED]**

### Questions

1. Which matrices apply — **state 7th-CPC/ROP (non-teaching) AND UGC academic
   (teaching) — both must be held, keyed by pay authority**? **[NEW]**
2. Exact adopted grids (levels × cell values), number of cells, rounding rule.
3. **Fitment factor used for 6th→7th transition (legacy arrears)? [NEW]**
4. How are revisions handled (new versioned matrix, not edits)?

**Pay Authority Master [NEW].** Every employee should be tied to a **pay
authority**, not directly to a matrix — the authority selects the grid/rules:

| Pay Authority |
|---|
| State Govt ROP (non-teaching) |
| UGC (teaching) |
| Project |
| Contractual / consolidated |

## 4.4 Increment, Fixation & MACP/CAS **[NEW]**

### Questions

1. Increment dates (1 Jan / 1 Jul) and 6-month eligibility as adopted?
2. Pay-fixation rule (notional increment → next-higher cell), **option form**, fixation statement.
3. **MACP** at 10/20/30 yrs (non-teaching), quota shared with promotions.
4. **CAS** stages and criteria (teaching) — kept separate from MACP.
5. How does EOL/withholding shift the next-increment date?
6. **Can increments be withheld (disciplinary)? Cumulative vs non-cumulative,
   and the restoration process? [NEW]**

## 4.5 Payroll Processing Workflow & Period States **[EXPANDED]**

### Current Workflow

Attendance/Leave → Processing → Accounts Verification → Finance Approval →
Bill Generation → Payment Release.

### Questions

1. Monthly timeline; approval hierarchy; reprocessing rules.
2. **Processing states and period LOCK** (Draft → Verified(DDO) → Approved →
   Submitted(Treasury) → Passed → Disbursed → **Locked**). **[NEW]**
3. **Post-lock corrections → supplementary/arrear bill, never edit. [NEW]**
4. **Treasury return loop** (returned bill re-enters with reason). **[NEW]**
5. **Proration** for mid-month join/retire/death/LWP. **[NEW]**
6. **Negative-net handling + deduction priority order. [NEW]**
7. **Retroactive change handling** — a back-dated government order (effective
   01-Jan-2025, issued today) triggers retro recompute + retro approval +
   arrear generation (the mechanics live in **4.6**). **[NEW]**
8. **Subsistence allowance** — a suspended employee draws subsistence allowance
   (not regular pay), revised on prolonged suspension, settled on reinstatement
   (service event from 3.2). **[NEW]**

## 4.6 Arrear Management **[EXPANDED]**

### Cases

Promotion, Pay Revision, DA Revision, Manual.

### Questions

1. Calculation method — **recompute each affected month with the rate/Basic in
   force then, diff vs PayslipHistory** (requires effective-dated master data +
   immutable pay history). **[NEW]**
2. **Deduction top-ups to NPS/GPF/IT schedules for arrear months. [NEW]**
3. **Taxability in year of receipt + §89(1)/Form 10E data. [NEW]**
4. **Idempotency** — re-running a trigger must not double-pay. **[NEW]**

## 4.7 Claims & Reimbursements **[NEW]**

### Catalogue

CEA, Hostel Subsidy, LTC (block-year, advance), Tour TA/DA, OTA, Bonus/Ex-gratia,
Medical reimbursement, Honorarium (exam/invigilation, guest faculty, committee).

### Questions

1. Ceilings/rates per claim (effective-dated); reimbursement (min of actual,
   ceiling) vs entitlement (rate × units by level).
2. Claim lifecycle (submit+proof → verify → sanction → pay → post taxable to record).
3. Separate claim bill vs merge into salary; tax-exempt limits.
4. **LTC advance ↔ final-claim settlement; excess → recovery.**
5. **External Payee abstraction (guest/exam staff with no Employee row) + non-salary TDS.**

**Supporting documents [NEW]** — claim workflows are document-heavy; capture the
proof required per claim:

| Claim | Documents |
|---|---|
| CEA | School certificate |
| LTC | Tickets / boarding passes |
| Tour TA/DA | Tour programme + bills |
| Medical | Hospital bills / prescriptions |

## 4.8 Loans & Advances **[NEW]**

### Questions

1. Loan catalogue (Festival, Vehicle, Computer, HBA, GPF advance) — ceilings,
   interest method (none/simple), recovery convention (principal-first vs blended),
   max installments.
2. Amortisation schedule generation; principal/interest split → accounting heads.
3. LWP/floor-month deferral (extend schedule, never silent skip).
4. Prepayment/foreclosure; **exit recovery from terminal benefits**; LPC carry on transfer.
5. **Can multiple loans coexist (festival + computer + vehicle)? Recovery
   priority + maximum total recovery cap? [NEW]** (feeds the 4.5 deduction-
   priority / negative-net rule).

## 4.9 Statutory & Compliance Outputs **[NEW]**

Form 16, **Form 24Q (quarterly)**, **Form 12BB (declaration)**, **Form 10E
(§89(1))**, **GPF annual statement**, **NPS transaction statement**,
**Professional Tax return**, pension/gratuity papers.

### Questions

1. Old vs new tax regime; 80C/80CCD; monthly TDS projection method.
2. Filing formats/portals (TRACES, state PT, NSDL/CRA).

**Annual Compliance Calendar [NEW]** — capture each statutory activity's
frequency; scheduling drives the payroll cycle as much as formulas do:

| Activity | Frequency |
|---|---|
| NPS contribution upload | Monthly |
| Professional Tax return | Monthly |
| Form 24Q (TDS return) | Quarterly |
| Form 16 | Annual |
| GPF annual statement | Annual |

## 4.10 Payroll → Accounting Interface **[NEW]**

Payroll does not end at net pay — it enters Finance. Capture **what journal
payroll must emit** and how it allocates:

```text
Salary expense → Department / Grant head
Employer NPS   → NPS liability (+ expenditure head)
Recoveries     → respective liability / fund accounts
Net pay        → Bank
```

### Questions

1. How is payroll posted to accounts — automatic **journal generation** from the bill?
2. **Cost-centre allocation** (which unit's expense) and **grant/fund allocation**
   (project-staff salary charged to the right fund)?
3. **Salary-component → accounting-head mapping** (each earning/employer-share to an object head)?
4. Employer-NPS as expenditure + liability legs?

> **De-dup:** this captures the **payroll→finance hand-off** (the journal payroll
> produces). The **chart of accounts / head structure** itself is **Phase 6**;
> cross-ref, don't redefine here.

## 4.11 Payroll Calendar **[NEW]**

The operational monthly cadence — many payroll issues come from deadlines, not
formulas. (Distinct from the Phase 0.8 *discovery* schedule.)

| Activity | Indicative date |
|---|---|
| Attendance / leave freeze | 25th |
| Payroll run | 27th |
| DDO verification | 28th |
| Treasury submission | 29th |
| Salary credit | 1st |

---

### Deliverables

* **Salary Component Catalogue** (earnings, with base/rate/formula/rounding/effective-date)
* **Deduction Catalogue** (incl. OPS/NPS fork, recoveries, priority)
* **OPS / NPS Rule Matrix** (scheme determination + contribution rules)
* **Pay Authority + Pay Matrix Catalogue** (grids by authority, versioned)
* **Increment & Fixation Rule Register** (increment dates, fixation, MACP/CAS, withheld)
* **Arrear Rule Register** (recompute method, top-ups, §89(1))
* **Claims Rule Matrix** (ceilings/rates, lifecycle, supporting docs)
* **Loan Rule Matrix** (catalogue, interest, recovery, multi-loan priority)
* **Annual Compliance Calendar**
* **Payroll → Accounting mapping** (component → head, allocations → Phase 6)
* **Payroll Workflow & State Diagram** (Draft → … → Locked)
* **Payroll (operational) Calendar**

> **Phase 4 success test:** you can answer **"why is Employee A's salary
> ₹82,433?"** — tracing every rupee to its base, rate (effective in month),
> rule, and scheme — not merely *what* the figure is. Then stop at the pension
> boundary: retirement settlement is large enough to be its own phase (Phase 5).

---

# Phase 5: Pension & Retirement Settlement **[NEW]**

## Goal

Capture terminal-benefit, retirement-processing, and ongoing-pensioner
requirements — absent from v1 despite "Retirement Management" being a listed
module. Payroll = monthly salary; pension = lifetime benefit. The rules,
documents, approvals, liabilities and audits are completely different, which is
why this is a separate phase. Discovers **what happens when service ends.**

> **Boundary:** Phase 5 stays on *retirement → benefit calculation → pension
> processing → pensioner lifecycle*. Pension **accounting journals / heads** are
> **Phase 6**; **CRA API integration** is **Phase 8** (cross-ref, not built here).

---

### 5.1 Retirement Event Types **[NEW]**

Different exit events trigger different benefit calculations — capture each:

| Type | Note |
|---|---|
| Superannuation | normal age retirement |
| Voluntary Retirement (VRS) | on request, qualifying-service condition |
| Premature / Compulsory Retirement | disciplinary / administrative |
| Death in Service | triggers family pension + DCRG + waivers |
| Invalid Pension | medical invalidation |

---

### 5.2 OPS Path

1. Qualifying service derivation (total − un-condoned EOL/dies-non; condonation rules).
2. Pension formula (last-drawn vs 10-month average; fraction; min/max).
3. **Commutation** (max %, age-factor table, reduction + ~15-yr restoration).
4. **Gratuity/DCRG** formula + statutory ceiling.
5. **Family pension** (enhanced then normal; eligibility).
6. **Leave encashment** = min(EL,300) × (Basic+DA)/30.
7. **GPF final payment** from ledger.

### 5.3 NPS Path

1. Exit process — corpus read from CRA, lump-sum % + mandatory annuity, threshold.
2. System initiates withdrawal/exit request.
3. **NPS reconciliation (process) [NEW]** — payroll → NPS schedule → CRA → **PRAN
   match / contribution tie-out**; how mismatches are resolved. *(The CRA API
   itself → Phase 8.)*

---

### 5.4 Pension Sanction Workflow **[NEW]**

Capture who does what, and *when*:

```text
Establishment → Pension Cell → Finance → Registrar
(initiate)      (verify svc +   (verify    (sanction +
                 calculate)      funds)      issue PPO)
```

Questions:

1. Who initiates the case, verifies service, calculates benefits, sanctions, issues PPO?
2. **Pre-retirement initiation [NEW]** — a case should start ~6–12 months before
   superannuation; when is it triggered relative to the retirement date?
3. **Provisional pension [NEW]** — if final settlement is delayed, is provisional
   pension paid until the PPO issues?

---

### 5.5 Pension Document Catalogue **[NEW]**

Pension is document-heavy — capture which are mandatory:

* Service Book · LPC · Pension application
* Nomination · Family details
* Bank details · Medical certificate (if applicable)

---

### 5.6 Family Pension Lifecycle **[NEW]**

Go beyond eligibility to activation and special cases:

```text
Employee dies → spouse/nominee submits claim → verification → family pension starts
```

* Activation flow + documents
* Multiple nominees; disabled dependents; unmarried daughters (special cases)
* Enhanced-then-normal rate transition

---

### 5.7 PPO Management **[NEW]**

OPS pension operations revolve around the **PPO (Pension Payment Order)**:

* Generation · Revision · Duplicate PPO · Transfer (between disbursing agencies)

---

### 5.8 Exit Clearance & No-Dues **[NEW]**

Before settlement, capture clearance:

* **Recoveries** — loans, festival/computer/vehicle advances, overpayment (netted
  from terminal benefits; death-time waiver checks).
* **Assets** — quarter, laptop, library books, vehicle.
* **No-Dues** — how the No-Dues certificate is generated and gates settlement.

---

### 5.9 Pension Revision Handling **[NEW]**

Pension itself gets revised, not just DR. Capture:

* Triggers — ROP / Pay Commission revision, court orders.
* Effective dates, **re-fixation**, and **arrears** (reuses the Phase 4.6
  recompute discipline, on the pension side).

---

### 5.10 Ongoing Pensioner Payroll

1. **Pensioner Dearness Relief (DR)** — basic pension × DR%, same cadence as DA.
2. Disbursement channel (university vs pension-disbursing bank/treasury).
3. **Annual Life Certificate [NEW]** — pensioners must submit a yearly life
   certificate (e.g. Jeevan Pramaan) to keep drawing pension; how is it tracked /
   pension held on non-submission?

> **Terminal-benefits accounting (pointer):** gratuity / commutation / encashment
> need accounting-head mapping + journals — **gathered in Phase 6** (mirrors the
> 4.10 dedup), not here.

---

### Deliverables

* **Retirement Event Matrix** (event → benefit path)
* Pension/gratuity/commutation **rule sheet** (AAU-confirmed)
* **Pension Workflow Diagram** (incl. pre-retirement + provisional pension)
* **Pension Document Checklist**
* **Family Pension Rule Matrix**
* **PPO Lifecycle note**
* **NPS Exit + Reconciliation note**
* **No-Dues / Exit-Clearance workflow**
* **Pension Revision Rule Register**
* Pensioner-payroll process flow (DR + life certificate)
* Sample existing pension papers

> **Phase 5 success test:** for any exit type you can state which scheme governs,
> which benefits compute, what documents + workflow + clearances are required, and
> how the pensioner is paid (and re-verified) thereafter — for OPS *and* NPS.

---

# Phase 6: Finance Module Discovery **[EXPANDED]**

> **What Phase 6 really discovers:** Phase 4 answered *why* salary was ₹82,433;
> Phase 6 answers *where it got booked* — which budget, which grant, which ledger.
> Finance owners often say "we do accounting in Tally and generate reports" —
> which tells you nothing. Dig into how money **moves, is controlled, is
> accounted, and is reported.**

## 6.1 Budget Management

Budget creation/approval/revision/monitoring; allocation department- / project- /
grant-wise; **expenditure checked against allotment before bill approval**. **[EXPANDED]**

### Questions

1. **Budget lifecycle [NEW]** — Original → Supplementary → Revised → Final. Does
   AAU follow this cycle?
2. **Budget control level [NEW]** — is control at department / **object-head** /
   project level? (Drives validation granularity; ties to cost centres, Phase 1.8.)

## 6.2 Expenditure Management

Bill → Verification → Approval → Payment → Accounting Entry; approval levels and limits.

### Questions [EXPANDED]

1. **GST handling on vendor payments? TDS on contractor/professional payments? [NEW]**
2. **Mapping of salary components → accounting heads (Major/Minor/Sub/Object). [NEW]**
3. **Commitment / encumbrance control [NEW]** — does a purchase order / commitment
   reduce *available* budget, or only on bill payment? *(Budget-control question
   only — full procurement stays out of scope per 6.5-Q2.)*
4. **Vendor Master [NEW]** — vendor categories, GST registration, PAN, bank
   details (the payment-side payee, parallel to the §11 employee/external payee).
   *Scoped to payments, not a procurement workflow.*
5. **Imprest / temporary advances [NEW]** — advances to departments/officers and
   their **settlement** (distinct from staff loans in Phase 4).

## 6.3 Revenue & Receipts **[NEW]**

### Questions

1. Income sources (student fees, farm/produce sales, soil/seed-testing labs,
   application fees, interest) and receipt workflow.
2. **Receipt classification [NEW]** — fee / grant / sale / interest / donation —
   how are receipts classified to heads?
3. GST on taxable receipts; revenue ledger; reconciliation with bank.
4. **Refund process [NEW]** — fee refund, security-deposit refund.

## 6.4 Fund, Grant & Project Management **[EXPANDED]**

Sources: State, Central, ICAR grants, Research grants, Sponsored Projects.

### Questions

1. Separate ledgers per fund; **Utilization Certificate (UC) generation**.
2. **Project cost centers; charging project-staff salary + expenditure to the
   right fund; closing/renewal of projects. [NEW]**
3. **Multi-funding [NEW]** — can one cost (e.g. a salary) be split across funds
   (60% Project A / 40% Project B)? (Consumes 4.10 allocation + 1.11 multi-grant.)
4. **Grant restrictions [NEW]** — equipment-only, salary-not-allowed, travel caps,
   end-date limits — how are restricted heads enforced at booking time?

## 6.5 Accounting Requirements

Chart of Accounts, Journal, Ledger, Cash Book, Bank Book, Trial Balance, Balance
Sheet, Income & Expenditure.

### Questions

1. Double-entry required? Audit using system reports?
2. **Accounting basis [NEW]** — cash vs accrual? (Significantly changes design.)
3. **Year-end closing [NEW]** — opening balances, carry-forward, audit adjustments;
   how is the financial year closed?
4. **Fixed-asset register / depreciation, Stores/Inventory, Procurement —
   in scope or explicitly excluded? Decide and record. [NEW]**

## 6.6 Banking & Treasury Management **[NEW]**

Finance-side banking operations + reconciliation. *(File formats / treasury API /
bank-file integration are **Phase 8** — cross-ref, not built here.)*

### Questions

1. **Bank accounts** — how many; per fund / per project?
2. **Bank reconciliation (BRS)** — how performed, frequency?
3. **Treasury** (if involved) — submission / return / acknowledgement process.
4. **Payment modes** — NEFT / RTGS / treasury / cheque.

## 6.7 Internal Controls & Audit (finance-specific) **[NEW]**

Government finance systems exist largely for audit. Capture the **finance-domain**
controls here; the cross-cutting ones live elsewhere.

### Questions

1. **Transaction immutability** — can a posted entry be edited, or only reversed?
2. **Reversal / correction mechanism** — how are accounting mistakes corrected?
3. **Supporting-document attachment** — how are bills/proofs attached to vouchers?

> Maker-checker / separation of duties → **Phase 7 (RBAC)**; the system-wide
> **audit trail** → **Phase 0.3 / Phase 11**. Not re-specified here.

## 6.8 Financial Reporting (pointer) **[NEW]**

The finance **report catalogue is gathered in Phase 10** (which already has a
Finance group). Note here only the split to carry into Phase 10:

* **Statutory** — Budget Utilization, Grant Utilization, **UC**, Ledger, Trial
  Balance, Balance Sheet, Income & Expenditure.
* **Management** — cost-centre expenditure, project expenditure, salary-cost analysis.

---

### Deliverables

* **Budget Rule Matrix** (lifecycle + control level)
* **Expenditure Workflow Diagram** (incl. commitment control, vendor master, imprest)
* **Revenue Classification Matrix** (incl. refunds)
* **Fund & Grant Rule Matrix** (multi-funding + restrictions + UC)
* **Chart-of-Accounts structure** (+ accounting basis)
* **Bank / Treasury Process Map** (BRS, payment modes; integration → Phase 8)
* **Audit & Control Matrix** (finance-specific; maker-checker → Phase 7)
* **Year-End Closing Procedure**
* Financial Report Catalogue (→ compiled in **Phase 10**)

> **Phase 6 success test:** for the ₹82,433 salary (and any expenditure/receipt)
> you can state which **budget** authorised it, which **fund/grant** bore it,
> which **ledger/heads** recorded it, how it **reconciles to the bank**, and how
> it is **controlled and reported** — under the right accounting basis.

---

# Phase 7: Approval Workflows, RBAC & ESS **[NEW]**

## Goal

Define access control, separation of duties, and the employee-facing channel —
the User Role Matrix was a v1 deliverable but never gathered. Phase 1 answered
*who owns what*; **Phase 7 answers *who can do what*** — different questions
("Payroll owner = Finance Section" ≠ "every Finance user can approve payroll").

> **Boundary:** discovery-level only — *who logs in, what they can do, how
> approvals flow.* Technical authentication design (OAuth / LDAP / JWT / SAML)
> belongs to **Phase 11**.

### 7.1 Roles & Permissions

* Enumerate roles (at minimum: **Employee, Dealing Assistant, DDO, Approver/
  Registrar, Auditor, Admin**).
* **Separation of duties** (preparer ≠ sanctioner ≠ auditor; DDO cannot
  self-approve own entry; Admin manages config, not bill sanction).
* **Permission scoping** = role × scope (own / unit-college / university) × action
  (read / write / sanction / lock).
* **Multiple concurrent roles [NEW]** — one person may hold several (Professor +
  Project PI + Dean); capture this and which role is **active** for a given action.
* **Acting / temporary roles [NEW]** — Officer-in-Charge when an officer is on
  leave; **effective from/to + auto-expire** (distinct from delegation — acting =
  temporarily *hold* a role; delegation = *pass* approval authority, 7.7).

### 7.2 Approval Workflow Engine

1. Configurable multi-level workflows per document type (salary bill, arrear,
   claim, leave, fixation, expenditure).
2. Delegation, escalation, return-with-reason; **digital signature (DSC/e-sign)** on approvals.
3. **Sequential vs parallel approval [NEW]** — sequential (Employee → HoD →
   Registrar) and parallel (Accounts + Audit both must approve).
4. **Conditional approval [NEW]** — routing by value/type (e.g. claim < ₹10,000 →
   HoD only; ≥ ₹10,000 → Registrar). Very common.

### 7.3 Employee & Pensioner Self-Service (ESS)

1. Apply leave (feeds the existing approval chain — never auto-grant).
2. View/download payslip & Form 16; submit Form 12BB.
3. View GPF/NPS, leave balance, service book.
4. **Employee data self-update [NEW]** — mobile / address / nominee / bank account:
   **direct vs approval-required?**
5. **Retiree / pensioner self-service [NEW]** — download pension slip, view DR
   revisions, update bank details (AAU has pensioners; ESS is not employee-only).
6. Authentication at discovery level (SSO/AD / govt employee ID / standalone),
   mobile vs web. *(Protocol design → Phase 11.)*

### 7.4 Audit Trail

Every privileged action logged who/when/old→new; paired with RBAC; immutable.

* **Audit risk-tiering [NEW]** — not all events audit alike. **High-risk** (salary
  changes, bank-account changes, pay fixation, budget approval) vs **low-risk**
  (e.g. profile photo) — different retention/visibility. *(System-wide audit
  infrastructure → Phase 0.3 / Phase 11.)*

### 7.5 Master Data Governance **[NEW]**

Wrong master data = wrong payroll = wrong finance — so govern who may change it.
For each master (employee categories, pay components, leave types, cost centres,
projects, accounting heads, rate tables):

1. Who can **create / modify**, and who **approves** the change?
2. Can it be **deleted, or only deactivated** (effective-dated)?

*(Distinct from Phase 0.3, which governs who decides project requirements; this is
runtime CRUD authority over live master data.)*

### 7.6 Notification & Escalation **[NEW]**

Approval systems live or die on notifications.

1. **Events** — what triggers a notification (pending approval, return, bill due).
2. **Escalation rules** — e.g. leave pending 5 days → escalate; bill-pending reminders.
3. **Channels** — email / SMS / app / dashboard. *(Gateway integration → Phase 8;
   here capture events + escalation logic + intended channel.)*

### 7.7 Delegation Rules **[NEW]**

1. **Planned delegation** — Registrar on leave → Joint Registrar (from/to dates).
2. **Emergency delegation** — can Admin assign temporarily; who approves it?
3. **Audit** — the action is recorded as **"approved by delegate"**, not as the
   original officer.

### Deliverables

* **Role Catalogue** + **Permission Matrix** (role × resource × scope × action)
* **Workflow Catalogue** (per document type; conditional + parallel)
* **Delegation Rules Matrix**
* **Notification Matrix** (event → escalation → channel)
* **Master Data Ownership Matrix** (who creates/modifies/approves; deactivate-not-delete)
* **Audit Event Catalogue** (risk-tiered)
* **ESS Feature Matrix** (employee + retiree; self-update direct vs approval)

> **Phase 7 success test:** for any user you can state which roles they hold (incl.
> acting/delegated), what they may do at what scope, how each document's approval
> routes (sequential/parallel/conditional), who governs each master, and what is
> audited at which tier.

---

# Phase 8: Integrations **[EXPANDED]**

Discovers **what systems exchange data — and what happens when they stop.**
Integrations delay ERP projects not through coding difficulty but because nobody
knows who owns it, what format it expects, how often it runs, or what to do when
it fails.

> **Boundary:** discovery-level only — *who exchanges what data, how often, who
> owns it, what happens on failure.* API design (JSON structure, OAuth flow,
> endpoint URLs) belongs to architecture/implementation, not here.

### 8.1 Per-Integration Discovery Template **[EXPANDED]**

Mandatory fields for **every** integration (not just direction/method):

| Field | Capture |
|---|---|
| Direction | inbound / outbound / bi-directional |
| Mechanism | file / API |
| Schema / format | (prescribed format reference — not designed here) |
| Frequency / **timing-SLA** | e.g. bank file by 29th to credit on 1st (ties to 4.11) |
| **Owner** | business owner of the interface |
| **Environment ownership [NEW]** | who provides endpoint / credentials / certs / **test + prod** env |
| **Failure handling [NEW]** | retry / manual fallback / correction workflow / escalation |
| **Reconciliation [NEW]** | ack/return file + tie-out (send → acknowledge → reconcile) |
| **Security [NEW]** | encryption, DSC, VPN, IP-whitelisting, govt-network (esp. Treasury/PFMS/CRA) |
| **Classification [NEW]** | replace / retain / modify / **retire** — and *who still depends on it* |

> Reconciliation is the norm, not "send and done": **NPS** → file → CRA → SCF →
> reconcile; **Bank** → payment file → success/reject file → reconcile (links 6.6
> BRS / 5.3 NPS recon). General security posture → **Phase 11**.

### 8.2 Integration Catalogue

Apply the 8.1 template to each:

* **Treasury / IFMS** — bill submission format, token/voucher, return loop.
* **Banking** — salary bank file, vendor payment file, multi-bank, returns/reissue.
* **NPS / NSDL-CRA** — PRAN generation, monthly contribution upload (both legs), SCF confirmation.
* **Income Tax** — Form 16/24Q, TRACES, tax computation, declaration workflow.
* **PFMS / DBT** (if applicable).
* **DSC / e-Sign** provider.
* **SSO / Active Directory**.
* **Biometric / attendance devices**.
* **SMS / email gateway**; **DigiLocker / DMS**.
* **ICAR / UGC portals, e-Office** (if applicable).
* Catalogue **all existing** integrations (often carry critical undocumented logic).

### 8.3 Source-of-Truth Matrix **[NEW]**

For each shared data entity, the single system of record — prevents conflicting masters:

| Data | System of Record |
|---|---|
| Employee | HRMS |
| Salary | Payroll |
| Budget / ledgers | Finance |
| PRAN / NPS corpus | CRA |

### 8.4 Master Data Synchronization **[NEW]**

When an employee is created in HRMS, should it appear automatically in Payroll /
Finance / Attendance? In a **unified ERP** modules share data (no sync needed) —
so the real questions are **external sync** (to CRA/treasury/etc.) and
**transition-period sync** during phased rollout while legacy systems still run.

### Deliverables

* **Integration Inventory** (the 8.1 template, filled per interface)
* **Integration Architecture Diagram**
* **Source-of-Truth Matrix**
* **Reconciliation Matrix**
* **Failure & Recovery Matrix**
* **Integration Ownership Matrix** (business + environment)
* **Retain / Retire Register** (replace/retain/modify/retire + dependents)

> **Phase 8 success test:** for every interface you can name its owner, format,
> frequency/SLA, environment provider, failure path, reconciliation, security
> mode, and whether it is replaced/retained/retired — without "we'll figure it
> out later."

---

# Phase 9: Data Migration Strategy **[EXPANDED]**

Migration (with Phase 2) most directly decides success/failure: users tolerate a
new UI/workflow/report, never a **wrong salary / leave / GPF / loan / pension
balance** — all of which originate here. Migration is not "copy data"; it is
**migration correctness**.

> **Boundary:** discovers *what data, how much, who validates, how we know it's
> correct.* ETL design / migration-script development is implementation, not here.

### 9.1 Source Systems & Historical Depth Policy

* HRMS, Payroll, Finance — database type, record counts, historical-data availability.
* **Historical Depth Policy [NEW]** — a recorded *decision*, not just availability:
  full history (e.g. 20 yrs salary) vs **current balances + N years** (e.g. 3).
  Huge effort driver.

### 9.2 Migration Scope

**Mandatory:** Employee Master, Service Book, Leave Balances, Salary History,
Payroll Components, **GPF opening balance + interest, outstanding loans
(remaining principal + installments), pay fixation/Level/cell + last increment
date, scheme/PRAN/GPF no.**

**Documents [NEW]:** service-book scans, appointment/promotion orders, pension
papers — decide **migrate / archive / link-externally** per type (cross-ref Phase
3.2 document inventory; DMS requirement → Phase 11).

**Optional:** historical reports.

### 9.3 Method (the pipeline)

```text
Quality assessment → cleansing → code mapping → transformation →
opening balances (+ provenance) → trial cycles → reconciliation →
parallel run → cutover → legacy retention
```

1. **Data-quality assessment + cleansing** (dedup, validation, mandatory-field gaps;
   consumes the Phase 2.5 observations).
2. **Code mapping [NEW]** — legacy → new value maps (gender M/F → MALE/FEMALE;
   designation, department, leave type, pay component). Mapping tables per field.
3. **Opening balances as initial ledger entries** with **provenance** — and
   **traceability** [NEW]: every new record traces back to its legacy record for audit.
4. **Trial migration cycles [NEW]** — multiple rehearsals (Trial 1 → fix → Trial 2
   → fix → final cutover); never a single run.
5. **Parallel run** — recompute a known past month, compare to legacy-paid figure
   within tolerance; gate go-live on a pass.
6. **Cutover plan** — freeze window, sequence, **rollback** strategy.
7. **Legacy retention/archival** (legal + audit).

> **Why this matters:** a wrong opening loan balance (original sanction instead
> of outstanding) silently over-recovers for months — a real loss. Migration
> correctness *is* payroll correctness.

### 9.4 Data Ownership Matrix **[NEW]**

Each dataset has a named validator — else everyone assumes someone else checked:

| Data | Validating Owner |
|---|---|
| Employee Master | Establishment |
| Leave Balances | HR |
| Salary History | Payroll |
| GPF / loans | Accounts |
| Pensioners | Pension Cell |

### 9.5 Reconciliation Matrix **[NEW]**

*What* is reconciled and the **tolerance** per item (ties to Phase 0.11 KPIs):

| Item | Tolerance |
|---|---|
| Employee / pensioner count | 0 (exact) |
| Leave / loan / GPF balance | 0 (exact) |
| Current-month salary (parallel run) | 0 (exact) |
| Historical report totals | ± small variance |

### 9.6 Data Freeze Calendar **[NEW]**

Define exactly what stops and when before cutover: employee creation freeze,
leave-update freeze, salary-processing freeze — with dates (avoid March close /
salary week, per Phase 0.10).

### 9.7 Exception & Orphan Handling **[NEW]**

Rules for broken records: employee-without-post, loan-without-employee, missing
PRAN, unmapped codes → captured in an **Exception Register**, resolved before sign-off.

### 9.8 Post-Go-Live Hypercare **[NEW]**

Who fixes migration issues after go-live and **for how long** (e.g. 30 / 60 / 90
days), with named ownership and an escalation path.

### Deliverables

* Data-migration plan + mapping
* **Historical Retention Policy**
* **Code Mapping Catalogue**
* Data-quality report
* **Data Ownership Matrix**
* **Reconciliation Matrix** (items + tolerance)
* **Trial Migration Plan**
* **Data Freeze Calendar**
* **Exception Register**
* Parallel-run sign-off criteria + cutover/rollback plan
* **Hypercare Plan**

> **Phase 9 success test:** for every mandatory dataset you can name its owner,
> source, historical depth, code mapping, reconciliation tolerance, freeze point,
> and exception rules — and a known past month recomputes to the legacy figure
> within tolerance across repeated trial runs.

---

# Phase 10: Reporting & Compliance **[EXPANDED]**

In government/university systems reports often *define* the system — a payroll
officer may touch only the Salary Register, Pay Bill and Salary Slip all month.
If a report is wrong (missing subtotal, footer, certification block) users call
the **system** wrong even when the calculation is correct. Phase 10 discovers how
management, auditors, agencies and employees **consume** the results.

> **Boundary:** discovers *what information users need* — not BI-tool selection or
> dashboard/Power-BI implementation (→ architecture).

## Report Catalogue (by domain)

### HR

Employee Register, Service History, **Promotion/Increment Report**, Retirement Forecast.

### Payroll

Salary Register, Pay Bill, Salary Slip, **Deduction Register**, NPS Report,
**GPF Report**, GIS Report, Income Tax Report, **Arrear (month-wise) Statement**.

### Statutory **[NEW]**

Form 16, 24Q, 12BB, Form 10E, GPF annual statement, NPS transaction statement, PT return.

### Pension **[NEW]**

Pensioner register, pension/gratuity papers, DR statement.

### Finance

Budget Utilization, **UC**, Ledger, Cash Book, **Bank Book**, Trial Balance,
Balance Sheet, **Income & Expenditure**, **fund/project-wise statements**.

### Requirement

Collect the **top 20 reports used every month** + every **statutory** return,
**with sample outputs and prescribed formats** — never accept "we need a Salary
Register"; get the *actual* one (PDF/Excel/print), so grouping, subtotals,
footers and certification blocks are captured, not lost.

## Report Attribute Template **[NEW]**

Every report carries these attributes (capture as one matrix):

| Attribute | Capture |
|---|---|
| **Classification** | operational / management / statutory / audit / ESS |
| **Owner** | e.g. Salary Register → Payroll, GPF → Accounts, Pension Register → Pension Cell |
| **Frequency** | monthly / quarterly / annual / on-demand |
| **Parameters** | month, college, department, grant, employee |
| **Certification** | prepared / verified / approved / DDO sign / DSC (which reports need it) |
| **Submission destination** | 24Q→TRACES, NPS→CRA, PT→state portal, UC→funding agency (feeds Phase 8) |
| **Historical scope** | current year vs N years (ties to the 9.1 Historical Depth Policy) |
| **Delivery** | screen / PDF / Excel / ESS download / scheduled |

## 10.1 Dashboards & KPIs **[NEW]**

Operational analytics modern users expect alongside reports (distinct from the
Phase 0.11 *project-success* KPIs):

* **HR** — vacancy %, retirement forecast
* **Payroll** — salary-cost trend, NPS liability
* **Pension** — pension liability
* **Finance** — budget vs actual, grant utilization

## 10.2 Ad-Hoc Reporting **[NEW]**

* Need an ad-hoc query / report builder?
* Excel export on any list?
* Pivot-style analysis (e.g. salary cost by department)?

## 10.3 Report Reconciliation Matrix **[NEW]**

Which reports must tie out — prevents future disputes (extends the 4.10 / 6.7 / 8
reconciliation discipline to reporting):

| Must match | … |
|---|---|
| Salary Register total | = Pay Bill total |
| Ledger | = Trial Balance |
| NPS deduction | = NPS schedule |
| Schedule totals | = bill deductions |

### Deliverables

* **Report Catalogue**
* **Report Attribute Matrix** (owner / frequency / classification / params / certification / destination / historical / delivery)
* **Statutory Submission Matrix** (report → destination)
* **Dashboard Requirements**
* **Report Reconciliation Matrix**
* **Ad-Hoc Reporting Requirements**
* **Sample Report Repository** (actual filled outputs)

> **Phase 10 success test:** for every report you can name its owner, type,
> frequency, parameters, certification, destination, historical scope and delivery
> — backed by a real sample — and you know which reports must reconcile to each other.

---

# Phase 11: Non-Functional & Technical Assessment **[EXPANDED]**

Phases 1–10 answer *what the ERP must do*; Phase 11 answers ***how well*, and
*under what constraints*** — e.g. not just "calculate salary" but "calculate
salary for 5,000 employees within 15 minutes."

> **Boundary:** constraints & quality attributes only — not architecture or
> implementation design (those follow discovery).

## Existing Infrastructure

Hosting, database, current user count, peak concurrent users.

## Non-Functional Requirements **[NEW]**

* **Performance / concurrency** targets (e.g. payroll run for N employees, peak ESS load).
* **Capacity & growth [NEW]** — growth horizon: employee / pensioner / document /
  transaction volume (e.g. 2,000 now → 4,000 in 5 yrs). Drives sizing.
* **Availability / SLA**, maintenance windows.
* **DR / BCP**, backup **RPO/RTO**.
* **Security**: RBAC, audit logs, digital approval trail, **VAPT / CERT-In**,
  document security, encryption.
* **Data privacy** — **DPDP Act 2023** compliance.
* **Legal & audit [NEW]** — **CAG / state audit** expectations, statutory
  **record-retention laws**, **DSC compliance**.
* **Document storage [NEW]** — expected document volume, scan-size limits,
  retention; **this is the DMS requirement landing point** (routed from 3.2 / 9.2).
* **Active-system retention [NEW]** — service-book / salary / pension retention
  (often decades). *Distinct from the **legacy** retention in Phase 9.*
* **Search [NEW]** — search by employee / PPO / PRAN / order-no / grant; poor
  search makes a correct ERP unusable.
* **Print & PDF [NEW]** — bulk generation (e.g. 2,000 salary slips/run), DSC on
  PDFs, volume → performance planning (links 7/8/10).
* **Observability & monitoring [NEW]** — alerts / health checks for payroll,
  integration and backup failures (links Phase 8 failure handling).
* **Localization** — Assamese language support; **accessibility**.
* **Mobile** support; **API standards**.
* **Hosting model** — govt cloud (e.g. state data centre / MeghRaj) vs on-prem; data residency.
* **Operating distribution / connectivity** — geographic spread (colleges,
  research stations, KVKs); low-bandwidth / remote sites; offline-capable
  processes + **sync strategy**; units currently on paper (flagged in Phase 1.13).

## 11.1 Environment Strategy **[NEW]**

Environments required: **Development · UAT · Training · Production · DR**.
Government organizations often mandate a dedicated **Training** environment.

## 11.2 Support & Operations Model **[NEW]**

Post-go-live BAU: who handles **user support, bug reports, change requests**, with
SLAs and escalation. *Distinct from the Phase 9.8 migration hypercare (which
fixes migration-specific issues for a fixed 30/60/90-day window).*

### Deliverables

* NFR specification (incl. capacity/growth, search, print/PDF, observability)
* Security, **legal & audit**, and **data-privacy** requirements
* **Document-storage & retention policy** (active + legacy boundary)
* **Environment strategy**
* **Support & operations model**
* **Test & Validation Strategy [NEW]** — payroll / migration / integration
  validation + UAT plan (validates the rules, integrations, migration and NFRs
  discovered across all phases)
* Hosting / architecture constraints

---

# Deliverables Before Development **[EXPANDED]**

1. HRMS User Manual
2. Payroll User Manual
3. Finance Process Documents
4. Sample Salary Slips
5. Sample Pay Bills
6. **Sample GPF/NPS/GIS/IT schedules, arrear bill, claim bills, pension papers [NEW]**
7. Sample Budget / Finance / UC Reports
8. Existing Database Schemas
9. Approval Hierarchies (per document type)
10. **User Role Matrix (role × scope × action) [EXPANDED]**
11. Data Migration Requirements (incl. opening balances + provenance)
12. Integration Requirements (per system spec)
13. **Master-data / rate tables with effective dates (DA/HRA/TA/PT/IT/GIS/matrix) [NEW]**
14. **NFR & compliance requirements [NEW]**
15. **Scope decisions (assets/inventory/procurement/recruitment in or out) [NEW]**

---

# Expected Outcome

At the end of discovery, the project team produces:

1. Business Requirement Document (BRD)
2. Software Requirement Specification (SRS) — functional + **non-functional**
3. Process Flow Diagrams (As-Is + To-Be)
4. Data Migration Plan (with parallel-run + cutover)
5. Integration Plan
6. **RBAC / Role-Permission Model + ESS scope [NEW]**
7. **Master-data & effective-dating design [NEW]**
8. Module-Wise Effort Estimation (reflecting the expanded scope)
9. Development Roadmap (phased per Phase 0.4)
10. ERP Architecture Design
11. **Test & Validation Strategy [NEW]** (payroll / migration / integration / UAT)

No development effort estimation should be finalized before completing the above
discovery activities. **Effort estimates must explicitly account for the v2
additions (Pension, Claims, Finance receipts, ESS/RBAC, integrations, NFRs) —
these were absent in v1 and materially change scope.**

---

# Appendix A: Domain Coverage Matrix (concept §01–19 → discovery phase)

| Domain area (learning §) | v1 | v2 phase |
|---|---|---|
| §01 Foundations / pay authority | partial | 1, 4.3 |
| §02 Employee Master & Service Book | partial | 3.2 |
| §03 Pay Matrix & Basic Pay | partial | 4.3 |
| §04 Pension-scheme determination (OPS/NPS) | **missing** | **4.2** |
| §05 Earnings & allowances (DA-on-TA) | partial | 4.1 |
| §06 Deductions (incl. GPF) | partial | 4.1 |
| §07 Increment / Fixation / MACP / CAS | partial | **4.4** |
| §08 Arrears (effective-dated recompute) | partial | 4.6 |
| §09 Leave (types + pay effect) | partial | 3.3 |
| §10 Attendance & Holiday Calendar | **missing** | **3.4** |
| §11 Claims & Reimbursements | **missing** | **4.7** |
| §12 Loans & Advances | partial | **4.8** |
| §13 Salary Bill / Treasury / Heads | partial | 4.5, 6.2 |
| §14 Period states / reconciliation | **missing** | **4.5** |
| §15 Statutory & compliance outputs | partial | **4.9, 10** |
| §16 Pension / Gratuity / DR / settlement | **missing** | **5** |
| §17 Master data / rate tables / reports | **missing** | 4.x, 10, Deliv. 13 |
| §18 Edge cases (suspension, LPC, death) | partial | 3.2, 4.5 |
| §19 ESS / RBAC / Data migration | **missing** | **7, 9** |

---

# Appendix B: Open Scope & Consistency Decisions to Confirm

1. **Name/scope alignment** — reconcile "Assam Agricultural University" (this
   plan) with the generic "Assam Government University" domain reference docs;
   capture AAU-specific rules (vacation-dept teachers, ICAR pay where applicable,
   KVK/research-station establishment, farm/lab revenue).
2. **Module in/out** — Recruitment, Asset/Inventory, Procurement, Stores: confirm
   each as in-scope or explicitly deferred.
3. **Pensioner payroll** — confirm AAU disburses pensions itself or via bank/treasury.
4. **Hosting & compliance mandate** — govt cloud vs on-prem; DPDP/CERT-In obligations.
5. **Tax regime defaults**, PT slabs, NPS cut-off date — confirm AAU-applicable values.
