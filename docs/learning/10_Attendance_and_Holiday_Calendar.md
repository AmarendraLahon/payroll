# Section 10 — Attendance & Holiday Calendar

> Learning roadmap §10. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §15 (Attendance), §34 (Holiday Calendar Master).
> Section 09 produced **leave** as the explicit absence ledger. This section
> supplies the **other half of presence**: the calendar that defines which days
> are *expected* working days, and the attendance signal that confirms a person
> actually worked them. Together they decide the **payable-day count** that
> proration (Section 05) and LWP (Section 06) depend on.

---

## 1. Purpose

Salary in government is conceptually **monthly and full** — a regular employee is
paid the whole month unless something *removes* a day (unauthorised absence, LWP,
dies-non, joining/leaving mid-month). To know what to remove, the system needs
two reference frames:

1. **Holiday Calendar** — which days the institution is *closed* (so absence on
   them is not absence at all), and which days are *working days* (the
   denominator for any proration).
2. **Attendance** — evidence that the employee was *present* on each working day,
   or accounted for by an approved leave (Section 09).

The payroll question this section answers:

> "For month M, how many days was this employee **payable** — and were any days
> **unauthorised** (no attendance, no approved leave) that must convert to LWP?"

For most regular staff this is a non-event (full month, full pay). It only bites
on the edges — new joiners, leavers, suspensions, unapproved absence, and
proration of attendance-linked allowances.

---

## 2. Governing Rules / Authority

- **Working days / holidays** are fixed by the **university's own Holiday
  Calendar**, issued yearly, aligned to the **state government gazetted holiday
  list** (General Administration Dept) plus local/college-specific holidays.
- **Weekly off** (Sunday; often the **second Saturday**) is per university
  service rule.
- **Unauthorised absence** treatment (conversion to **dies-non / LWP**) flows
  from the **Assam Services / FR-SR** leave-and-absence rules (Section 09's
  authority), not from attendance hardware.
- **Vacation department** rules (teachers) mean the academic calendar's
  vacation period is *paid non-working* time — it is **not** treated as absence
  (recall §09: vacation staff get reduced EL precisely because vacation is paid).

> Attendance technology (biometric/face) is an **administrative/HR** control. It
> *feeds* payroll but the **legal basis** for docking pay is always a leave/
> absence rule, never "the machine had no punch".

---

## 3. Core Concepts

### 3.1 The three attendance modes (§15)

The concept doc lists three ways presence is captured. They differ in *evidence
strength*, not in payroll meaning:

| Mode | How presence is proven | Typical use |
|---|---|---|
| **Leave-based attendance** | Present-by-default; only **leave** records absence | Most government offices, teaching staff |
| **Biometric attendance** | Fingerprint punch per day (in/out) | Non-teaching, urban campuses |
| **Face-recognition attendance** | Camera match per day | Newer deployments |

> **Key insight — leave-based is the default mental model.** In a leave-based
> regime an employee is **assumed present** every working day *unless* a leave or
> absence record says otherwise. Biometric/face just add a positive *punch* signal
> on top. The payroll engine should treat the punch as **corroboration**, and the
> **leave ledger** as the **source of truth** for pay — otherwise a missed punch on
> a day someone actually worked would wrongly dock pay.

### 3.2 Holiday Calendar Master (§34)

Four day-types per the concept doc:

| Day-type | Paid? | Working? | Note |
|---|---|---|---|
| **Gazetted Holiday** | Yes | No | Fixed, closed, paid |
| **Restricted Holiday (RH)** | Yes | No (if availed) | Optional list; employee picks ≤ quota (§09) |
| **Weekly Off** | Yes | No | Sunday / 2nd Saturday etc. |
| **Working Day** | Yes | Yes | The proration denominator |

- The calendar is **per-year and per-college/campus** — a constituent college may
  have **local holidays** the main campus does not.
- It drives **payable-day counts, comp-off eligibility, and CL-adjacency rules**
  (e.g. CL cannot normally be sandwiched to bridge two holidays — that's a
  calendar-aware validation).

### 3.3 Working days vs calendar days — the proration denominator

Two different denominators exist; choosing wrong is a classic payroll bug:

```text
Calendar days in month   = 28..31         (actual length)
Working days in month    = calendar − (gazetted + weekly-off + RH availed)
```

Government practice for salary proration is usually **calendar-day based**
(₹/30 or ₹/actual-days), **not** working-day based — i.e. a mid-month joiner is
paid `monthly_pay × served_days / month_days`, where holidays *within* the served
span are **paid**. Which convention Assam uses is a §8 confirm item, but the data
model must support either.

### 3.4 Holidays inside an absence span are still (usually) holidays

