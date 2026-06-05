# Section 09 — Leave Management

> Learning roadmap §09. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §14 (Leave Management), §33 (additional govt leave types).
> Phase 4 begins. Leave is not just an HR record — it is a **direct input to the
> salary engine** (some leave reduces pay) and to **pension** (some leave reduces
> qualifying service). This section connects leave to money.

---

## 1. Purpose

Leave management answers two questions the payroll engine needs every month:

1. **Balance** — does the employee have enough of the right leave type to cover
   their absence? (accrual, credit, debit, caps)
2. **Pay effect** — does this leave pay **full**, **half**, or **nothing**, and
   does it count as service?

> **Key reframing:** A leave system that only tracks balances is an HR toy. A
> *payroll* leave system must emit, for each absence, a **pay instruction**
> (full/half/nil + service-counting) that the salary engine (Section 05/06) and
> pension (Section 16) consume. That linkage is the heart of this section.

---

## 2. Governing Rules / Authority

- Leave is governed by **Assam Services (Leave) Rules / Fundamental Rules**,
  modelled on **CCS (Leave) Rules, 1972** (Section 01).
- **Teaching staff are "vacation department"** — because they get summer/winter
  vacation, their **EL entitlement is reduced** versus non-teaching staff. The
  teaching/non-teaching fork (§01) drives the accrual rule.
- Special leaves (Maternity/Paternity/CCL) follow **central DoPT-style orders**
  as adopted by the state.

> **Reminder:** the quantities below are common 7th-CPC/CCS practice. **Exact
> Assam figures are configurable** — store as accrual config (Section 16/17),
> never hard-code (§8).

---

## 3. Core Concepts

### 3.1 Leave types at a glance (with pay effect)

| Leave | Annual entitlement | Credit | Pay | Counts as service? |
|---|---|---|---|---|
| **Earned Leave (EL)** | 30 (non-teaching) | Half-yearly 15+15, advance | Full | Yes |
| **Casual Leave (CL)** | ~12 | Calendar year, no carry-fwd | Full | Yes |
| **Half Pay Leave (HPL)** | 20 | Half-yearly 10+10 | **Half** basic + DA on half | Yes |
| **Commuted Leave** | from HPL | 2 HPL = 1 commuted | Full | Yes |
| **Extraordinary Leave (EOL)** | as sanctioned | — | **Nil** | Usually no (dies-non) |
| **Maternity** | 180 days | — | Full | Yes (no debit) |
| **Paternity** | 15 days | — | Full | Yes (no debit) |
| **Child Care Leave (CCL)** | up to 730 (career) | — | Full yr1 / 80% yr2 | Yes (no debit) |
| **Study Leave** | up to ~24 months | — | Per rule | Per rule |
| **Duty Leave** | as needed | — | Full (on-duty) | Yes |
| **Special Casual Leave (SCL)** | purpose-based | — | Full | Yes (no debit) |
| **Compensatory Off** | earned | per holiday worked | Full (day off) | n/a |
| **Restricted Holiday (RH)** | ~2/yr | from RH list | Holiday | n/a |

### 3.2 Accrual & credit mechanics

- **EL**: credited **in advance** half-yearly (15 on 1 Jan, 15 on 1 Jul), capped
  at **300 days** accumulation; the excess lapses. Pro-rata for part-year service.
- **HPL**: credited 10+10 half-yearly; no upper cap like EL but availed at half
  pay (or commuted).
- **CL**: ~12/year, **lapses** at year-end, **no carry-forward**.

> **Example — EL advance credit:** On 1 Jan, 15 EL are credited *before* they're
> earned. If the employee retires/quits mid-year having used more than earned,
> the excess is **recovered**. The advance-credit model is why mid-year exits need
> a leave settlement (Section 16).

### 3.3 The pay-effect classification (the payroll link)

This is the table the salary engine actually consumes:

| Pay class | Leave types | Salary engine rule |
|---|---|---|
| **Full pay** | EL, CL, Maternity, Paternity, CCL(yr1), Commuted, Duty, SCL | No reduction |
| **Half pay** | HPL | Reduce: pay **half basic** + DA on that half for leave days |
| **80%** | CCL year 2 | Apply 0.8 factor for those days |
| **No pay** | EOL / LWP | Deduct full pay for leave days; mark **dies-non** |

> **Example — HPL hits the payslip:** 6 days HPL in a 30-day month → those 6 days
> paid at half basic. If Basic ₹25,500, per-day ≈ ₹850; half-pay loss ≈ 6 × ₹425
> = **₹2,550** reduction (plus proportionate effect on DA). The leave module must
> hand the salary engine "6 days HPL" so it can apply this.

