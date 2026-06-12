# Visit Closure Document

**Project:** Assam Agricultural University (AAU) — Unified ERP & Payroll System
**Document type:** Initial Study — Visit Closure & Handover
**Prepared by:** Bohniman Systems Private Limited (BSPL)
**Date of issue:** 09 June 2026
**Visit dates:** 8 – 9 June 2026
**Version:** 1.0 (Draft for client acknowledgement)

---

## 1. Purpose of this Document

This document closes the **initial study visit** conducted at AAU. It records what
was observed and understood, states the assumptions and scope boundaries on which
our subsequent work will be based, and lists the inputs we require from the
University to proceed.

It is **not** a proposal, a contract, or a price quotation. The commercial
budget and cost estimate will be submitted after the detailed analysis and online
clarification meetings described in Section 8.

We request the University to **review and acknowledge** this document (Section 10)
so that both parties share a common baseline before the next phase begins.

---

## 2. Visit Summary

| Item | Detail |
|---|---|
| Objective | Initial study of existing systems and processes; scoping for an ERP/Payroll replacement; basis for budgeting |
| Location | Assam Agricultural University, [campus] |
| Duration | 8 – 9 June 2026 |
| Method | Stakeholder discussions, system walkthroughs, review of existing modules |

**Participants — BSPL side:**
- Polen Patowary (Project Head)
- Amarendra Lahon (Team Lead)
- Mrinmoy Dutta (Senior Software Developer)

**Participants — University side:** [to be filled]

*(University participants to be completed and confirmed.)*

---

## 3. Our Understanding of the Engagement

The University intends to replace its current fragmented systems with a single,
web-based ERP platform. Based on the initial study, we understand the landscape
as follows:

**Existing systems observed**
- **HRMS** — employee/faculty master, departments, courses, service, leave and
  related data. This is the most actively and correctly used system today.
- **Payroll** — salary structure (maintained pay-grade wise), deductions, bill
  generation.
- **Finance / fund processes** — budget, funds and treasury interaction, largely
  maintained offline.

**Cross-cutting characteristics**
- The system is **master-driven**: funds, budget heads, pay scales, designations,
  formulas and deductions are maintained as dynamic master entries and mapped
  together to form operating settings.
- **PAN and email** act as the linking identifiers across sub-systems and with
  external agencies.
- Several listed modules exist on paper but are not all actively used; this will
  be confirmed during detailed analysis.

A High-Level Design (architecture and workflow) reflecting this understanding has
been prepared and presented separately during the visit.

---

## 4. Scope Understanding (to be confirmed)

The proposed platform is understood to cover three connected systems plus
supporting modules. Final scope and phasing will be confirmed after clarification.

**Core systems**
1. **Payroll** — master-driven salary calculation, dynamic deductions, payslips,
   annual reports, bill generation, increments, corrections and arrears.
2. **EFMS (E-File Movement System)** — access-based file routing, multiple user
   types and access levels, full lifecycle log, reporting-officer notifications.
3. **FOC (Fixation of Ceiling)** — multiple fund sources, fund-to-head mapping,
   purpose-bound allocation and ceiling control.

**Supporting modules (phasing to be decided)**
- HRMS, Pension & Retirement, GPF, Leave, Claims, Loans & Advances,
  Asset & Estate, Store & Purchase, Budget Management, Finance & Accounts,
  Establishment, User Management, Bill Tracking, Employee Portal (ESS).

> Indicative phasing — a **Phase 1 core** (payroll engine, masters, deductions,
> payslip, bill generation, HRMS reuse) and a **Phase 2 dependent scope** (EFMS,
> FOC/fund reconciliation, pension, full loan lifecycle, offline modules,
> external integrations). This is indicative only and subject to confirmation
> during detailed analysis.

---

## 5. Assumptions & Exclusions

The following are our current working assumptions. They will be validated during
detailed analysis; any change may affect scope, timeline and cost.

**Assumptions**
- Existing HRMS data is reasonably complete and usable as a primary source.
- PAN is available and unique for employees and can serve as a key identifier.
- The University will provide access to required data, samples and personnel.
- Salary, fund and formula logic in the current systems can be made available for
  reverse-engineering (see Section 7, vendor handover).

**Exclusions (unless later agreed in scope)**
- **TA/DA** is handled in a separate billing module and is outside the salary
  engine; it is not part of the monthly salary calculation.
