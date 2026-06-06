# Section 14 — Payroll Period, States & Reconciliation

> Learning roadmap §14. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §26 (Payroll Period & Processing States), §27 (Reconciliation & Post-Disbursement).
> Section 13 produced **one month's bill** and pushed it to disbursement. This
> section is about the **discipline around the month itself**: treating the
> payroll month as a **first-class, lockable entity**, the **state machine** it
> moves through, and the **post-disbursement reconciliation** that proves the
> money actually landed where the bill said it would.

---

## 1. Purpose

Payroll is not a continuous trickle — it is a **periodic batch** that **closes**.
Once a month is paid, it must become **read-only**, because banks, treasury, NSDL,
GPF, and the income-tax department have all acted on those exact figures.
Retroactively editing a disbursed month would desynchronise every downstream
agency.

The questions this section answers:

> "What **state** is this payroll month in — can it still be edited, or is it
> locked? Once disbursed, did every rupee **actually reach** its destination
> (bank, NPS, GPF, IT), and do the **schedules tie out** to the bill? What happens
> when a bank credit **bounces** or a recovery **under-collects**?"

Sections 08 (arrears) and 13 (bill lock) both *assumed* this locking discipline.
This section makes it the explicit governing model.

---

## 2. Governing Rules / Authority

- **Financial Year = April–March**; the **salary month** is the unit of
  processing and a first-class entity.
- **Treasury/Financial Rules**: a **disbursed bill cannot be altered**;
  corrections flow to a **Supplementary Bill** or a **next-month adjustment** —
  never a silent edit.
- **NPS (PFRDA/NSDL)**: contributions must be **uploaded** and **PRAN-posted**;
  the system must confirm the **SCF (Subscriber Contribution File)** acceptance.
- **GPF rules**: subscriptions + **annual interest** posted to each subscriber's
  GPF ledger.
- **Schedule–bill tie-out** is an **audit requirement**: GPF/NPS/GIS/IT schedule
  totals must equal the bill's corresponding deductions.

---

## 3. Core Concepts

### 3.1 The payroll month as a state machine (§26)

```text
Draft → Verified (DDO) → Approved → Bill Submitted (Treasury)
      → Passed / Returned → Disbursed → Period Locked
```

Each state controls **what is allowed**:

| State | Editable? | Meaning |
|---|---|---|
| **Draft** | Yes | Being computed; re-runnable freely |
| **Verified** | Limited | DDO checked; minor corrections loop back |
| **Approved** | No (pre-treasury) | Sanctioned, budget-checked |
| **Submitted** | No | At treasury (token assigned) |
| **Passed / Returned** | Returned→re-edit | Treasury accepted / sent back with reason |
| **Disbursed** | No | Money released to bank |
| **Period Locked** | **Read-only** | Closed; corrections = supplementary/next-month |

### 3.2 The lock is the linchpin

```text
BEFORE Disbursed  → reprocessing allowed (recompute, fix, re-run)
AFTER  Disbursed  → period LOCKED → any change is a NEW transaction:
                     • Supplementary Bill (this period, extra claim)
                     • Next-month adjustment / Arrear (§08)
                     • Recovery carried forward (§27)
```

This is why §08 arrears exist at all: a locked month can't be edited, so a
back-dated correction *must* become a forward-dated arrear/adjustment.

### 3.3 The treasury return loop (§26)

The bill workflow is **not one-way**. A **Returned** bill (treasury found an
error) re-enters at **Draft/Verified** with the **return reason captured**. The
system must model this loop explicitly — a returned bill is not a dead end.

### 3.4 Reconciliation — proving the money landed (§27)

Disbursement is a **claim**, not a **confirmation**. Four reconciliations close
the loop:

| Reconciliation | Checks | Failure handling |
|---|---|---|
| **Bank Return** | Each net credit succeeded | Failed credit → **hold + reissue** |
| **NPS Upload** | SCF accepted, PRAN-posted at NSDL | Re-upload / correct PRAN |
| **GPF Posting** | Subscriptions + interest in GPF ledger | Post / correct annually |
| **Schedule ↔ Bill tie-out** | Σ schedule = bill deductions | Block close until equal |

### 3.5 Bank return handling

A net credit can **bounce** (wrong/closed account). That employee's pay is
**held**, the account fixed, and the credit **reissued** — without re-opening the
locked period (the bill already disbursed; the reissue is a payout-level action,
the *liability* stays settled).