### 3.4 Commuted leave conversion

HPL taken on **full pay** for medical grounds, but it **debits HPL at 2×**:

```text
1 day Commuted Leave = debits 2 days HPL balance, paid at full pay
```

> **Example:** Employee with 20 HPL balance takes 5 days **commuted** leave →
> full pay for 5 days, but **10 days** deducted from HPL balance.

### 3.5 EOL / dies-non — the pension echo

EOL is **leave without pay**. Beyond the immediate pay loss, it usually counts as
**dies-non** — not service — which (a) **shifts the increment date** (Section 07)
and (b) **reduces qualifying service** for pension (Section 16).

> This is the same EOL spell that has appeared in Sections 02, 07. Recorded once
> in the Service Book, consumed by leave-pay (here), increment (§07), and pension
> (§16). One fact, three consumers.

### 3.6 Additional govt leaves (§33)

- **Special Casual Leave (SCL)** — election duty, blood donation, sterilization,
  sports — full pay, **no debit** to CL/EL.
- **Compensatory Off** — earned for working a holiday/weekly-off; availed later;
  tracked with earn-date + expiry.
- **EL surrender (in-service encashment)** — encash a few EL days (e.g. up to 10/
  yr), often with LTC, **while still serving** (distinct from retirement
  encashment, Section 16).
- **Restricted Holidays (RH)** — optional from a published list (~2/yr), against
  the **Holiday Calendar** (Section 10).

### 3.7 Vacation department (teachers)

Teachers get **vacations** instead of full EL accrual → **reduced EL**. The
accrual engine must apply the right rule per `is_vacation_dept` (set in §01).

### 3.8 Approval workflow

```text
Employee → HOD → Registrar → Approval
```

The application captures type, dates, and reason; on approval, balance is
debited and a **pay instruction** is generated for the affected month(s).

---

## 4. Data Model

```text
LeaveType (reference/config)
  ├─ code : EL|CL|HPL|COMMUTED|EOL|MAT|PAT|CCL|STUDY|DUTY|SCL|COMPOFF|RH
  ├─ accrual : {rate, frequency, advance?, cap, carry_forward?}
  ├─ pay_class : FULL | HALF | EIGHTY | NIL
  ├─ counts_as_service : bool
  ├─ debits_balance : bool      (Mat/Pat/CCL/SCL = false)
  ├─ debit_multiplier : 1 or 2  (commuted = 2)
  └─ applies_to : staff_type / vacation_dept condition

LeaveBalance (per employee per type)
  ├─ employee_code, type, balance
  └─ last_credited_on

LeaveTransaction (ledger — append-only)
  ├─ employee_code, type, from_date, to_date, days
  ├─ action : CREDIT | DEBIT | LAPSE | ENCASH | RECOVER
  ├─ pay_instruction : {pay_class, service_days, dies_non?}
  ├─ approval_state, approver
  └─ recorded_by/at

HolidayCalendar (→ Section 10) for RH / comp-off / working-day basis
```

Design rules:
- Leave is a **ledger** (credits, debits, lapses) like GPF — balance is a
  projection, mirroring the §02 event-sourcing pattern.
- Each approved leave emits a **pay_instruction** consumed by the salary engine.
- `debits_balance=false` types (Maternity/CCL/SCL) don't touch EL/HPL balances.
- **Accrual config is data**, effective-dated; vacation-dept teachers use a
  different EL rule.

---

## 5. Rules & Logic

### 5.1 Half-yearly accrual (EL example)

```text
credit_EL(employee, on_date in {1 Jan, 1 Jul}):
    add 15 (pro-rata if part-period)
    if balance > 300: balance = 300            # cap, excess lapses
```

### 5.2 Apply leave to a salary month

```text
leave_pay_effect(employee, month):
    for each approved LeaveTransaction in month:
        if pay_class == FULL:   no change
        if pay_class == HALF:   reduce (basic/2 + DA on basic/2) × half_pay_days
        if pay_class == EIGHTY: apply 0.8 × per_day × days
        if pay_class == NIL:    deduct full per_day × days; mark dies_non
    feed reductions to salary engine (Section 05/06)
```

### 5.3 Commuted debit

```text
take_commuted(employee, days):
    require HPL_balance >= 2 × days
    HPL_balance -= 2 × days
    pay_class = FULL
```

---

## 6. Worked Example (leave → payslip)

**Mr. Das**, Basic ₹25,500, a 30-day month, takes during the month:
- 2 days **CL** (full pay), and
- 4 days **HPL** (half pay).

