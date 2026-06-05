# Section 07 — Increment, Pay Fixation & MACP

> Learning roadmap §07. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §11 (Increment), §12 (Pay Fixation), §24 (Increment & Fixation rules + MACP).
> Sections 03–06 computed pay for a **static** position. This section is about
> **how the position changes over time** — the events that move an employee
> through and across the Pay Matrix.

---

## 1. Purpose

An employee's Basic isn't static — it rises through three distinct mechanisms,
and the system must apply each correctly because **each emits a ServiceEvent
(§02), re-derives Basic (§03), and often produces arrears (§08):**

| Mechanism | What moves | Frequency |
|---|---|---|
| **Annual Increment** | Cell +1 (same Level) | Yearly |
| **Promotion / MACP** | Level up + fixation | On promotion / at 10-20-30 yrs |
| **Pay Fixation** | Re-compute Basic after a Level change/revision | On each of the above |

The recurring trap: people think "increment = +3%". Mechanically it's "**move one
cell right and read the new value**" — and *when* that move is allowed is a real
rule with dates and eligibility.

---

## 2. Governing Rules / Authority

- **Increment** under 7th CPC / Assam ROP 2017: **two annual increment dates —
  1 January and 1 July** (the 6th CPC had a single 1 July date).
- **Pay fixation** on promotion governed by **Fundamental Rules** (the classic
  **FR 22** family) — one notional increment + placement in higher level.
- **MACP (Modified Assured Career Progression)** — financial upgradation at
  **10, 20, 30 years** of service to relieve stagnation (non-teaching).
- **Teaching staff** progress by **CAS (Career Advancement Scheme)** under **UGC
  Regulations 2018**, *not* MACP — different criteria (service + academic
  performance). Keep the two engines separate (recall §01).

---

## 3. Core Concepts

### 3.1 Annual Increment — the dual-date rule

Under 7th CPC there are **two increment dates: 1 Jan and 1 Jul**. An employee is
assigned **one** of them based on when they joined / were last fixed, and must
have rendered **at least 6 months** of qualifying service on that date to earn
the increment.

```text
increment: pay_cell += 1     # move one cell right; Basic auto-updates (§03)
# the ~3% raise is already baked into the next cell (§03)
```

> **Example — the 6-month rule:** Join on **5 Jan 2024** → first increment falls
> on **1 Jul 2024**? No — only ~6 months by 1 Jul, but the rule needs 6 months of
> service *as on* the increment date; joining 5 Jan gives ~6 months by 1 Jul, so
> the **1 Jul** cycle applies. Someone joining **5 Feb 2024** hasn't completed 6
> months by 1 Jul 2024, so their first increment shifts to **1 Jan 2025**. The
> exact cutoff is a rule — confirm Assam's adoption (§8).

### 3.2 Withheld / deferred increment

An increment can be **withheld** (penalty) or **deferred** because of
**dies-non/EOL** (Section 02). The **Next Increment Date** then shifts.

> **Example:** 30 days EOL in a year can push the next increment date forward,
> because the lost period breaks the qualifying service. This is the §02 EOL
> spell surfacing again — one event, many consumers.

### 3.3 Pay Fixation — recomputing Basic on a Level change

When an employee moves to a higher Level (promotion, MACP, or a pay revision),
Basic is **re-fixed**, not carried as-is. The classic rule:

```text
1. Grant one NOTIONAL increment in the current level (cell+1 value).
2. Place at the cell in the NEW level that is equal to or next-above that value.
3. Employee may OPT for the fixation date:
     (a) date of promotion, OR
     (b) date of next increment
   — whichever gives better long-term benefit (the "option form").
```

> **Example — promotion fixation:** At Level 2, Cell 3 = ₹21,100. Promoted to
> Level 4.
> 1. Notional increment in Level 2 → Cell 4 = ₹21,700.
> 2. In Level 4, find the first cell ≥ 21,700 → say ₹25,500.
> 3. New Basic = **₹25,500** at Level 4. Employee files an **option** for whether
>    fixation takes effect on the promotion date or the next increment date.

### 3.4 The Option Form (why it matters)