### 3.6 Suspense / recovery carry (§27)

When a deduction or recovery **can't fully collect** in a month (negative-net
floor, §06; LWP, §10; loan defer, §12), the **shortfall is carried** to the next
period via a **suspense/recovery-carry** mechanism — tracked, never dropped.

> **Example — recovery carry:** Mr. Das's loan installment ₹3,000 can't fully
> recover in a low-pay month (only ₹1,800 of room above the floor). ₹1,200 is
> **carried to suspense** and recovered next month. The loan ledger (§12) and the
> period reconciliation both reflect the carry — nothing silently vanishes.

---

## 4. Data Model

```text
PayrollPeriod (first-class entity)
  ├─ period (YYYY-MM), financial_year
  ├─ unit/DDO
  ├─ state : DRAFT|VERIFIED|APPROVED|SUBMITTED|PASSED|RETURNED|DISBURSED|LOCKED
  ├─ return_reason (nullable, on RETURNED)
  ├─ locked_at, disbursed_at
  └─ bill_ref (§13)

StateTransition (audit log)
  ├─ period_ref, from_state→to_state
  ├─ actor (role, §19/RBAC), timestamp
  └─ reason (esp. for RETURNED)

ReconciliationRun (post-disbursement)
  ├─ period_ref
  ├─ bank : {credited[], failed[]→reissue_queue}
  ├─ nps_upload : {scf_id, accepted, pran_exceptions[]}
  ├─ gpf_posting : {posted, exceptions[]}
  └─ schedule_tieout : {gpf, nps, gis, it : scheduled vs bill — must equal}

SuspenseCarry
  ├─ employee_code, source : LOAN|RECOVERY|DEDUCTION
  ├─ shortfall_amount, from_period → to_period
  └─ status : CARRIED | RECOVERED
```

Design rules:
- **PayrollPeriod owns the lock**; no pay record changes once `LOCKED` —
  corrections spawn **supplementary/arrear** transactions (§08/§13).
- **Every transition is logged** with actor + reason (RBAC §19/§38, audit §18).
- **Reconciliation is a required gate**: a period isn't truly "closed" until
  **schedules tie out** and **bank/NPS/GPF** confirm.
- **Suspense carries are tracked entities**, reconciled against the source ledger
  (loan §12, recovery §06) — never silent.

---

## 5. Rules & Logic

### 5.1 State guard

```text
edit_pay(period, change):
    if period.state in {APPROVED, SUBMITTED, DISBURSED, LOCKED}:
        reject → route to Supplementary Bill or Arrear (§08)
    else:
        apply + reprocess
```

### 5.2 Close gate (schedule tie-out)

```text
close_period(period):
    for sched in {GPF, NPS, GIS, IT}:
        assert Σ schedule[sched] == bill.deductions[sched]     # tie-out
    assert bank.all_credited or bank.failed → reissue_queue
    assert nps.scf_accepted and gpf.posted
    period.state = LOCKED
```

### 5.3 Post-disbursement handling

```text
on bank_return(emp):    hold(emp.net); fix_account; reissue   # period stays LOCKED
on under_recovery(emp): SuspenseCarry(shortfall, → next_period)
on returned_bill:       state = DRAFT/VERIFIED; capture return_reason; re-run
```

---

## 6. Worked Example (a month through its states)

**June payroll, Mr. Das's unit** (the §13 bill):

```text
01 Jun  DRAFT       compute all payslips (§05–12), re-runnable
03 Jun  VERIFIED    DDO checks register; one HRA correction → re-run in Draft → re-verify
05 Jun  APPROVED    budget heads checked (§13) — now pre-treasury, no edits
06 Jun  SUBMITTED   presented to treasury → token no. assigned
08 Jun  RETURNED    treasury flags a schedule mismatch → reason captured
                    → loops to VERIFIED, schedule fixed, tie-out re-checked
09 Jun  PASSED      voucher no. assigned
10 Jun  DISBURSED   net released to bank
```

