# Section 05 — Earnings & Monthly Allowances

> Learning roadmap §05. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §4 (earnings), §6 (DA), §7 (HRA), §8 (TA), §9 (academic allowances), §22 (formulas).
> Section 03 produced **Basic**. This section turns Basic into **Gross earnings**
> by stacking the monthly allowances on top.

---

## 1. Purpose

Gross salary is **Basic + a stack of allowances**. Most allowances are not
independent numbers — they are **derived from Basic** by a percentage or a slab.
So once Basic is known (Section 03), the earnings side is largely mechanical *if*
you know each allowance's **base, rate, and rule**.

This section's job: define, for every earning component, the **five attributes**
the engine needs —

> **base** (what it's a % of) · **rate** (the %/slab) · **formula** ·
> **rounding** · **effective date**.

Miss any one and the salary is subtly wrong (e.g. right DA% but wrong rounding →
₹1 mismatches that break treasury reconciliation).

---

## 2. Governing Rules / Authority

- **DA, HRA, TA** rates are set by **government orders** (centre issues; Assam
  notifies its own rates/dates). They change **periodically** — DA typically
  twice a year.
- **City classification (X/Y/Z)** for HRA and TA is fixed by government order
  based on city population.
- **Academic/university allowances** come from **UGC** and/or the **university's
  own Statutes/Ordinances** (Section 01).
- All rates are **effective-dated**, which is what makes mid-year revisions and
  arrears (Section 08) necessary.

> **Recall:** "which rate applies?" always means **the rate in force in the month
> being processed**, not today's rate.

---

## 3. Core Concepts

### 3.1 The earnings stack

```text
  Basic Pay              (from matrix, §03)         ← the base
+ Dearness Allowance     (Basic × DA%)              ← inflation comp
+ House Rent Allowance   (Basic × HRA%)             ← housing, by city class
+ Transport Allowance    (slab + DA on TA)          ← commuting
+ Academic/Special/etc.  (fixed or rule-based)      ← role-specific
─────────────────────────
= Gross Salary
```

### 3.2 Dearness Allowance (DA)

Compensation against inflation. **Base = Basic Pay. Rate = DA% (a single
nationwide-style figure that steps up over time).**

```text
DA = Basic × DA%
```

> **Example:** Basic ₹25,500, DA 50% → DA = ₹12,750. When the government raises DA
> to 53% from a back-date, the extra 3% for past months becomes **DA arrear**
> (Section 08). DA is the most frequent arrear source precisely because it
> changes twice a year with retrospective effect.

### 3.3 House Rent Allowance (HRA)

Housing compensation, as a **% of Basic that depends on city classification**.

| City Class | Population tier | HRA rate (7th CPC norm) |
|---|---|---|
| **X** | Metro / largest cities | 24% |
| **Y** | Mid-size cities | 16% |
| **Z** | Smaller towns / rest | 8% |

Two conditions modify it:

1. **Government accommodation:** if the employee occupies a government quarter,
   **HRA is not paid** (instead a **licence fee** may be recovered — Section 06).
2. **DA-linked revision:** HRA rates step up (e.g. to 27/18/9%) when DA crosses
   defined thresholds — so HRA% itself is effective-dated.

```text
HRA = Basic × HRA%(city_class, effective_date)     # 0 if govt quarter occupied
```

> **Example — Assam reality:** Most Assam university towns are likely **Z (8%)**;
> Guwahati may be **Y (16%)**. So the *same* Basic ₹25,500 yields HRA ₹2,040 (Z)
> vs ₹4,080 (Y) by posting city alone. City class must be a data attribute, not
> an assumption. (Confirm actual classification — §8.)

### 3.4 Transport Allowance (TA)

For commuting. Unlike DA/HRA, TA is **not a % of Basic** — it's a **slab** based
on **Pay Level** and **city category**, and crucially **DA is paid on TA too**.

```text
TA payable = TA_slab(pay_level, city_category) + DA% × TA_slab
```

> **Example — DA applies on TA:** TA slab ₹3,600, DA 50% → TA payable = 3,600 +
> 1,800 = **₹5,400**. Forgetting the "DA on TA" component is a common
> under-payment bug. Higher Levels get a higher slab; certain locations get a
> higher city rate.

Special cases: differently-abled employees get **double TA**; employees on EOL or
absent the whole month typically get **no TA** (it's for actual commuting).

### 3.5 Academic / University-Specific Allowances (§9)

Role- or activity-based, often **fixed amounts** set by UGC or the university's
Statutes:

- Academic Allowance, Research Allowance
- Special Duty Allowance
- Examination Duty Honorarium, Invigilation Payment (these are often *claim-based*
  → handled in Section 11, not monthly)

> Distinguish **monthly allowances** (paid every month with salary — covered here)
> from **claim/honorarium payments** (paid on submission of a claim — Section 11).
> The same word "allowance" spans both; the system must not.

### 3.6 Gross Salary

```text
Gross = Basic + DA + HRA + TA + (academic/special monthly allowances)
```

Gross feeds the **deduction** side (Section 06) and tax (Section 15).

---

## 4. Data Model

Allowances are defined by **versioned rate tables** plus per-employee
eligibility flags; amounts are **derived**, never stored as free numbers.

```text
DA_Rate (reference, versioned)
  ├─ da_pct, effective_from, effective_to

HRA_Rate (reference, versioned)
  ├─ city_class : X | Y | Z
  ├─ hra_pct, effective_from, effective_to

TA_Slab (reference, versioned)
  ├─ pay_level_band, city_category
  ├─ ta_amount, effective_from, effective_to

CityClassification (reference)
  ├─ city/location → class (X/Y/Z) and TA city_category

Allowance_Master (fixed/special)
  ├─ code, name, calc_type : FIXED | PCT_OF_BASIC | SLAB
  ├─ value/rate, applies_to (staff_type/designation)

Employee earning inputs (from §02/§03)
  ├─ basic_pay (derived)
  ├─ posting_city → city_class, ta_city_category
  ├─ govt_quarter_occupied : bool        (kills HRA)
  └─ special_allowance_eligibilities[]
```

Design rule: **every rate row is effective-dated**; the engine selects the row
valid in the processed month. This is the same versioning pattern as the pay
matrix (Section 03) and is what makes arrears (Section 08) possible.

---

## 5. Rules & Formulas

### 5.1 The monthly earnings computation

```text
compute_earnings(employee, month):
    basic = basic_pay(employee, month)                       # §03

    da_pct  = DA_Rate.effective_in(month)
    da      = round(basic × da_pct/100)

    if employee.govt_quarter_occupied:
        hra = 0
    else:
        hra_pct = HRA_Rate.effective_in(month, employee.city_class)
        hra     = round(basic × hra_pct/100)

    ta_slab = TA_Slab.effective_in(month, employee.pay_level_band,
                                   employee.ta_city_category)
    ta      = round(ta_slab + da_pct/100 × ta_slab)          # DA on TA!

    special = Σ eligible Allowance_Master (fixed/pct/slab)

    gross = basic + da + hra + ta + special
    return gross, {basic, da, hra, ta, special}
```

### 5.2 Proration (mid-month / LWP)

```text
factor = paid_days / days_in_month
each component (except some fixed ones per rule) × factor
# joining, retirement, EOL/LWP → Section 13/30
```

### 5.3 Rounding

Apply **one documented rule per component** (commonly round to nearest rupee).
Inconsistent rounding is the #1 cause of bill-vs-schedule mismatches in
reconciliation (Section 14).

---

## 6. Worked Example (Basic → Gross, end to end)

**Mr. Das**, non-teaching, **Level 4, Basic ₹25,500**, posted in a **Z-class**
town, **no government quarter**, DA **50%**, TA slab **₹3,600**.

```text
Basic                              = 25,500
DA   = 25,500 × 50%                = 12,750
HRA  = 25,500 × 8%  (Z class)      =  2,040
TA   = 3,600 + (50% × 3,600)       =  5,400      ← includes DA on TA
Special/academic (none)            =      0
─────────────────────────────────────────────
Gross Salary                       = 45,690
```

Now change **one input** and watch the stack move:

- **Posted in Guwahati (Y class, 16%)** → HRA = ₹4,080 → Gross = **₹47,730**.
- **Occupies a govt quarter** → HRA = 0 (licence fee recovered instead, §06) →
  Gross = **₹43,650**.
- **DA rises to 53% (back-dated)** → DA = ₹13,515, TA = ₹5,508 → Gross jumps, and
  the past-month difference becomes **DA arrear** (Section 08).

Each allowance traced to its **base × rate (effective in month)**. That
traceability is the whole point — at audit you can show *why* every rupee.

---

## 7. System Implications

- Define every earning by its **five attributes** (base, rate, formula, rounding,
  effective date) in **versioned rate tables** — never hard-code a %.
- **DA on TA** must be implemented; it's easy to forget and silently underpays.
- **Government-quarter flag zeroes HRA** and should trigger **licence-fee
  recovery** on the deduction side (Section 06) — keep the two in sync.
- **City classification** is per-posting data; don't assume one class for the
  whole university (Guwahati vs district towns differ).
- Separate **monthly allowances** (here) from **claim-based honoraria**
  (Section 11) even though both are called "allowances".
- A DA/HRA revision is a **new rate-table version**, not edits — this auto-creates
  the data needed for arrears (Section 08).
- Apply **consistent rounding**; document it once; reconcile-proof the totals.
- Handle **proration** for mid-month join/leave/LWP uniformly across components.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Current Assam DA%** and its revision history (dates + rates) — needed for
   current pay *and* legacy arrears.
2. **City classification** of this university's location(s) — X/Y/Z for HRA and
   the TA city category (Guwahati vs district towns).
3. **HRA rate set** Assam follows (24/16/8 or the DA-linked 27/18/9, and from
   which DA threshold).
4. **TA slabs** by Pay Level band and city category as adopted by Assam, plus the
   **double-TA** rule for differently-abled.
5. Whether HRA is **fully withdrawn** on quarter occupancy and the **licence-fee**
   recovery rate.
6. **Academic/special allowances** and amounts authorised by UGC + university
   Statutes (which are monthly vs claim-based).
7. Any **DA-on-TA** local variation or capping.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Gross Salary** | Basic + all earnings, before deductions. *Note:* the figure deductions and tax work off (Section 06, 15). |
| **Dearness Allowance (DA)** | `Basic × DA%`, inflation compensation. *Note:* revised ~twice yearly, often back-dated → main arrear source. |
| **DA%** | The current dearness rate. *Note:* effective-dated; a past month uses its own DA%, not today's. |
| **House Rent Allowance (HRA)** | `Basic × HRA%`, by **city class**. *Note:* 0 if govt quarter occupied; rate steps up with DA thresholds. |
| **City Classification (X/Y/Z)** | Population-based tiers fixing HRA% (24/16/8). *Note:* per-posting attribute; affects HRA and TA. |
| **Government Quarter / Licence Fee** | Official accommodation; HRA withdrawn, a licence fee recovered. *Note:* couples an earning (HRA off) with a deduction (Section 06). |
| **Transport Allowance (TA)** | Commuting allowance: **slab by Level+city, plus DA on TA**. *Note:* not a % of Basic; "DA on TA" is mandatory and often missed. |
| **DA on TA** | DA% also applied to the TA slab. *Note:* forgetting it underpays; include in TA formula. |
| **Academic / Special Allowance** | Role-based monthly allowances (UGC/university). *Note:* distinguish monthly ones from claim-based honoraria (Section 11). |
| **Base / Rate / Formula / Rounding / Effective date** | The five attributes every component needs. *Note:* the section's core checklist; all five must be defined. |
| **Rate Table (versioned)** | Effective-dated DA/HRA/TA values. *Note:* a revision = new version; enables arrears (Section 08). |
| **Proration** | Scaling pay by paid-days/days-in-month. *Note:* for mid-month join/leave/LWP; applied per component. |
| **Rounding rule** | Fixed per-component rounding (usually nearest ₹). *Note:* inconsistency breaks reconciliation (Section 14). |

---

### Status
Section 05 complete. Update roadmap tracker: 05 → ✅ Done.
Next: **Section 06 — Deductions**.
