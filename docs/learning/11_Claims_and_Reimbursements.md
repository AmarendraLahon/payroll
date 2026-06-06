# Section 11 — Claims & Reimbursements

> Learning roadmap §11. Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §31 (Additional Allowances & Reimbursements), §35 (Honorarium & Non-Regular Payments).
> Sections 05–08 handled **automatic monthly** money (computed from position).
> This section handles **event-driven, claim-based** money — paid only when an
> employee *submits a bill or proof*, on its own approval flow, often **outside**
> the monthly salary run.

---

## 1. Purpose

Not all money an employee receives is a formula on Basic. A large class is
**reimbursement and claim** — the employee **spends or does something first**
(sends a child to school, travels on tour, works overtime, donates leave to
travel), then **claims** it with documentary proof, and the institution
**sanctions and pays**.

The defining contrast with Section 05:

| | Monthly allowance (§05) | Claim / reimbursement (§11) |
|---|---|---|
| Trigger | Position exists | An **event** + a **bill** |
| Amount | Derived (Basic × rate) | **Actuals vs ceiling** |
| Timing | Every month, automatic | When claimed, **approved** |
| Bill | Inside salary bill | Often a **separate claim bill** |
| Proof | None | **Receipts / certificates** required |

The system needs a **Claims module** that runs parallel to the salary engine,
feeds the **bank payout** and the **employee's pay record for tax**, but does
**not** inflate the monthly Basic-driven computation.

---

## 2. Governing Rules / Authority

- **CEA / Hostel Subsidy** — central pattern (DoPT) adopted by state; per-child
  annual ceiling, max 2 children, hostel a higher separate ceiling.
- **LTC** — Leave Travel Concession rules: **block-year** based (Home-Town /
  All-India), fare reimbursed by entitled class, **tied to leave**, advance
  permissible.
- **Tour TA/DA** — travelling-allowance rules: **mileage/fare + Daily Allowance +
  lodging** entitlements **graded by pay level**; distinct from the monthly
  Transport Allowance (§05).
- **OTA** — overtime rules for **Grade-IV / drivers**: hours beyond duty × rate.
- **Bonus / Ad-hoc Bonus / Ex-gratia** — annual festival bonus for eligible
  **non-gazetted** staff; **formula-capped** (calculation ceiling).
- **Honorarium / guest / part-time** (§35) — sanction-based remuneration for
  non-regular persons or extra duties; governed by university/finance sanction
  orders, **not** the pay matrix.
- **Tax**: most reimbursements have **exemption limits** (CEA, LTC under IT rules);
  the excess and honoraria are **taxable** and must reach Form 16/24Q (Section 15).

---

## 3. Core Concepts

### 3.1 The two shapes of a claim

```text
Reimbursement = min(actual_spent, ceiling)        # CEA, hostel, medical, LTC fare
Entitlement   = rule_rate × units (by pay level)  # Tour DA, OTA, mileage
```

- **Reimbursement** caps **actuals** at a ceiling — you never pay more than spent,
  never more than the cap.
- **Entitlement** computes from a **rate × quantity** graded by pay level — closer
  to a formula, but still **event-triggered** and claimed.

### 3.2 The claim lifecycle (common to all)

```text
SUBMIT (employee + proof) → VERIFY (eligibility, ceiling, block-year)
→ SANCTION (competent authority) → PAY (claim bill / merged into salary)
→ POST to pay record (for tax) → (ADJUST advance, if any)
```

Every claim type is the **same workflow** with different **eligibility +
ceiling** rules. Build one engine, parameterise the rules.

### 3.3 The catalogue (§31)

| Claim | Shape | Key rule |
|---|---|---|
| **CEA** | Reimbursement | Per child, **max 2**, fixed **annual cap**; needs school proof |
| **Hostel Subsidy** | Reimbursement | Child in hostel; **higher separate ceiling** than CEA |
| **LTC** | Claim (fare) | **Block-year** (Home-Town / All-India); class by pay level; **advance** allowed; **tied to leave** |
| **Tour TA/DA** | Entitlement | **Mileage/fare + Daily Allowance + lodging**, graded by pay level; per-tour bill |
| **OTA** | Earning | Grade-IV/drivers; **hours × rate**; may merge into salary |
| **Bonus / Ex-gratia** | Earning | Non-gazetted; **formula-capped**; festival timing |
| **Medical Reimbursement** | Claim | **Actuals vs** fixed Medical Allowance |

### 3.4 Advances and adjustment (LTC, Tour)

LTC and Tour allow an **advance** before travel; the **final claim** must be
**adjusted** against it (recover unspent, pay shortfall). The system must track an
**advance → claim settlement** link, or the advance becomes an untracked
recoverable (Section 06/12).

