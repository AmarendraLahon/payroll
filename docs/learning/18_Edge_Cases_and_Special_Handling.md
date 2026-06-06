# Section 18 — Edge Cases & Special Handling

> Learning roadmap §18. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §30 (Edge Cases & Special Handling).
> Sections 05–17 built the **happy path**: a regular employee, present, paid in
> full, every month. This section is the **catalogue of where that path breaks** —
> suspension, negative net, mid-month exit, transfer, death, service breaks — and
> the **audit spine** that makes all of it defensible. Most are not new subsystems;
> they are **specific interactions** of subsystems already built.

---

## 1. Purpose

Real payroll spends most of its *correctness budget* on the **5% of cases that
aren't normal**. A system that pays a present, full-month, single-unit employee is
easy; one that correctly handles a suspended employee whose subsistence rate
changes, a person transferring mid-month with an outstanding loan, or a
death-in-service with dues to waive and a family pension to start — that is the
real engineering.

The questions this section answers:

> "When the happy path breaks — no full pay, no full month, no single unit, no
> living employee — what does the system pay, recover, carry, or waive, and **can
> it prove why** afterward?"

The unifying theme: **edge cases are compositions** of the scheme fork (§04),
proration (§10), recoveries (§06/§12), period lock (§14), settlement (§16), and —
above all — the **audit trail** that records who did what.

---

## 2. Governing Rules / Authority

- **Suspension** — service rules: a suspended employee is paid **Subsistence
  Allowance** (a fraction of pay), revised on **prolonged** suspension, settled on
  **reinstatement** (full/partial restoration per the order).
- **Negative net / recovery priority** — FR-SR + deduction-priority rule (§06):
  apply priority order, **carry unrecovered balance** forward (suspense, §14).
- **Transfer** — **LPC (Last Pay Certificate)** carries pay, recovery, and leave
  balances to the new unit/DDO (§13).
- **Death-in-service** — family pension, **DCRG**, dues settlement with **waiver
  checks** (§16).
- **Dies-non / EOL** — no pay, **no qualifying-service credit**; defers increment
  (§07) and reduces pension reckoning (§16).
- **Audit** — all Service Book / pay / leave changes **logged with who/when/
  old→new** (statutory audit requirement).

---

## 3. Core Concepts

### 3.1 The edge-case catalogue (§30)

| Case | Core handling | Composes |
|---|---|---|
| **Suspension** | Pay **Subsistence Allowance**, not regular pay; revise on prolonged; settle on reinstatement | §05, §14, audit |
| **Negative net pay** | Apply **deduction priority**; carry unrecovered balance forward | §06, §12, §14 |
| **Loan/Advance specials** | Simple interest, installments, **foreclosure**, recovery priority | §12 |
| **Mid-month retire/death** | **Prorate**; trigger settlement + leave encashment | §10, §16 |
| **Transfer between colleges** | Issue **LPC**; continue recovery/leave at new unit | §12, §13 |
| **Death in service** | Family pension, DCRG, dues settlement, **recovery waiver** | §16, §06 |
| **Dies-non (EOL)** | No pay, no service credit; defers increment/pension | §07, §10, §16 |
| **Audit trail** | Log all changes (who/when/old→new) | everything |

The right mental model: **almost no edge case is a new module** — each is a
**specific orchestration** of existing engines under an abnormal condition.

### 3.2 Suspension — pay without working

```text
on_suspension(employee, order):
    stop regular pay
    pay Subsistence Allowance = rate% × (Basic+DA)   (e.g. 50%, revised if prolonged)
    suspend increment accrual / leave earning per rule
on_reinstatement(employee, order):
    decide period treatment: duty / not-duty / leave
    pay ARREAR for restored portion (§08) or recover excess subsistence
```

Subsistence is a **distinct earning type**, not prorated regular pay; the
**reinstatement order decides** whether the suspension period becomes duty (full
back-pay arrear) or stays partial.

### 3.3 Negative net — when deductions exceed pay

A month's deductions (loan + recovery + statutory) can exceed gross (low-pay
month, multiple loans, overpayment recovery). The §06 rule:

```text
apply deductions in PRIORITY order until the minimum-pay floor is hit;
the unrecovered remainder → SUSPENSE carry-forward (§14), never forced negative.
```

> **Example:** Gross ₹18,000; statutory ₹4,000 (must take) leaves ₹14,000; two
> loan installments ₹6,000 + an overpayment recovery ₹10,000 = ₹16,000 wanted but
> only ₹14,000 − floor available. Lower-priority recoveries **partially collect**;
> the rest **carries** to next month. Net never goes below the floor.

### 3.4 Mid-month exit — proration meets settlement

A retire/death on the 18th means: pay **18/30 of the month** (proration §10),
**then** run the **terminal settlement** (§16) — encashment, gratuity/corpus,
dues recovery. Two engines fire in sequence for one event.

