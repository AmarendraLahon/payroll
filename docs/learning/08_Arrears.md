# Section 08 — Arrears

> Learning roadmap §08. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §13 (Arrear), §25 (Arrear calculation logic).
> This section is the **payoff for all the effective-dating** insisted on in
> Sections 03–07. Arrears are only computable *because* every rate, matrix, and
> position was versioned by date.

---

## 1. Purpose

Government pay decisions are routinely **back-dated**: a DA hike is announced in
October but effective from July; a promotion order issues in August but takes
effect from a date months earlier. The employee was **underpaid** for those past
months. **Arrear** is the retroactive payment of that difference.

The system must answer:

> "For each past month affected, what *should* the employee have been paid (under
> the new rate/position) versus what they *were actually* paid — and what's the
> total difference owed?"

This is impossible unless the engine can **recompute any past month with the
rules in force then** (the "rule in force in month M" service built across
Sections 03–07). Arrears are where that discipline pays off.

---

## 2. Governing Rules / Authority

- Arrears arise from the same authorities that set the original pay: **government
  DA orders, promotion/MACP/fixation orders, and pay-revision (ROP/CPC)
  notifications** — each carrying an **effective date earlier than its issue
  date**.
- Arrear payment is sanctioned via an **Arrear Bill** drawn through the DDO/
  treasury (Section 13).
- **Income Tax** treats arrears as **taxable in the year of receipt** (with
  **Section 89(1) relief** available to spread the tax burden back to the years
  it related to) — Section 15.

---

## 3. Core Concepts

### 3.1 What an arrear fundamentally is

```text
Arrear(month M) = new_amount(M) − paid_amount(M)
Total Arrear    = Σ over affected months
```

- `new_amount(M)` = recompute month M using the **revised** rate/Basic that is now
  effective in M.
- `paid_amount(M)` = what was **actually disbursed** in M (stored historical fact).

The difference, summed across all affected months, is the arrear.

### 3.2 The three trigger types

| Trigger | What changes | Span of affected months |
|---|---|---|
| **DA Arrear** | DA% raised with back-date | From DA effective date to now |
| **Promotion / MACP Arrear** | Basic re-fixed at higher Level from a back-date | From fixation effective date to now |
| **Pay Revision Arrear** | Whole matrix replaced (new ROP/CPC) | From revision effective date to now |

> **Example — DA arrear (most common):** DA goes 50% → 53%, **effective 1 Jul**,
> but **ordered 1 Oct**. For Jul, Aug, Sep the employee was paid at 50% but
> should have had 53%. The 3% × Basic for each of those three months is the DA
> arrear, paid in October's bill.

### 3.3 Arrears ripple through dependent components

Recomputing a month doesn't just change one line — it cascades:

- Higher Basic (promotion arrear) → higher **DA, HRA, TA** for those months too.
- Higher (Basic+DA) → higher **NPS 10%** (and employer 14%) → the **NPS schedule**
  for those months must be **topped up** (Section 13/14).
- Higher pay → possibly more **GPF** and definitely more **income tax**.

> **Example — promotion arrear cascade:** Back-dated promotion raises Basic from
> ₹21,100 to ₹25,500 for 5 past months. The arrear is **not** just 5 × (25,500 −
> 21,100). It's the difference in **Basic + DA + HRA + TA** across those months,
> minus the extra **NPS/GPF/tax** that should also have been deducted. An arrear
> engine that only diffs Basic is wrong.

### 3.4 Arrear is a net concept (earnings up, deductions up)

```text
Arrear(M) = (new earnings(M) − old earnings(M))
          − (new statutory deductions(M) − old deductions(M))
```

Because higher pay also means higher NPS/GPF/tax for those months, the **net**
arrear paid is less than the gross earnings difference, and the deduction
top-ups flow into the respective schedules.

### 3.5 Taxability