> **Example — LTC advance:** Dr. Sharma draws ₹40,000 LTC advance, actually
> claims ₹46,000 fare. System pays the **₹6,000 balance** and closes the advance.
> Had she claimed only ₹34,000, the **₹6,000 excess advance** becomes a
> **recovery** (Section 06).

### 3.5 Block-year logic (LTC)

LTC entitlement is per **block of years** (e.g. a 4-year block with Home-Town
sub-blocks), **carry-forward** of an unused block into the first year of the next
is allowed. The system tracks **per-employee block consumption**, not a simple
yearly reset.

### 3.6 Honorarium & non-regular payments (§35) — a parallel stream

Money to people who are **not regular monthly-salaried**, or to staff for **extra
duties** outside their role:

| Payment | Recipient | Basis |
|---|---|---|
| Exam / Invigilation Honorarium | Staff + external | Per session / per script |
| Guest / Visiting Faculty | Guest faculty | Per lecture / per hour |
| Part-time / Contractual | Contract staff | Consolidated / hourly |
| Committee / Special-Duty Honorarium | Staff | Per assignment |

Needs a **remuneration master** (rate per activity), a **claim/sanction** flow,
**TDS** (often **non-salary** TDS — different section, Section 15), and a **bank
payout** — structurally separate from the salary engine. An **external** guest
faculty has **no Employee Master row**, so the model needs a **Payee** abstraction
broader than "employee".

---

## 4. Data Model

```text
ClaimType (config)
  ├─ code : CEA | HOSTEL | LTC | TOUR_TADA | OTA | BONUS | MEDICAL | HONORARIUM
  ├─ shape : REIMBURSEMENT | ENTITLEMENT | EARNING
  ├─ ceiling_rule / rate_rule (by pay level)     effective-dated (§17)
  ├─ proof_required[], approval_levels[]
  ├─ tax_exempt_limit
  └─ pay_via : SEPARATE_BILL | MERGE_SALARY

Claim (per submission)
  ├─ payee_ref (employee_code OR external_payee_id)
  ├─ claim_type, period/block, event_date
  ├─ claimed_amount, admissible_amount (after ceiling)
  ├─ advance_ref (nullable → links advance)
  ├─ status : SUBMITTED|VERIFIED|SANCTIONED|PAID|ADJUSTED|REJECTED
  ├─ proof_docs[], sanction_ref
  └─ taxable_portion

LTCBlockLedger (per employee)
  ├─ block_years, type (HOME_TOWN|ALL_INDIA)
  └─ consumed / carried_forward

Payee (superset of Employee — for §35 externals)
  ├─ payee_id, name, PAN, bank, is_employee
  └─ tds_category : SALARY | NON_SALARY
```

Design rules:
- **Ceilings/rates are effective-dated master data** (Section 17), never hard-coded.
- Claims are a **separate ledger** from monthly payslips; only the **taxable
  portion** posts into the pay/tax record.
- **Advance and claim are linked** — settlement is mandatory, not optional.
- **Payee ⊃ Employee** so externals (guest faculty, exam staff) can be paid with
  correct **non-salary TDS**.

---

## 5. Rules & Logic

### 5.1 Generic claim processing

```text
process_claim(claim):
    assert eligible(payee, claim_type, period/block)        # max-2-children, block-year, grade
    admissible = apply_ceiling_or_rate(claim_type, claim, pay_level)
    if claim.advance_ref: net = admissible − advance_paid    # may be +/-
    taxable = max(0, admissible − tax_exempt_limit)
    route(pay_via): SEPARATE_BILL → claim bill; MERGE_SALARY → next payslip
    post_to_pay_record(taxable)                              # → Section 15
    if net < 0: raise_recovery(−net)                         # → Section 06
```

### 5.2 Worked rule — CEA

```text
admissible_CEA = min(actual_fees_per_child, annual_cap) for up to 2 children
# Hostel subsidy: same shape, higher cap, requires hostel certificate.
```

### 5.3 Worked rule — Tour DA (entitlement, by level)

```text
tour_claim = mileage_rate(level)×distance + DA_rate(level)×days + min(lodging_actual, lodging_ceiling(level))
```

---

## 6. Worked Example (CEA + a tour, same employee, same month)

**Mr. Das** in June files two unrelated claims:

**CEA** — two children, fees ₹14,000 and ₹9,000; annual cap **₹27,000/child**.
```text
Child 1: min(14,000, 27,000) = 14,000
Child 2: min( 9,000, 27,000) =  9,000
CEA admissible = 23,000   (tax-exempt within IT limit → taxable portion = 0)
```

**Tour TA/DA** — 3-day official tour, his level: DA ₹600/day, fare ₹2,200,
lodging actual ₹3,000 vs ceiling ₹3,600.
```text
Tour = 2,200 (fare) + 600×3 (DA) + min(3,000, 3,600) = 2,200 + 1,800 + 3,000 = 7,000
```

