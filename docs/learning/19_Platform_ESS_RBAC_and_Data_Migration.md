# Section 19 — Platform: ESS, RBAC & Data Migration

> Learning roadmap §19 (final). Source concept: `../Assam_Govt_University_Payroll_Concepts.md`
> §38 (System Concerns — ESS, RBAC, Opening Balances & Data Migration).
> Sections 01–18 defined **what the system computes**. This closing section defines
> **how people get into it, what each role may do, and how it is born with correct
> starting state**. None of these are payroll *math* — but without them the engine
> has no users, no access discipline, and no day-one data to run on.

---

## 1. Purpose

A correct payroll engine is useless if (a) employees can't reach their own
payslip, (b) anyone can edit anyone's pay, or (c) on go-live there are no opening
balances so the **first payroll is wrong**. This section covers the three
cross-cutting platform concerns:

1. **ESS (Employee Self-Service)** — the employee's door into the existing
   workflows.
2. **RBAC (Role-Based Access Control)** — who is allowed to do what, paired with
   the audit trail (§18).
3. **Opening Balances & Data Migration** — the one-time onboarding that gives the
   system its **initial truth** before any month runs.

The questions this section answers:

> "How does an employee apply for leave or grab their Form 16 without a clerk? Who
> can enter data vs sanction a bill vs only read? And on the very first day, where
> do leave balances, GPF, loans, and pay fixation **come from** so month-one is
> correct?"

---

## 2. Governing Rules / Authority

- **ESS** has no separate statute — it is a **channel** that must feed the *same*
  sanction/approval flows the rules already require (leave §09, 12BB §15).
- **RBAC** enforces the **separation of duties** government financial rules assume:
  the person who **prepares** a bill is not the person who **sanctions** it; an
  **auditor** only reads.
- **Migration** has no formula but is the precondition for **legal correctness** of
  the first bill — opening GPF/loan/leave/fixation must reconcile to the prior
  (often manual/legacy) records.
- All three lean on the **audit trail** (§18) — every ESS submission, privileged
  action, and migrated value is logged.

---

## 3. Core Concepts

### 3.1 ESS — a channel, not a new workflow (§38)

```text
Employee Self-Service feeds EXISTING flows, never bypasses them:
  ├─ Apply for leave        → §09 approval flow (not auto-grant)
  ├─ View/download payslip & Form 16   → §13/§15 outputs (read)
  ├─ Submit Form 12BB / declaration    → §15 TDS projection (input)
  └─ View GPF/NPS balance, leave balance, service book → §14/§09/§02 (read)
```

> **Key insight:** ESS is **plumbing to the front door**, not a parallel system. A
> leave applied via ESS still hits the **same §09 sanction chain**; a 12BB
> submitted via ESS still drives the **same §15 projection**. ESS changes *who
> enters the data* (the employee, not a clerk), not *what happens next*. This cuts
> data-entry load and errors while preserving every control.

### 3.2 RBAC — separation of duties (§38)

| Role | May do | May NOT do |
|---|---|---|
| **Employee** | Self-service (apply leave, view own pay/balances, submit 12BB) | See/edit others; approve anything |
| **Dealing Assistant** | Data entry, bill **preparation** | Sanction/approve; lock period |
| **DDO** | **Verify & sanction** bills, draw on treasury | Self-approve own data entry (segregation) |
| **Approver / Registrar** | Final approval, establishment decisions | — |
| **Auditor** | **Read-only** everything + audit trail | Any change |

```text
Principle: the PREPARER ≠ the SANCTIONER ≠ the AUDITOR.
Each privileged action checks role-permission AND writes the audit trail (§18).
```

RBAC and the **audit trail** are a **pair**: RBAC says *who may act*, audit says
*who did act* — together they make the system defensible (§13/§14/§18).

### 3.3 Scoping — not just role, but reach

A role isn't enough; permissions are **scoped**:

```text
permission = (role) × (scope: own | unit/college | university-wide) × (action: read|write|sanction)
```

A Dealing Assistant of College A prepares **College A** bills, not College B's. An
employee sees **only their own** record. Scoping is what keeps a multi-college
university's data partitioned.

### 3.4 Opening Balances & Data Migration — being born correct (§38)

The system cannot compute month-one from nothing. It must be **seeded** with each
employee's **current state**:

| Opening balance | Feeds | Without it… |
|---|---|---|
| **Leave balances** (EL/HPL/CL) | §09 ledger | leave accrual/encashment wrong |
| **GPF opening balance + interest** | §14/§16 | GPF statement & final payment wrong |
| **Outstanding loan principal + remaining installments** | §12 | loan recovery wrong / never ends |
| **Current pay fixation, Level/Cell, last increment date** | §03/§07 | Basic & next increment wrong |
| **NPS PRAN / GPF account no., scheme assignment** | §04/§13 | can't route deductions/schedules |