Arrears are taxed in the **year received**, which can bump the employee into a
higher slab. **Section 89(1) relief** lets them notionally spread the arrear back
to the relevant years to reduce tax. The system should produce the data
(year-wise arrear breakup) needed for that relief — Section 15.

---

## 4. Data Model

Arrears need **historical pay snapshots** to diff against — you cannot recompute
"what was paid" if you didn't store it.

```text
PayslipHistory (immutable, per employee per month)   ← the "paid_amount" source
  ├─ employee_code, month
  ├─ level, cell, basic, da, hra, ta, special
  ├─ gpf/nps, gis, pt, tds, recoveries
  ├─ gross, total_deductions, net
  └─ rate_versions_used (DA%, matrix version, etc.)

ArrearRun
  ├─ trigger : DA_REVISION | PROMOTION | MACP | PAY_REVISION
  ├─ effective_from, ordered_on
  └─ affected_employees[]

ArrearLine (per employee per affected month)
  ├─ month
  ├─ old_{basic,da,hra,ta,deductions,net}     (from PayslipHistory)
  ├─ new_{...}                                  (recomputed with revised rule)
  ├─ earnings_diff, deduction_diff, net_arrear
  └─ schedule_topups {nps, gpf, tds, ...}
```

Design rules:
- **PayslipHistory is immutable** and stores **which rate versions were used** —
  this is the ground truth for `paid_amount(M)`.
- Recompute uses the **same engine** as a normal month, just with the **revised**
  effective-dated rule — no separate "arrear formula".
- Each arrear line carries **deduction top-ups** routed to schedules
  (Section 13/14), not just a net figure.

---

## 5. Rules & Logic

### 5.1 The core algorithm (§25)

```text
compute_arrear(employee, trigger, effective_from):
    total = 0
    topups = {}
    for M in months(effective_from .. current):
        old = PayslipHistory[employee, M]                    # what was paid
        new = run_salary_engine(employee, M, use=revised_rule) # what should be
        earn_diff = new.earnings − old.earnings
        ded_diff  = new.statutory_deductions − old.statutory_deductions
        net_arr   = earn_diff − ded_diff
        total    += net_arr
        topups   += (new.nps−old.nps, new.gpf−old.gpf, new.tds−old.tds, ...)
    return ArrearBill(total, month_wise_lines, topups)
```

The key move: **`run_salary_engine(employee, M, use=revised_rule)`** is the
*ordinary* monthly computation (Sections 05–06) pointed at month M with the new
rule version. Arrears reuse everything; they don't reimplement it.

### 5.2 Output

- **Arrear Bill** with a **month-wise difference statement** (audit + treasury).
- **Schedule top-ups** for NPS/GPF/tax for the recovery months.
- **Year-wise breakup** for income-tax Section 89(1) relief (Section 15).

---

## 6. Worked Example (DA arrear, month-wise)

**Mr. Das**, Basic **₹25,500**. DA revised **50% → 53%**, effective **1 Jul**,
ordered in **October** (so Jul/Aug/Sep were underpaid).

Per-month DA difference = (53% − 50%) × 25,500 = 3% × 25,500 = **₹765**.
But the higher DA also raises **DA-on-TA**: TA slab ₹3,600 → extra DA = 3% ×
3,600 = **₹108**. So gross diff per month = 765 + 108 = **₹873**.

| Month | Old DA (50%) | New DA (53%) | DA diff | TA-DA diff | Gross arrear |
|---|---|---|---|---|---|
| Jul | 12,750 | 13,515 | 765 | 108 | 873 |
| Aug | 12,750 | 13,515 | 765 | 108 | 873 |
| Sep | 12,750 | 13,515 | 765 | 108 | 873 |
| **Total gross** | | | | | **2,619** |

Now the deduction top-up (if NPS): extra NPS = 10% × (DA diff 765) = ₹76.5/month
→ ~₹230 over three months (deducted from the arrear and added to the NPS
schedule).

```text
Net DA arrear ≈ 2,619 − 230 ≈ ₹2,389, paid in October's arrear bill,
with ₹230 topped into the NPS schedule for Jul–Sep.
```