```text
Both paid via a SEPARATE claim bill (not in the salary run).
CEA ₹23,000 + Tour ₹7,000 = ₹30,000 disbursed.
His monthly Basic-driven salary (Section 05) is UNTOUCHED — claims don't inflate it.
Only any taxable excess posts to his Form-16 data (Section 15).
```

> Swap Mr. Das for an **external exam invigilator** (§35): no Employee row, paid
> from the **remuneration master** (₹/session), **non-salary TDS** deducted,
> bank payout via the **Payee** abstraction — same claim engine, different payee
> and TDS category.

---

## 7. System Implications

- Build a **Claims module** parallel to the salary engine: one **lifecycle**
  (submit → verify → sanction → pay → post), parameterised per **ClaimType**.
- Model two **shapes** — **reimbursement** (min of actual, ceiling) and
  **entitlement** (rate × units by level) — plus simple **earning** (OTA/bonus).
- Keep **ceilings and rates as effective-dated master data** (Section 17).
- **Link advances to final claims** (LTC/Tour) and auto-raise a **recovery**
  (Section 06) on excess advance.
- Track **LTC block-year consumption** per employee, with carry-forward — not a
  yearly reset.
- **Pay via separate claim bill or merge into salary** — configurable per type;
  either way post only the **taxable portion** to the pay/tax record (Section 15).
- Introduce a **Payee superset** so **external** recipients (guest faculty, exam
  staff) get paid with **non-salary TDS** — the salary engine stays
  employee-only.
- **Claims never inflate Basic-driven monthly pay** — keep the two ledgers
  separate (mirrors the §08 immutability discipline).

---

## 8. Open Questions / State-Specific (confirm before build)

1. Assam/university **CEA & hostel ceilings**, and whether a **third-child**
   exception (twins, special needs) applies.
2. **LTC** scheme as adopted — block-year definition, Home-Town vs All-India
   pattern, entitled travel class by level, advance %.
3. **Tour TA/DA** slab tables by pay level (DA rates, mileage, lodging ceilings,
   road/rail/air entitlement).
4. **OTA** eligibility (which posts) and the **hour rate** basis.
5. **Bonus / Ex-gratia** — eligible ceiling (pay limit), calculation ceiling, and
   timing.
6. **Honorarium rate master** — per-activity rates, sanction authority, and
   whether TDS is **salary** or **non-salary (194J etc.)** for staff vs externals.
7. Which claims **merge into the salary bill** vs go on a **separate claim bill**.
8. **Tax-exemption limits** to apply per claim (CEA, LTC) and how the **taxable
   excess** feeds Section 15.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **Claim / Reimbursement** | Event-driven money paid on proof. *Note:* contrast §05 automatic monthly allowances. |
| **Reimbursement shape** | Pay = min(actual, ceiling). *Note:* never more than spent or capped. |
| **Entitlement shape** | Pay = rate × units, graded by pay level. *Note:* Tour DA/mileage/lodging. |
| **CEA** | Children Education Allowance. *Note:* per child, max 2, annual cap; school proof. |
| **Hostel Subsidy** | Higher-cap allowance for hostelling children. *Note:* separate ceiling from CEA. |
| **LTC** | Leave Travel Concession. *Note:* block-year, tied to leave, advance allowed, class by level. |
| **Block Year** | Multi-year window for LTC entitlement. *Note:* tracked per employee; carry-forward, not yearly reset. |
| **Tour TA/DA** | Travel claim: fare + Daily Allowance + lodging by level. *Note:* distinct from monthly Transport Allowance (§05). |
| **Daily Allowance (DA-tour)** | Per-day tour subsistence. *Note:* graded by pay level; not the salary DA%. |
| **OTA** | Overtime Allowance. *Note:* Grade-IV/drivers; hours × rate. |
| **Bonus / Ex-gratia** | Festival bonus for non-gazetted. *Note:* formula-capped; eligibility ceiling. |
| **Advance & Adjustment** | Pre-travel money settled against the final claim. *Note:* excess → recovery (§06). |
| **Honorarium** | Sanction-based pay for extra duty / non-regular work. *Note:* §35; remuneration master, non-salary TDS. |
| **Payee (superset)** | Any paid party, employee or external. *Note:* lets guest/exam staff be paid; carries TDS category. |
| **Remuneration Master** | Rate-per-activity table for §35 payments. *Note:* drives honorarium/guest-faculty amounts. |
| **Separate Claim Bill** | Payment outside the monthly salary run. *Note:* keeps claims from inflating Basic-driven pay. |

---

### Status
Section 11 complete. Update roadmap tracker: 11 → ✅ Done.
Next: **Section 12 — Loans & Advances**.