```text
Migration = load these as the system's INITIAL ledgers/positions,
            reconciled against legacy (often manual) records,
            so the FIRST computed month matches what the employee actually expects.
```

### 3.5 Migration is itself an arrear/audit risk

If opening data is wrong, month-one is wrong, and corrections become **arrears**
(§08) or recoveries (§06) against real people. So migration must be **reconciled
and audited** like any financial event — opening balances are entered with
**provenance** (source record ref), and a **parallel-run** (compute a known past
month, compare to what was actually paid) validates the seed before go-live.

> **Example — opening loan:** Mr. Das's vehicle loan was sanctioned ₹1,80,000,
> already 12 installments recovered in the legacy system. Migration must seed
> **outstanding ₹1,44,000 with 48 installments left** (§12), not the original
> ₹1,80,000 — or the system would over-recover by a year. This single field, wrong,
> is a real financial loss; hence reconcile + audit.

### 3.6 The module structure (the whole system, assembled)

The concept doc's suggested modules map the 19 learning sections into buildable
units:

```text
1. Employee & Service Book    → §01,02,04,18(audit)
2. Leave & Attendance         → §09,10
3. Payroll Processing         → §03,05,06,07,08,14,17
4. Claims & Reimbursements    → §11,12
5. Treasury, Budget & Recon   → §13,14
6. Statutory & Compliance     → §15
7. Pension & Settlement       → §16
8. Platform (ESS/RBAC/Migrate)→ §19   ← this section binds the rest
```

This section is the **binding layer**: it gives the other seven their **users,
access rules, and starting data**.

---

## 4. Data Model

```text
User
  ├─ user_id, linked_employee_code (nullable for pure-admin)
  ├─ status, auth (credentials/SSO)
  └─ roles[]

Role
  ├─ role_code : EMPLOYEE | DEALING_ASSISTANT | DDO | APPROVER | AUDITOR
  └─ permissions[] : (resource, action)

PermissionGrant (scoped)
  ├─ user/role, resource (LEAVE|BILL|MASTER|PAY|REPORT…)
  ├─ action : READ | WRITE | SANCTION | LOCK
  └─ scope : OWN | UNIT(college_code) | UNIVERSITY

ESSRequest
  ├─ employee_code, type : LEAVE | DECLARATION_12BB | PROFILE_UPDATE
  ├─ payload, status (feeds §09/§15 flows)
  └─ submitted_at

MigrationBatch (go-live)
  ├─ batch_id, as_on_date
  └─ records[]:
       ├─ employee_code
       ├─ opening_leave{EL,HPL,CL}, gpf_opening{balance,interest}
       ├─ loans[]{sanctioned, outstanding, installments_left}   ← §12
       ├─ pay_position{level,cell,basic,last_increment_date}    ← §03/§07
       ├─ scheme{OPS|NPS}, pran/gpf_no                          ← §04
       └─ source_ref (legacy record provenance)  + reconciled flag
```

Design rules:
- **Every privileged action checks a scoped PermissionGrant** and **writes the
  audit trail** (§18) — no action without both.
- **ESS writes feed the existing approval flows** (§09/§15) — never auto-commit.
- **Migration records carry provenance + a reconciled flag**; go-live is gated on
  a **parallel-run** validation.
- **Opening balances become the initial ledger entries** of §09/§12/§14 — the same
  ledgers the engine appends to thereafter (continuity, not a separate store).

---

## 5. Rules & Logic

### 5.1 Permission check (every privileged call)

```text
authorise(user, resource, action, target):
    grant = find PermissionGrant(user.roles, resource, action)
    assert grant exists and scope_covers(grant.scope, user, target)
    proceed; audit_log(user, action, target, old→new)        # §18
```

### 5.2 ESS submission

```text
ess_submit(employee, type, payload):
    create ESSRequest(status=PENDING)
    route to the SAME flow a clerk-entered item would hit:
        LEAVE → §09 sanction chain;  12BB → §15 projection recompute
    employee may VIEW status; cannot self-approve
```

### 5.3 Go-live migration

```text
migrate(batch, as_on_date):
    for rec in batch:
        seed leave ledger (§09), gpf (§14), loans (§12), pay position (§03/§07), scheme (§04)
        attach source_ref; mark reconciled
    PARALLEL RUN: compute a known prior month → compare to legacy paid figures
    if matches within tolerance → allow first live period; else fix seed
```

---

## 6. Worked Example (go-live for one employee, then month-one)

**Mr. Das**, migrated as on **31 May** for a **1 June** go-live:

```text
Seeded opening state (from legacy records, reconciled):
  Leave:    EL 45, HPL 20, CL 6
  GPF:      n/a (he's NPS) — instead PRAN seeded, scheme = NPS
  Loan:     vehicle outstanding 1,44,000, 48 installments left (NOT 1,80,000/60)
  Pay:      Level 4, Cell 3, Basic 25,500, last increment 1-Jul-2024
  Scheme:   NPS, PRAN xxxx
  source_ref: legacy service book + loan register page nos.

PARALLEL RUN (validate the seed):
  recompute MAY using seeded position → compare to what legacy actually paid Das in May
  match ✓ → seed trusted
```