> Change the trigger to a **back-dated promotion** and the same loop runs, but now
> Basic itself differs each month, so DA/HRA/TA/NPS/GPF/tax **all** differ — the
> arrear is far larger and the schedule top-ups span every contribution.

---

## 7. System Implications

- **Store an immutable PayslipHistory** for every employee-month, including the
  **rate versions used** — without it, arrears are uncomputable.
- **Reuse the salary engine** for recompute; never write a parallel "arrear
  formula". Arrears = (engine with revised rule) − (history).
- Compute arrears as a **net** of earnings diff and deduction diff; **top up the
  schedules** (NPS/GPF/tax) for affected months — don't just pay a net number.
- Produce a **month-wise difference statement** (treasury/audit) and a
  **year-wise breakup** (for IT §89(1), Section 15).
- A back-dated **ServiceEvent or rate-version** (Sections 03–07) should be able to
  **trigger an arrear run** automatically.
- Mark arrear income as **taxable in year of receipt** and feed Section 15.
- Make arrears **idempotent/re-runnable**: re-running for the same trigger must
  not double-pay (track what's already been arrear-settled).

---

## 8. Open Questions / State-Specific (confirm before build)

1. Whether **PayslipHistory** exists for legacy months at go-live, or arrears
   before the cutover must be handled manually (links to Section 19 migration).
2. Assam's treatment of **deduction top-ups** in arrears (are NPS/GPF arrears
   recovered from the arrear bill or separately?).
3. **Income Tax §89(1)** relief computation expectation — does the system produce
   Form 10E data?
4. Rounding convention for arrear differences (per-month vs on-total).
5. Whether **DA arrear** is paid in cash or **part-credited to GPF/NPS** (some
   orders credit a portion).
6. How **pay-revision (ROP) transition arrears** (6th→7th) are computed for staff
   who pre-date the system — fitment-factor based.
7. Handling of arrears for **retired/transferred** employees (pay via LPC/last
   unit).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Arrear** | Retroactive payment of an underpaid difference. *Note:* = recomputed − actually-paid, summed over affected months. |
| **Effective Date vs Order Date** | When a change applies vs when it was ordered. *Note:* the gap between them *is* the arrear period. |
| **DA Arrear** | Arrear from a back-dated DA% rise. *Note:* most frequent; also raises DA-on-TA. |
| **Promotion / MACP Arrear** | Arrear from back-dated re-fixation. *Note:* Basic changes → DA/HRA/TA/NPS/GPF/tax all change too. |
| **Pay Revision Arrear** | Arrear from a new matrix (ROP/CPC). *Note:* fitment-factor based; spans from revision date. |
| **new_amount(M) / paid_amount(M)** | Recomputed vs historically-paid for month M. *Note:* the two operands of every arrear line. |
| **PayslipHistory** | Immutable per-month pay record. *Note:* the source of `paid_amount`; must store rate versions used. |
| **Month-wise Difference Statement** | The arrear bill's per-month breakup. *Note:* required for treasury + audit. |
| **Schedule Top-up** | Extra NPS/GPF/tax for arrear months added to schedules. *Note:* arrears change deductions too, not just earnings. |
| **Net Arrear** | Earnings diff − deduction diff. *Note:* what's actually disbursed; less than gross diff. |
| **Section 89(1) / Form 10E** | Income-tax relief spreading arrear tax to original years. *Note:* needs year-wise arrear breakup (Section 15). |
| **Fitment Factor** | Old→new Basic multiplier at revision (7th CPC = 2.57). *Note:* drives pay-revision arrears for legacy staff. |
| **Idempotent arrear run** | Re-runnable without double-paying. *Note:* track already-settled arrears. |

---

### Status
Section 08 complete. Update roadmap tracker: 08 → ✅ Done.
Phase 3 (Salary Build-Up) complete. Next: **Section 09 — Leave Management** (Phase 4).
