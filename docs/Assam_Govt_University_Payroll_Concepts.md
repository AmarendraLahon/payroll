# Assam Government University Payroll & Leave Management Concepts

## Overview

Most Assam Government Universities follow:

- UGC Pay Structure (Teaching Staff)
- State Government Pay Rules
- 7th Pay Commission Pay Matrix
- State Finance Department Rules
- GPF/NPS/Pension Rules

---

# Payroll Flow

```text
Employee Master
      ↓
Attendance
      ↓
Leave Processing
      ↓
Salary Calculation
      ↓
Allowances
      ↓
Deductions
      ↓
Arrear Calculation
      ↓
Salary Bill
      ↓
Treasury/Bank
      ↓
Payslip
```

---

# 1. Employee Master

## Common Fields

- Employee Code
- Employee Name
- Designation
- Department
- College
- Employee Type
- Date of Joining
- Retirement Date
- Pay Level
- Basic Pay
- Bank Account

## Employee Categories

### Teaching
- Professor
- Associate Professor
- Assistant Professor

### Non-Teaching
- Registrar
- Finance Officer
- Superintendent
- Assistant
- Driver
- Grade IV

### Contractual
- Consultant
- Project Staff
- Temporary Staff

### Daily Wage
- Casual Labour

---

# 2. Service Book

The Service Book is the lifelong employment record of an employee.

Contains:

- Joining
- Promotions
- Transfers
- Pay Fixation
- Leave Records
- Suspension
- Retirement

---

# 3. Pay Matrix

Under the 7th Pay Commission:

```text
Level 10
Level 11
Level 12
...
Level 14
```

Employees move through cells via annual increments.

---

# 4. Salary Components

## Earnings

- Basic Pay
- Dearness Allowance (DA)
- House Rent Allowance (HRA)
- Transport Allowance (TA)
- Medical Allowance
- Special Allowance
- Academic Allowance
- Project Allowance

## Deductions

- NPS
- GPF
- Income Tax (TDS)
- Professional Tax
- GIS
- Loan Recovery
- Advance Recovery

---

# 5. Basic Pay

Core salary component.

Most allowances and deductions are derived from Basic Pay.

---

# 6. Dearness Allowance (DA)

Compensation against inflation.

Keywords:

- DA Rate
- DA Effective Date
- DA Arrear

---

# 7. House Rent Allowance (HRA)

Depends on:

- City Classification
- Government Accommodation Status
- Rental Eligibility

Keywords:

- HRA
- Quarter Occupancy
- HRA Exemption

---

# 8. Transport Allowance (TA)

Provided for commuting.

Depends on:

- Pay Level
- Posting Location

---

# 9. Academic / University Specific Allowances

Examples:

- Academic Allowance
- Research Allowance
- Special Duty Allowance
- Examination Duty Honorarium
- Invigilation Payment

---

# 10. Deductions

## National Pension System (NPS)

Keywords:

- PRAN
- Employee Contribution
- Employer Contribution
- NPS Tier-I

## General Provident Fund (GPF)

Keywords:

- GPF Account Number
- Subscription
- Advance
- Withdrawal

## Group Insurance Scheme (GIS)

Monthly insurance deduction.

## Income Tax

Keywords:

- TDS
- Old Regime
- New Regime
- Form 12BB
- 80C
- 80CCD(1B)

---

# 11. Increment

Annual salary progression.

Keywords:

- Increment Date
- Normal Increment
- Withheld Increment
- Next Increment Date

---

# 12. Pay Fixation

Occurs due to:

- Promotion
- MACP
- Pay Revision

Keywords:

- Pay Fixation
- Option Form
- Fixation Statement

---

# 13. Arrear

Retroactive salary payment.

Examples:

- DA Arrear
- Promotion Arrear
- Pay Revision Arrear

Keywords:

- Arrear Bill
- Difference Calculation

---

# 14. Leave Management

> **Note on values:** The accrual quantities, caps, and ratios below reflect
> common 7th-CPC / CCS (Leave) Rules practice. Exact figures are governed by
> Assam Finance Department / university statutes and must be stored as
> **configurable values with effective dates** (see *Master Data & Rate Tables*).

