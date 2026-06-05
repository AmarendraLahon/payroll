# Section 01 — Foundations & Governance

> Learning roadmap §01. Source concept: `../Assam_Govt_University_Payroll_Concepts.md` (Overview).
> This is the bedrock section: it explains *who sets the rules* that every later
> section (pay, allowances, leave, pension) merely applies.

---

## 1. Purpose

Before computing a single rupee of salary, you must know **which rulebook
applies to which employee**. An Assam Government University does not invent its
own pay or leave rules — it inherits them from a stack of external authorities:
the Pay Commission, the UGC, state service rules, and central tax law.

Getting this wrong at the foundation corrupts everything downstream. Example: if
you apply state-government pay rules to a Professor who is actually governed by
**UGC** scales, the Basic Pay, increment dates, and promotion path will all be
wrong. So the first job of the payroll system is to **classify each employee
under the correct rule-set** and pull the right rulebook.

---

## 2. Governing Rules / Authority

Think of governance as a layered stack. Each layer owns a slice of payroll.

```text
                 ┌─────────────────────────────────────────┐
 Central law     │ Income Tax Act 1961 (TDS, Form 16)       │  → applies to EVERYONE
                 ├─────────────────────────────────────────┤
 Pay framework   │ 7th Pay Commission (structure & matrix)  │
                 ├──────────────────────┬──────────────────┤
 Adopted by      │ State: Assam ROP     │ Teaching: UGC     │
 employee type   │ Rules 2017           │ Regulations 2018  │
                 │ (non-teaching)       │ (teaching/CAS)    │
                 ├──────────────────────┴──────────────────┤
 Service rules   │ Assam Services: Leave / Pension / GPF /  │
                 │ Conduct / Fundamental Rules              │
                 ├─────────────────────────────────────────┤
 Money handling  │ Assam Treasury Rules / Financial Rules   │
                 ├─────────────────────────────────────────┤
 University law  │ State University Act + Statutes/Ordinances│
                 └─────────────────────────────────────────┘
```

### 2.1 The Pay Commission (7th CPC)

The **Central Pay Commission** is constituted roughly every 10 years to revise
central government pay. The **7th CPC** introduced the **Pay Matrix** (replacing
the old "pay band + grade pay" system), effective **1 January 2016** for central
employees.

States are not automatically bound by it. Each state issues its own
notification adopting (often with modifications) the CPC structure.

> **Example — adoption lag:** Central employees got 7th CPC pay from Jan 2016.
> Assam adopted it via its own **Revision of Pay (ROP) Rules, 2017**, with
> monetary benefit from a later date. So a central clerk and an Assam university
> clerk on "Level 2" may have started the new pay on different dates — and that
> date difference is exactly what drives **arrear** calculations (Section 08).

### 2.2 UGC — for teaching staff

Teachers in universities are **not** paid under state pay rules. They follow
**UGC pay scales** adopted into the **7th CPC for teachers** via the
**UGC Regulations, 2018**. These define:

- **Academic Pay Levels** (Academic Level 10 to 15A) — a parallel matrix to the
  non-teaching one.
- **Career Advancement Scheme (CAS)** — the teacher promotion ladder
  (Assistant → Associate → Professor) based on years of service + API/academic
  criteria, *not* the MACP used for non-teaching staff.

> **Example — two "Level 10s" are different:** A non-teaching *Assistant* may sit
> at Pay Matrix Level 10; an *Assistant Professor* enters at **Academic Level
> 10**. Same label "10", **different matrix, different cell values, different
> increment rules**. The system must keep two separate matrices keyed by staff
> type. (Detail in Section 03.)

### 2.3 State service rules (the "how" of service life)

The day-to-day mechanics — how much leave, how pay is fixed, what's deducted —
come from **Assam Services rules**, which mirror the central CCS rules:

| Domain | Central rule (model) | Assam equivalent |
|---|---|---|
| Leave | CCS (Leave) Rules, 1972 | Assam Services (Leave) Rules / FR-SR |
| Pension (old) | CCS (Pension) Rules | Assam Services (Pension) Rules |
| Provident Fund | GPF (CS) Rules | GPF (Assam Services) Rules |
| Pay fixation, joining time, foreign service | Fundamental Rules (FR) & Subsidiary Rules (SR) | Assam Fundamental Rules |
| Conduct & discipline | CCS (CCA) Rules | Assam Services (Discipline & Appeal) Rules |

### 2.4 Treasury & financial rules

How a sanctioned salary actually leaves the government account is governed by
**Assam Treasury Rules** and **Assam Financial Rules** — DDO duties, bill forms,
treasury passing, voucher numbers (Section 13).

### 2.5 Central tax law

**Income Tax Act, 1961** sits above everything and applies uniformly: TDS on
salary, Form 16, Form 24Q (Section 06, Section 15). The state cannot alter it.