```text
Per-day basic            = 25,500 / 30 = 850
CL (2 days, full)        → no reduction
HPL (4 days, half)       → loss = 4 × (850 / 2) = 4 × 425 = 1,700
                           (plus proportionate DA reduction on the half)
This month's basic ≈ 25,500 − 1,700 = 23,800 (before DA recompute)
```

The leave module hands the salary engine: **"4 days HPL (half), 2 days CL
(full)"**. The engine reduces pay accordingly; deductions (NPS/GPF on the reduced
base) and net follow (Sections 05–06).

> **Contrast — EOL:** had those 4 days been **EOL** instead of HPL, the loss would
> be the **full** 4 × ₹850 = ₹3,400, *and* 4 days would be **dies-non** — nudging
> the increment date (§07) and shaving qualifying service (§16). Same 4 days,
> very different downstream cost, decided purely by leave *type*.

---

## 7. System Implications

- Model leave as a **ledger** (credit/debit/lapse/encash); balance is a
  projection — mirrors §02 event-sourcing.
- Every approved leave must emit a **pay instruction** (full/half/80/nil +
  service-counting) to the salary engine — this is the payroll linkage.
- **Advance EL credit** (15 on Jan/Jul) requires **recovery on mid-year exit** if
  over-availed (Section 16).
- Enforce **caps** (EL 300) and **carry-forward rules** (CL lapses).
- Implement **commuted 2× debit**, **no-debit** special leaves, and **dies-non**
  marking for EOL.
- Apply **vacation-department reduced EL** for teachers (`is_vacation_dept`).
- Keep **accrual quantities/caps in effective-dated config**, not code.
- Integrate the **Holiday Calendar** (Section 10) for RH, comp-off, and
  working-day/proration basis.
- Route applications through the **approval workflow** before balance debit.

---

## 8. Open Questions / State-Specific (confirm before build)

1. Exact **Assam EL/HPL/CL** entitlements, credit dates, and **EL cap** (300?).
2. **Vacation-department EL** figure for teachers in Assam.
3. **CCL** total (730?), year-2 pay (80%?), and conditions adopted by Assam.
4. **Maternity (180?) / Paternity (15?)** durations and conditions.
5. **EL in-service surrender** limit and LTC linkage.
6. **SCL** purposes and day-limits recognised by Assam.
7. **Compensatory-off** earn/expiry rules.
8. Leave **approval hierarchy** at this university (HOD → Registrar → ?).
9. Treatment of leave for **contractual/daily-wage** staff (often only limited CL).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Earned Leave (EL)** | Full-pay leave, advance-credited half-yearly, cap 300. *Note:* over-availed advance recovered on exit; teachers get reduced EL. |
| **Casual Leave (CL)** | ~12/yr full-pay, lapses yearly. *Note:* no carry-forward; can't combine with EL/HPL. |
| **Half Pay Leave (HPL)** | 20/yr at half basic + DA on half. *Note:* directly reduces the payslip; convertible to commuted. |
| **Commuted Leave** | Full-pay medical leave debiting HPL at **2×**. *Note:* 5 days commuted = 10 HPL gone. |
| **Extraordinary Leave (EOL/LWP)** | No-pay leave; usually **dies-non**. *Note:* full pay loss + shifts increment + cuts qualifying service. |
| **Maternity / Paternity / CCL** | Special leaves, full pay (CCL yr2 80%), **no balance debit**. *Note:* don't touch EL/HPL. |
| **Special Casual Leave (SCL)** | Purpose-based full-pay leave, no debit. *Note:* election/blood-donation/sports etc. |
| **Compensatory Off** | Day off earned for working a holiday. *Note:* tracked with earn-date + expiry. |
| **Restricted Holiday (RH)** | Optional holiday from a list (~2/yr). *Note:* against the Holiday Calendar (Section 10). |
| **EL Surrender (in-service encashment)** | Encashing a few EL days while serving. *Note:* distinct from retirement encashment (Section 16). |
| **Pay class (full/half/80/nil)** | The pay effect of a leave type. *Note:* the instruction the salary engine consumes. |
| **Dies-non** | Period not counting as service. *Note:* EOL effect; hits increment (§07) and pension (§16). |
| **Vacation Department** | Teachers with vacation → reduced EL. *Note:* accrual rule keyed to `is_vacation_dept` (§01). |
| **Leave Ledger** | Append-only credit/debit history. *Note:* balance is a projection; same pattern as §02. |
| **Pay Instruction** | The full/half/nil + service-days output of an approved leave. *Note:* the bridge from leave to payroll. |

---

### Status
Section 09 complete. Update roadmap tracker: 09 → ✅ Done.
Next: **Section 10 — Attendance & Holiday Calendar**.