## Earned Leave (EL)

| Attribute | Typical Value |
|---|---|
| Annual entitlement | 30 days |
| Credit frequency | Half-yearly (15 + 15), advance credit on 1 Jan / 1 Jul |
| Max accumulation | 300 days |
| Encashment | On retirement / LTC; capped at 300 days |
| Pay during leave | Full pay |

Keywords:

- EL Balance
- EL Credit
- EL Encashment
- Pro-rata Credit (for part-year service)

## Casual Leave (CL)

Short-term leave.

| Attribute | Typical Value |
|---|---|
| Annual entitlement | 12 days (calendar year) |
| Carry forward | Not allowed (lapses year-end) |
| Combine with | Cannot combine with EL/HPL; holidays not counted as CL |
| Pay during leave | Full pay |

Keywords:

- CL Balance
- CL Register

## Half Pay Leave (HPL)

| Attribute | Typical Value |
|---|---|
| Annual entitlement | 20 days |
| Credit frequency | Half-yearly (10 + 10) |
| Pay during leave | **Half** of basic + full DA on that half |
| Use | Medical grounds or private affairs |

Keywords:

- HPL Balance
- Medical Leave

## Commuted Leave

HPL taken on full pay for medical grounds. Conversion ratio: **2 days HPL = 1 day Commuted Leave** (debits HPL balance at 2×). Paid at full pay.

## Extraordinary Leave (EOL)

Leave without pay.

| Attribute | Typical Value |
|---|---|
| Pay during leave | Nil (LWP) |
| Effect | Counts as dies-non for increment/pension unless specially sanctioned |

Keywords:

- EOL
- LWP (Leave Without Pay)

## Maternity Leave

180 days (full pay), for up to two surviving children. Does not debit leave account.

## Paternity Leave

15 days (full pay), within 6 months of childbirth.

## Child Care Leave (CCL)

Up to 730 days over entire service (women employees; single male parent where applicable). First 365 days at full pay, next 365 days at 80% (per current orders). Does not debit leave account.

## Study Leave

Used for:

- Higher Studies
- Research
- Training

Typical max 24 months (extendable to 36 in career). Subject to bond/service obligation.

## Duty Leave

Used for:

- Conferences
- Workshops
- Academic Assignments

Treated as on-duty; full pay; does not debit leave account.

## Leave–Pay Interaction (Salary Engine Input)

| Leave Type | Pay Effect | Salary Calc Rule |
|---|---|---|
| EL, CL, Maternity, Paternity, CCL (yr 1), Commuted, Duty | Full pay | No salary reduction |
| HPL | Half basic + DA on half | Reduce basic for leave days |
| CCL (yr 2) | 80% | Apply 0.8 factor for those days |
| EOL / LWP | No pay | Deduct full pay for leave days; mark dies-non |

Leave year, accrual job, and the leave→pay reduction must be wired into the
monthly salary run, not handled manually.

---

# Leave Approval Workflow

```text
Employee
    ↓
HOD
    ↓
Registrar
    ↓
Approval
```

---

# 15. Attendance

May be:

- Leave-based attendance
- Biometric attendance
- Face recognition attendance

---

# 16. Loans and Advances

Examples:

- Festival Advance
- Vehicle Loan
- Computer Loan
- House Building Advance

Keywords:

- Principal
- Interest
- Installments

---

# 17. Pension

Applicable under pension rules.

Keywords:

- Pension
- Gratuity
- Leave Encashment
- Commutation

---

# 18. Salary Bill Generation

Documents:

- Salary Bill
- Salary Register
- Payslip
- Abstract Report

Schedules:

- GPF Schedule
- NPS Schedule
- GIS Schedule
- Income Tax Schedule

---

# 19. Treasury Concepts

Keywords:

- DDO (Drawing and Disbursing Officer)
- Treasury Code
- Bill Number
- Token Number
- Voucher Number

---

# 20. Reports

## Payroll Reports

- Pay Bill
- Salary Register
- Payslip
- Deduction Register

## Leave Reports

