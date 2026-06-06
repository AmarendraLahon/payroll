# Section 16 — Pension, Gratuity, DR & Retirement Settlement

> Learning roadmap §16. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §17 (Pension), §29 (Pension, Gratuity & Retirement Settlement — OPS), §32 (Pensioner DR).
> This is the **terminal payoff** of the whole system. Every discipline insisted on
> earlier — the **scheme fork** (§04), **qualifying service** with EOL/dies-non
> echoes (§02/§07/§10), the **EL balance** (§09), **outstanding loans** (§12), and
> **last-drawn pay** (§05) — all converge here, at the moment an employee exits.

---

## 1. Purpose

When an employee **retires, dies in service, or otherwise exits**, the system must
compute and disburse their **terminal benefits**. The path depends entirely on the
**pension scheme** decided back in §04:

- **OPS** → a **defined-benefit monthly pension** for life + **gratuity** +
  **commutation** + **leave encashment** + **GPF final payment**, with **family
  pension** on death.
- **NPS** → a **corpus settlement**: accumulated contributions, part lump-sum +
  mandatory **annuity** per PFRDA rules.

And after retirement, OPS pensioners keep receiving **Dearness Relief (DR)** — the
pension-side twin of DA — for life.

The questions this section answers:

> "On this employee's exit, which scheme governs, how much **qualifying service**
> counts, what is the **pension / gratuity / encashment / commutation** (OPS) or
> **corpus + annuity** (NPS), what **outstanding dues** net off, and how is the
> ongoing **pension + DR** maintained thereafter?"

---

## 2. Governing Rules / Authority

- **OPS** — state pension rules (CCS-Pension-style, as adopted by Assam): pension,
  **DCRG/gratuity**, **commutation**, **family pension** formulas.
- **Qualifying Service** — service that counts toward pension; **excludes
  un-condoned dies-non/EOL** (the §02/§07/§10 echo).
- **NPS** — **PFRDA/NSDL** exit rules: lump-sum % + mandatory annuity above a
  corpus threshold.
- **Leave Encashment** — EL balance (capped, commonly **300**) × (Basic+DA)/30 at
  exit (links §09).
- **Dearness Relief (DR)** — pensioner DA-equivalent, revised on the **same
  cadence as DA** (§05), on **basic pension**.
- **Commutation factor** — age-based table fixing the lump-sum for commuted
  pension.

---

## 3. Core Concepts

### 3.1 The exit fork (the §04 decision, finally cashed out)

```text
exit(employee):
    if scheme == OPS  → defined-benefit path (pension + gratuity + commute + encash + GPF)
    if scheme == NPS  → corpus path (accumulated units → lump-sum % + annuity)
    common to both    → leave encashment, dues recovery, GIS payout, final settlement
```

The single field decided at joining (§04) routes the **entire** terminal
computation. Both paths still share **leave encashment**, **loan/dues recovery
(§12)**, and **GIS** payout.

### 3.2 Qualifying Service — where EOL finally bites

```text
qualifying_service = total_service − un-condoned (dies-non + EOL) periods
```

The **EOL spell** threaded through §02 → §07 → §10 lands here: it **reduced
qualifying service**, which **directly reduces the pension**. This is the payoff
of tracking it as an immutable event all along.

> **The throughline realised:** Mr. Das's 30-day EOL in 2021 (§07) shifted his
> increment *then*; here it shaves ~1 month off qualifying service, marginally
> lowering pension. One event, consumed by three sections across a career.

### 3.3 OPS benefit formulas (§29)

| Benefit | Formula (illustrative, confirm Assam) | Note |
|---|---|---|
| **Pension** | ½ × (last-drawn **or** 10-month-avg emoluments) × (QS / max-QS) | Monthly, for life |
| **Commutation** | commuted-fraction × pension × **commutation factor**(age) | Lump sum; pension reduced by the commuted part, restored after ~15 yrs |
| **Gratuity (DCRG)** | per-rule (service & emoluments based), **statutory ceiling** | One-time lump sum |
| **Family Pension** | enhanced rate then normal rate | On death (service or after) |
| **Leave Encashment** | EL-balance(≤300) × (Basic+DA)/30 | Common to OPS & NPS |