### 2.6 University's own law

Each state university is created by a **State Act** (e.g. an Act of the Assam
Legislative Assembly). Under it, the university makes **Statutes, Ordinances and
Regulations** that can set *university-specific* allowances or honoraria (e.g.
examination remuneration rates), provided they don't conflict with state rules.
Authorities: **Vice-Chancellor, Registrar, Finance Officer, Executive
Council/Syndicate**.

---

## 3. Core Concepts

### 3.1 Teaching vs Non-teaching — the primary fork

This single classification decides which entire rulebook applies.

| Aspect | Teaching | Non-teaching |
|---|---|---|
| Pay authority | UGC Regulations 2018 | Assam ROP Rules 2017 (7th CPC) |
| Pay grid | Academic Pay Levels (10–15A) | Pay Matrix Levels (1–18) |
| Promotion | CAS | Promotion / MACP |
| Leave | Often vacation-department rules (EL differs) | Full EL accrual |

> **Example — leave differs by type:** Teachers are typically **"vacation
> department"** staff: because they get summer/winter vacation, their **Earned
> Leave entitlement is lower** than non-teaching staff who earn full EL. Same
> employer, different leave rule — driven purely by the teaching/non-teaching
> fork. (Section 09.)

### 3.2 Funding source

A **state** university's salaries are paid largely from **State Government
grants** routed through the treasury; a **central** university draws from UGC/MoE
grants. This affects which treasury/PFMS channel issues payment — but the *pay
rules* are the same. For Assam Government Universities, assume **state grant +
state treasury**.

### 3.3 Effective dates everywhere

Because rules are adopted by notification on specific dates, **every rule carries
an effective date**. The system must always ask "which rule was in force *in the
month being processed*?" — not "which rule is in force today?"

> **Example:** Processing a June 2017 salary in 2026 must use the DA% and pay
> rules effective in June 2017, not today's. This is why master data is
> versioned (Section 17) and arrears exist (Section 08).

---

## 4. Data Model (foundational)

At the foundation level the system needs to *store the rule classification* per
employee, so later modules can branch correctly.

```text
Employee
  ├─ staff_type         : TEACHING | NON_TEACHING | CONTRACTUAL | DAILY_WAGE
  ├─ pay_authority      : UGC_2018 | ASSAM_ROP_2017 | CONTRACT_TERMS
  ├─ is_vacation_dept   : boolean         (drives leave rules)
  ├─ pension_scheme     : OPS | NPS       (derived, Section 04)
  └─ university_unit     : college / department (org hierarchy)

RuleSet (reference)
  ├─ code               : e.g. ASSAM_LEAVE_RULES, UGC_2018, ITA_1961
  ├─ domain             : PAY | LEAVE | PENSION | GPF | TAX | TREASURY
  ├─ effective_from
  └─ effective_to        (nullable = current)
```

The key foundational field is **`staff_type` → `pay_authority`**. Everything
else (matrix, leave accrual, promotion engine) reads off it.

---

## 5. Rules & Logic

The foundational rule is a **classification + routing** rule, not a formula:

```text
determine_rulebook(employee):
    if employee.staff_type == TEACHING:
        pay_rules    = UGC_Regulations_2018      # Academic Pay Levels, CAS
        leave_rules  = Assam_Leave_Rules(vacation_dept = true)
    elif employee.staff_type == NON_TEACHING:
        pay_rules    = Assam_ROP_Rules_2017       # Pay Matrix, MACP
        leave_rules  = Assam_Leave_Rules(vacation_dept = false)
    elif employee.staff_type == CONTRACTUAL:
        pay_rules    = contract_terms              # consolidated pay, limited rules
        leave_rules  = contract_terms
    # tax, treasury, GPF/NPS rules then layer on top for all regular staff
```

Edge note: **contractual / daily-wage** staff often get **consolidated pay** (a
fixed lump sum) with *no* DA/HRA/increment/pension — so most of the salary engine
simply does not apply to them. The foundation must flag this so downstream
modules skip the inapplicable logic.

---

## 6. Worked Example (end-to-end classification)

Two new joiners on the same day at an Assam Government University:

**Person A — Dr. Sharma, Assistant Professor**
- `staff_type = TEACHING` → `pay_authority = UGC_2018`
- Placed at **Academic Level 10** (UGC matrix), entry cell.
- Leave: vacation-department → reduced EL.
- Promotion path: **CAS** (to Associate Professor after qualifying service + criteria).
- Pension: joined after NPS cut-off → **NPS** (Section 04).