- Leave Balance Report
- Leave Ledger
- Leave Register

## Service Reports

- Service Book
- Promotion History
- Increment Report

## Finance Reports

- NPS Report
- GPF Report
- Income Tax Report

---

# Important Keywords

## Payroll

- Pay Matrix
- Pay Level
- Basic Pay
- Gross Salary
- Net Salary
- Arrear
- Pay Fixation
- Increment

## Leave

- EL
- CL
- HPL
- Commuted Leave
- EOL
- CCL
- Duty Leave

## Finance

- GPF
- NPS
- GIS
- TDS
- DDO

## Service

- Service Book
- Promotion
- Transfer
- Suspension
- Retirement

## Treasury

- Salary Bill
- Schedule
- Token Number
- Voucher Number

---

# 21. Pension Scheme Eligibility (NPS vs OPS/GPF)

The single most important branching rule in the system. It decides which
deduction set and which retirement-benefit path applies to an employee.

| Joining Date | Scheme | Retirement Deductions | Retirement Benefit |
|---|---|---|---|
| Before NPS cut-off date* | Old Pension Scheme (OPS) | GPF, GIS | Pension + Gratuity + Commutation |
| On/after NPS cut-off date* | National Pension System (NPS) | NPS (Tier-I), GIS | NPS corpus + Annuity |

> *The cut-off date for Assam state employees is set by State Finance Department
> notification. Store as a configurable system parameter — do not hard-code.
> An employee's scheme is derived from Date of Joining vs this parameter.

**Contribution rates (NPS):**

- Employee: 10% of (Basic + DA)
- Employer (Government): 14% of (Basic + DA)

Employer share is both a budget cost and a schedule line; the system must
compute and report it, not just the employee deduction.

---

# 22. Rules & Formulas (Salary Engine)

Each component needs five attributes: **base, rate source, formula, rounding,
effective date**. Values below are standard 7th-CPC structure; actual rates are
configurable and effective-dated.

## Earnings

| Component | Formula | Notes |
|---|---|---|
| Basic Pay | From Pay Matrix cell (Level × Index) | Driven by fixation/increment |
| Dearness Allowance | `Basic × DA%` | DA% from rate table, effective-dated |
| House Rent Allowance | `Basic × HRA%` | X/Y/Z city class = 24% / 16% / 8% (revised on DA triggers); nil if govt quarter occupied |
| Transport Allowance | Slab by Pay Level × posting city | `TA + (DA% × TA)` — DA applies on TA |
| Special / Academic / Project | Fixed or rule-based | Per university order |

## Gross / Net

```text
Gross Salary = Basic + DA + HRA + TA + other earnings
Total Deductions = NPS/GPF + GIS + Income Tax + Prof. Tax + Loan/Advance recovery
Net Salary = Gross Salary − Total Deductions
```

## Proration (mid-month join / leave / LWP)

```text
Payable Days Factor = Paid Days / Total Days in Month
Component (prorated) = Component (full) × Payable Days Factor
```

Applies to joining, retirement, death, transfer, and EOL/LWP days.

## Rounding

Define one rule per component (typically round to nearest rupee). Document it
once; the engine applies uniformly to avoid reconciliation mismatches.

---

# 23. Master Data & Rate Tables

Versioned, effective-dated reference data the engine reads at run time. Without
these the system cannot compute correctly or produce arrears.

- **Pay Matrix Grid** — full Level × Cell value table (7th CPC). Source for Basic, increment, fixation.
- **DA Rate Table** — DA% with effective date (history retained for arrears).
- **HRA Rate Table** — % per city class + city-classification master.
- **TA Slab Table** — amount by Pay Level and city category.
- **Professional Tax Slabs** — Assam-specific slab by salary range (statutory).
- **Income Tax Slabs** — old & new regime, per assessment year.
- **GIS Rate Table** — subscription + insurance split by group.
- **Leave Accrual Config** — entitlement, credit frequency, caps per leave type.
- **NPS/GPF Parameters** — contribution %, employer %, scheme cut-off date.

Rule: every rate row carries `effective_from` (and optional `effective_to`).
Salary for a past month always reads the rate effective in that month.

