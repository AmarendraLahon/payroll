# Section 12 — Loans & Advances

> Learning roadmap §12. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §16 (Loans and Advances).
> Section 06 introduced **recoveries** as one deduction bucket. This section is the
> deepest, most structured recovery type: **sanctioned loans** that the employee
> *receives as a lump sum* and **repays via monthly salary deductions** over years,
> with **principal, interest, and an installment schedule** the system must track
> independently of any single month's payslip.

---

## 1. Purpose

The institution lends money to staff for sanctioned purposes — a festival, a
vehicle, a computer, building a house. Each loan is a **disbursement now,
recovery over time**. The payroll system is the **collection agent**: every month
it must deduct the **correct installment**, split it into **principal vs
interest**, **reduce the outstanding balance**, and **stop** exactly when the loan
is cleared.

The questions this section answers:

> "For this employee this month, which loans are active, what installment is due
> on each, how much is principal vs interest, and what's the remaining balance
> after this deduction?"

Unlike a one-off recovery (§06), a loan is a **stateful, multi-year obligation**
with its own ledger that long outlives any one payslip — and must survive
arrears, leave-without-pay months, transfers, and retirement.

---

## 2. Governing Rules / Authority

- Loan **types, ceilings, interest rates, and max installments** are fixed by
  **government / university financial sanction orders** (e.g. GPF-advance rules,
  HBA rules, vehicle/computer advance rules).
- **Interest** is typically **simple interest**, often recovered **after** the
  principal is fully repaid (the classic government pattern: principal in N
  installments, then interest in further installments).
- **Festival Advance** is usually **interest-free**, recovered in a small fixed
  number of installments (e.g. 10).
- **GPF Advance/Withdrawal** is governed by GPF rules (recovery into the same GPF,
  links Sections 04/06).
- Recovery runs through the **monthly salary deduction** schedule and is subject
  to the **negative-net / minimum-pay** protection (Section 06).

---

## 3. Core Concepts

### 3.1 A loan is a lifecycle, not a number

```text
SANCTION (amount, rate, installments) → DISBURSE (lump sum to employee)
→ RECOVER (monthly installment, salary deduction) → CLOSE (balance = 0)
```

The payslip only ever sees the **current month's installment**. The **loan
account** (separate ledger) holds the whole story: sanctioned amount, rate,
schedule, paid-to-date, outstanding.

### 3.2 The loan catalogue (§16)

| Loan / Advance | Interest | Typical recovery | Note |
|---|---|---|---|
| **Festival Advance** | Interest-free | ~10 small installments | Recurs yearly; small ceiling |
| **Vehicle Loan / Advance** | Simple interest | Principal then interest | Ceiling by purpose/pay |
| **Computer Loan / Advance** | Simple interest | Principal then interest | Once-in-service typically |
| **House Building Advance (HBA)** | Simple interest | Long (many years) | Largest; principal phase then interest phase |
| **GPF Advance / Withdrawal** | (refundable/non-refund) | Into GPF | Links §04/§06 |

### 3.3 Principal vs interest split

Each installment is **not** pure repayment — it must be **split**:

```text
installment = principal_part + interest_part
outstanding_principal −= principal_part
```

Two common government conventions:
- **Principal-first**: recover the full principal in N installments, *then* recover
  accumulated interest in further installments (very common for HBA/vehicle).
- **Blended**: each installment carries both (EMI-style) — less common in govt.

The system must support the convention the sanction order specifies; the **split
matters** for accounting heads (Section 13) and for what the employee sees.

> **Example — principal-first:** Vehicle advance ₹1,80,000, 60 principal
> installments of ₹3,000 + interest recovered after. Months 1–60 deduct ₹3,000
> **principal**, outstanding drops ₹3,000 each month; months 61+ deduct the
> **interest** installments until interest is cleared. The loan closes only when
> *both* phases finish.

### 3.4 Installment schedule (amortisation)

At sanction the system **generates the full schedule** — month-by-month
installment, principal part, interest part, running balance. This **schedule is
the plan**; actual recovery posts against it. Deviations (a skipped month due to
LWP, a part-payment, a lump prepayment) **re-align** the schedule.

### 3.5 Skips, prepayment, and balance protection

- **LWP / nil-pay month** (§06/§10): no salary → installment **can't be
  recovered** → it **defers** (schedule extends) or is **flagged arrears-of-
  installment**, per rule. Never silently skip without trace.
- **Prepayment / lump closure**: employee clears outstanding early → remaining
  schedule **cancelled**, interest **recomputed** to the closure date.
