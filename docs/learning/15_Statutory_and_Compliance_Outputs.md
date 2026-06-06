# Section 15 — Statutory & Compliance Outputs

> Learning roadmap §15. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §28 (Statutory & Compliance Outputs), with the **monthly TDS projection** logic.
> Sections 05–14 computed and disbursed pay. This section is about the
> institution's **legal obligations to outside authorities** arising from that
> pay: deducting the right **income tax** each month, filing **returns**, and
> issuing the **certificates/statements** every employee and agency is entitled to.

---

## 1. Purpose

Paying an employee creates **statutory duties to third parties** — chiefly the
**Income Tax Department** (TDS), plus the GPF/NPS/GIS/PT authorities. The system is
a **withholding and reporting agent**: it must estimate each employee's **annual
tax**, deduct it in **monthly slices**, file the **quarterly/annual returns**, and
hand every employee the **proof documents** they need.

The questions this section answers:

> "How much **income tax** must come off *this* employee *this* month so that, by
> March, the full year's liability is collected smoothly? What **returns** must be
> filed and when, and what **certificates/statements** (Form 16, GPF, NPS) must
> each employee receive?"

The hard part isn't the forms — it's the **TDS projection**: tax is annual but
deducted monthly, under a **regime the employee chooses**, adjusted as
**declarations and pay change** mid-year.

---

## 2. Governing Rules / Authority

- **Income Tax Act / Rules** — TDS on salary under **Section 192**; annual
  **Form 16**, quarterly **Form 24Q** (via TRACES), employee **Form 12BB**
  declaration. **Section 89(1) / Form 10E** relief for arrears (links §08).
- **Old vs New Tax Regime** — the employee **chooses**; slabs and which
  exemptions/Chapter-VI-A deductions apply differ. Default regime applies if no
  declaration.
- **GPF / NPS / GIS** statements — under their respective fund rules.
- **Professional Tax** — **state** statutory deduction with its own **return**
  (Assam PT slabs, §06).
- **Pension / Gratuity papers** — issued on retirement (Section 16).

---

## 3. Core Concepts

### 3.1 The TDS projection — annual tax, monthly slices

The central engine of this section:

```text
1. Project ANNUAL gross  = pay-to-date + (expected pay × remaining months)
2. Subtract exemptions   = HRA exemption, std deduction, §10 allowances (regime-dependent)
3. Subtract Ch.VI-A      = 80C/80D/NPS 80CCD etc. from Form 12BB (regime-dependent)
4. Compute annual tax    = slabs(chosen regime) + cess
5. Subtract TDS already deducted this FY
6. Monthly TDS           = remaining tax / remaining months in FY
7. RECOMPUTE whenever 12BB or pay changes (re-spreads the balance)
```

> **Key insight:** TDS is **not** a flat % of monthly salary. It's an **estimate
> of the whole year divided by the months left**, **re-projected** every time a
> declaration or pay event changes the estimate. Early-year months may deduct
> little (declarations pending); later months catch up.

### 3.2 Regime choice changes everything

```text
Old regime: lower-ish slabs BUT exemptions (HRA, LTC) + Ch.VI-A (80C/80D/…) allowed
New regime: wider/lower slabs BUT most exemptions/deductions DISALLOWED
```

The employee's **declared regime** decides which exemptions step 2–3 apply. The
system must compute under the **chosen** regime (and ideally **advise** which is
better). Default-regime rules apply absent a declaration.

### 3.3 Form 12BB drives the projection (§28)

**Form 12BB** is the employee's **investment/exemption declaration** (rent paid,
80C investments, home-loan interest, etc.). It **feeds** the projection — until
filed, the system projects on **defaults** (often higher TDS); when filed/updated,
the projection **recomputes** and re-spreads the remaining tax.

### 3.4 The compliance outputs (§28)

| Output | What | When | Source |
|---|---|---|---|
| **Form 16** | Annual TDS certificate to employee (Part A+B) | Year-end | Salary + TDS records |
| **Form 24Q** | Quarterly TDS return (TRACES) | Quarterly | Per-employee TDS, deductee details |
| **Form 12BB** | Employee declaration (input, not output) | Start/anytime | Employee (ESS §19) |
| **GPF Annual Statement** | Year-end GPF balance + interest | Annual | GPF ledger (§14) |
| **NPS Transaction Statement** | PRAN-wise contribution record | Periodic | NPS schedule (§13) |
| **Professional Tax Return** | State PT filing | Per state rule | PT deductions (§06) |
| **Pension / Gratuity papers** | On retirement | At exit | Section 16 |

