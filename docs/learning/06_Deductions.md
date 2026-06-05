# Section 06 — Deductions

> Learning roadmap §06. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §4 (deductions), §10 (NPS/GPF/GIS/IT), §36 (overpayment recovery, court
> attachment).
> Section 05 built **Gross**. This section subtracts from it to reach **Net** —
> and which deductions apply forks on the **OPS/NPS branch from Section 04**.

---

## 1. Purpose

```text
Net Salary = Gross Salary − Total Deductions
```

Deductions fall into three buckets, and the system must apply the **right set**
to the **right employee** in the **right order**:

1. **Scheme-driven** — GPF (OPS) **or** NPS (post-cutoff) — the fork from §04.
2. **Universal statutory** — GIS, Income Tax (TDS), Professional Tax — apply to
   (almost) everyone.
3. **Recoveries** — loans/advances, overpayment, court attachment, quarter
   licence fee — situational.

Getting deductions wrong doesn't just mis-pay the employee; it breaks the
**schedules** that go to GPF/NPS/IT authorities (Section 13/14) and can create
under-recovery that snowballs.

---

## 2. Governing Rules / Authority

- **GPF** → GPF (Assam Services) Rules; **NPS** → PFRDA/CRA rules (Section 04).
- **GIS** (Group Insurance Scheme) → state GIS scheme rules.
- **Income Tax / TDS** → **Income Tax Act, 1961** (central; deduction-at-source
  on salary). Full computation logic is **Section 15** — here we only place it in
  the deduction stack.
- **Professional Tax** → **state** tax on professions (Assam levies it; slab by
  income). A statutory deduction with a small monthly cap.
- **Court attachment** → by **court order** under civil procedure; only a limited
  portion of pay is attachable.
- **Overpayment recovery** → under FR/financial rules, requires a sanction.

---

## 3. Core Concepts

### 3.1 The deduction stack (and the fork)

```text
                         Gross Salary (§05)
                                 │
        ┌────────────── scheme-driven (from §04) ──────────────┐
   OPS employee                                         NPS employee
   GPF subscription                                NPS Tier-I (10% of Basic+DA)
        └──────────────────────┬───────────────────────┘
                               │
                universal statutory (both schemes)
                GIS · Income Tax (TDS) · Professional Tax
                               │
                        recoveries (situational)
        Loan/Advance EMI · Overpayment · Court attachment · Quarter licence fee
                               │
                        Total Deductions → Net Salary
```

### 3.2 GPF — OPS only

Employee chooses a **subscription** (within rule limits, a min %/max of pay).
It's the employee's **own savings**, returned with **interest** at exit. Supports
**advance** (refundable) and **withdrawal** (non-refundable, for specified
purposes). No employer match.

> **Example:** OPS employee subscribes ₹6,000/month to GPF. It reduces this
> month's net pay but is *his money* growing with interest — not a true "cost"
> like tax. Advances taken are recovered as additional GPF deductions.

### 3.3 NPS — post-cutoff only

**Employee 10% of (Basic + DA)** deducted to PRAN. (The **employer 14%** is a
government cost + schedule, **not** a salary deduction — see §04.)

> **Example:** Basic ₹25,500 + DA ₹12,750 = ₹38,250 → NPS deduction = ₹3,825.
> A GPF employee at the same pay has *no* NPS line, and vice-versa. The engine
> picks exactly one based on `pension_scheme`.

### 3.4 GIS — Group Insurance Scheme (both)

A small **monthly deduction** split into two parts: a **savings fund** (returned
with interest at exit) and an **insurance premium** (covers death-in-service
payout). The amount is a **fixed slab by employee group/Level**, not a % of pay.

> **Example:** GIS ₹360/month for a particular group — part savings, part
> insurance. On death-in-service, the insurance portion pays a lump sum to the
> nominee; on retirement, the savings portion + interest is returned.

### 3.5 Income Tax (TDS) — both

Tax deducted at source on salary, spread across the year. **Old vs New regime**,
80C/80CCD investments, Form 12BB declarations all feed it — but that machinery is
**Section 15**. Here it's just a monthly line:

```text
monthly_TDS = projected_annual_tax / remaining_months_in_FY     # detail → §15
```

### 3.6 Professional Tax (PT) — both