**Person B — Mr. Das, Junior Assistant (non-teaching)**
- `staff_type = NON_TEACHING` → `pay_authority = ASSAM_ROP_2017`
- Placed at **Pay Matrix Level 2** (non-teaching matrix), entry cell.
- Leave: full EL accrual.
- Promotion path: departmental promotion + **MACP** at 10/20/30 years.
- Pension: joined after cut-off → **NPS**.

Same employer, same joining date — yet **different pay grid, different increment
rules, different leave, different promotion engine**. All of it flows from the
one foundational classification. This is why Section 01 comes first.

---

## 7. System Implications

- **`staff_type` is mandatory** at employee creation and effectively immutable
  (a change implies re-appointment, not an edit). Validate it hard.
- Maintain **two pay grids** from day one (UGC Academic Levels + state Pay
  Matrix). Do not collapse them into one table.
- Store **rule-sets as versioned reference data** with effective dates; never
  hard-code a rate or a cut-off in code (Section 17).
- Build the **"rule in force on date D"** lookup as a shared service — pay,
  leave, arrears, and pension all need it.
- Flag **contractual/daily-wage** employees so the engine **skips** DA/HRA/
  increment/pension automatically.
- Keep a **rule-source citation** on each computed component (which notification
  authorised this DA%) — invaluable for audit and treasury queries.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Exact Assam ROP Rules 2017 effective date** and whether monetary benefit
   differs from notional fixation date (affects arrears).
2. **Assam's NPS cut-off date** for OPS vs NPS (Section 04 depends on it).
3. Whether the university follows **UGC Regulations 2018** as adopted by Assam
   *as-is* or with state modifications (some states delay/modify CAS).
4. **Vacation-department EL entitlement** figure for teachers in Assam.
5. Any **university-specific allowances/honoraria** set by its own Statutes.
6. Funding/payment channel: **state treasury vs PFMS vs direct bank** for this
   university.
7. Whether **work-charged / muster-roll** categories exist beyond the four in
   the concept doc.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Pay Commission (CPC)** | Central body revising govt pay ~every 10 yrs. 7th CPC = current framework. *Note:* states adopt separately, so dates lag — this lag creates arrears. |
| **7th CPC / Pay Matrix** | The current pay structure: a grid of Levels × cells replacing old pay-band+grade-pay. *Note:* "Level" alone is ambiguous until you know teaching vs non-teaching. |
| **Assam ROP Rules 2017** | Assam's notification adopting 7th CPC for **state (non-teaching)** staff. *Note:* governs non-teaching pay; confirm exact effective date. |
| **UGC Regulations 2018** | Rulebook for **teaching** staff pay & promotion (7th CPC for teachers). *Note:* defines Academic Pay Levels + CAS; entirely separate from state matrix. |
| **Academic Pay Level** | Teacher pay grid (Level 10–15A). *Note:* numerically overlaps non-teaching levels but values/rules differ — keep two matrices. |
| **CAS (Career Advancement Scheme)** | Teacher promotion ladder by service + academic criteria. *Note:* teaching analogue of MACP; do **not** mix the two. |
| **MACP** | Financial upgradation for non-teaching staff at 10/20/30 yrs. *Note:* applies to non-teaching only (Section 07). |
| **Vacation Department** | Staff (teachers) entitled to vacation, hence **reduced EL**. *Note:* a leave-rule flag, set by staff type. |
| **Fundamental Rules (FR/SR)** | Core service rules: pay fixation, joining time, etc. *Note:* Assam has its own adapted FR. |
| **CCS Rules** | Central Civil Services rules (Leave/Pension/Conduct) — the **model** Assam rules follow. *Note:* useful reference when Assam text is silent. |
| **GPF Rules** | Govern the General Provident Fund (old-scheme staff). *Note:* applies only to OPS employees (Section 04, 06). |
| **OPS / NPS** | Old Pension Scheme vs National Pension System. *Note:* chosen by joining date vs cut-off — the core branch (Section 04). |
| **Income Tax Act 1961** | Central tax law; TDS/Form 16. *Note:* applies to all; state cannot modify. |
| **Treasury / Financial Rules** | Govern how bills are passed and paid. *Note:* Assam Treasury Rules; drives Section 13. |
| **University Act / Statutes / Ordinances** | The university's own legal framework. *Note:* may add local allowances/honoraria within state-rule limits. |
| **DDO** | Drawing & Disbursing Officer — draws salary bills from treasury. *Note:* central to bill flow (Section 13). |
| **Effective Date** | The date a rule/rate starts applying. *Note:* every rate is versioned by it; always compute "rule in force in the processed month". |
| **Consolidated Pay** | Fixed lump-sum pay for contractual/daily-wage staff. *Note:* no DA/HRA/increment/pension — engine skips those. |

---

### Status
Section 01 complete. Update roadmap tracker: 01 → ✅ Done.
Next: **Section 02 — Employee Master & Service Book**.
