# Section 13 — Salary Bill, Treasury & Budget Heads

> Learning roadmap §13. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §18 (Salary Bill Generation), §19 (Treasury Concepts), §37 (Establishment & Budget Heads).
> Sections 05–12 computed **what each individual is owed**. This section is about
> what happens **after** the per-employee math: rolling all employees into a
> **bill**, classifying every rupee against a **government accounting head**,
> generating the **schedules** that route deductions to GPF/NPS/GIS/IT, and
> pushing it through the **DDO → Treasury** disbursement machinery.

---

## 1. Purpose

A government does not pay salaries one bank transfer at a time off a manager's
say-so. It pays by **drawing a bill** on the **treasury**, against a **sanctioned
budget head**, certified by a **Drawing & Disbursing Officer (DDO)**. The payroll
system must produce that bill and its mandatory companions.

The questions this section answers:

> "For this month, what is the **consolidated bill** for this unit — total
> earnings, total deductions, net payable — broken down by **accounting head**,
> with the **schedules** (GPF/NPS/GIS/IT) that tell each agency who contributed
> what, and the **treasury identifiers** (bill no., token, voucher) that track it
> to disbursement?"

This is the bridge from **per-employee payslip** (micro) to **institutional
expenditure against budget** (macro). Both views must reconcile to the rupee.

---

## 2. Governing Rules / Authority

- **Treasury Rules / Financial Rules** (state) govern how bills are drawn,
  presented, and passed; the **DDO** is the statutory officer who draws pay.
- **Accounting classification** follows the government chart of accounts:
  **Major Head → Minor Head → Sub Head → Object Head** (e.g. Salaries, DA, HRA as
  object heads). Every bill line maps to a head.
- **Budget Allotment vs Expenditure control** — a head can only be drawn against
  to the extent of its **sanctioned allotment**; over-drawal is blocked.
- **Sanctioned Posts / Establishment** — pay can only be drawn for **sanctioned,
  filled** posts; vacancy is tracked against sanctioned strength.
- **Schedules** (GPF/NPS/GIS/IT) are mandated companions of the pay bill so each
  recovery reaches the right fund/agency.

---

## 3. Core Concepts

### 3.1 From payslips to a bill (the roll-up)

```text
Per-employee payslip (§05–12)  →  group by unit/DDO  →  Salary Bill
Bill totals  =  Σ earnings  −  Σ deductions  =  Σ net  (must tie out exactly)
```

The **Salary Bill** is the consolidated claim on the treasury for **net payable**;
the **deductions** don't leave the system as cash to employees — they're **routed
via schedules** to GPF/NPS/GIS/IT/recovery accounts.

### 3.2 The four bill documents (§18)

| Document | What it is | Audience |
|---|---|---|
| **Salary Bill** | The consolidated treasury claim (this unit, this month) | Treasury / audit |
| **Salary Register** | Employee-wise earnings/deductions/net grid | Establishment / audit |
| **Payslip** | One employee's monthly statement | Employee |
| **Abstract Report** | Head-wise / category summary totals | DDO / finance |

### 3.3 The schedules (§18) — where deductions go

Every statutory deduction collected in the bill must be **scheduled out** to its
destination:

| Schedule | Routes | Destination |
|---|---|---|
| **GPF Schedule** | GPF subscriptions + advances/refunds | GPF accounts (OPS staff) |
| **NPS Schedule** | 10% employee + 14% employer, PRAN-wise | NSDL/CRA (NPS staff) |
| **GIS Schedule** | Group Insurance premium | GIS fund |
| **Income Tax Schedule** | TDS deducted | IT dept (→ 24Q, Section 15) |

> **Key insight:** the schedules are why **employer NPS 14%** (§04) matters here
> even though it's *not* an employee deduction — the **NPS schedule** must carry
> **both** legs (employee 10% + employer 14%) PRAN-wise to NSDL. The bill funds the
> employer share as expenditure under its own object head.

### 3.4 Accounting classification (§37) — every line has a head

```text
Major Head  →  Minor Head  →  Sub Head  →  Object Head
(function)     (programme)    (scheme)      (Salaries / DA / HRA / Employer-NPS …)
```

Every earning line and the employer contributions map to an **Object Head**, so
the bill is simultaneously a **payroll document** and a **budget-expenditure
document**. The system must **tag each component with its head** and roll up
head-wise totals (the Abstract).

### 3.5 Establishment & budget control (§37)

- **Sanctioned Strength** per cadre vs **filled** posts → **vacancy** tracking.
- Pay drawn only for **sanctioned + filled** posts.
- **Budget Allotment vs Expenditure**: each head has an allotment; the month's
  bill **consumes** it; the system blocks/flags **over-drawal**.

### 3.6 Treasury identifiers & the bill lifecycle (§19 + §26)

The bill acquires tracking identifiers as it moves:

| Identifier | Stage |
|---|---|
| **Bill Number** | On bill generation (DDO) |
| **Token Number** | On presentation at treasury |
| **Voucher Number** | On the bill being passed |

```text
Draft → Verified (DDO) → Approved → Bill Submitted (Treasury)
      → Passed / Returned → Disbursed → Period Locked
```

A **Returned** bill loops back for correction; once **Disbursed**, the period is
**locked** — later corrections become **arrears** (Section 08), never edits. This
is the immutability discipline again (§08).

---

## 4. Data Model

```text
SanctionedPost (establishment)
  ├─ post_id, cadre, level, unit/college
  ├─ sanctioned_strength, filled_count
  └─ vacancy = sanctioned − filled

AccountingHead (chart of accounts, effective-dated §17)
  ├─ major, minor, sub, object        (object: SALARY|DA|HRA|TA|EMPLOYER_NPS|…)
  ├─ head_code
  └─ component_mapping[]               (which pay components post here)

BudgetAllotment (per head per FY)
  ├─ head_code, fy, allotment_amount
  └─ expenditure_to_date              (derived from posted bills)

SalaryBill (per unit/DDO per month)
  ├─ bill_no, period, ddo_code, treasury_code
  ├─ token_no, voucher_no             (acquired through lifecycle)
  ├─ status : DRAFT|VERIFIED|APPROVED|SUBMITTED|PASSED|RETURNED|DISBURSED|LOCKED
  ├─ gross_total, deduction_total, net_total
  └─ head_wise_totals[]               (the Abstract)

BillLine (per employee per bill)
  ├─ employee_code, earnings{}, deductions{}, net
  └─ head_tags[]                       (each component → AccountingHead)

Schedule (per bill, per type)
  ├─ type : GPF|NPS|GIS|IT
  └─ rows[] : payee/PRAN/GPF-no, amount(s)   (NPS: employee+employer legs)
```

Design rules:
- The **bill is immutable once disbursed**; corrections become **arrears** (§08).
- **Net total of the bill = Σ employee net** and **= gross − deductions** — a
  three-way reconciliation that must hold (Section 14 verifies it).
- **Every component carries a head tag**; head-wise totals are **derived**, not
  typed.
- **Budget expenditure is derived** from posted bills and checked against
  **allotment** before approval.
- **Schedules are generated from the same deduction lines** — never re-keyed.

---

## 5. Rules & Logic

### 5.1 Bill generation

```text
generate_bill(unit, month):
    lines = [payslip(emp, month) for emp in filled_posts(unit)]   # §05–12
    bill.gross     = Σ lines.earnings
    bill.deduction = Σ lines.deductions
    bill.net       = Σ lines.net
    assert bill.gross − bill.deduction == bill.net                # reconciliation
    bill.head_wise = rollup_by_head(lines)                        # Abstract
    for head in bill.head_wise:
        assert expenditure(head) + amount <= allotment(head)      # budget control
    schedules = build_schedules(lines)   # GPF/NPS(2 legs)/GIS/IT
    bill.status = DRAFT
```

### 5.2 Lifecycle transitions

```text
DRAFT →(DDO verify)→ VERIFIED →(approve)→ APPROVED →(present)→ SUBMITTED[+token_no]
→ PASSED[+voucher_no] → DISBURSED → LOCKED
RETURNED → back to DRAFT/VERIFIED for correction (no silent edit after DISBURSED)
```

### 5.3 Post-disbursement

```text
on DISBURSED: lock period (§14), post expenditure to heads, release schedules
              to GPF/NSDL/GIS/IT, hand net to bank payout file.
any later correction → ARREAR run (§08), never an edit to a locked bill.
```

---

## 6. Worked Example (a 3-employee unit bill)

Unit with **Mr. Das (NPS)**, **Dr. Sharma (NPS)**, **Mr. Roy (OPS/GPF)** —
illustrative June figures:

| Employee | Gross | Deductions | Net |
|---|---|---|---|
| Mr. Das | 45,690 | 6,893 | 38,797 |
| Dr. Sharma | 1,28,000 | 22,400 | 1,05,600 |
| Mr. Roy | 52,000 | 11,500 | 40,500 |
| **Bill total** | **2,25,690** | **40,793** | **1,84,897** |

Reconciliation: `2,25,690 − 40,793 = 1,84,897` ✓ (= Σ net).

**Schedules generated from the same deduction lines:**
```text
NPS Schedule : Das + Sharma — each with employee 10% AND employer 14% leg, PRAN-wise → NSDL
GPF Schedule : Roy — subscription + any advance refund → GPF account
GIS Schedule : all three — premium → GIS fund
IT  Schedule : whoever had TDS → IT dept (feeds 24Q, §15)
```