```text
1 June (first live month):
  Basic 25,500 (from seeded position §03) → full salary engine §05–06 runs
  Loan recovers installment 13 of 60 against outstanding 1,44,000 (§12) — correct, no over-recovery
  Leave ledger opens at EL 45 (§09); July accrual will add to it
Mr. Das logs into ESS: views June payslip, submits his Form 12BB → §15 reprojects his TDS.
```

> Get the **opening loan field wrong** (seed 1,80,000/60 instead of 1,44,000/48)
> and the system silently **over-recovers for 12 extra months** — a real loss to a
> real person, surfacing only on audit. Migration correctness *is* payroll
> correctness; the parallel-run is the safety net.

---

## 7. System Implications

- Build **ESS as a channel into existing flows** (leave §09, 12BB §15, payslip/
  Form 16 §13/§15, balance views) — **never auto-commit**, never a parallel
  workflow.
- Implement **RBAC with scoped permissions** (`role × scope × action`) enforcing
  **separation of duties** (preparer ≠ sanctioner ≠ auditor); pair **every**
  privileged action with the **audit trail** (§18).
- **Scope** access by **own / unit-college / university** so a multi-college
  university's data stays partitioned.
- Treat **go-live migration as a first-class project**: seed **leave, GPF, loans,
  pay fixation, scheme/PRAN** as the **initial ledger state** of §09/§12/§14/§03/
  §04, with **provenance** on every value.
- **Reconcile and parallel-run** before the first live period — a known past month
  must recompute to the legacy-paid figure within tolerance.
- Recognise **migration errors propagate as arrears/over-recoveries** against real
  people — gate go-live on validation, audit every seeded value.
- Assemble the 19 sections into the **suggested module structure**; this platform
  layer **binds** the other modules with users, access, and starting data.

---

## 8. Open Questions / State-Specific (confirm before build)

1. **Authentication** for ESS — university SSO, government employee ID, or
   standalone credentials; mobile vs web.
2. The **exact role set and permission matrix** the university uses (titles,
   sanction hierarchy, who locks a period).
3. **Multi-college scoping** model — fully partitioned vs shared central
   establishment.
4. **Legacy data sources** for migration (manual service books, an old system,
   spreadsheets) and their reliability.
5. **Reconciliation tolerance** and the **parallel-run** window for go-live
   sign-off.
6. **Opening-balance authority** — who certifies seeded GPF/loan/leave figures.
7. **Phased vs big-bang** go-live (college-by-college rollout?).
8. **ESS scope** at launch — read-only first, or leave/12BB submission from day
   one.

---

## 9. Keywords / Glossary (with notes)

| Keyword | Meaning & note |
|---|---|
| **ESS (Employee Self-Service)** | Employee's door into existing flows. *Note:* a channel, not a parallel workflow; never auto-commits. |
| **RBAC** | Role-Based Access Control. *Note:* who may act; paired with audit trail (who did act). |
| **Separation of Duties** | Preparer ≠ sanctioner ≠ auditor. *Note:* the control RBAC enforces; govt financial-rule requirement. |
| **Dealing Assistant** | Data-entry / bill-prep role. *Note:* prepares, cannot sanction. |
| **DDO** | Drawing & Disbursing Officer. *Note:* verifies/sanctions; can't self-approve own entry. |
| **Auditor (role)** | Read-only access incl. audit trail. *Note:* no change rights. |
| **Permission Scope** | own / unit-college / university reach. *Note:* partitions multi-college data. |
| **Opening Balances** | Day-one seeded state. *Note:* leave/GPF/loan/fixation/scheme; initial ledger entries. |
| **Data Migration** | One-time onboarding load. *Note:* precondition for a correct first payroll. |
| **Outstanding (migrated loan)** | Remaining principal + installments left. *Note:* seed this, NOT the original sanction — else over-recovery. |
| **Provenance / source_ref** | The legacy record behind a seeded value. *Note:* audit + reconciliation. |
| **Parallel Run** | Recompute a known past month, compare to legacy paid. *Note:* go-live validation gate. |
| **Reconciled Flag** | Marks a migrated value as verified. *Note:* gate before trusting the seed. |
| **Module Structure** | The 19 sections grouped into buildable units. *Note:* this section is the binding platform layer. |
| **Go-Live** | First live payroll period. *Note:* allowed only after seed + parallel-run pass. |

---

### Status
Section 19 complete. Update roadmap tracker: 19 → ✅ Done.
**All 19 learning sections complete — the full Indian/Assam govt university payroll
& leave domain is now documented end-to-end.**