- **Minimum-pay rule** (§06): if the installment would push net below the floor,
  it **partially recovers or defers** — the loan ledger must reconcile what was
  *actually* recovered vs *scheduled*.

### 3.6 Outstanding at exit (retirement / death / transfer)

- **Retirement**: any outstanding loan is **recovered from terminal benefits**
  (gratuity / encashment) — links Section 16.
- **Death-in-service**: outstanding may be **written off** or recovered from
  settlement per rule (Section 18).
- **Transfer**: the loan **balance moves with the LPC** (Last Pay Certificate) to
  the new DDO (Sections 13/18).

---

## 4. Data Model

```text
LoanType (config, effective-dated §17)
  ├─ code : FESTIVAL | VEHICLE | COMPUTER | HBA | GPF_ADVANCE
  ├─ interest_rate, interest_method : NONE | SIMPLE
  ├─ recovery_convention : PRINCIPAL_FIRST | BLENDED
  ├─ max_amount (ceiling), max_installments
  └─ accounting_head (§13)

LoanAccount (per sanctioned loan — the durable ledger)
  ├─ loan_id, employee_code, loan_type
  ├─ sanctioned_amount, rate, sanction_ref, disburse_date
  ├─ total_installments, installment_amount
  ├─ outstanding_principal, accrued_interest, interest_recovered
  ├─ status : ACTIVE | CLOSED | DEFERRED | WRITTEN_OFF
  └─ phase : PRINCIPAL | INTEREST                   (principal-first)

LoanSchedule (rows, generated at sanction)
  ├─ loan_id, installment_no, due_month
  ├─ principal_part, interest_part, balance_after
  └─ status : DUE | RECOVERED | DEFERRED | WAIVED

LoanRecovery (actual postings — what really came off the payslip)
  ├─ loan_id, month, amount_recovered (principal/interest split)
  └─ payslip_ref
```

Design rules:
- The **LoanAccount + Schedule are the source of truth**; the payslip's loan
  deduction is just **this month's posting** against them.
- **Scheduled vs actually-recovered are separate** — LWP/floor months make them
  diverge; reconcile, don't overwrite.
- **Outstanding is derived** from postings, never typed in.
- Each recovery carries a **principal/interest split** for correct **accounting
  heads** (Section 13).
- Loan rules (rate, ceiling, max installments) are **effective-dated master data**
  (Section 17).

### 4.1 Where a loan sits in the deduction stack (recall §06)

```text
Earnings (§05)            +Gross
Statutory deductions       −NPS/GPF, GIS, IT, PT
Recoveries  ───────────►   −Loan installment(s)   ← THIS section feeds here
                           −Other recoveries (§06)
                          = Net (≥ minimum floor, §06)
```

The loan engine **produces the installment**; Section 06's **priority + floor**
rules decide how much actually comes off when money is tight.

---

## 5. Rules & Logic

### 5.1 Sanction & schedule generation

```text
sanction_loan(employee, type, amount, installments):
    assert amount <= ceiling(type) and installments <= max(type)
    open LoanAccount(outstanding_principal = amount, phase = PRINCIPAL)
    generate LoanSchedule rows per recovery_convention + interest_method
    disburse(amount)                                  # lump sum out
```

### 5.2 Monthly recovery

```text
recover_month(loan, month):
    due = LoanSchedule[loan, month]
    actual = min(due.amount, room_after_floor(employee, month))   # §06 floor
    post LoanRecovery(split principal/interest)
    outstanding_principal −= principal_part
    if actual < due.amount: defer remainder (extend schedule / flag arrear)
    if outstanding_principal == 0 and phase==PRINCIPAL: phase = INTEREST
    if all interest recovered: status = CLOSED
```

### 5.3 Closure & exit

```text
if prepayment: outstanding = 0 after lump; recompute interest to date; CLOSE
at retirement: recover outstanding from terminal benefits (§16)
at transfer: carry outstanding to LPC (§13/§18)
```

---

## 6. Worked Example (festival + vehicle, one payslip)

**Mr. Das** has two active loans in June:

**Festival Advance** — ₹30,000, interest-free, 10 installments.
```text
Installment = 30,000 / 10 = 3,000/month (all principal)
Month 4 of 10 → outstanding before = 21,000 → deduct 3,000 → after = 18,000
```

**Vehicle Advance** — ₹1,80,000, simple interest, principal-first, 60 + interest.
```text
Month 12 of 60 → principal installment 3,000 → outstanding before = 1,47,000
→ deduct 3,000 (principal) → after = 1,44,000   (still in PRINCIPAL phase)
```