- **Inventory / Store management**, currently maintained offline, is excluded from
  the initial phase unless explicitly requested.
- Modules confirmed as unused will not be rebuilt by default.
- Hardware, network/connectivity provisioning and third-party licence costs are
  not part of the software scope unless specified.

A full assumptions/exclusions register will accompany the BRD.

---

## 6. Open Points Requiring Clarification

Several points from the initial study are uncertain, contradictory, or unscoped
and must be resolved before a reliable estimate can be produced. The key items:

1. **Fund source & actual disbursal** — fund-to-head mapping is described, yet a
   gap was noted in tracking the actual source of funds. The real flow must be
   confirmed.
2. **Module reality** — which of the listed modules are live, partial, unused or
   offline.
3. **Formula engine governance** — who authors formulas, versioning, and whether
   mid-year changes recompute prior months.
4. **Scope boundaries** — income-tax (deduction only vs full statutory
   compliance), loans (full lifecycle vs deduction line), pension (integrated vs
   handoff), and EFMS vs the salary-bill workflow (one engine or two).

A complete, itemised question set has been prepared and will be circulated to the
relevant officers ahead of the online meetings.

---

## 7. Inputs Required from the University

To carry out detailed analysis and produce the budget, we request the following.
Owners and a target date should be assigned to each.

**7.1 Documents & samples** *(real, filled examples — not blank templates)*
- A real payslip, a real salary/pay bill as sent to treasury
- 2–3 real calculation-formula definitions from the master
- Fund-source list and one project's funding-to-disbursal paper trail
- JSON schema dumps (qualification, employment, research profiles)
- The 8 appraisal formats
- EFMS role / access-level definitions
- Sample loan schedule and GIS/LIC/SSS deduction sheets
- A sample arrear / salary-correction case
- Master-table list (DDO, designation, grade, fund type, budget head, discipline,
  nature type, payscale, deduction breakup)
- Retirement-age rules (by cadre/designation)
- Module usage-status sheet (live / partial / unused / offline) for all modules

**7.2 Existing-vendor handover** *(time-critical)*
We request that the University formally instruct the current HRMS and Payroll
vendor(s) to release, ideally via a contractual or exit clause:
- Database schema / ER diagrams
- Stored procedures and scheduled/batch jobs
- Report SQL and integration specifications

> The genuine business logic (salary rules, rounding, arrears, fixation) typically
> resides in this code, not in any manual. Securing it early is essential and is
> often delayed when a vendor is being replaced.

**7.3 People — SMEs & decision authority**
- Nomination of subject-matter experts for HR, Payroll, Finance and IT for the
  online clarification meetings.
- Nomination of **decision-making authorities** empowered to confirm requirements
  and sign off scope, to avoid conflicting inputs later.

**7.4 Data privacy & secure transfer**
The data involved includes sensitive personal information (PAN, Aadhaar). We will
treat all shared data as **confidential** and request agreement on a secure method
of transfer for any sample data. A confidentiality/NDA undertaking can be executed
if required.

---

## 8. Solution Approach (high level)

Our approach for the next stage:

1. **Detailed analysis** at our office using the materials collected.
2. **Online clarification meetings** with the nominated SMEs to resolve the open
   points in Section 6.
3. **Baselined requirement document (BRD)** with confirmed scope and phasing.
4. **Budget & cost submission** based on the agreed scope.

The proposed High-Level Design illustrates the target architecture: a layered
platform with role-based access, a master-driven payroll/rule engine, workflow and
audit services, and controlled integration with treasury, bank, NPS and tax
systems.

---

## 9. Communication Plan

| Role | University | BSPL |
|---|---|---|
| Single point of contact | | Amarendra Lahon |
| Escalation | | Polen Patowary |
| Meeting channel | | — |

All decisions taken during clarification meetings will be recorded in a shared
decision log and confirmed in writing.

---

## 10. Acknowledgement

This document records a shared understanding of the initial study. It is not a
commercial commitment. Acknowledgement confirms agreement on the understanding,
assumptions and required inputs described above.

| | University | BSPL |
|---|---|---|
| Name | | |
| Designation | | |
| Signature | | |
| Date | | |

---

*Prepared on the basis of the initial study visit. Contents are subject to
confirmation during detailed requirement analysis.*
