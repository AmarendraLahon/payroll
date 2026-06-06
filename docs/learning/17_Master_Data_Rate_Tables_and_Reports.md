# Section 17 — Master Data, Rate Tables & Reports

> Learning roadmap §17. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §23 (Master Data & Rate Tables), §20 (Reports).
> This section names the **substrate every prior section quietly stood on**. Each
> formula in §05–16 said "read the rate effective in month M" — *this* is the data
> layer that makes that possible. It is the **single most reused design pattern**
> in the system: **versioned, effective-dated reference data**. Reports are its
> mirror image — the **read-out** of everything the engine produced.

---

## 1. Purpose

A payroll engine is **mostly rules reading rates**. The rules (DA = Basic × DA%)
are stable for years; the **rates** (the DA%, the matrix, the slabs) **change on
dates set by government orders**. If rates were hard-coded, every order would mean
a code change, and — fatally — **you could never recompute a past month**, killing
arrears (§08), pension averages (§16), and audit.

The discipline this section establishes:

> "Every value that can change by government order lives in a **table row carrying
> `effective_from` (and optional `effective_to`)**. Computing any month reads the
> row **in force that month**. Code holds the *formula*; data holds the *numbers*."

And the dual: **Reports** are the structured read-out — pay bills, registers,
ledgers, statutory and finance reports — that turn stored computation into
documents people and auditors consume.

---

## 2. Governing Rules / Authority

- Rate values originate from **government orders** (DA notifications, ROP/CPC pay
  matrix, PT/IT slab notifications, GIS/NPS/GPF parameter orders) — each with an
  **effective date** independent of its issue date.
- The **effective-dating rule** is not optional polish: it is what makes the system
  **legally reconstructable** (recompute any month exactly as it was paid).
- **Reports** satisfy **audit, treasury, employee, and statutory** consumers
  (Sections 13/14/15) — formats often prescribed by treasury/IT rules.

---

## 3. Core Concepts

### 3.1 The effective-dated row — the universal pattern

```text
Every rate/config row:
  ├─ <the value(s)>
  ├─ effective_from   (mandatory)
  └─ effective_to     (optional; null = still current)

Lookup:  rate_in_force(table, date) = the row where effective_from ≤ date < next effective_from
```

This one shape repeats across **every** master table. The engine never asks "what
is the DA%?" — it asks "**what was the DA% in month M?**" The answer is a row
lookup, and **history is never deleted** (old rows stay for arrears/pension/audit).

> **Key insight (the §08 payoff, generalised):** because DA% 50% (eff 1-Jan) and
> 53% (eff 1-Jul) **coexist** as two rows, recomputing June reads 50% and
> recomputing August reads 53% — automatically. Arrears, pension averages, and
> "rule in force in month M" all fall out of this single discipline for free.

### 3.2 The master-data catalogue (§23)

| Master Table | Holds | Consumed by |
|---|---|---|
| **Pay Matrix Grid** | Level × Cell → Basic (7th CPC; + UGC academic) | §03, §07 |
| **DA Rate Table** | DA% by effective date | §05, §08, §16(DR) |
| **HRA Rate Table** | % per city class + **city-classification master** | §05 |
| **TA Slab Table** | Amount by Pay Level × city category | §05 |
| **Professional Tax Slabs** | Assam PT by salary range | §06, §15 |
| **Income Tax Slabs** | Old & new regime, per assessment year | §15 |
| **GIS Rate Table** | Subscription + insurance split by group | §06 |
| **Leave Accrual Config** | Entitlement, credit frequency, caps per type | §09 |
| **NPS/GPF Parameters** | Contribution %, employer %, scheme cut-off | §04, §06 |
| **Holiday Calendar** | Day-types per year per campus (§10) | §10 |
| **Loan Parameters** | Rates, ceilings, max installments (§12) | §12 |
| **Claim Ceilings/Rates** | CEA caps, Tour DA slabs, etc. (§11) | §11 |
| **Accounting Heads** | Major/Minor/Sub/Object (§13) | §13 |

Almost **every section's "config" box** is a row in this layer — §17 is where they
all live.

### 3.3 Master data vs transactional data

```text
Master/Reference  = slowly-changing, effective-dated, shared    (rates, matrix, config)
Transactional     = per-employee per-month events/results       (payslips, leave ledger, arrears)
```

The engine = **transactional data computed by rules reading master data**. Keeping
them separate is what lets you **re-run** a month: same transactional inputs +
same master rows → same result.

### 3.4 Derive-don't-store (recall §03/§05)

Because rates are looked up, the engine **stores positions and events, not
computed amounts**. Basic isn't a stored number — it's `matrix(level, cell)` at
the matrix version in force. DA isn't stored — it's `Basic × rate_in_force`. This
keeps a single source of truth and makes recomputation trivial.