The employee can choose the fixation date because the two choices yield different
future pay trajectories. The system must **record the option** and may need to
**compute both scenarios** to advise. The choice affects the **next increment
date** in the new level too.

### 3.5 MACP — financial upgradation without promotion

If an employee **stagnates** (no promotion) they still get financial relief:

- Granted at **10, 20, 30 years** of continuous service.
- Moves the employee to the **next Pay Level** in the matrix (a financial
  upgradation — same duties, higher Level/pay).
- Triggers a **pay fixation** (same FR-22-style logic + option).

> **Example:** A Junior Assistant with no promotion in 10 years gets **1st MACP**
> → moved from Level 2 to Level 3 (next level), pay re-fixed. At 20 years → 2nd
> MACP (Level 4). At 30 → 3rd MACP. Promotions already taken **count against**
> the MACP quota (3 financial upgradations total across promotions + MACP).

### 3.6 CAS — the teaching analogue (pointer)

Teachers don't use MACP. **CAS** advances Assistant → Associate → Professor based
on years in grade + academic criteria (API/PBAS as applicable), each stage a
**fixation** in the UGC academic matrix. Same *fixation mechanics*, different
*eligibility rules*. Handled wherever teaching pay is processed; flagged here so
the engines aren't conflated.

---

## 4. Data Model

```text
ServiceEvent (from §02) — these events drive pay movement:
  ├─ INCREMENT      { date, old_cell→new_cell }
  ├─ PROMOTION      { date, old_level/cell → new_level/cell, order_ref }
  ├─ MACP           { stage:1|2|3, date, old_level → new_level }
  ├─ PAY_FIXATION   { trigger, notional_basis, opted_date, statement_ref }
  └─ (EOL_SPELL shifts next_increment_date)

Employee (current, §02/§03)
  ├─ pay_level, pay_cell, basic_pay (derived)
  ├─ increment_cycle : JAN | JUL
  ├─ next_increment_date
  └─ macp_count      : 0..3   (upgradations used; promotions count here too)

IncrementRule / FixationRule (config)
  ├─ dual_dates, min_service_months (6)
  ├─ fixation_method (FR-22 variant), option_allowed
  └─ effective_from/to
```

Design rules:
- Every movement is a **ServiceEvent** (auditable, replayable) — never a silent
  Basic edit (§02 principle).
- `next_increment_date` is **derived/maintained** by the rules, adjusted by
  EOL/withholding.
- **MACP quota** tracks promotions + MACP together (max 3).
- Fixation **method and option rule are config**, not hard-code (they vary).

---

## 5. Rules & Logic

### 5.1 Annual increment

```text
grant_increment(employee, increment_date):
    if qualifying_service(employee, increment_date) >= 6 months
       and not withheld:
        emit INCREMENT: pay_cell += 1
        next_increment_date = same cycle next year
    else:
        defer to next eligible cycle
```

### 5.2 Pay fixation (promotion / MACP / revision)

```text
fix_pay(employee, new_level, opted_date):
    notional = matrix(current_level, current_cell + 1)      # 1 notional increment
    new_cell = first cell in new_level with amount >= notional
    emit PAY_FIXATION + set (pay_level=new_level, pay_cell=new_cell)
    set next_increment_date per opted_date choice
```

### 5.3 MACP trigger

```text
on_service_anniversary(employee):
    yrs = continuous_service(employee)
    if yrs in {10,20,30} and macp_count < 3 and no_recent_promotion_upgrade:
        next_level = level_above(current_level)
        fix_pay(employee, next_level, opted_date)
        macp_count += 1
```

---

## 6. Worked Example (a career's pay movement)

**Mr. Das**, non-teaching, JUL increment cycle:

| Date | Event | Level/Cell | Basic | Note |
|---|---|---|---|---|
| 01-Jul-2018 | Join (entry) | 2 / 1 | 19,900 | increment_cycle = JUL |
| 01-Jul-2019 | Increment | 2 / 2 | 20,500 | cell +1 |
| 15-Mar-2021 | EOL 30 days | 2 / — | — | next incr date shifts |
| 01-Jan-2022 | Increment (shifted) | 2 / 3 | 21,100 | delayed by EOL |
| 01-Jul-2028 | **1st MACP** (10 yrs) | 3 / fixed | refixed | stagnation relief, +1 Level |
| 01-Aug-2030 | Promotion → Level 4 | 4 / fixed | refixed | option filed |

