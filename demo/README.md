# Assam Government University — Payroll & Leave Management System (Static Demo)

A **static, HTML-only mock** of an Assam Government University Payroll & Leave
Management System. Every page uses hard-coded sample data — there is **no
backend, no real authentication, no database, no build step**. It is a
clickable prototype that reflects the domain documented in
[`../docs/Assam_Govt_University_Payroll_Concepts.md`](../docs/Assam_Govt_University_Payroll_Concepts.md)
and the learning sections `docs/learning/01–19`.

## How to open

- **Double-click `login.html`** in any modern browser. That's it.
- Works **fully offline** from the file system (`file://`) — no server needed.
- Also works on **GitHub Pages** (all links are relative). Point Pages at the
  repo and open `demo/login.html`.

No internet connection, npm install, or local server is required.

## How to use

1. On `login.html`, optionally pick a **role** (Employee / Dealing Assistant /
   DDO / Approver / Auditor — reflecting RBAC, §19), then click **Login**.
   Any username/password works (fields are non-functional).
2. You land on **`dashboard.html`**, the hub. Every other page is reachable from
   here via tiles, and from the **top nav bar present on every page**.
3. **Logout** (top-right of the nav) returns to `login.html`.

The chosen role is shown in the header (stored in `localStorage` only, for
display — it does not gate anything).

## Pages

| Page | Module | Doc |
|---|---|---|
| `login.html` | Entry point + role selector (RBAC) | §19 |
| `dashboard.html` | Hub: tiles, summary widgets, period state | — |
| `employee.html` | Employee Master & Service Book timeline | §02 |
| `payslip.html` | Monthly payslip (Mr. Das example) | §05–06 |
| `pay-matrix.html` | 7th CPC Pay Matrix grid (Levels × Cells) | §03 |
| `leave.html` | Balances, ledger, mock Apply-Leave form | §09 |
| `increment-macp.html` | Career pay movement & fixation | §07 |
| `arrears.html` | DA-arrear difference statement (50%→53%) | §08 |
| `loans.html` | Active loans, recovery, amortisation | §12 |
| `claims.html` | CEA + Tour TA/DA claim examples | §11 |
| `salary-bill.html` | Multi-employee unit bill, schedules, heads | §13 |
| `pension.html` | OPS settlement vs NPS corpus (tabs) | §16 |
| `reports.html` | Pay bill, registers, Form 16 (mock tables) | §17/§20 |
| `admin.html` | Role-permission matrix + rate tables | §17/§19 |

Every page is reachable from `login.html` in **≤ 2 clicks** (login → dashboard →
any page; the shared top nav also links every page directly).

## Role workspaces (workflow wireframes)

Picking a **role** on the login page routes to that role's own workspace folder,
each with role-specific workflow wireframes and a role sub-nav. These sit
alongside the shared module pages above (which they link into as "All Modules").

| Role folder | Workflow wireframes |
|---|---|
| `employee/` | self-service home · apply-leave · Form 12BB · my documents |
| `dealing-assistant/` | work queue · **bill prep (5-step)** · service event · process leave · verify claims · draft arrear |
| `ddo/` | verification queue · verify & sanction · treasury & disburse |
| `approver/` | approval inbox · approve bill · approve leave · establishment |
| `auditor/` | oversight · audit trail · reconciliation (read-only) |
| `admin/` | console · rate tables (insert-not-edit) · users & roles · data migration |

The wireframes mirror the bill lifecycle across roles — the same bill object
moves Draft → Verified (DDO) → Approved (Registrar) → Disbursed → Locked, each
role seeing it in its own mode. All actions are mock (nothing is saved).

## Sample data

- **Mr. A. Das** — non-teaching, NPS. Level 4, Cell 3, Basic **₹25,500** →
  Gross **₹45,690** → Net **₹38,797** (the worked example from the docs).
- **Dr. R. Sharma** — teaching, NPS (UGC Academic Level 13A).
- **Mr. P. Roy** — non-teaching, OPS/GPF, retiring (used for the OPS pension
  settlement example).

All figures are illustrative, matching the worked examples in the concept docs.
Amounts use Indian number formatting and the ₹ symbol.

## Files

```
demo/
├── login.html                 entry point
├── dashboard.html             hub
├── employee.html  payslip.html  pay-matrix.html  leave.html
├── increment-macp.html  arrears.html  loans.html  claims.html
├── salary-bill.html  pension.html  reports.html  admin.html
├── styles.css                 one shared stylesheet
├── app.js                     vanilla JS: nav, tabs, table filter, leave form
└── README.md                  this file
```

## Implementation notes

- **HTML + one CSS file + one small vanilla JS file.** No frameworks, no build.
- `app.js` injects the shared top nav (so links stay consistent), renders the
  pay-matrix grid, and powers tabs, table filtering, and the mock leave form.
  It uses **no `fetch`/XHR**, so nothing breaks under `file://`.
- This is a **mock**: data is static, "Login" just navigates, and the
  Apply-Leave form only appends a row on screen — nothing is saved or sent.