**Head-wise Abstract (budget view):**
```text
Object Head SALARIES (Basic)        Σ basics
Object Head DA                      Σ DA
Object Head HRA                     Σ HRA
Object Head EMPLOYER-NPS            Σ 14% legs   ← expenditure, not a deduction
… each checked against its allotment before APPROVED.
```

```text
Bill no. assigned at DRAFT → DDO verifies → APPROVED (budget OK) → SUBMITTED
(token no.) → PASSED (voucher no.) → DISBURSED → June LOCKED.
Find an error in July? → it's an ARREAR (§08), not an edit to June.
```

> The **same ₹1,84,897 net** that is "three payslips" to employees is "one
> treasury claim against budget heads" to finance. Micro and macro tie to the
> rupee — that's the whole job of this section.

---

## 7. System Implications

- **Roll per-employee payslips into a unit/DDO bill**; enforce the three-way
  reconciliation `gross − deductions = net = Σ employee net`.
- Generate the **four documents** (Bill, Register, Payslip, Abstract) and the
  **four schedules** (GPF/NPS/GIS/IT) **from the same lines** — never re-key.
- Carry the **NPS schedule with both legs** (employee 10% + employer 14%),
  PRAN-wise; fund the **employer share** under its own **object head**.
- **Tag every component with an accounting head**; derive head-wise totals;
  **check expenditure against budget allotment** before approval.
- Track **sanctioned strength vs filled vs vacancy**; draw pay only for
  **sanctioned + filled** posts.
- Implement the **bill lifecycle** with **treasury identifiers** (bill/token/
  voucher) and a hard **lock on disbursement** — post-lock corrections are
  **arrears (§08)**, never edits.
- On disbursement, **post expenditure** to heads, **release schedules** to the
  agencies, and emit the **bank payout file** for net.
- Support **LPC / transfer** carry-over so a mid-period mover's pay and loan
  balances (§12) land on the right unit's bill (links §18 edge cases).

---

## 8. Open Questions / State-Specific (confirm before build)

1. Assam treasury's exact **bill formats** and whether submission is via a state
   portal (e.g. an IFMS/treasury system) with prescribed schemas.
2. The **accounting head structure** (major/minor/sub/object codes) actually used
   for university salaries, and the **component → head** mapping.
3. Whether the university is **DDO-based** (draws on treasury) or runs on its own
   **funds/grant** (bank-based payout) — changes the lifecycle.
4. **NPS remittance** mechanism — NSDL/CRA upload format, employer-share funding
   head, and timing.
5. **GPF/GIS** schedule formats and destinations.
6. **Budget allotment** granularity and the over-drawal control rule (block vs
   warn).
7. **Sanctioned-post** master source and vacancy reporting needs.
8. **Bill numbering / token / voucher** conventions and who assigns them.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Salary Bill** | Consolidated monthly treasury claim for a unit. *Note:* net total = Σ employee net = gross − deductions. |
| **Salary Register** | Employee-wise earnings/deductions/net grid. *Note:* establishment/audit document. |
| **Abstract Report** | Head-wise / category summary totals. *Note:* the budget-expenditure view of the bill. |
| **Schedule (GPF/NPS/GIS/IT)** | Deduction routing list to each agency/fund. *Note:* built from the same deduction lines; NPS carries both legs. |
| **DDO** | Drawing & Disbursing Officer. *Note:* statutory officer who draws/certifies pay bills. |
| **Treasury Code** | Identifier of the treasury a DDO draws on. *Note:* on every bill. |
| **Bill / Token / Voucher Number** | Lifecycle tracking IDs. *Note:* bill@generate, token@present, voucher@passed. |
| **Major/Minor/Sub/Object Head** | Government accounting classification. *Note:* every pay component maps to an object head. |
| **Object Head** | Lowest classification (Salaries, DA, HRA, Employer-NPS). *Note:* what a bill line posts against. |
| **Budget Allotment** | Sanctioned spend per head per FY. *Note:* bill consumes it; over-drawal blocked/flagged. |
| **Expenditure Control** | Drawing limited to allotment. *Note:* checked before APPROVED. |
| **Sanctioned Strength / Vacancy** | Approved posts vs filled. *Note:* pay only for sanctioned + filled posts. |
| **Employer NPS (in bill)** | 14% employer share as expenditure. *Note:* not a deduction; own object head; on NPS schedule. |
| **Bill Lifecycle** | Draft→…→Disbursed→Locked. *Note:* post-lock change = arrear (§08), not edit. |
| **Reconciliation (3-way)** | gross − deductions = net = Σ employee net. *Note:* must hold exactly (verified §14). |
| **LPC (Last Pay Certificate)** | Pay+recovery state carried on transfer. *Note:* lands mover on correct unit's bill (§12/§18). |

---

### Status
Section 13 complete. Update roadmap tracker: 13 → ✅ Done.
Next: **Section 14 — Payroll Period, States & Reconciliation** (closes Phase 5).