If an employee is on **EL** Friday–Monday with a Sunday in between, the Sunday is
**not debited** from EL (it was already a non-working paid day). But for **EOL/
dies-non**, prefix/suffix holidays can sometimes be **included** in the
loss-of-pay span depending on the rule. This is exactly why leave (Section 09)
and the calendar must be evaluated **together**, never independently.

> **Example:** Mr. Das takes EL Fri 12th → Mon 15th. Calendar shows Sat 13th =
> 2nd-Saturday off, Sun 14th = weekly off. EL **debited = 2 days** (Fri, Mon),
> not 4 — the calendar absorbs the weekend. Switch the leave to **EOL** and the
> rule may dock all 4 (or just 2) — a calendar-aware leave rule decides.

### 3.5 Unauthorised absence → LWP conversion

The bridge from attendance to pay: a working day with **no punch and no approved
leave** is **unauthorised absence**. After due process it converts to
**dies-non / LWP** (Section 06 recovery, Section 09 leave-type), which:

- removes that day's pay (proration), and
- breaks **qualifying service** (echoes to increment §07 and pension §16).

The attendance system **flags** it; an HR/sanction decision **converts** it; the
payroll engine then **prorates**. Three distinct steps — don't fuse them.

---

## 4. Data Model

```text
HolidayCalendar (per year, per campus/college)
  ├─ calendar_id, year, campus/college_code
  └─ days[]:
       ├─ date
       ├─ day_type : GAZETTED | RESTRICTED | WEEKLY_OFF | WORKING
       ├─ name            (e.g. "Bihu", "Republic Day")
       └─ is_local        (college-specific add-on)

AttendanceMode (config, per employee group)
  └─ mode : LEAVE_BASED | BIOMETRIC | FACE

AttendanceRecord (per employee per day — only for biometric/face regimes)
  ├─ employee_code, date
  ├─ status : PRESENT | ABSENT | HALF_DAY | ON_LEAVE | HOLIDAY | WEEKLY_OFF
  ├─ punch_in, punch_out        (nullable; corroboration only)
  └─ source : BIOMETRIC | FACE | MANUAL_REGULARISED

MonthlyAttendanceSummary (per employee per month — what payroll reads)
  ├─ month
  ├─ working_days, present_days, holiday_days, weekly_offs
  ├─ approved_leave_days {EL, CL, HPL, EOL, ...}   (from §09 ledger)
  ├─ unauthorised_days                              (→ LWP after sanction)
  └─ payable_days                                   (the proration numerator)
```

Design rules:
- The **calendar is master data**, effective-dated and **per campus** (Section 17
  pattern) — never hard-code holidays.
- **Daily AttendanceRecord is optional** — only materialised in biometric/face
  regimes. Leave-based groups derive presence from calendar + leave ledger alone.
- Payroll consumes the **MonthlyAttendanceSummary**, not raw punches — keep the
  hardware feed decoupled from the pay engine.
- `payable_days` is **derived**, never typed in:
  `payable_days = working_days − unauthorised_days` (holidays/weekly-offs are
  already paid; approved leave is paid per its pay-class from §09).

---

## 5. Rules & Logic

### 5.1 Building the monthly summary

```text
build_summary(employee, month):
    cal      = HolidayCalendar[employee.campus, month.year]
    working  = [d for d in days(month) if cal[d].type == WORKING]
    leaves   = LeaveLedger[employee, month]            # §09, with pay-class
    for d in working:
        if d in leaves.approved:        mark ON_LEAVE (pay per class)
        elif mode != LEAVE_BASED and no punch(employee,d) and d not regularised:
                                        mark UNAUTHORISED
        else:                           mark PRESENT
    unauthorised_days = count(UNAUTHORISED)            # pending sanction → LWP
    payable_days      = len(working) − lwp_converted_days
    return summary
```

### 5.2 Proration handoff (to Section 05/06)

```text
prorated_pay = monthly_full_pay × payable_days / proration_base
# proration_base = month_days (calendar) OR working_days — per Assam convention (§8)
```

LWP days flow to Section 06 as a recovery/zero-pay span; their **service-break**
flag flows to Sections 07 (increment shift) and 16 (qualifying service).

### 5.3 Calendar-aware validations

- **Comp-off**: only earned for work on a `GAZETTED`/`WEEKLY_OFF` day (Section 09)
  — the calendar tells you it *was* a holiday.
- **CL adjacency**: block/allow CL bridging two holidays per rule.
- **RH**: an availed RH consumes the optional-holiday quota (§09) and marks the
  day non-working for that employee only.

---

## 6. Worked Example (payable days, mid-month join)

**Mr. Das** joins **16 June** (a 30-day month). June calendar (his campus):
4 Sundays, one 2nd-Saturday, **Gazetted** holiday on 20 June.