---

# 24. Increment & Pay Fixation Rules

## Increment (7th CPC)

- Two increment dates: **1 January** and **1 July**.
- Minimum 6 months service in the level on the increment date to qualify.
- Normal increment = move to next cell in the same Level (≈3% of Basic, per matrix).
- Withheld increment / dies-non from EOL can defer the next increment date.

## MACP (Modified Assured Career Progression)

Financial upgradation on stagnation, independent of promotion:

- Granted at **10, 20, 30 years** of continuous service.
- Moves employee to the next Pay Level in the matrix.
- Triggers a pay fixation event (with option-date choice).

## Pay Fixation

On Promotion / MACP / Pay Revision: one notional increment in current level,
then placement in the higher level; employee may **opt** for the fixation date
(date of event or next increment date). System records option form + fixation
statement and feeds the new Basic back into Employee Master with effective date.

---

# 25. Arrear Calculation Logic

Arrear = Σ over affected months of (recomputed amount − originally paid amount).

```text
For each month M in [effective_date .. current]:
    new_amount(M)  = recompute using rate/Basic effective in M
    paid_amount(M) = what was actually disbursed in M
    arrear(M)      = new_amount(M) − paid_amount(M)
Total Arrear = Σ arrear(M)
```

Triggers: DA revision, promotion/MACP fixation, pay revision. Output: Arrear
Bill with month-wise difference statement. Arrear is taxable in year of receipt
and feeds GPF/NPS schedules for the recovery months.

---

# 26. Payroll Period & Processing States

Payroll is periodic and must lock once disbursed.

```text
Draft → Verified (DDO) → Approved → Bill Submitted (Treasury)
      → Passed / Returned → Disbursed → Period Locked
```

- **Financial Year**: April–March; salary month is a first-class entity.
- **Period Lock**: once disbursed, the month is read-only; corrections go to a
  **Supplementary Bill** or next-month adjustment, never silent edits.
