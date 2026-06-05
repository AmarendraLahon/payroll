# Section 03 — Pay Matrix & Basic Pay

> Learning roadmap §03. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §3 (Pay Matrix), §5 (Basic Pay).
> Section 02 stored *where* an employee sits (Level, Cell). This section explains
> **what that position means** and how it produces the single most important
> number in payroll: **Basic Pay**.

---

## 1. Purpose

**Basic Pay is the seed from which almost the entire salary grows.** DA, HRA,
NPS/GPF, pension, gratuity, leave encashment — all are computed *from* Basic. So
the system must answer one question with total precision:

> "Given this employee's **Level** and **Cell**, what is their Basic Pay — and
> how does it change on increment, promotion, or pay revision?"

The **Pay Matrix** is the lookup table that answers it. Understanding its
geometry (rows = Levels, columns = Cells) is the whole of this section.

---

## 2. Governing Rules / Authority

- **7th CPC Pay Matrix** is the structure; for Assam **non-teaching** staff it is
  adopted via **Assam ROP Rules 2017** (Section 01).
- For **teaching** staff, the **UGC Regulations 2018** define a *separate*
  matrix — the **Academic Pay Levels** (10–15A).
- Movement within/between cells is governed by **FR/SR pay-fixation rules** and
  the **increment rules** (Section 07 expands this).

> **Recall from §01:** there are **two matrices**. "Level 10" in the state matrix
> ≠ "Academic Level 10". The system keys every lookup by `(pay_authority, level,
> cell)`, never by level alone.

---

## 3. Core Concepts

### 3.1 The matrix geometry

The Pay Matrix is a 2-D grid:

- **Rows = Pay Levels** — replace the old "Grade Pay". A Level corresponds to a
  rank/status (e.g. Level 1 = lowest Grade IV; higher Levels = senior posts).
- **Columns = Cells (Index 1, 2, 3 …)** — successive **annual increment stages**
  within a Level. Each cell is the previous cell × **≈1.03**, rounded to the next
  ₹100 (the 7th CPC "3% increment, round up to 100" rule).

```text
            Cell→  1        2        3        4     ...
 Level 1          18000    18500    19100    19700  ...
 Level 2          19900    20500    21100    21700  ...
 Level 3          21700    22400    23100    23800  ...
   ...
 Level 10         56100    57800    59500    61300  ...   (entry grade for officers / Asst Prof in academic matrix)
```

*(Values above are the standard central 7th-CPC matrix, shown to illustrate
shape. Assam's adopted figures — and the UGC academic figures — must be loaded
from the actual notification; see §8.)*

### 3.2 Basic Pay = one cell of the matrix

An employee's **Basic Pay is simply the value at their `(Level, Cell)`**. Nothing
is calculated — it is **read** from the matrix.

> **Example:** Employee at **Level 2, Cell 3** → Basic = the value in that cell,
> e.g. ₹21,100. That's it. The complexity is not in *reading* Basic but in
> *deciding which cell* the employee occupies after life events.

### 3.3 The three ways Basic changes

| Trigger | Movement in matrix | Section |
|---|---|---|
| **Annual Increment** | Same Level, **move down one cell** (Cell n → n+1) | 07 |
| **Promotion / MACP** | Move to a **higher Level**, placed at the appropriate cell | 07 |
| **Pay Revision** (new CPC/ROP) | **Whole matrix replaced**; pay re-fixed in new grid | 08 |

> **Example — increment is a column move:** Level 2, Cell 3 (₹21,100) gets annual
> increment → Level 2, **Cell 4** (₹21,700). Same row, next column. The ~₹600
> jump *is* the ~3% increment, already baked into the matrix.

> **Example — promotion is a row jump:** Promoted from Level 2 to Level 4. You
> don't stay in "Cell 4"; pay is **re-fixed** in Level 4 (one notional increment
> in old level, then the next-higher cell in the new level). The exact landing
> cell is a fixation rule (Section 07). The point here: promotion changes the
> **row**, not just the column.

### 3.4 Two matrices side by side