| Quantity | Value | Note |
|---|---|---|
| Calendar days served (16–30 Jun) | 15 | join date onward |
| Holidays/weekly-offs within span | 3 | 2 Sundays + 20 Jun gazetted |
| Working days within span | 12 | |
| Unauthorised days | 0 | all present |
| **Payable days** | **15** | calendar-day proration → holidays in span are paid |

```text
Prorated pay = monthly_full_pay × 15 / 30   (calendar-day convention)
# Holidays within the served span are PAID — they're not subtracted.
# Only the 1–15 Jun pre-joining span is unpaid (he wasn't an employee yet).
```

> Now add an **unauthorised absence** on 25 June (working day, no leave, no
> punch). After sanction it converts to **1 day LWP** → payable days 15 → 14, pay
> docked one day, and that day flags a (small) **service break** that §07/§16
> will read. Same engine, one fewer payable day.

---

## 7. System Implications

- Build a **Holiday Calendar master**: per-year, **per-campus/college**,
  effective-dated, with the four day-types — the backbone for proration, comp-off,
  and leave-adjacency rules.
- Support **all three attendance modes** but treat **leave-based as the pay source
  of truth**; biometric/face punches are **corroboration**, surfaced for HR, not a
  direct pay-docking trigger.
- Produce a **MonthlyAttendanceSummary** per employee-month as the **single input**
  payroll reads; keep raw punch ingestion decoupled.
- **Derive `payable_days`** (working − LWP); never store holidays/weekly-offs as
  unpaid.
- Evaluate **leave and calendar together** (weekend absorption, EOL prefix/suffix,
  comp-off eligibility) — never in isolation.
- Implement **unauthorised → LWP** as a three-step flow (flag → sanction →
  prorate); propagate the **service-break** to increment (§07) and pension (§16).
- Make the **proration base** (calendar-day vs working-day) **configurable** to
  match Assam convention.
- Support **manual regularisation** of missed punches (with audit) so honest work
  isn't docked by a hardware miss.

---

## 8. Open Questions / State-Specific (confirm before build)

1. Assam/university **proration convention** — calendar-day (₹/30 or ₹/actual) or
   working-day based?
2. Which **attendance mode** is authoritative per staff group (teaching usually
   leave-based; non-teaching biometric)?
3. **Weekly-off** definition — every Saturday, only 2nd Saturday, or campus-varied?
4. **Holiday treatment inside EOL/dies-non** spans — included in or excluded from
   the loss-of-pay count?
5. **Unauthorised-absence** due process and the trigger for **dies-non vs LWP**
   conversion.
6. **Per-college local holidays** — who issues them, and do they affect treasury
   bill day-counts?
7. **Vacation-department** handling — confirm vacation period is flagged paid
   non-working (no proration), and its interaction with EL accrual (§09).
8. Does treasury/audit require an **attendance certificate** with the salary bill
   (Section 13)?

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Holiday Calendar Master** | Per-year, per-campus list of day-types. *Note:* backbone for proration, comp-off, leave-adjacency. |
| **Gazetted Holiday** | Fixed, paid, non-working day. *Note:* from state gazette list; closed campus. |
| **Restricted Holiday (RH)** | Optional holiday from a quota list. *Note:* per employee; consumes §09 RH quota. |
| **Weekly Off** | Sunday / 2nd-Saturday etc. *Note:* paid non-working; absorbs weekends inside leave spans. |
| **Working Day** | A day work is expected. *Note:* the proration denominator; presence/leave required. |
| **Leave-based Attendance** | Present-by-default; only leave marks absence. *Note:* the pay source of truth. |
| **Biometric / Face Attendance** | Punch/camera presence capture. *Note:* corroboration only — never the sole pay-docking trigger. |
| **Payable Days** | Days the employee is paid for in a month. *Note:* derived = working − LWP; holidays already paid. |
| **Proration Base** | Denominator for partial-month pay. *Note:* calendar-day vs working-day — configurable (§8). |
| **Unauthorised Absence** | Working day with no punch and no approved leave. *Note:* flagged → sanctioned → converts to LWP. |
| **Dies-non / LWP** | Day that doesn't count for pay/service. *Note:* breaks qualifying service (→ §07, §16). |
| **Manual Regularisation** | HR override of a missed/wrong punch. *Note:* audited; prevents docking honest work. |
| **MonthlyAttendanceSummary** | The per-month roll-up payroll reads. *Note:* decouples hardware feed from pay engine. |
| **Vacation Department** | Teaching unit with paid vacation. *Note:* vacation = paid non-working, not absence (links §09 reduced EL). |

---

### Status
Section 10 complete. Update roadmap tracker: 10 → ✅ Done.
Phase 4 (Leave & Attendance) complete. Next: **Section 11 — Claims & Reimbursements** (Phase 5).