- **Treasury Return Loop**: a returned bill re-enters at Draft/Verified with
  reason captured (gap in the doc's one-way workflow arrow).
- **Reprocessing**: allowed only on unlocked periods.

---

# 27. Reconciliation & Post-Disbursement

- **Bank Return Handling** — failed/rejected credit → hold + reissue.
- **NPS Upload** — contribution file to NSDL/CRA; confirm SCF/PRAN posting.
- **GPF Posting** — subscriptions + interest credited to GPF ledger annually.
- **Schedule vs Bill Tie-out** — GPF/NPS/GIS/IT schedule totals must equal bill deductions.
- **Suspense / Recovery Carry** — under-recovery carried to next period.

---

# 28. Statutory & Compliance Outputs

| Output | Purpose |
|---|---|
| Form 16 | Annual TDS certificate to employee |
| Form 24Q | Quarterly TDS return (TRACES) |
| Form 12BB | Employee investment declaration (drives TDS projection) |
| GPF Annual Statement | Year-end GPF balance + interest |
| NPS Transaction Statement | PRAN-wise contribution record |
| Professional Tax Return | State statutory filing |
| Pension / Gratuity Papers | On retirement (see Pension section) |

**Monthly TDS projection:** estimate annual tax (gross − exemptions − Ch.VI-A
under chosen regime), divide by remaining months in the FY, deduct monthly;
recompute when declarations (12BB) or pay change.

---

# 29. Pension, Gratuity & Retirement Settlement (OPS)

For OPS employees (and applicable family-pension cases):

- **Qualifying Service** — service counted toward pension (excludes dies-non/EOL not condoned).
- **Pension** — `½ × last drawn (or 10-month average) emoluments × (qualifying service / max)`, subject to rules.
- **Commutation** — lump sum against a portion of pension (commutation factor by age).
- **Gratuity** — service gratuity / DCRG, subject to statutory ceiling.
- **Family Pension** — on death; enhanced then normal rate.
- **Leave Encashment** — EL balance (max 300) × (Basic + DA) / 30.

For NPS employees: corpus settlement + annuity per PFRDA rules.

---

# 30. Edge Cases & Special Handling

| Case | Handling |
|---|---|
| Suspension | Pay **Subsistence Allowance** (not regular pay), revised on prolonged suspension; settle on reinstatement |
| Negative net pay | Apply **deduction priority order**; carry unrecovered balance forward |
| Loan/Advance | Interest method (simple), recovery installments, foreclosure, recovery priority |
| Mid-month retire/death | Prorate; trigger settlement + leave encashment |
| Transfer between colleges | Issue **LPC (Last Pay Certificate)**; continue recovery/leave balances at new unit |
| Death in service | Family pension, DCRG, dues settlement, recovery waiver checks |
| Dies-non (EOL) | No pay, no service credit; defers increment/pension reckoning |
| Audit trail | All Service Book / pay / leave changes logged with who/when/old→new |

---

# 31. Additional Allowances & Reimbursements

Standard entitlements beyond the monthly allowances in Section 4. Most are
claim-based (paid on submission of bill/proof), not automatic monthly add-ons.

| Allowance | Type | Basis / Rule |
|---|---|---|
| Children Education Allowance (CEA) | Reimbursement | Per child, up to 2 children; fixed annual cap; hostel subsidy higher cap |
| Hostel Subsidy | Reimbursement | For children in hostel; separate higher ceiling than CEA |
| Leave Travel Concession (LTC) | Claim | Block-year based (Home Town / All-India); fare reimbursement; advance allowed; tied to leave |
| Tour TA/DA | Claim | Official travel: mileage/fare + Daily Allowance + lodging by pay level; distinct from monthly Transport Allowance |
| Overtime Allowance (OTA) | Earning | Grade IV / drivers; hours beyond duty × rate |
| Bonus / Ad-hoc Bonus / Ex-gratia | Earning | Festival/annual bonus for eligible non-gazetted staff; formula-capped |
| Medical Reimbursement | Claim | Actual medical expense vs fixed Medical Allowance |

Keywords:

- CEA, Hostel Subsidy
- LTC, Block Year, Home Town LTC, LTC Advance
- TA/DA, Daily Allowance, Mileage, Tour Bill
- OTA, Bonus, Ex-gratia

> CEA/LTC/TA-DA are processed as **separate claim bills** with their own
> approval flow, not always inside the monthly salary run. The system needs a
> claims module feeding both payment and the employee's pay record (for tax).

---

# 32. Pensioner Dearness Relief (DR)

The pension-side parallel of DA. Pensioners receive **Dearness Relief** on
basic pension, revised on the same cycle as DA for serving staff.

```text
DR Amount = Basic Pension × DR%
```

Keywords:

- Dearness Relief (DR)
- DR Rate, DR Effective Date
- Pension Revision

Belongs to the Pension module (Section 29); rate table shares the DA cadence.

---

# 33. Additional Leave Types (Government-Specific)

Supplements Section 14.

## Special Casual Leave (SCL)

Granted for specific sanctioned purposes — election/poll duty, blood donation,
sterilization, sports/cultural representation, natural-calamity. Full pay, does
**not** debit the CL/EL account.

## Compensatory Off (Comp-Off)

Earned for working on a gazetted holiday / weekly off. Availed later as a day
off. Tracked as a separate balance with earn-date and expiry.

## Surrender / Encashment of EL in Service

Encashment of a limited number of EL days (commonly up to 10/year) while still
in service, often tied to LTC. Distinct from retirement encashment (Section 29).

## Restricted Holidays (RH)

Optional holidays from a published list; employee may avail a fixed number
(commonly 2) per year. Tracked against the **Holiday Calendar master**.

Keywords:

- SCL, Comp-Off, RH
- EL Surrender, In-service Encashment

---

# 34. Holiday Calendar Master

Attendance (Section 15) and leave depend on a defined calendar.

- **Gazetted Holidays** — fixed, paid, non-working.
- **Restricted Holidays** — optional list (see Section 33).
- **Weekly Off** — Sunday / second Saturday etc., per university rule.
- **Working Day** — basis for proration and attendance.

Per-year, per-college calendar (a college may have local holidays). Drives
payable-day counts, comp-off eligibility, and CL/holiday adjacency rules.

---

# 35. Honorarium & Non-Regular Payments

Payment streams to people who are not regular monthly-salaried staff, or to
staff for extra duties.

| Payment | Recipient | Basis |
|---|---|---|
| Examination / Invigilation Honorarium | Staff + external | Per session / per script |
| Guest / Visiting Faculty Remuneration | Guest faculty | Per lecture / per hour |
| Part-time / Contractual Remuneration | Contract staff | Consolidated / hourly |
| Committee / Special Duty Honorarium | Staff | Per assignment |

Needs a remuneration master (rates per activity), a claim/sanction flow, TDS
(may be non-salary TDS), and bank payout — parallel to but separate from the
salary engine.

---

# 36. Additional Deduction Types

Beyond Section 10.

| Deduction | Trigger | Rule |
|---|---|---|
| Recovery of Overpayment | Excess salary paid earlier | Recover in installments; needs sanction; separate from loan |
| Court Attachment / Garnishee | Court order | Attach part of salary to a third party; statutory limits on attachable amount |
| Other Statutory Recovery | Govt order | e.g. license fee for govt quarter, water/electricity |

Each plugs into the **deduction priority order** and negative-net-pay handling
already noted in Section 30.

---

# 37. Service Events & Establishment

## Service Events (extend Service Book, Section 2)

- **Probation** — initial period; increment/confirmation may depend on it.
- **Confirmation** — regularization after probation.
- **Pay Protection** — protect last pay on appointment from another govt post.
- **Stepping Up of Pay** — remove anomaly where a junior draws more than senior.
- **Deputation** — service in another organization; deputation allowance.

## Establishment & Budget Heads

Govt payroll is tied to sanctioned posts and accounting classification.

- **Sanctioned Posts / Establishment** — approved strength per cadre; vacancy tracking.
- **Accounting Classification** — Major Head → Minor Head → Sub Head → **Object Head** (Salaries, DA, etc.); every bill line maps to a head.
- **Budget Allotment vs Expenditure** — control against sanctioned budget per head.

Keywords:

- Sanctioned Strength, Vacancy
- Major/Minor/Sub/Object Head
- Budget Allotment, Expenditure Control

---

# 38. System Concerns (Cross-Cutting)

## Employee Self-Service (ESS)

Employee-facing entry point feeding existing workflows:

- Apply for leave (feeds Section 14 approval flow)
- View / download payslip & Form 16
- Submit Form 12BB / investment declaration (feeds TDS projection, Section 28)
- View GPF/NPS balance, leave balance, service book

## Roles & Access Control (RBAC)

Distinct roles with scoped permissions:

- Employee (self-service)
- Dealing Assistant (data entry / bill prep)
- DDO (verification, sanction)
- Approver / Registrar
- Auditor (read-only)

Pairs with the audit trail in Section 30 (who changed what, old → new).

## Opening Balances & Data Migration (Go-Live)

One-time onboarding when the system starts, before any month can run:

- Opening leave balances (EL/HPL/CL) per employee
- GPF opening balance + interest
- Outstanding loan/advance principal & remaining installments
- Current pay fixation, Pay Level/cell, last increment date
- NPS PRAN / GPF account numbers, scheme assignment

Without a migration plan the system cannot produce a correct first payroll.

---

# Suggested Module Structure

1. Employee & Service Book Management *(scheme determination, probation/confirmation, audit trail)*
2. Leave & Attendance *(accrual engine, leave→pay interaction, holiday calendar, SCL/comp-off)*
3. Payroll Processing *(rate tables, salary engine, arrears, period lock)*
4. Claims & Reimbursements *(CEA, LTC, Tour TA/DA, honorarium, guest faculty)*
5. Treasury, Budget & Reconciliation *(bill states, accounting heads, returns, NPS/GPF posting)*
6. Statutory & Compliance Reporting *(Form 16/24Q/12BB, schedules)*
7. Pension & Retirement Management *(OPS settlement, NPS exit, gratuity, DR)*
8. Platform *(ESS portal, RBAC, audit, data migration)*