### 3.4 Commutation — trading pension for a lump sum

A pensioner may **commute** a fraction of pension (e.g. up to 40%) into a **lump
sum** = commuted pension × **commutation factor** (from an age table) × 12. The
**monthly pension reduces** by the commuted portion, and is **restored** after a
fixed period (commonly ~15 years). The system tracks the **commuted amount,
reduction, and restoration date**.

### 3.5 NPS exit (§29)

```text
NPS_corpus = Σ (employee 10% + employer 14% + returns)   ← from PRAN/CRA, not an internal formula
exit: withdraw up to allowed % as lump-sum + buy mandatory ANNUITY for the rest
      (below a small corpus threshold → full lump-sum allowed)
```

Crucially, the **corpus lives with NSDL/CRA**, not in the payroll DB — the system
**initiates the exit/withdrawal request** and reconciles, rather than *computing*
a defined benefit. This is the structural opposite of OPS.

### 3.6 Pensioner Dearness Relief (DR) (§32)

```text
DR Amount = Basic Pension × DR%
```

After retirement (OPS), the pensioner is paid **basic pension + DR**, with **DR
revised on the same cycle as serving-staff DA** (§05). The **rate table is shared
cadence** with DA — so the master-data engine (§17) serves both. Pension is itself
a small ongoing "payroll" run for retirees.

### 3.7 Dues recovery at exit (links §12)

Outstanding **loans/advances (§12)**, **overpayments (§06)**, and **GPF advances**
are **netted from terminal benefits** (typically gratuity) before payout. On
**death-in-service**, some dues may be **waived** per rule (§18).

### 3.8 GPF final payment (OPS)

The **GPF balance + interest** (the OPS savings leg, §04) is **paid out in full**
at retirement — separate from pension, sourced from the GPF ledger (§14).

---

## 4. Data Model

```text
RetirementCase (per exit)
  ├─ employee_code, exit_type : SUPERANNUATION | VRS | DEATH | INVALIDATION
  ├─ exit_date, scheme : OPS | NPS
  ├─ qualifying_service (derived: total − un-condoned EOL/dies-non)
  ├─ last_emoluments / ten_month_avg
  └─ status : INITIATED | VERIFIED | SANCTIONED | SETTLED

OPSSettlement (if scheme==OPS)
  ├─ basic_pension
  ├─ commutation : {fraction, factor, lump_sum, reduced_pension, restore_date}
  ├─ gratuity (DCRG, capped), family_pension_rates
  ├─ leave_encashment, gpf_final
  └─ dues_recovered (loans §12, overpay §06)

NPSExit (if scheme==NPS)
  ├─ corpus (from CRA), lump_sum_%, annuity_amount
  ├─ annuity_provider, withdrawal_request_ref
  └─ leave_encashment, dues_recovered

PensionerAccount (post-retirement, OPS)
  ├─ pensioner_id, basic_pension, commuted_reduction, restore_date
  ├─ dr_rate (shared cadence with DA §05/§17)
  └─ monthly_pension = (basic − commuted_reduction) + basic×DR%

FamilyPensionCase (on death)
  ├─ beneficiary, enhanced_rate_until, normal_rate
  └─ dependency/eligibility flags
```

Design rules:
- **Scheme field routes everything** (OPS vs NPS) — the §04 decision is the
  top-level switch here too.
- **Qualifying service is derived** from the immutable service ledger (§02) minus
  un-condoned EOL/dies-non — never typed.
- **NPS corpus is read from CRA**, not computed; the system **initiates exit** and
  reconciles.
- **Dues (§12/§06) net off** terminal benefits; **death** may trigger **waiver**
  (§18).