| | Non-teaching (state) | Teaching (UGC) |
|---|---|---|
| Grid name | Pay Matrix Levels 1–18 | Academic Pay Levels 10–15A |
| Source | Assam ROP Rules 2017 | UGC Regulations 2018 |
| Asst Professor entry | — | Academic Level 10 |
| Associate Professor | — | Academic Level 13A |
| Professor | — | Academic Level 14 |
| Junior Assistant | Level 2 (illustrative) | — |

The engine must hold **both grids** and pick by `pay_authority` (set in §01).

### 3.5 Entry Pay

Each Level has an **entry cell** (Cell 1) — the Basic a fresh recruit starts at.
Direct recruits begin at entry pay; promotees are *fixed* (not started at entry).

---

## 4. Data Model

The matrix is **versioned master data** (it changes with each pay revision), and
Basic is **derived**, not stored as a free number.

```text
PayMatrix (reference, versioned)
  ├─ pay_authority   : ASSAM_ROP_2017 | UGC_2018       (which grid)
  ├─ level           : e.g. 2  | ACADEMIC_10
  ├─ cell_index      : 1,2,3,...
  ├─ basic_amount    : the rupee value at (level, cell)
  ├─ effective_from                                    (revision version)
  └─ effective_to     (null = current)
  PK = (pay_authority, level, cell_index, effective_from)

Employee (from §02) holds only the POSITION:
  ├─ pay_authority, pay_level, pay_cell
  └─ basic_pay  ← DERIVED = lookup PayMatrix(authority, level, cell, on=month)
```

Design rules:
- **Never store Basic as an independent editable number.** Store the *position*
  `(level, cell)`; look up the amount. This guarantees Basic always agrees with
  the matrix and makes pay revisions a data swap, not a per-employee edit.
- The matrix is **effective-dated** so a past month reads the *old* grid (this is
  what makes pay-revision arrears computable — Section 08).
- Hold **both authorities' grids** in the same table, discriminated by
  `pay_authority`.

> **Example — why position not amount:** When Assam notifies a new ROP, you load
> a new matrix version with a new `effective_from`. Every non-teaching employee's
> Basic updates automatically because it's *derived* from their unchanged
> `(level, cell)`. If you had stored Basic as a number, you'd edit thousands of
> rows by hand and lose the old values needed for arrears.

---

## 5. Rules & Logic

### 5.1 Read Basic for a given month

```text
basic_pay(employee, month):
    grid = PayMatrix.version_effective_in(month)        # past month → old grid
    return grid.lookup(employee.pay_authority,
                       employee.pay_level,
                       employee.pay_cell)
```

### 5.2 Annual increment (column move)

```text
increment(employee):
    employee.pay_cell += 1          # next cell, same level
    # Basic auto-updates via lookup. (Eligibility/date rules → Section 07)
```

### 5.3 Promotion (row move + fixation)

```text
promote(employee, new_level):
    notional = matrix(current_level, current_cell + 1)   # one notional increment
    new_cell = first cell in new_level whose amount >= notional
    employee.pay_level = new_level
    employee.pay_cell  = new_cell
    # exact rule (FR 22 etc.) is configurable → Section 07
```

### 5.4 Pay revision (grid swap)

```text
revise_pay(employee, new_grid):
    revised_basic = old_basic × fitment_factor   # e.g. 7th CPC used 2.57
    employee.(level,cell) = cell in new_grid matching/above revised_basic
    # difference vs old pay for past months → arrears (Section 08)
```

---

## 6. Worked Example (position drives everything)

**Mr. Das**, non-teaching, `pay_authority = ASSAM_ROP_2017`:

| Event | Level | Cell | Basic (read from matrix) |
|---|---|---|---|
| Joins (entry pay) | 2 | 1 | ₹19,900 |
| Annual increment | 2 | 2 | ₹20,500 |
| Annual increment | 2 | 3 | ₹21,100 |
| Promotion to Level 4 (fixation) | 4 | (fixed) | refixed, e.g. ₹25,500 |

Now watch the ripple — **everything downstream reads that final Basic**:

```text
Basic (Level 4)        = 25,500
DA  @ (say) 50%        = 12,750        (Basic × DA%)        → Section 05
HRA @ (say) 16%        =  4,080        (Basic × HRA%)       → Section 05
NPS @ 10% of (Basic+DA)=  3,825        (deduction)          → Section 06
Pension/gratuity later  based on this Basic                 → Section 16
```

Change the **cell** and every one of those numbers moves. That is why this
section is the hinge between "where the employee sits" (§02) and "what they get
paid" (§05 onward).

---

## 7. System Implications

- Store **`(level, cell)` as the employee's pay position; derive Basic** by
  matrix lookup. Forbid free-editing Basic.
- Keep the **matrix as versioned, effective-dated master data**; a pay revision
  is a *new version*, not edits to employee rows.
- Maintain **two grids** (state + UGC academic) keyed by `pay_authority`.
- Implement three distinct movements — **increment (cell+1), promotion (level
  change + fixation), revision (grid swap + fitment)** — as separate, auditable
  operations that each emit a **ServiceEvent** (§02).
- Provide a **"Basic in month M"** function (reads the version effective then) —
  consumed by arrears (§08) and every retro calculation.
- Validate that an employee's `(level, cell)` actually **exists** in the grid
  effective for the month (no orphan cells after a revision).

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Assam ROP 2017 matrix values** — load the exact non-teaching grid (Levels &
   cell amounts) from the notification; do not assume central figures.
2. **UGC Academic Pay Level values** as adopted by Assam (10–15A grid).
3. **Fitment factor** used by Assam (central used **2.57**) — needed for the
   6th→7th transition arrears of legacy staff.
4. Exact **promotion fixation rule** (which FR clause; one notional increment +
   next-higher-cell, or variant) — feeds Section 07.
5. **Rounding rule** in the adopted matrix (3% then round up to next ₹100, or
   state variant).
6. Mapping of **designations → Levels** for both teaching and non-teaching cadres
   at this university.
7. Number of **cells per Level** in the adopted grid (central runs to ~40).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Pay Matrix** | 2-D grid: rows = Levels, columns = Cells. *Note:* replaces 6th-CPC pay-band + grade-pay; the single source for Basic. |
| **Pay Level** | A row = a rank/status. *Note:* ambiguous until paired with `pay_authority` — state Level ≠ academic Level. |
| **Cell / Index** | A column = an annual increment stage in a Level. *Note:* each cell ≈ prev × 1.03, rounded up to ₹100. |
| **Basic Pay** | The rupee value at the employee's `(Level, Cell)`. *Note:* **derive by lookup**, never store as a free number. |
| **Entry Pay / Entry Cell** | Cell 1 of a Level — a fresh recruit's start. *Note:* direct recruits start here; promotees are *fixed*, not started here. |
| **Annual Increment** | Move one cell to the right (same Level). *Note:* the ~3% raise is pre-baked into the matrix (Section 07 for date/eligibility). |
| **Promotion (row move)** | Jump to a higher Level with pay **re-fixed**. *Note:* not "same cell in new row"; uses a fixation rule. |
| **Pay Fixation** | Computing the landing cell after promotion/MACP/revision. *Note:* one notional increment then next-higher cell (configurable). |
| **Fitment Factor** | Multiplier converting old-grid Basic to new-grid (7th CPC = 2.57). *Note:* used at pay revision; drives transition arrears. |
| **Academic Pay Level** | UGC teaching grid (10–15A). *Note:* separate matrix; Asst Prof=10, Assoc=13A, Prof=14 (confirm Assam adoption). |
| **Pay Revision** | Replacing the whole matrix (new CPC/ROP). *Note:* a versioned data swap; old version retained for arrears. |
| **Effective-dated matrix** | Each grid version valid for a date range. *Note:* lets a past month read its own grid — essential for arrears (§08). |
| **Notional Increment** | A "paper" increment used only to compute fixation, not paid as such. *Note:* appears in promotion/revision math. |

---

### Status
Section 03 complete. Update roadmap tracker: 03 → ✅ Done.
Next: **Section 04 — Pension Scheme Determination (NPS vs OPS/GPF)**.
