# Indian / Assam Govt University Payroll — Learning Roadmap

Goal: understand the full payroll + leave domain before building the system.
Source concepts: `../Assam_Govt_University_Payroll_Concepts.md` (Sections 1–38).

Each section below becomes one detailed document in this `learning/` folder,
built **one at a time** in the order shown. Order follows dependency —
later sections assume earlier ones.

---

## How each section document is structured

Every section doc follows the same template for consistency:

1. **Purpose** — what this concept is, why it exists.
2. **Governing Rules / Authority** — which Act/order/commission governs it.
3. **Core Concepts** — definitions, terminology.
4. **Data Model** — entities, fields, relationships needed to store it.
5. **Rules & Formulas** — exact logic, rates, effective-dating, edge cases.
6. **Worked Examples** — concrete numbers end-to-end.
7. **System Implications** — what the software must do, validations, states.
8. **Open Questions / State-Specific** — Assam values to confirm before build.
9. **Keywords / Glossary**.

---

## Roadmap (build order)

### Phase 1 — Foundations
| # | Section | Covers (concept doc §) |
|---|---|---|
| 01 | Foundations & Governance | Pay structures (UGC, State Rules, 7th CPC), Finance Dept, GPF/NPS/Pension rule sources (Overview) |
| 02 | Employee Master & Service Book | §1, §2, §37 (service events: probation, confirmation, pay protection, stepping-up, deputation) |
| 03 | Pay Matrix & Basic Pay | §3, §5 |

### Phase 2 — The Core Branching Rule
| # | Section | Covers |
|---|---|---|
| 04 | Pension Scheme Determination (NPS vs OPS/GPF) | §21: joining-date cut-off, which deduction/benefit path |

### Phase 3 — Salary Build-Up
| # | Section | Covers |
|---|---|---|
| 05 | Earnings & Monthly Allowances | §4 (earnings), §6–9, §22: Basic, DA, HRA, TA, academic/special + formulas |
| 06 | Deductions | §4 (deductions), §10, §36: NPS/GPF/GIS/IT/PT + overpayment recovery, court attachment |
| 07 | Increment, Pay Fixation & MACP | §11, §12, §24 |
| 08 | Arrears | §13, §25: month-wise difference logic |

### Phase 4 — Leave & Attendance
| # | Section | Covers |
|---|---|---|
| 09 | Leave Management | §14, §33: all leave types, accrual, leave→pay interaction, SCL, comp-off, EL surrender, RH |
| 10 | Attendance & Holiday Calendar | §15, §34: leave-based/biometric/face, holiday calendar master |

### Phase 5 — Claims & Money Movement
| # | Section | Covers |
|---|---|---|
| 11 | Claims & Reimbursements | §31, §35: CEA, hostel subsidy, LTC, Tour TA/DA, OTA, bonus, honorarium, guest/part-time faculty |
| 12 | Loans & Advances | §16 |
| 13 | Salary Bill, Treasury & Budget Heads | §18, §19, §37: bill, schedules, DDO/treasury codes, establishment, accounting heads |
| 14 | Payroll Period, States & Reconciliation | §26, §27: lifecycle, locking, bank/NPS/GPF posting |

### Phase 6 — Compliance & Exit
| # | Section | Covers |
|---|---|---|
| 15 | Statutory & Compliance Outputs | §28: Form 16/24Q/12BB, TDS projection |
| 16 | Pension, Gratuity, DR & Retirement Settlement | §17, §29, §32: OPS settlement, NPS exit, gratuity, encashment, Dearness Relief |

### Phase 7 — Cross-Cutting & Platform
| # | Section | Covers |
|---|---|---|
| 17 | Master Data, Rate Tables & Reports | §20, §23: versioned effective-dated rates, all reports |
| 18 | Edge Cases & Special Handling | §30: suspension, negative net, transfer/LPC, death-in-service, audit trail |
| 19 | Platform — ESS, RBAC & Data Migration | §38: self-service portal, roles/access control, opening balances, go-live migration |

---

## Concept-section → Learning-section coverage map

Confirms all 38 concept sections are covered.

| Concept § | Learning # | Concept § | Learning # |
|---|---|---|---|
| Overview | 01 | §20 Reports | 17 |
| §1 Employee Master | 02 | §21 Scheme Eligibility | 04 |
| §2 Service Book | 02 | §22 Rules & Formulas | 05 |
| §3 Pay Matrix | 03 | §23 Master Data | 17 |
| §4 Salary Components | 05 / 06 | §24 Increment/Fixation | 07 |
| §5 Basic Pay | 03 | §25 Arrear Logic | 08 |
| §6 DA | 05 | §26 Period & States | 14 |
| §7 HRA | 05 | §27 Reconciliation | 14 |
| §8 TA | 05 | §28 Statutory Outputs | 15 |
| §9 Academic Allowances | 05 | §29 Pension Settlement | 16 |
| §10 Deductions | 06 | §30 Edge Cases | 18 |
| §11 Increment | 07 | §31 Additional Allowances | 11 |
| §12 Pay Fixation | 07 | §32 Pensioner DR | 16 |
| §13 Arrear | 08 | §33 Additional Leave | 09 |
| §14 Leave Mgmt | 09 | §34 Holiday Calendar | 10 |
| §15 Attendance | 10 | §35 Honorarium | 11 |
| §16 Loans & Advances | 12 | §36 Additional Deductions | 06 |
| §17 Pension | 16 | §37 Service Events/Establishment | 02 / 13 |
| §18 Salary Bill | 13 | §38 System Concerns | 19 |
| §19 Treasury | 13 | | |

---

## Progress Tracker

| # | Section | Status |
|---|---|---|
| 01 | Foundations & Governance | ✅ Done |
| 02 | Employee Master & Service Book | ✅ Done |
| 03 | Pay Matrix & Basic Pay | ✅ Done |
| 04 | Pension Scheme Determination | ✅ Done |
| 05 | Earnings & Monthly Allowances | ✅ Done |
| 06 | Deductions | ✅ Done |
| 07 | Increment, Fixation & MACP | ✅ Done |
| 08 | Arrears | ✅ Done |
| 09 | Leave Management | ✅ Done |
| 10 | Attendance & Holiday Calendar | ☐ Not started |
| 11 | Claims & Reimbursements | ☐ Not started |
| 12 | Loans & Advances | ☐ Not started |
| 13 | Salary Bill, Treasury & Budget Heads | ☐ Not started |
| 14 | Payroll Period & Reconciliation | ☐ Not started |
| 15 | Statutory & Compliance | ☐ Not started |
| 16 | Pension, DR & Retirement Settlement | ☐ Not started |
| 17 | Master Data & Reports | ☐ Not started |
| 18 | Edge Cases & Special Handling | ☐ Not started |
| 19 | Platform — ESS, RBAC & Migration | ☐ Not started |

Update Status to ✅ Done as each section doc is completed.
