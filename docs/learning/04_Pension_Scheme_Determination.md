# Section 04 — Pension Scheme Determination (NPS vs OPS/GPF)

> Learning roadmap §04. Source concept: `../Assam_Govt_University_Payroll_Concepts.md` §21.
> This is the **single most important branching rule in the system**. It decides
> which deductions run every month and which benefit an employee gets at exit.
> Phase 2 sits alone for a reason: everything in Phase 3 (deductions) forks here.

---

## 1. Purpose

Two government employees, identical Level and Basic, can have **completely
different monthly deductions and retirement outcomes** — purely because of *when
they joined*. One contributes to **GPF** and will get a lifelong **pension**; the
other contributes to **NPS** and will get a **market-linked corpus + annuity**.

The system must, for every employee, answer:

> "Is this person under the **Old Pension Scheme (OPS)** or the **National Pension
> System (NPS)**?"

That one boolean cascades into Section 06 (which deductions), Section 13/14
(which schedules), and Section 16 (which exit benefit). Decide it wrong → wrong
deduction every single month and a wrong settlement at retirement.

---

## 2. Governing Rules / Authority

- **NPS** was introduced by the Government of India for new entrants joining on or
  after **1 January 2004** (central). States adopted it from their **own
  notified dates** — Assam's cut-off is a **state notification date**, not the
  central one.
- **OPS** (pension + GPF) is governed by **Assam Services (Pension) Rules** and
  **GPF (Assam Services) Rules** (the CCS models from Section 01).
- **NPS** is regulated by **PFRDA** (Pension Fund Regulatory & Development
  Authority); accounts are maintained by **NSDL/CRA** under a **PRAN**.

> **Critical:** Do **not** hard-code 2004/2005. The branch date for *Assam state*
> employees is a **configurable parameter** set by the state's notification.
> Using the central date for a state university will mis-classify a band of
> employees. (Flagged in §8.)

> **Emerging (note, verify):** The **Unified Pension Scheme (UPS)** was notified
> for central employees (operational from **1 April 2025**) as an *option* for
> NPS-covered staff, offering an assured payout. Some states are evaluating
> adoption. Whether/when Assam adopts UPS for university staff is an open item —
> design the scheme field as an **enum that can grow** (OPS | NPS | UPS), not a
> hard binary.

---

## 3. Core Concepts

### 3.1 The branch

```text
                         Date of Joining (from §02)
                                  │
                 ┌────────────────┴─────────────────┐
        DOJ < Assam NPS cut-off            DOJ >= Assam NPS cut-off
                 │                                  │
              OPS path                           NPS path
        ┌────────┴────────┐               ┌────────┴────────┐
   Deductions: GPF, GIS              Deductions: NPS (Tier-I), GIS
   Exit: Pension + Gratuity          Exit: Corpus + Annuity
        + Commutation + DR                 (PFRDA rules)
```

### 3.2 OPS — Old Pension Scheme

- **GPF (General Provident Fund):** employee saves a chosen subscription;
  government pays **interest**; full balance withdrawable at retirement.
  **No employer contribution** to GPF.
- **Defined Benefit at exit:** guaranteed **pension** (a formula on last pay /
  qualifying service), **gratuity**, option to **commute** part of pension for a
  lump sum, and **Dearness Relief** on pension thereafter (Section 16, §32).
- Risk borne by **government** (it promises a defined payout).

### 3.3 NPS — National Pension System

- **Defined Contribution:** both sides pay in monthly; the money is **invested**;
  the final benefit depends on **market returns**.
  - **Employee: 10%** of (Basic + DA)
  - **Employer (Government): 14%** of (Basic + DA)
- **No GPF** for pure-NPS employees.
- At exit: a corpus; a portion must buy an **annuity** (the monthly pension),
  the rest can be withdrawn (per PFRDA rules) — Section 16.
- Risk borne by **employee** (payout not guaranteed).
- Identified by a **PRAN** (Permanent Retirement Account Number).

### 3.4 The employer-contribution insight

OPS costs the government **interest on GPF** + a future pension liability. NPS
costs the government **14% cash every month, now**. That 14% is:

1. a **budget/expenditure** line (accounting head, Section 13), and
2. a **schedule** line uploaded to NSDL/CRA (Section 13/14).

> **Example — the engine must compute employer share, not just deductions:** For
> an NPS employee with Basic ₹25,500 and DA 50% (₹12,750):
> - Employee NPS deduction = 10% × 38,250 = **₹3,825** (cut from salary)
> - Employer NPS contribution = 14% × 38,250 = **₹5,355** (NOT cut from salary —
>   it's a government cost paid *alongside*)
> A payroll system that only models deductions will **miss the ₹5,355** and
> under-report both cost and the NSDL upload. This is a classic gap.

### 3.5 What's common to both

**GIS (Group Insurance Scheme)** and **Income Tax/TDS** apply to *both* OPS and
NPS staff. The fork is specifically **GPF+pension (OPS)** vs **NPS contributions**.

---

## 4. Data Model

```text
Employee (from §02)
  ├─ date_of_joining
  ├─ pension_scheme   : OPS | NPS | UPS    (DERIVED at creation, then fixed)
  ├─ pran             : NPS account no.     (NPS/UPS only)
  └─ gpf_account_no   : GPF account no.     (OPS only)

PensionSchemeConfig (reference, state-specific)
  ├─ nps_cutoff_date              (Assam notification date — configurable!)
  ├─ nps_employee_pct  = 10
  ├─ nps_employer_pct  = 14
  └─ effective_from / to          (rates can change over time)
```

Design rules:
- `pension_scheme` is **derived once** from DOJ vs `nps_cutoff_date`, then treated
  as **fixed** (a scheme change is a policy event, not an edit).
- Exactly **one** of `pran` / `gpf_account_no` is populated, matching the scheme —
  validate this hard.
- Contribution percentages live in **config**, effective-dated (they have changed
  historically — e.g. central employer share rose from 10% to 14%).

---

## 5. Rules & Logic

### 5.1 Determine the scheme

```text
determine_scheme(employee):
    cfg = PensionSchemeConfig.current()
    if employee.date_of_joining < cfg.nps_cutoff_date:
        return OPS        # → GPF + GIS deductions; pension at exit
    else:
        return NPS        # → NPS Tier-I + GIS deductions; corpus at exit
    # UPS: only if employee opted AND state adopted — handle as explicit override
```

### 5.2 NPS contribution amounts (monthly)

```text
nps_base       = basic_pay + dearness_allowance
employee_nps   = round(nps_base × cfg.nps_employee_pct/100)   # deducted
employer_nps   = round(nps_base × cfg.nps_employer_pct/100)   # govt cost + schedule
# both reported; only employee_nps reduces net pay
```

### 5.3 OPS — GPF

```text
gpf_subscription = employee_chosen_amount   # within rule min/max of pay
# no employer match; interest credited annually (Section 06/14)
```

---

## 6. Worked Example (same pay, different scheme)

Two non-teaching Assistants, both **Level 4, Basic ₹25,500, DA 50% (₹12,750)**.
Assume Assam NPS cut-off = some notified date D.

**Person X — joined *before* D → OPS**
| Line | Amount |
|---|---|
| GPF subscription (chosen) | ₹6,000 (saved, returns to her with interest) |
| GIS | (group rate) |
| Employer cost | none to GPF |
| At retirement | **Pension** (formula) + Gratuity + Commutation + DR |

**Person Y — joined *on/after* D → NPS**
| Line | Amount |
|---|---|
| NPS employee 10% of 38,250 | ₹3,825 (to PRAN) |
| NPS employer 14% of 38,250 | ₹5,355 (govt pays alongside; not deducted) |
| GIS | (group rate) |
| At retirement | **Corpus + Annuity** (market-linked) |

Identical Basic and DA → **different deduction, different employer cost,
different retirement promise**. The only differentiator is the **joining date vs
the cut-off**. This is why Phase 2 is its own phase.

---

## 7. System Implications

- Compute `pension_scheme` **once at employee creation** from `DOJ` vs the
  **configurable cut-off**; never hard-code 2004/2005, never the central date for
  state staff.
- **Branch the deduction engine** (Section 06) on scheme: OPS → GPF; NPS → NPS
  Tier-I. GIS + IT apply to both.
- **Model the employer 14% as a first-class amount** — needed for budget/cost,
  accounting heads (Section 13), and the **NSDL/CRA upload** (Section 14). Do not
  treat NPS as "just a deduction".
- Keep contribution **percentages in effective-dated config** (they change).
- Make `pension_scheme` an **extensible enum (OPS | NPS | UPS)** so a future UPS
  adoption is a config/option event, not a schema change.
- Validate **PRAN ⇔ NPS** and **GPF No. ⇔ OPS** consistency at data entry.
- Carry the scheme into **exit processing** (Section 16): OPS → pension papers;
  NPS → CRA exit/withdrawal.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Exact Assam NPS cut-off date** for university/state employees — the linchpin
   parameter. Get the notification.
2. Whether Assam has **reverted to OPS** or offered an **OPS-option window** for a
   band of NPS staff (several states did 2022–2023) — could re-classify people.
3. **Assam's stance on UPS** (Unified Pension Scheme) and any option window.
4. **Employer contribution %** history (was it 10% before rising to 14%, and from
   when?) — affects past-month recompute/arrears.
5. **NPS legacy / missing-credit** handling for periods before regular CRA upload
   (some early NPS years have gaps).
6. GPF **interest rate** schedule (set quarterly by government) for OPS staff.
7. For **autonomous university** staff — do they map to state NPS/CRA, or a
   separate corporate NPS model? Confirm the CRA/PFMS routing.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **OPS (Old Pension Scheme)** | Defined-benefit: GPF while serving + guaranteed pension at exit. *Note:* applies to pre-cutoff joiners; government bears the risk. |
| **NPS (National Pension System)** | Defined-contribution: 10% employee + 14% employer invested; payout market-linked. *Note:* post-cutoff joiners; employee bears the risk. |
| **NPS Cut-off Date** | The joining-date boundary OPS↔NPS. *Note:* **state-specific & configurable** — not the central 2004 date. The linchpin of this section. |
| **GPF (General Provident Fund)** | OPS savings fund; employee subscribes, govt pays interest, no employer match. *Note:* OPS only; full balance returned at exit. |
| **PRAN** | Permanent Retirement Account Number — the NPS account ID. *Note:* one per NPS employee; used for every CRA upload. |
| **NSDL / CRA** | Central Recordkeeping Agency for NPS. *Note:* monthly contribution files uploaded here; confirmation needed (Section 14). |
| **PFRDA** | Regulator of NPS/UPS. *Note:* governs contribution, exit, annuity rules. |
| **Employee Contribution (NPS)** | 10% of (Basic + DA), deducted. *Note:* reduces net pay. |
| **Employer Contribution (NPS)** | 14% of (Basic + DA), govt-paid alongside. *Note:* **not** a deduction — a cost + schedule line; commonly missed. |
| **Defined Benefit vs Defined Contribution** | Guaranteed payout (OPS) vs invested-pot payout (NPS). *Note:* the conceptual heart of the fork. |
| **Annuity** | The pension bought from NPS corpus at exit. *Note:* mandatory minimum portion; rest may be withdrawn (Section 16). |
| **Commutation** | Trading part of an OPS pension for a lump sum. *Note:* OPS-only; restored after a period (Section 16). |
| **Dearness Relief (DR)** | DA-equivalent on OPS pension. *Note:* OPS pensioners only (Section 16, §32). |
| **UPS (Unified Pension Scheme)** | Newer assured-payout option over NPS (central from Apr-2025). *Note:* state adoption uncertain — keep scheme enum extensible. |
| **GIS** | Group Insurance — applies to **both** OPS and NPS. *Note:* not part of the fork; common to all. |

---

### Status
Section 04 complete. Update roadmap tracker: 04 → ✅ Done.
Next: **Section 05 — Earnings & Monthly Allowances**.