A **state** levy on earning a livelihood. Small, **slab-based on monthly/annual
salary**, with a statutory annual ceiling (commonly ₹2,500/year in many states).

> **Example:** PT might be ₹208/month for salaries in a band (so the annual stays
> within the cap, often with a different final-month figure). It's a fixed slab
> lookup, not a calculation off Basic.

### 3.7 Additional deductions (§36)

| Deduction | Trigger | Rule |
|---|---|---|
| **Loan/Advance EMI** | Active loan/advance | Principal/interest installment (Section 12) |
| **Recovery of Overpayment** | Excess paid earlier | Recover in sanctioned installments; separate from loans |
| **Court Attachment / Garnishee** | Court order | Pay part to a third party; **statutory limit** on attachable amount |
| **Quarter Licence Fee** | Govt accommodation | Recovered when HRA withdrawn (couples to §05) |
| **Other statutory** | Govt order | e.g. water/electricity for quarter |

### 3.8 Deduction priority & negative net pay

Total deductions can exceed gross (heavy recoveries + a low-pay month). A
**priority order** decides which deductions take precedence and which **carry
forward** when net would go negative.

```text
Typical priority: statutory (IT, PT, GIS) and scheme (GPF/NPS) first,
then court attachment (within legal limit),
then loans/overpayment recoveries (these get deferred if pay runs out).
Net pay must never go below a floor (often cannot be negative).
```

> **Example:** A month with low pay (long LWP) and a big loan EMI + overpayment
> recovery could push net below zero. The engine pays statutory/scheme dues,
> **defers** part of the loan/overpayment recovery to next month, and logs the
> **carry-forward** — it never disburses a negative salary.

---

## 4. Data Model

```text
DeductionRule (reference)
  ├─ code         : GPF | NPS | GIS | IT | PT | LOAN | OVERPAY | COURT | LICENCE
  ├─ applies_to   : scheme/staff_type condition
  ├─ calc_type    : PCT_OF(base) | SLAB | FIXED | SCHEDULE_DRIVEN
  ├─ priority     : ordering for negative-net handling
  └─ effective_from/to

EmployeeDeduction (per employee, active)
  ├─ employee_code, code
  ├─ amount / rate / slab_ref
  ├─ balance_outstanding     (loans, overpayment, advances)
  ├─ start_month / end_month
  └─ status : ACTIVE | DEFERRED | CLOSED

GIS_Slab / PT_Slab / NPS_Config (versioned reference)
```

Design rules:
- The engine **selects deductions by `pension_scheme` + active recoveries**, not a
  fixed list.
- Recoveries carry a **running balance**; each month reduces it; **deferral**
  doesn't lose the balance.
- Every deduction has a **priority** so negative-net handling is deterministic.
- Amounts that feed **schedules** (GPF/NPS/GIS/IT) must reconcile exactly to the
  bill (Section 14).

---

## 5. Rules & Logic

```text
compute_deductions(employee, gross, month):
    d = []
    # 1. scheme fork (§04)
    if employee.pension_scheme == OPS:
        d += GPF_subscription(employee) + GPF_advance_recovery(employee)
    else:  # NPS
        d += round((basic+da) × nps_employee_pct/100)

    # 2. universal statutory
    d += GIS_slab(employee.group)
    d += professional_tax_slab(gross, month)
    d += monthly_TDS(employee, month)            # detail → §15

    # 3. recoveries (situational), each with priority + balance
    d += loan_emis(employee)
    d += overpayment_recovery(employee)
    d += court_attachment(employee)              # capped at legal limit
    d += quarter_licence_fee(employee)           # if quarter occupied

    total, deferred = apply_priority_and_floor(d, gross)   # no negative net
    net = gross − total
    return net, d, deferred
```

---

## 6. Worked Example (Gross → Net, both schemes)

Carry **Mr. Das**, **Level 4**, Gross **₹45,690** (from Section 05: Basic 25,500,
DA 12,750, HRA 2,040, TA 5,400).

**If Mr. Das is NPS (post-cutoff joiner):**
```text
NPS  10% of (25,500+12,750=38,250)   = 3,825
GIS                                  =   360
Professional Tax                     =   208
Income Tax (TDS, illustrative)       = 1,500
Loan EMI (festival advance)          = 1,000
─────────────────────────────────────────────
Total Deductions                     = 6,893
Net Salary = 45,690 − 6,893          = 38,797
```

