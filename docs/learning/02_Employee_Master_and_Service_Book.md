# Section 02 — Employee Master & Service Book

> Learning roadmap §02. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §1 (Employee Master), §2 (Service Book), §37 (Service Events).
> Section 01 told us *which rulebook* applies. This section is the **system of
> record for the person** that rulebook acts on.

---

## 1. Purpose

Payroll computes numbers, but those numbers all derive from **facts about the
employee**: who they are, what post they hold, what Level/cell their pay sits at,
when they joined, what scheme they're under. Two stores hold these facts:

- **Employee Master** — the *current* snapshot used by every salary run
  (today's designation, today's Basic, today's bank account).
- **Service Book** — the *full history* of the employee's service life, the
  permanent legal record (every promotion, transfer, pay fixation, leave spell).

> **Analogy:** Employee Master is the **balance** on your bank statement; Service
> Book is the **transaction ledger** that produced it. Payroll reads the
> balance; audit and pension read the ledger.

Get the master wrong → this month's salary is wrong. Get the service book wrong →
pension, seniority, and arrears (which look *backwards* in time) go wrong.

---

## 2. Governing Rules / Authority

- **Maintenance of Service Book** is mandatory under the **Fundamental Rules /
  Assam Fundamental Rules** — every government servant must have one, maintained
  by the establishment, with entries attested and shown to the employee
  periodically.
- **Service events** (probation, confirmation, pay protection, stepping-up,
  deputation) are governed by **FR/SR** and **Assam Services rules**.
- Employee classification (teaching/non-teaching/contractual/daily-wage) carries
  forward from **Section 01** and decides which fields/events are relevant.

> **Example:** Probation and confirmation are meaningful for a regular
> **non-teaching Assistant**, but a **daily-wage casual labour** has no
> probation/confirmation concept — the same Service Book schema must tolerate
> "not applicable" cleanly.

---

## 3. Core Concepts

### 3.1 Employee Master — the current snapshot

Identity + posting + pay-relevant current state. Concept-doc fields plus what a
real engine needs:

- **Identity:** Employee Code, Name, DOB, Gender, PAN, Aadhaar (masked).
- **Posting:** Designation, Department, College/Unit, Employee Type.
- **Service anchors:** Date of Joining, Date of Retirement (derived from DOB).
- **Pay state:** Pay Authority (UGC/State, from §01), Pay Level, Cell, Basic Pay,
  Next Increment Date.
- **Scheme:** Pension Scheme (OPS/NPS), PRAN / GPF No., GIS group.
- **Payment:** Bank Account, IFSC.

> **Example — derived field:** Retirement Date is **not** typed in; it is
> computed: `DOB + 60 years → last day of that month` (superannuation age per
> Assam rule; teachers may differ, e.g. 65). Storing it as derived prevents the
> classic bug where DOB and retirement date silently disagree.

### 3.2 Employee Categories (recap from §1, with pay impact)

| Category | Examples | Pay impact |
|---|---|---|
| Teaching | Professor, Associate Prof, Asst Prof | UGC Academic Levels, CAS |
| Non-teaching | Registrar, Finance Officer, Superintendent, Assistant, Driver, Grade IV | State Pay Matrix, MACP |
| Contractual | Consultant, Project/Temp staff | Consolidated pay, limited rules |
| Daily Wage | Casual labour | Daily rate, no service benefits |

### 3.3 Service Book — the permanent history

A chronological, attested record. Key event groups (concept-doc §2):

- Joining & verification of antecedents
- **Probation → Confirmation**
- Promotions / CAS / MACP
- **Pay Fixation** events (with option dates)
- Transfers / **Deputation**
- Leave records (esp. EOL/dies-non — affects pension)
- Increment entries
- Suspension / reinstatement
- Nominations (GPF/GIS/pension)
- Retirement / settlement

> **Why history matters for money:** An **EOL (leave without pay)** spell of 3
> months recorded in the Service Book reduces **qualifying service** for pension
> *decades later* and may **shift the increment date**. The fact is captured
> once here and consumed by Sections 07, 16. Miss it now → wrong pension at exit.

### 3.4 Service Events (§37) explained

| Event | What it is | Payroll effect | Example |
|---|---|---|---|
| **Probation** | Trial period on first appointment | Usually normal pay; increment may be deferred until cleared in some rules | New Asst on 2-yr probation |
| **Confirmation** | Made permanent after probation | Confirms seniority; unlocks certain benefits | Confirmed after satisfactory probation |
| **Pay Protection** | On joining from another govt post, protect previous higher pay | Fix Basic so it's not reduced | Clerk from state dept joins university, pay protected |
| **Stepping Up** | Raise a senior's pay to match a junior who (due to fixation rules) draws more | Basic increased to remove anomaly | Senior Asst stepped up to junior's Basic |
| **Deputation** | Serving in another org temporarily, lien retained | May get **deputation allowance**; pay drawn per deputation terms | Officer deputed to a state board |

---

## 4. Data Model

The crucial design decision: **Employee Master is current; Service Book is an
append-only event log.** The master is a *projection* of the latest events.

```text
Employee (master / current snapshot)
  ├─ employee_code (PK, immutable)
  ├─ name, dob, gender, pan, aadhaar_masked
  ├─ staff_type, pay_authority            (from §01)
  ├─ designation, department, college_unit
  ├─ date_of_joining
  ├─ date_of_retirement   (DERIVED from dob + superannuation rule)
  ├─ pay_level, pay_cell, basic_pay        (current)
  ├─ next_increment_date
  ├─ pension_scheme, pran, gpf_no, gis_group
  └─ bank_account, ifsc

ServiceEvent (append-only history — the Service Book)
  ├─ event_id (PK)
  ├─ employee_code (FK)
  ├─ event_type    : JOINING | PROBATION | CONFIRMATION | PROMOTION |
  │                  CAS | MACP | PAY_FIXATION | TRANSFER | DEPUTATION |
  │                  PAY_PROTECTION | STEPPING_UP | LEAVE_SPELL |
  │                  INCREMENT | SUSPENSION | REINSTATEMENT | RETIREMENT
  ├─ effective_date
  ├─ order_no, order_date          (sanction reference)
  ├─ old_value / new_value (JSON)   (e.g. {level,cell,basic} before→after)
  ├─ remarks
  └─ recorded_by, recorded_at       (audit, pairs with §30/§38)

Nomination
  ├─ employee_code (FK)
  ├─ scheme        : GPF | GIS | PENSION | NPS
  └─ nominee details, share %
```

Design rules:
- **Employee Code immutable** (changing identity = new person).
- **Service Book events are never edited or deleted** — a correction is a new
  reversing/superseding event with its own order reference (legal record).
- The master's `basic_pay / level / cell / next_increment_date` must always be
  **reconstructable** by replaying the relevant ServiceEvents — this is what lets
  arrears (Section 08) recompute the past.

> **Example — append-only in action:** A promotion wrongly recorded at Level 11
> instead of 12 is **not** overwritten. You add a corrective `PAY_FIXATION`
> event citing the rectification order. The history shows both — auditors see
> what happened and when it was fixed.

---

## 5. Rules & Logic

### 5.1 Deriving the master from events

```text
rebuild_master(employee):
    events = ServiceEvent[employee].sort_by(effective_date)
    for e in events:
        apply(e)            # PROMOTION/MACP/FIXATION update level,cell,basic
                            # LEAVE_SPELL(EOL) may shift next_increment_date
                            # RETIREMENT closes the record
    master = state_after_last_event
```

### 5.2 Retirement date

```text
date_of_retirement = last_day_of_month( dob + superannuation_age )
# superannuation_age: 60 for non-teaching (confirm Assam value);
# teachers may be 65 (confirm). Drives pension trigger + final-month proration.
```

### 5.3 Probation → increment interaction (rule-dependent)

```text
if rule_defers_increment_during_probation and not confirmed:
    hold normal increment until confirmation, then release as due
else:
    grant normal increment on due date regardless of probation
```

This is exactly the kind of rule that must be **configurable**, not coded — it
varies by state/era.

---

## 6. Worked Example (history → current state)

**Mr. Das, Junior Assistant** (the non-teaching joiner from Section 01):

| Date | ServiceEvent | Resulting master state |
|---|---|---|
| 01-Jul-2018 | JOINING, Level 2 cell 1, Basic ₹X | Level 2/1 |
| 01-Jul-2018 | PROBATION (2 yrs) | on probation |
| 01-Jul-2019 | INCREMENT (annual) | Level 2 cell 2 |
| 01-Jul-2020 | CONFIRMATION | confirmed |
| 15-Mar-2021 | LEAVE_SPELL: EOL 30 days | next increment date shifts |
| 01-Jul-2021 | INCREMENT (delayed per EOL) | Level 2 cell 3 |
| 01-Aug-2023 | PROMOTION → Level 4 + PAY_FIXATION | Level 4, refixed Basic |

Current Employee Master = replay of the above = **Level 4, current cell, Basic
refixed, confirmed, next increment date adjusted for the 2021 EOL**. Every later
module (salary, arrears, pension) reads this projection but can always drill into
the events that produced it.

> Notice the **EOL in 2021 silently changed the increment date** — and that one
> fact will also reduce qualifying service at retirement in ~2050. One event,
> two downstream consumers, decades apart. That is why the Service Book is the
> backbone, not a formality.

---

## 7. System Implications

- Model **Employee Master as a projection** of an **append-only ServiceEvent
  log** — don't let users free-edit Basic/Level directly; they must raise an
  event (with order reference). This gives audit + arrear-replay for free.
- **Derive** retirement date and (ideally) next-increment date — never free-type
  values that can drift from their source.
- Every event carries **order number + date** (sanction proof) and
  **recorded_by/at** (audit, §30/§38).
- Support **"not applicable"** gracefully for contractual/daily-wage (no
  probation/confirmation/fixation).
- Provide a **service verification view** for pension/audit: full chronological
  ledger with attested entries.
- **Effective-dating on every event** so the engine can answer "what was this
  person's Level in month M?" — required by arrears (Section 08).
- Validate transitions: CONFIRMATION requires a prior PROBATION; RETIREMENT
  closes the record; no events after RETIREMENT except settlement.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Superannuation age** in Assam — 60 for non-teaching? **65 for teachers?**
   Confirm; it sets retirement date for everyone.
2. **Probation period** length per cadre, and whether increment is **deferred**
   during probation or granted normally.
3. **Pay protection** rules — when joining from another govt post, what exactly
   is protected (Basic only? Level?).
4. **Stepping-up** conditions recognised by Assam (junior-senior anomaly).
5. **Deputation** terms — deputation allowance %, lien handling, who pays.
6. Whether the legacy **physical Service Book** must be digitised at go-live and
   how opening events seed the log (links to Section 19 migration).
7. Required **attestation/periodic-show-to-employee** workflow for compliance.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Employee Master** | Current snapshot of an employee used by each salary run. *Note:* a projection of the Service Book, not the source of truth for history. |
| **Service Book** | Permanent, attested, chronological record of service life. *Note:* legal document; append-only; basis for pension & seniority. |
| **Employee Code** | Immutable unique ID. *Note:* never reuse or change; identity change = new record. |
| **Date of Joining (DOJ)** | Service start date. *Note:* anchors seniority, increment, NPS/OPS branch (§04), qualifying service. |
| **Retirement / Superannuation Date** | Date service ends on age. *Note:* **derive** from DOB + age rule; teachers may differ from non-teaching. |
| **Probation** | Trial period on first appointment. *Note:* may defer increment until confirmation (configurable). |
| **Confirmation** | Making service permanent after probation. *Note:* fixes seniority; some benefits unlock here. |
| **Pay Protection** | Safeguarding prior higher pay when joining from another post. *Note:* prevents pay drop; recorded as a fixation event. |
| **Stepping Up** | Raising a senior's pay to match an anomalously higher-paid junior. *Note:* anomaly-removal rule; needs both employees' data. |
| **Deputation** | Temporary service in another org with lien retained. *Note:* may add deputation allowance; pay per deputation terms. |
| **Lien** | Right to return to one's substantive post (e.g. after deputation). *Note:* must survive a deputation/transfer without losing the home post. |
| **Dies-non / EOL spell** | Period not counting as service (e.g. unsanctioned EOL). *Note:* shifts increment date and cuts qualifying service — record precisely. |
| **Pay Fixation event** | Re-setting Basic on promotion/MACP/revision. *Note:* stored with option date; replayed by arrears (§08). |
| **Nomination** | Declared beneficiary for GPF/GIS/pension. *Note:* mandatory; pulled at death/retirement settlement (§16). |
| **Attestation** | Officer's certification of a Service Book entry. *Note:* compliance requirement; entries periodically shown to employee. |
| **Projection / Replay** | Rebuilding current state by applying all past events. *Note:* the pattern that makes audit + arrears possible. |

---

### Status
Section 02 complete. Update roadmap tracker: 02 → ✅ Done.
Next: **Section 03 — Pay Matrix & Basic Pay**.