June payslip loan deductions:
```text
Festival   3,000  (principal)
Vehicle    3,000  (principal)
Total loan recovery = 6,000  → flows into §06 deduction stack
```

```text
Check §06 floor: if Net after ALL deductions would dip below the minimum,
the LOWER-priority loan installment partially defers — schedule extends,
LoanAccount reconciles scheduled(6,000) vs recovered(actual).
```

> Festival clears at month 10 (deduction **stops automatically** — balance 0).
> Vehicle continues: after month 60 it flips to the **INTEREST phase** and keeps
> deducting until interest is cleared, *then* closes. At retirement, any
> outstanding on either is netted from **terminal benefits** (Section 16).

---

## 7. System Implications

- Model a loan as a **durable LoanAccount + generated Schedule**, separate from the
  payslip; the monthly deduction is a **posting against** it, not the loan itself.
- Generate the **full amortisation schedule at sanction** per the **recovery
  convention** (principal-first vs blended) and **interest method** (none/simple).
- **Split every installment** into principal vs interest for correct **accounting
  heads** (Section 13) and employee statements.
- Keep **scheduled vs actually-recovered** distinct; **LWP/floor** months **defer**
  (extend schedule / flag installment-arrear), never silently skip.
- **Auto-stop** recovery at zero balance; **auto-flip** principal→interest phase;
  support **prepayment / lump closure** with interest recomputation.
- Enforce **ceiling and max-installment** validation at sanction from
  **effective-dated** loan master data (Section 17).
- On **exit** (retirement/death/transfer), surface **outstanding** to terminal
  settlement (§16) or **LPC** carry-over (§13/§18).
- Feed the installment into Section 06's **priority + minimum-pay floor** — the
  loan engine proposes, §06 disposes.

---

## 8. Open Questions / State-Specific (confirm before build)

1. Assam/university **loan catalogue** actually offered, with **ceilings, rates,
   and max installments** per type.
2. **Interest method/convention** per loan — simple interest, **principal-first**
   vs blended, and how interest installments are computed.
3. **Festival Advance** terms — amount, installment count, recurrence eligibility.
4. **HBA** specifics — ceiling (by Basic), phases, insurance/mortgage conditions.
5. **LWP/nil-pay month** handling — defer-and-extend vs installment-arrear.
6. **Prepayment** rule — interest rebate on early closure?
7. **Exit handling** — recovery from terminal benefits, **write-off** on death,
   **LPC** carry-over format on transfer.
8. **GPF advance/withdrawal** interplay with GPF balance (refundable vs
   non-refundable) — links Sections 04/16.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Loan / Advance** | Lump sum lent, recovered via salary over time. *Note:* stateful multi-year obligation, own ledger. |
| **LoanAccount** | The durable per-loan ledger. *Note:* source of truth; payslip deduction is a posting against it. |
| **Sanction** | Approval fixing amount/rate/installments. *Note:* triggers schedule generation + disbursement. |
| **Principal** | The borrowed amount being repaid. *Note:* outstanding drops by the principal part each month. |
| **Interest (Simple)** | Charge on principal. *Note:* govt usually recovers it **after** principal (principal-first). |
| **Recovery Convention** | Principal-first vs blended. *Note:* decides each installment's principal/interest split. |
| **Installment** | Monthly recovery amount. *Note:* split into principal + interest; flows into §06 deductions. |
| **Amortisation Schedule** | Full month-by-month plan at sanction. *Note:* actual recovery posts against it; deviations re-align. |
| **Outstanding Balance** | Remaining principal (+interest). *Note:* derived from postings, never typed in. |
| **Festival Advance** | Small interest-free advance. *Note:* ~10 installments; recurs yearly. |
| **HBA** | House Building Advance. *Note:* largest, longest; principal phase then interest phase. |
| **Phase (Principal/Interest)** | Which part is currently being recovered. *Note:* auto-flips when principal hits zero. |
| **Installment Deferral** | Skipped recovery in a nil-pay month. *Note:* extends schedule / flags arrear; never silent. |
| **Prepayment / Lump Closure** | Early full settlement. *Note:* cancels remaining schedule, recomputes interest. |
| **Exit Recovery** | Outstanding netted at retirement/death/transfer. *Note:* from terminal benefits (§16) or LPC (§13/§18). |
| **LPC (Last Pay Certificate)** | Doc carrying pay + loan balance on transfer. *Note:* moves the loan to the new DDO. |

---

### Status
Section 12 complete. Update roadmap tracker: 12 → ✅ Done.
Next: **Section 13 — Salary Bill, Treasury & Budget Heads** (Phase 5 continues).