**If Mr. Das were OPS (pre-cutoff joiner), same Gross:**
```text
GPF subscription (chosen)            = 6,000   ← his own savings, not NPS
GIS                                  =   360
Professional Tax                     =   208
Income Tax (TDS, illustrative)       = 1,500
Loan EMI                             = 1,000
─────────────────────────────────────────────
Total Deductions                     = 9,068
Net Salary = 45,690 − 9,068          = 36,622
```

Same gross, **different deduction set and different net**, purely from the §04
fork. (Note: the OPS net is *lower* only because he chose to save more in GPF —
that's his money, unlike NPS where 10% is mandated.)

> **Negative-net twist:** if a long LWP cut Gross to ₹12,000 this month but the
> loan EMI + overpayment recovery summed to ₹15,000, the engine pays statutory
> dues, **defers** the excess recovery, logs carry-forward, and disburses a
> small but **non-negative** net.

---

## 7. System Implications

- **Branch deductions on `pension_scheme`** (GPF vs NPS); never apply both.
- Remember the **employer NPS 14% is not here** — it's a cost/schedule (§04, §13),
  not a salary deduction.
- Hold **GIS/PT/NPS** as **versioned slab/config** reference data.
- Model recoveries (loan, overpayment, court, licence fee) with a **running
  balance** and a **priority**; support **deferral** so net never goes negative.
- **Cap court attachment** at the legal attachable limit.
- Keep **licence-fee recovery in sync with HRA-off** (Section 05 coupling).
- Deduction amounts must **tie out to schedules** (Section 13/14) to the rupee.
- TDS appears here as a single line; its computation is **Section 15** — don't
  duplicate the logic.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **GPF subscription** min/max rules and **interest rate** schedule (set
   quarterly by government).
2. **GIS slab** amounts and savings/insurance split by group/Level (Assam scheme).
3. **Assam Professional Tax slabs** and annual ceiling (exact bands + final-month
   figure).
4. **Court attachment** legal limit (attachable fraction of pay) applied in Assam.
5. **Overpayment recovery** sanction process and max installment rule.
6. **Quarter licence-fee** rates and the HRA-withdrawal coupling.
7. **Deduction priority order** officially followed (for negative-net handling).
8. Whether **contractual/daily-wage** staff have any of these (often only PT/TDS).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Net Salary** | Gross − Total Deductions; the amount disbursed. *Note:* must never be negative — deferral handles shortfalls. |
| **GPF** | OPS savings fund deduction; own money + interest. *Note:* OPS only; supports advance (refundable) & withdrawal. |
| **NPS (Tier-I)** | 10% of (Basic+DA) deduction to PRAN. *Note:* post-cutoff only; employer 14% is *not* a deduction. |
| **GIS** | Group Insurance: fixed slab, part savings + part insurance. *Note:* applies to both schemes; pays nominee on death. |
| **Income Tax / TDS** | Monthly tax at source. *Note:* one line here; full logic in Section 15 (regimes, 80C, 12BB). |
| **Professional Tax (PT)** | State slab tax on livelihood, small, annual cap. *Note:* slab lookup, not % of Basic; Assam-specific bands. |
| **Loan/Advance EMI** | Installment recovery of a loan/advance. *Note:* carries an outstanding balance (Section 12). |
| **Overpayment Recovery** | Reclaiming excess salary paid earlier. *Note:* needs sanction; separate from loans; installment-based. |
| **Court Attachment / Garnishee** | Court-ordered diversion of part of pay. *Note:* capped at a legal attachable limit. |
| **Quarter Licence Fee** | Charge for govt accommodation. *Note:* recovered when HRA is withdrawn — couples to Section 05. |
| **Deduction Priority** | Order deciding which deductions win when pay is short. *Note:* statutory/scheme first; recoveries deferred. |
| **Carry-forward / Deferral** | Postponing unrecovered recovery to next month. *Note:* preserves balance; prevents negative net. |
| **Schedule tie-out** | Deduction totals matching the schedules sent to authorities. *Note:* rupee-exact; reconciliation depends on it (Section 14). |

---

### Status
Section 06 complete. Update roadmap tracker: 06 → ✅ Done.
Next: **Section 07 — Increment, Pay Fixation & MACP**.