- **PensionerAccount is an ongoing payroll** — DR shares the DA rate table (§17).
- **Formulas/factors are config** (commutation table, gratuity ceiling, family-
  pension rates) — they vary by era/state.

---

## 5. Rules & Logic

### 5.1 OPS settlement

```text
settle_OPS(employee, exit_date):
    QS       = qualifying_service(employee)                 # §02 ledger − EOL
    emol     = max-benefit of (last_drawn, 10_month_avg)
    pension  = 0.5 × emol × (QS / max_QS)
    if opts_commutation:
        lump = commuted_fraction × pension × factor(age) × 12
        reduced_pension = pension − commuted_fraction × pension   # restored later
    gratuity = min(rule_gratuity(QS, emol), ceiling)
    encash   = min(EL_balance, 300) × (basic+DA)/30
    gpf_final= GPF_ledger_balance(employee)
    net_payout = gratuity + lump + encash + gpf_final − dues(§12,§06)
    open PensionerAccount(basic_pension=pension, reduced_pension, restore_date)
```

### 5.2 NPS exit

```text
exit_NPS(employee, exit_date):
    corpus = read_from_CRA(PRAN)                            # not internal
    lump   = corpus × allowed_lump_%
    annuity= buy_annuity(corpus − lump)                    # mandatory above threshold
    encash = min(EL_balance,300) × (basic+DA)/30
    net    = lump + encash − dues
    initiate_withdrawal_request(PRAN)                      # reconcile via §14
```

### 5.3 Ongoing pension + DR (OPS)

```text
monthly_pension(pensioner, month):
    dr% = DR_rate(month)                                    # shared cadence with DA §05/§17
    return (basic_pension − commuted_reduction(month)) + basic_pension × dr%
    # commuted_reduction → 0 after restore_date
```

---

## 6. Worked Example (OPS retirement settlement)

**Mr. Roy** (OPS), retires at superannuation. Last Basic **₹56,100**, DA **53%**,
EL balance **300**, qualifying service **33 years** (after a small EOL deduction),
outstanding vehicle loan **₹40,000**.

```text
Emoluments (Basic+DA) = 56,100 + 53% = 56,100 + 29,733 = 85,833 (for encashment)
Pension (½ × last Basic, full QS)     = 0.5 × 56,100        ≈ 28,050 / month
Leave encashment = 300 × 85,833 / 30                        = 8,58,330
Commutation (say 40% of pension, factor illustrative):
   commuted pension = 0.40 × 28,050 = 11,220
   lump = 11,220 × factor(≈8.371) × 12 ≈ 11,27,000 (illustrative)
   reduced pension = 28,050 − 11,220 = 16,830 (restored after ~15 yrs)
Gratuity (DCRG, capped)                ≈ (per rule, e.g.) 11,50,000
GPF final balance                      ≈ (from ledger) say 9,00,000
Less: outstanding loan (§12)           − 40,000
```
```text
One-time payout ≈ encash 8,58,330 + commute 11,27,000 + gratuity 11,50,000
                  + GPF 9,00,000 − loan 40,000 ≈ ₹39,95,330 (illustrative)
Ongoing: PensionerAccount → monthly 16,830 + DR; pension restores to 28,050 + DR after ~15 yrs.
On death → Family Pension (enhanced then normal) to spouse.
```

> Swap Mr. Roy for **Mr. Das (NPS)**: no defined pension. His **corpus** (10%+14%
> + returns, read from CRA) is split into a **lump-sum** + **annuity**; he still
> gets **leave encashment** and the same **loan recovery**. The §04 fork produces
> two entirely different retirements from the same engine shell.

---

## 7. System Implications

- **Route the entire settlement on the §04 scheme field** — OPS defined-benefit
  vs NPS corpus — sharing only encashment, dues recovery, and GIS.
- **Derive qualifying service** from the immutable service ledger (§02) minus
  un-condoned EOL/dies-non — the EOL echo from §07/§10 must land here.