> **Exception — the immutable snapshot:** once a month is **disbursed** (§13/§14),
> its **PayslipHistory** *is* stored as a frozen fact (the `paid_amount` for §08).
> Derive-don't-store governs **live** computation; **history** is deliberately
> snapshotted. Both serve recomputability.

### 3.5 Reports — the read-out (§20)

| Group | Reports | Primarily for |
|---|---|---|
| **Payroll** | Pay Bill, Salary Register, Payslip, Deduction Register | Treasury, audit, employee |
| **Leave** | Leave Balance, Leave Ledger, Leave Register | Establishment, employee |
| **Service** | Service Book, Promotion History, Increment Report | Establishment, audit |
| **Finance** | NPS Report, GPF Report, Income Tax Report | Funds, statutory (§15) |

Reports are **queries over transactional data** (with master data for labels/
rates), not new computation. A report must **tie out** to the bill/ledger it
summarises (the §13/§14 reconciliation discipline extends to reporting).

### 3.6 Versioning, audit, and change control

- A rate change = **insert a new row** with a new `effective_from`, **never an
  update-in-place** (in-place edits destroy the past).
- Every master change is **audit-logged** (who/when/old→new) — same audit spine as
  §13/§14/§18.
- An inserted **back-dated** rate row can **trigger an arrear run** (§08)
  automatically — the data layer drives the recompute.

---

## 4. Data Model

```text
RateTable<T> (generic effective-dated reference)
  ├─ table_id, scope_key (e.g. city_class, group, regime, level)
  ├─ value(s)
  ├─ effective_from   (mandatory)
  ├─ effective_to     (nullable)
  ├─ source_order_ref (the govt order)
  └─ created_by, created_at        (audit)

PayMatrixVersion
  ├─ matrix_id (STATE_7CPC | UGC_ACADEMIC), effective_from/to
  └─ cells[] : (level, cell) → basic

CityClassificationMaster
  └─ city → class (X|Y|Z)   (drives HRA, TA)   effective-dated

LeaveAccrualConfig, NPSGPFParams, GISRates, PT/ITSlabs, LoanParams,
ClaimCeilings, AccountingHeads, HolidayCalendar
  └─ all share the effective_from/to + source_ref shape

ReportDefinition
  ├─ report_code, group : PAYROLL|LEAVE|SERVICE|FINANCE
  ├─ query (over transactional + master)
  ├─ params : period, unit, employee, FY
  └─ output_format : PDF | XLSX | TREASURY_SCHEMA
```

Design rules:
- **One generic effective-dated shape** reused for every rate/config — don't
  bespoke-model each.
- **Inserts, never in-place updates** for rate changes; **history retained
  forever**.
- **`rate_in_force(table, date)`** is a **single shared lookup service** every
  section calls (the "rule in force in month M" service).
- **Reports read; they don't compute** — and must **tie out** to source ledgers.
- Every master change is **audit-logged** and can **trigger arrears** (§08).

---

## 5. Rules & Logic

### 5.1 The universal lookup

```text
rate_in_force(table, scope_key, date):
    return row in table where scope matches
           and effective_from ≤ date
           and (effective_to is null or date < effective_to)
    # exactly one row must match; overlapping ranges = data error
```

### 5.2 Applying a rate change (a government order)

```text
apply_order(table, new_value, effective_from, order_ref):
    close prior open row: set its effective_to = effective_from   (no value edit)
    insert new row(new_value, effective_from, effective_to=null, order_ref)
    audit_log(insert)
    if effective_from < current_month:
        trigger arrear_run(affected_employees, effective_from)    # §08
```

### 5.3 Generating a report

```text
run_report(report_code, params):
    rows = query(transactional_data, params)         # payslips/leave/service
    enrich with rate_in_force(...) for labels/checks
    assert report_totals tie out to bill/ledger      # §13/§14 discipline
    render(output_format)
```

---

## 6. Worked Example (one DA order, four downstream effects)

Government issues: **DA 50% → 53%, effective 1 Jul, ordered 1 Oct.**

```text
apply_order(DA_Rate_Table, 53, eff=1-Jul, order=DA/2024/xx):
   ① close 50%-row: effective_to = 1-Jul     (the 50% history is preserved)
   ② insert 53%-row: effective_from = 1-Jul, effective_to = null
   ③ audit_log the insert (who/when/order ref)
   ④ eff (1-Jul) < current (Oct) → trigger ARREAR run for Jul/Aug/Sep (§08)
```

Now the **same data** serves four readers, no code change:

| Reader | Reads | Gets |
|---|---|---|
| **July salary (live)** | `rate_in_force(DA, Jul)` | **53%** |
| **June recompute** | `rate_in_force(DA, Jun)` | **50%** (old row still there) |
| **Arrear engine (§08)** | both rows | 3% diff × Jul–Sep |
| **Pensioner DR (§16)** | DR table (shared cadence) | revised DR% |

```text
Reports then read it out:
  Pay Bill / Salary Register (Oct) shows 53% DA + the arrear line.
  Deduction Register shows the NPS top-up on the arrear.
  Finance (NPS) Report reflects the extra employer/employee contribution.
All tie out to October's bill (§14).
```

> **One row insert → live pay, past recompute, arrears, pension DR, and four
> reports** — all correct, all from the effective-dated discipline. This is why
> every prior section insisted on it.

---

## 7. System Implications

- Model **all rates/config as one generic effective-dated table shape**
  (`effective_from`/`effective_to` + source order) — matrix, DA, HRA, TA, PT, IT,
  GIS, leave, NPS/GPF, loans, claims, heads, calendar.
- Expose a **single `rate_in_force(table, date)` lookup service** every section
  uses; forbid asking for "current" rate without a date.
- **Insert new rows for changes; never update-in-place**; **retain history
  forever** — this is what powers arrears (§08), pension averages (§16), and audit.
- **Audit-log every master change**; let a **back-dated insert trigger an arrear
  run** (§08) automatically.
- Keep **master vs transactional** data cleanly separated so any month is
  **re-runnable** (same inputs → same output).
- Honour **derive-don't-store** for live computation, but **snapshot
  PayslipHistory** on disbursement (the deliberate exception).
- Build **Reports as queries that read, not compute**, grouped Payroll/Leave/
  Service/Finance, each **tying out** to its source ledger/bill.
- Support **treasury/statutory report schemas** (Sections 13/15) as output formats,
  not just PDFs.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Source and update cadence** for each rate table (who enters DA/PT/IT orders;
   manual vs feed).
2. The **actual Assam values** still flagged across §05–16 (DA%, city
   classification, PT slabs, NPS cut-off, leave entitlements, loan/claim ceilings)
   — all land as rows here.
3. **Two pay matrices** (state 7th-CPC + UGC academic) — sourcing and versioning of
   each.
4. **Report formats** prescribed by treasury/IT (24Q, pay bill, schedules) vs
   internal.
5. **Granularity of effective-dating** (date vs month) and the **overlap-prevention**
   constraint.
6. **Who may change master data** (RBAC §19/§38) and the approval workflow for a
   rate insert.
7. Whether master data is **shared across colleges** or per-campus overridable
   (e.g. local holidays §10, local allowances).
8. **Report delivery** — ESS download (§19), scheduled generation, bulk export.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Master / Reference Data** | Slowly-changing shared config the engine reads. *Note:* rates, matrix, slabs, calendars. |
| **Effective-Dated Row** | A value with `effective_from`/`effective_to`. *Note:* the universal pattern; enables past recompute. |
| **`rate_in_force(table, date)`** | The single shared lookup. *Note:* every section asks "rate in month M", never "current". |
| **Pay Matrix Grid** | Level × Cell → Basic table. *Note:* versioned; source for §03/§07. |
| **DA / HRA / TA Rate Tables** | Effective-dated allowance rates. *Note:* HRA needs city-classification master. |
| **City Classification Master** | City → X/Y/Z class. *Note:* drives HRA % and TA category. |
| **PT / IT Slabs** | Statutory tax slab tables. *Note:* PT Assam-specific; IT old+new per AY. |
| **Leave Accrual Config** | Entitlement/frequency/caps per leave type. *Note:* the §09 numbers as data. |
| **NPS/GPF Parameters** | Contribution %, employer %, cut-off date. *Note:* the §04 fork values as data. |
| **Insert-not-update** | Rate change = new row, old kept. *Note:* in-place edit destroys the past; forbidden. |
| **History Retention** | Old rows never deleted. *Note:* powers arrears, pension averages, audit. |
| **Derive-don't-store** | Compute amounts from positions+rates live. *Note:* exception: disbursed PayslipHistory is snapshotted. |
| **Transactional Data** | Per-employee per-month results/events. *Note:* computed by rules over master data. |
| **Report (read-out)** | Query over transactional+master data. *Note:* reads, doesn't compute; must tie out. |
| **Tie-out** | Report totals = source ledger/bill. *Note:* extends §13/§14 reconciliation to reporting. |
| **Source Order Ref** | The govt order behind a rate row. *Note:* audit + provenance. |

---

### Status
Section 17 complete. Update roadmap tracker: 17 → ✅ Done.
Next: **Section 18 — Edge Cases & Special Handling** (Phase 7 continues).