**Post-disbursement reconciliation:**
```text
Bank      : 2 of 3 credited; Mr. Roy's credit FAILED (closed account)
            → held + reissued 12 Jun (period stays LOCKED)
NPS       : SCF uploaded to NSDL → accepted, Das & Sharma PRANs posted
GPF       : Roy's subscription posted to GPF ledger
Tie-out   : Σ(GPF+NPS+GIS+IT schedules) == bill deductions 40,793  ✓
Suspense  : Das loan under-recovered ₹1,200 → carried to July
```
```text
12 Jun  PERIOD LOCKED   June is now read-only.
Error found in July? → Supplementary Bill or Arrear (§08). June is never edited.
```

> The **RETURNED loop** (08 Jun) and the **bank reissue** (12 Jun) are the two
> places naive systems get wrong: they model payroll as a one-way pipeline and
> have no way to re-enter or to fix a payout without unlocking the period. Both
> must be first-class.

---

## 7. System Implications

- Make **PayrollPeriod a first-class, stateful entity** with an explicit **state
  machine** and a hard **lock at disbursement**.
- Implement the **treasury return loop** — a Returned bill re-enters at Draft/
  Verified with a **captured reason**, not a dead end.
- Allow **reprocessing only on unlocked periods**; route all post-lock changes to
  **Supplementary Bill / next-month adjustment / Arrear (§08)**.
- Gate period close on **reconciliation**: **schedule↔bill tie-out**, **bank
  credit confirmation**, **NPS SCF acceptance**, **GPF posting**.
- Handle **bank returns** as **hold + reissue** at the payout layer **without
  unlocking** the period.
- Track **suspense / recovery carry-forward** as real entities reconciled against
  loan (§12) and recovery (§06) ledgers — never drop a shortfall.
- **Log every state transition** with actor + reason (RBAC §38, audit §18).
- Treat the **financial year (Apr–Mar)** and **salary month** as core temporal
  anchors for tax (§15), arrears (§08), and reports (§17).

---

## 8. Open Questions / State-Specific (confirm before build)

1. Assam's **exact bill states** and whether the treasury/IFMS portal imposes its
   own state names/transitions to mirror.
2. **Supplementary Bill** mechanics — when used vs next-month adjustment vs arrear.
3. **NPS SCF** upload/confirmation cycle and exception handling (PRAN mismatch,
   late joiner).
4. **GPF posting** cadence (monthly subscription vs annual interest) and ledger
   ownership (university vs AG).
5. **Bank return** turnaround and whether reissue needs fresh sanction.
6. **Suspense head** usage — accounting treatment of carried recoveries.
7. **Period-lock authority** — which role can lock/unlock (RBAC §38) and under
   what exception.
8. Treatment of **mid-period joiners/leavers** straddling a lock (links §13 LPC,
   §18 edge cases).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Payroll Period** | The salary month as a lockable first-class entity. *Note:* owns the state + lock. |
| **Financial Year** | Apr–Mar accounting year. *Note:* temporal anchor for tax/arrears/reports. |
| **Processing State** | Where the month is in its lifecycle. *Note:* controls what edits are allowed. |
| **Period Lock** | Read-only status after disbursement. *Note:* the linchpin; forces corrections into arrears/supplementary. |
| **Reprocessing** | Re-running computation. *Note:* allowed only on unlocked periods. |
| **Treasury Return Loop** | Returned bill re-entering at Draft/Verified. *Note:* with captured reason; not one-way. |
| **Supplementary Bill** | Extra claim for an already-processed period. *Note:* one route for post-lock correction. |
| **Reconciliation** | Proving disbursed money reached destinations. *Note:* required close gate. |
| **Bank Return** | Failed/bounced credit. *Note:* hold + reissue without unlocking period. |
| **NPS Upload / SCF** | Contribution file to NSDL/CRA. *Note:* confirm acceptance + PRAN posting. |
| **GPF Posting** | Subscriptions + annual interest to GPF ledger. *Note:* reconciled post-disbursement. |
| **Schedule ↔ Bill Tie-out** | Σ schedules = bill deductions. *Note:* audit gate before close. |
| **Suspense / Recovery Carry** | Shortfall carried to next period. *Note:* tracked entity; reconciled vs loan/recovery ledger. |
| **State Transition Log** | Audit of every state change. *Note:* actor + reason (esp. RETURNED). |

---

### Status
Section 14 complete. Update roadmap tracker: 14 → ✅ Done.
Phase 5 (Claims & Money Movement) complete. Next: **Section 15 — Statutory & Compliance Outputs** (Phase 6).