Each row is a **ServiceEvent**; Basic is always **re-derived** from the resulting
`(Level, Cell)` against the matrix version effective that month. A back-dated MACP
order would also generate **arrears** for the months between the effective date
and the processing date (Section 08).

> **The throughline:** increment = column move, MACP/promotion = row move +
> fixation, and the 2021 EOL still echoes — it delayed the increment *and* will
> reduce qualifying service at retirement. Sections 02 → 07 → 16 all read it.

---

## 7. System Implications

- Implement **two increment dates (Jan/Jul)** with the **6-month eligibility**
  rule; assign each employee a cycle and **derive** next increment date.
- Treat increment as **cell+1 then re-derive Basic** — don't store a "+3%"
  number.
- Make **fixation a first-class operation**: notional increment → next-higher
  cell → record **option** → set new next-increment-date.
- Track **MACP at 10/20/30 yrs** with a **shared quota** against promotions
  (max 3 upgradations).
- Keep **MACP (non-teaching) and CAS (teaching) engines separate** — different
  eligibility, same fixation mechanics.
- Reflect **EOL/withholding** by shifting `next_increment_date` (consumes §02).
- Every movement emits a **ServiceEvent**; back-dated orders must trigger
  **arrears** (Section 08).
- Keep increment/fixation **rules in config** (dates, method, option) — they vary
  by era and state.

---

## 8. Open Questions / State-Specific (confirm before build)

1. Has Assam adopted the **dual increment dates (Jan/Jul)** and the exact
   **6-month** eligibility cutoff, or a variant?
2. Exact **fixation method** Assam follows (which FR clause; standard one-notional
   + next-higher-cell?).
3. **Option-form** rules — choices allowed and default if no option filed.
4. **MACP** specifics in Assam — levels granted, hierarchy vs next-level,
   counting of promotions, and any **benchmark/ACR** condition.
5. **CAS** stages, service requirements, and academic criteria as adopted by
   Assam/this university (for teaching).
6. How **EOL/dies-non** shifts the increment date (exact rule).
7. **Withheld increment** — cumulative vs non-cumulative effect.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Annual Increment** | Yearly move to the next cell (same Level). *Note:* ~3% baked into the matrix; mechanically just cell+1. |
| **Increment Date (Jan/Jul)** | The two 7th-CPC increment dates. *Note:* each employee on one cycle; needs 6 months service on that date. |
| **6-Month Eligibility** | Minimum service on the increment date to earn it. *Note:* decides which cycle a new joiner's first increment lands on. |
| **Next Increment Date** | When the next increment is due. *Note:* derived; shifts on EOL/withholding. |
| **Withheld Increment** | Increment stopped as a penalty. *Note:* may be cumulative or not — config. |
| **Pay Fixation** | Re-computing Basic after a Level change/revision. *Note:* notional increment → next-higher cell; emits a ServiceEvent. |
| **Notional Increment** | A paper increment used only to compute fixation. *Note:* not paid as such; the basis for the new cell. |
| **Option Form** | Employee's choice of fixation date (promotion date vs next increment). *Note:* affects future trajectory; must be recorded. |
| **Fixation Statement** | The document showing how new Basic was derived. *Note:* audit + arrear basis. |
| **MACP** | Financial upgradation at 10/20/30 yrs (next Level). *Note:* non-teaching; max 3, shared quota with promotions. |
| **Financial Upgradation** | Higher Level/pay without changed duties. *Note:* what MACP grants; not a real promotion. |
| **CAS** | Teaching career advancement (UGC). *Note:* analogue of MACP for teachers; separate engine. |
| **Qualifying Service** | Service that counts toward increment/MACP/pension. *Note:* EOL/dies-non reduces it. |

---

### Status
Section 07 complete. Update roadmap tracker: 07 → ✅ Done.
Next: **Section 08 — Arrears**.