### 3.5 Arrears and §89(1) relief (links §08)

Arrears are taxed **in the year received**, possibly bumping a slab. **Section
89(1)** lets the employee **notionally spread** the arrear back to its original
years to reduce tax; the system must produce the **year-wise arrear breakup** for
**Form 10E** (the §08 hand-off realised here).

### 3.6 Perquisites and employer contributions

Some items are **taxable perquisites** (e.g. rent-free quarter value, concessional
loan interest below a threshold). And **employer NPS** within limits is deductible
under **80CCD(2)** — so the projection must read both **earnings** and **certain
employer contributions**, not just the payslip net.

---

## 4. Data Model

```text
TaxProfile (per employee per FY)
  ├─ regime : OLD | NEW                     (declared; default if none)
  ├─ form12bb : {hra_rent, 80C[], 80D, home_loan_interest, 80CCD1B, …}
  ├─ projected_annual_gross, exemptions, chvia_deductions
  ├─ projected_annual_tax, tds_deducted_to_date
  └─ recompute_log[]                        (each re-projection event)

MonthlyTDS (per employee per month)
  ├─ month, taxable_this_month, tds_deducted
  └─ basis_snapshot (projection inputs used)

Form16 (per employee per FY)
  ├─ part_a : tds_summary (from 24Q/TRACES)
  └─ part_b : salary breakup, exemptions, deductions, tax

Form24Q (per quarter)
  └─ deductee_rows[] : pan, taxable, tds, section

StatutoryStatement (GPF/NPS/PT)
  ├─ type, period, per-employee figures
  └─ source_ref (ledger/schedule §13/§14)

Form10E (per employee, when arrears paid)
  └─ year_wise_arrear[]                     (from §08 ArrearRun)
```

Design rules:
- The **TaxProfile is re-projected** on every relevant change (12BB, pay event,
  arrear); each projection is **logged** (auditable, explains a TDS jump).
- **Compute under the declared regime**; never hard-code one.
- Outputs are **derived from pay/TDS records** (§13/§14) — Form 16/24Q must
  **tie out** to what was actually deducted and deposited.
- **PAN is mandatory** for every deductee (else higher TDS / return rejection).
- **Arrear year-wise breakup** comes straight from the §08 ArrearRun → Form 10E.

---

## 5. Rules & Logic

### 5.1 Monthly TDS projection

```text
project_tds(employee, month):
    annual_gross = paid_to_date + expected_monthly × months_remaining
    taxable      = annual_gross − exemptions(regime) − chvia(regime, form12bb)
    annual_tax   = slab_tax(taxable, regime) + cess
    balance_tax  = annual_tax − tds_to_date
    monthly_tds  = max(0, balance_tax / months_remaining)
    log projection
    return monthly_tds
```

### 5.2 Recompute triggers

```text
on form12bb_update | pay_change | arrear_paid | regime_change:
    re-run project_tds → re-spread remaining balance over remaining months
```

### 5.3 Year-end outputs

```text
at FY close:
    Form 24Q (Q4) → TRACES → Form 16 Part A (TDS) + Part B (computation)
    GPF annual statement, NPS transaction statement, PT return
if arrears paid: Form 10E year-wise breakup (§08)
```

---

## 6. Worked Example (TDS projection, mid-year change)

**Dr. Sharma**, monthly taxable salary ≈ **₹1,10,000**, **old regime**.

**April projection (no 12BB yet → defaults):**
```text
Annual gross    ≈ 1,10,000 × 12        = 13,20,000
− std deduction                          −50,000
Taxable (no other exemptions yet)      ≈ 12,70,000
Annual tax (old slabs + cess)          ≈ (illustrative) 1,90,000
Monthly TDS = 1,90,000 / 12            ≈ 15,833/month
```

**July — files Form 12BB:** 80C ₹1,50,000 + 80D ₹25,000 + home-loan interest
₹2,00,000.
```text
Taxable = 12,70,000 − 1,50,000 − 25,000 − 2,00,000 = 8,95,000
Annual tax (old)                       ≈ 92,000
TDS already deducted Apr–Jun (3×15,833)≈ 47,500
Balance = 92,000 − 47,500              = 44,500
Remaining months (Jul–Mar) = 9
Monthly TDS Jul onward = 44,500 / 9    ≈ 4,944/month
```