### 3.5 Transfer — the LPC hand-off

```text
on_transfer(employee, from_unit, to_unit):
    issue LPC = { last pay drawn, pay particulars, recovery balances (loans §12),
                  leave balances (§09), last-paid month }
    new unit RESUMES from the LPC — loans keep recovering, leave continues,
    no double-pay in the overlap month (one unit pays, the other starts after).
```

The LPC is the **state-transfer packet** so the employee remains **one continuous
record** across units (recall §02: the employee is a projection of an append-only
log — transfer doesn't fork it).

### 3.6 Death-in-service — the most composed case

```text
on_death(employee, date):
    prorate final month (§10)
    start FAMILY PENSION (enhanced→normal, §16)
    pay DCRG / NPS corpus to nominee, leave encashment
    settle dues — but apply WAIVER rules (some loans written off on death, §12/§06)
    audit every step; notify, generate settlement papers
```

The defining twist vs retirement: **dues may be waived**, and a **family pension**
(not the employee's pension) begins. Maximum subsystem composition in one event.

### 3.7 Dies-non / EOL — the recurring echo, catalogued

The EOL spell threaded §02 → §07 → §10 → §16 is itself an edge case: **no pay, no
service credit**, defers increment, reduces pension. Listed here to close the loop:
it's the canonical example of **one abnormal event consumed by many sections**.

### 3.8 The audit trail — the spine under all of it

```text
every change to Service Book / pay / leave / master data:
   log { who, when, old_value → new_value, reason/order_ref }
```

Edge cases are exactly where **disputes and audits land**, so the audit trail
isn't a feature — it's the **evidence layer** that makes every special handling
**defensible**. Same spine referenced in §13/§14/§17.

---

## 4. Data Model

```text
SpecialStatus (per employee, effective-dated)
  ├─ type : SUSPENDED | DEPUTATION | ON_EOL | TRANSFERRED | RETIRED | DECEASED
  ├─ order_ref, from_date, to_date
  └─ pay_treatment : SUBSISTENCE | NONE | PRORATED | NORMAL

SubsistenceConfig
  └─ rate% (initial, prolonged), revision_after_months

LPC (Last Pay Certificate)
  ├─ employee_code, from_unit, to_unit, last_paid_month
  ├─ pay_particulars (level/cell/basic, allowances)
  ├─ recovery_balances[] (loans §12, overpay §06)
  └─ leave_balances[] (§09)

SuspenseLedger (negative-net carry, §14)
  ├─ employee_code, source, amount, from_period → to_period
  └─ status : CARRIED | RECOVERED | WAIVED

WaiverDecision (death/special)
  ├─ employee_code, dues_ref, amount, waived?, authority_ref

AuditLog (universal spine)
  ├─ entity (employee/pay/leave/master), record_id
  ├─ field, old_value → new_value
  ├─ actor (role §38), timestamp, reason/order_ref
  └─ (append-only, immutable)
```

Design rules:
- Edge cases set an **effective-dated SpecialStatus** that **redirects** the
  normal engines (pay treatment, accrual, settlement) — they don't bypass them.
- **LPC is the only sanctioned way** to move an employee's pay/recovery/leave state
  between units — no ad-hoc re-keying.
- **Negative-net remainder always lands in the SuspenseLedger** — never a forced
  negative payslip.
- **Waivers are explicit decisions** with authority refs, not silent skips.
- **AuditLog is append-only and universal** — every special handling writes to it.

---

## 5. Rules & Logic

### 5.1 Suspension pay

```text
pay_month(employee, month):
    if status==SUSPENDED:
        rate = subsistence_rate(months_suspended)        # initial, then prolonged
        pay = rate × (Basic + DA); skip normal allowances
    else: normal §05–06
```

### 5.2 Negative-net resolution (extends §06)

```text
resolve_net(employee, month):
    take statutory (mandatory) first
    for ded in recoveries by PRIORITY:
        room = current_net − floor
        collected = min(ded.due, room)
        if collected < ded.due: SuspenseLedger.carry(ded.due − collected)
```

### 5.3 Transfer & death

```text
transfer: issue LPC; new unit resumes from LPC; no overlap double-pay
death:    prorate; start family pension; settle with waiver checks; audit all
```

---

## 6. Worked Example (transfer mid-month, with a live loan)

**Mr. Das** transfers from College A to College B, effective **16 June**, with an
active vehicle loan (outstanding ₹1,44,000, §12) and EL balance 45 days (§09).

```text
College A (old unit):
  pays 1–15 June  = monthly_pay × 15/30 (proration §10)
  recovers HALF the June loan installment? — per rule, usually A recovers up to
  its paid span; remainder noted on LPC
  issues LPC = { last pay particulars, loan outstanding 1,44,000,
                 EL balance 45, last_paid = 15 June }

College B (new unit):
  resumes 16–30 June = monthly_pay × 15/30
  picks up loan recovery from the LPC (no reset, no double recovery)
  carries EL balance 45 forward (no lapse on transfer)
```

```text
Result: Mr. Das is paid for ALL of June (15 + 15 days), across two units, with
ONE continuous loan ledger and ONE leave balance — because the LPC moved the
state, not a re-entry. AuditLog records the transfer on both sides.
```

> Change the event to **death on 16 June** instead: College A prorates 1–15,
> **no** College B — instead **family pension starts**, gratuity/corpus + EL
> encashment pay to the nominee, the vehicle loan hits **waiver checks** (may be
> written off), every step audited. Same proration, totally different tail.

---

## 7. System Implications

- Model edge cases as **effective-dated SpecialStatus** that **redirects** the
  normal engines (pay treatment, accrual, settlement) — compose, don't fork the
  code.
- Implement **Subsistence Allowance** as a distinct earning with
  **initial/prolonged** rates and **reinstatement settlement** (back-pay arrear or
  excess recovery).
- Always resolve **negative net** via **priority + floor**, carrying the remainder
  to the **SuspenseLedger** (§14) — never emit a negative payslip.
- Make the **LPC the sole mechanism** for inter-unit transfer of pay, recovery
  (§12), and leave (§09) state; prevent **double-pay** in the overlap month.
- Sequence **mid-month exit** as **proration (§10) → settlement (§16)**; for
  **death**, also **start family pension** and apply **dues waivers** with
  authority refs.
- Treat **dies-non/EOL** consistently across §07/§10/§16 — one event, many
  consumers; never recompute its effects ad hoc.
- Build a **universal, append-only AuditLog** (who/when/old→new/reason) over
  Service Book, pay, leave, and master data — the **evidence layer** for every
  special case.
- Surface edge cases to **RBAC-controlled** roles (§38) — these actions
  (suspension, waiver, LPC) need elevated authority and sanction refs.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Subsistence Allowance** rate(s) and the prolonged-suspension revision rule in
   Assam; reinstatement period treatment.
2. **Negative-net** policy — exact deduction priority and the **minimum-pay floor**
   value/definition.
3. **LPC** format and the inter-college transfer workflow (who issues/accepts,
   overlap-month rule).
4. **Death-in-service** dues **waiver** rules (which loans/advances are written
   off) and the settlement document set.
5. **Family pension** start trigger, rates, and beneficiary eligibility (links
   §16).
6. **Condonation** of dies-non/EOL for qualifying service and increment.
7. **Audit-log retention** period and access (who can read the trail).
8. **Loan foreclosure** on exit/transfer mechanics (§12) and any rebate.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Edge Case** | A break from the full-pay/full-month/single-unit/living-employee norm. *Note:* mostly compositions, not new modules. |
| **Suspension** | Employee kept off duty pending inquiry. *Note:* paid Subsistence, not regular pay. |
| **Subsistence Allowance** | Fractional pay during suspension. *Note:* initial rate, revised if prolonged; distinct earning type. |
| **Reinstatement** | Return from suspension. *Note:* order decides duty/back-pay (arrear) vs partial. |
| **Negative Net** | Deductions exceed pay. *Note:* priority + floor; remainder to SuspenseLedger, never negative payslip. |
| **Suspense / Carry-Forward** | Unrecovered amount moved to next period. *Note:* §14; tracked, reconciled vs source ledger. |
| **Proration** | Partial-month pay. *Note:* days/30 (§10); first step of mid-month exit. |
| **LPC (Last Pay Certificate)** | State packet for transfer. *Note:* carries pay, loan (§12), leave (§09); prevents double-pay. |
| **Mid-month Exit** | Retire/death partway through a month. *Note:* prorate (§10) then settle (§16). |
| **Death-in-Service** | Death while employed. *Note:* family pension + DCRG/corpus + dues waiver; most composed case. |
| **Dues Waiver** | Writing off recoverable on death/special. *Note:* explicit decision + authority ref, not silent. |
| **Family Pension** | Pension to dependents. *Note:* starts on death; enhanced→normal (§16). |
| **Dies-non / EOL** | No-pay, no-service-credit period. *Note:* defers increment (§07), cuts pension (§16); one event, many readers. |
| **Audit Trail** | Append-only log of all changes. *Note:* who/when/old→new/reason; the evidence layer for edge cases. |
| **SpecialStatus** | Effective-dated abnormal-state flag. *Note:* redirects normal engines; doesn't bypass them. |

---

### Status
Section 18 complete. Update roadmap tracker: 18 → ✅ Done.
Next: **Section 19 — Platform: ESS, RBAC & Data Migration** (final section, closes Phase 7).