- Implement **OPS formulas** (pension, **commutation** with age-factor + reduction
  + restoration, **gratuity** with ceiling, **family pension** enhanced→normal) as
  **config-driven** (era/state-varying).
- For **NPS**, **read corpus from CRA** and **initiate the exit/annuity request** —
  don't compute a defined benefit; reconcile via §14.
- Compute **leave encashment** = min(EL, 300) × (Basic+DA)/30 from the §09 ledger.
- **Net outstanding dues (§12/§06)** from terminal benefits; handle **death-time
  waivers** (§18).
- **Pay GPF final balance** (OPS) from the GPF ledger (§14).
- Run a **PensionerAccount as an ongoing mini-payroll**: basic pension + **DR**
  (shared DA cadence §05/§17), with **commutation restoration** on schedule.
- Generate **pension/gratuity papers** (the §28/§15 exit documents) and trigger
  **family pension** on death.

---

## 8. Open Questions / State-Specific (confirm before build)

1. Assam's exact **pension formula** (last-drawn vs 10-month average; the
   fraction/ max-QS) and **minimum/maximum** pension.
2. **Commutation** — max commutable %, the **age-factor table**, and restoration
   period.
3. **Gratuity (DCRG)** formula and the current **statutory ceiling**.
4. **Family pension** enhanced/normal rates and eligibility (spouse, children,
   dependents).
5. **NPS exit** rules as adopted — lump-sum %, annuity threshold, provider choice.
6. **Leave encashment** cap (confirm 300) and the emoluments base.
7. **DR** rate source/cadence and whether pension is disbursed by the university or
   a pension-disbursing bank/treasury.
8. **Death-in-service** dues **waiver** rules and the settlement document set.
9. **Condonation** of EOL/dies-non for qualifying service (when service breaks are
   condoned).

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Terminal Benefits** | All payouts at exit. *Note:* path set by §04 scheme; some parts common to OPS & NPS. |
| **Qualifying Service (QS)** | Service counting toward pension. *Note:* total − un-condoned EOL/dies-non (§02/§07/§10 echo). |
| **OPS Pension** | Defined-benefit monthly pension for life. *Note:* ≈ ½ × emoluments × QS/max. |
| **Emoluments** | Pay base for pension/gratuity. *Note:* last-drawn or 10-month average — whichever rule says. |
| **Commutation** | Trading pension fraction for a lump sum. *Note:* age-factor table; pension reduced then restored (~15 yrs). |
| **Commutation Factor** | Age-based multiplier for the lump sum. *Note:* config table. |
| **Gratuity / DCRG** | One-time lump sum at exit. *Note:* service+emoluments based; statutory ceiling. |
| **Family Pension** | Pension to dependents on death. *Note:* enhanced rate then normal. |
| **Leave Encashment** | EL balance cashed at exit. *Note:* min(EL,300) × (Basic+DA)/30; common to both schemes. |
| **GPF Final Payment** | Full GPF balance+interest at retirement (OPS). *Note:* from GPF ledger (§14). |
| **NPS Corpus** | Accumulated NPS contributions+returns. *Note:* read from CRA; not internally computed. |
| **Annuity** | Mandatory NPS pension purchase. *Note:* from corpus above threshold; provider-paid. |
| **Dearness Relief (DR)** | Pensioner DA-equivalent. *Note:* on basic pension; shared cadence with DA (§05/§17). |
| **PensionerAccount** | Ongoing post-retirement payroll. *Note:* basic pension + DR, with commutation restoration. |
| **Dues Recovery at Exit** | Netting loans/overpay from benefits. *Note:* §12/§06; may be waived on death (§18). |
| **Condonation** | Officially excusing a service break. *Note:* restores qualifying service. |

---

### Status
Section 16 complete. Update roadmap tracker: 16 → ✅ Done.
Phase 6 (Compliance & Exit) complete. Next: **Section 17 — Master Data, Rate Tables & Reports** (Phase 7).