```text
TDS DROPS from ₹15,833 → ₹4,944 once declarations land — exactly the re-spread.
Each projection is LOGGED so the employee can see why the deduction changed.
At year-end: Form 24Q → Form 16; if any salary arrear was paid, Form 10E too.
```

> Switch Dr. Sharma to the **new regime** and steps change: the ₹3,75,000 of
> 80C/80D/home-loan **disallowed**, taxable stays ~₹12,70,000+, but **new slabs**
> apply — the system computes **both** to advise which regime costs less.

---

## 7. System Implications

- Build a **TDS projection engine**: annual estimate ÷ remaining months,
  **recomputed** on every 12BB/pay/arrear/regime change, with **each projection
  logged** (explains TDS swings to employees and audit).
- Support **both tax regimes**; compute under the **declared** one and ideally
  **advise** the cheaper.
- Treat **Form 12BB as a first-class input** (via ESS §19), defaulting
  conservatively until filed.
- Generate **Form 24Q** (quarterly, TRACES-ready, PAN-mandatory) and **Form 16**
  (Part A from TDS deposits, Part B computation) that **tie out** to actual
  deductions (§13/§14).
- Produce **GPF annual**, **NPS transaction**, and **PT** statements/returns from
  the respective ledgers/schedules.
- Realise the **§08 hand-off**: **Form 10E year-wise arrear breakup** for §89(1)
  relief.
- Handle **taxable perquisites** (rent-free quarter, concessional loan) and
  **80CCD(2) employer NPS** — read earnings **and** relevant employer
  contributions, not just net.
- Enforce **PAN presence** and reconcile **deposited vs deducted** TDS (challan
  matching) before issuing certificates.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Regime default** policy and the declaration/locking window the university
   follows.
2. Exact **exemptions/perquisites** in play (rent-free university quarter
   valuation, transport, CEA/LTC exemption limits from §11).
3. **TRACES/24Q** filing mechanism — in-house vs outsourced; RPU/FVU format.
4. **Form 16** generation — Part A from TRACES download vs system-built.
5. **GPF interest rate** and statement format/owner (university vs AG).
6. **Professional Tax** Assam slabs, exemption threshold, and **return** format/
   cadence.
7. **Form 10E / §89(1)** — does the system compute relief or just supply data?
8. **Challan / deposit reconciliation** workflow (monthly TDS deposit, BIN/CIN
   matching).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **TDS (Section 192)** | Tax deducted at source on salary. *Note:* annual liability collected in monthly slices. |
| **TDS Projection** | Estimating annual tax ÷ remaining months. *Note:* recomputed on every 12BB/pay/arrear change. |
| **Tax Regime (Old/New)** | The slab+exemption scheme the employee picks. *Note:* decides which exemptions/deductions apply. |
| **Form 12BB** | Employee investment/exemption declaration. *Note:* input that drives the projection; defaults until filed. |
| **Form 16** | Annual TDS certificate (Part A + B). *Note:* must tie out to deducted+deposited TDS. |
| **Form 24Q** | Quarterly salary-TDS return (TRACES). *Note:* PAN-mandatory deductee rows. |
| **Chapter VI-A** | 80C/80D/80CCD etc. deductions. *Note:* allowed in old regime, mostly disallowed in new. |
| **Standard Deduction** | Flat salary deduction. *Note:* part of step-2 exemptions. |
| **80CCD(2)** | Deduction for employer NPS share. *Note:* projection reads employer contribution, not just net. |
| **Section 89(1) / Form 10E** | Relief spreading arrear tax to original years. *Note:* needs §08 year-wise breakup. |
| **Perquisite** | Taxable non-cash benefit (rent-free quarter, cheap loan). *Note:* added to taxable income. |
| **GPF Annual Statement** | Year-end GPF balance + interest. *Note:* from GPF ledger (§14). |
| **NPS Transaction Statement** | PRAN-wise contribution record. *Note:* from NPS schedule (§13). |
| **Professional Tax Return** | State PT statutory filing. *Note:* from §06 PT deductions; Assam slabs. |
| **PAN** | Permanent Account Number. *Note:* mandatory per deductee; absence → higher TDS / return reject. |
| **Challan Reconciliation** | Matching deposited TDS to deducted. *Note:* gate before issuing Form 16. |

---

### Status
Section 15 complete. Update roadmap tracker: 15 → ✅ Done.
Next: **Section 16 — Pension, Gratuity, DR & Retirement Settlement** (closes Phase 6).
