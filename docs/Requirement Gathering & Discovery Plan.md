# Assam Agricultural University ERP Replacement Project

## Requirement Gathering & Discovery Plan

### Project Objective

Replace the existing systems currently used by Assam Agricultural University:

1. Existing HRMS (Native PHP)
2. Existing Payroll System (Third-Party Vendor)
3. Existing Finance Management Processes

The objective is to build a unified web-based ERP platform covering:

* Human Resource Management
* Payroll Management
* Finance & Accounting
* Approval Workflows
* Reporting & Analytics
* Integration with External Systems

---

# Phase 1: Organization Discovery

## Goal

Understand the organizational structure before discussing software requirements.

### Information to Collect

#### University Structure

* Headquarters
* Constituent Colleges
* Regional Research Stations
* Krishi Vigyan Kendras (KVKs)
* Regional Offices
* Project Offices

#### Questions

1. How many organizational units exist?
2. How many employees are currently working?
3. Is payroll centralized or decentralized?
4. Which offices prepare salary bills?
5. Which offices approve salary bills?
6. Who releases payments?

### Deliverables

* Organization Hierarchy Diagram
* Approval Hierarchy Diagram
* User Role Matrix

---

# Phase 2: Existing System Assessment

## Goal

Understand how the current systems operate.

---

## HRMS Assessment

### Identify Existing Modules

* Employee Master
* Service Book
* Leave Management
* Transfer Management
* Promotion Management
* Increment Management
* Retirement Management
* Recruitment Management

### Questions

1. Which modules are actively used?
2. Which modules are not used?
3. Which modules require improvement?
4. Which reports are generated regularly?

### Documents Required

* HRMS User Manual
* Sample Reports
* Database Structure (if available)

---

## Payroll System Assessment

### Process Walkthrough

Request a complete demonstration of:

1. Salary Processing
2. Approval Workflow
3. Salary Bill Generation
4. Payment Process
5. Report Generation

### Questions

1. Who initiates salary processing?
2. What data sources are used?
3. How are leave deductions handled?
4. How are arrears processed?
5. How are salary revisions implemented?

### Documents Required

* Payroll User Manual
* Sample Salary Slip
* Sample Salary Register
* Sample Pay Bill

---

# Phase 3: HRMS Detailed Study

## Employee Categories

### Teaching Staff

* Professor
* Associate Professor
* Assistant Professor

### Non-Teaching Staff

* Registrar
* Accounts Personnel
* Administrative Staff
* Technical Staff

### Other Categories

* Contractual Employees
* Project Employees
* Daily Wage Workers
* Guest Faculty

### Questions

1. Are payroll rules different for each category?
2. Are service rules different?
3. Are leave rules different?

---

## Service Book Management

### Events to Capture

* Appointment
* Confirmation
* Promotion
* Transfer
* Increment
* Pay Revision
* Leave Without Pay
* Suspension
* Retirement

### Questions

1. Is service book maintained digitally?
2. Is physical service book still maintained?
3. Which records are mandatory?

---

## Leave Management

### Leave Types

* Casual Leave
* Earned Leave
* Medical Leave
* Maternity Leave
* Child Care Leave
* Extraordinary Leave

### Questions

1. Leave accumulation rules?
2. Encashment rules?
3. Carry forward limits?

---

# Phase 4: Payroll Deep Dive

## Salary Structure Analysis

### Earnings

* Basic Pay
* Dearness Allowance (DA)
* House Rent Allowance (HRA)
* Transport Allowance (TA)
* Medical Allowance
* Academic Allowance
* Special Allowance
* Research Allowance

### Deductions

* NPS
* GIS
* Professional Tax
* Income Tax (TDS)
* Loan Recovery
* Advance Recovery
* Miscellaneous Recovery

---

## Pay Matrix

### Questions

1. Which pay matrix is currently followed?
2. Are UGC pay scales used?
3. Are state government pay scales used?
4. How are revisions handled?

---

## Payroll Processing Workflow

### Current Workflow

Attendance / Leave
↓
Payroll Processing
↓
Accounts Verification
↓
Finance Approval
↓
Salary Bill Generation
↓
Payment Release

### Questions

1. Monthly payroll process timeline?
2. Approval hierarchy?
3. Salary freeze process?
4. Reprocessing rules?

---

## Arrear Management

### Cases

* Promotion Arrear
* Pay Revision Arrear
* DA Revision Arrear
* Manual Arrear

### Questions

1. How are arrears calculated?
2. How are arrears approved?

---

# Phase 5: Finance Module Discovery

## Goal

Determine the actual scope of the Finance Module.

---

## Budget Management

### Questions

1. Is budget allocated department-wise?
2. Is budget allocated project-wise?
3. Is budget allocated grant-wise?

### Required Features

* Budget Creation
* Budget Approval
* Budget Revision
* Budget Monitoring

---

## Expenditure Management

### Process

Bill Creation
↓
Verification
↓
Approval
↓
Payment
↓
Accounting Entry

### Questions

1. How are expenditure bills processed?
2. What approval levels exist?
3. Are expenditure limits defined?

---

## Fund Management

### Sources

* State Government Funds
* Central Government Funds
* ICAR Grants
* Research Grants
* Sponsored Projects

### Questions

1. Are separate ledgers maintained?
2. Are utilization certificates generated?

---

## Accounting Requirements

### Verify Need For

* Chart of Accounts
* Journal Entries
* Ledger
* Cash Book
* Bank Book
* Trial Balance
* Balance Sheet
* Income & Expenditure Statement

### Questions

1. Is double-entry accounting required?
2. Are audits conducted using system reports?

---

# Phase 6: Integrations

## Treasury Integration

Questions:

1. Is Assam Treasury used?
2. Is file upload required?
3. Is API integration required?

---

## Banking Integration

Questions:

1. Salary bank file generation?
2. Vendor payment files?
3. Multiple banks supported?

---

## NPS Integration

Questions:

1. PRAN generation?
2. Monthly contribution upload?

---

## Income Tax

Questions:

1. Form 16 generation?
2. Tax computation?
3. Tax declaration workflow?

---

## External Systems

Identify all existing integrations.

---

# Phase 7: Data Migration Strategy

## Existing Systems

### HRMS

* Database Type
* Record Count
* Historical Data Availability

### Payroll

* Database Type
* Salary History Available
* Arrear History Available

### Finance

* Ledger Data Available
* Historical Transactions Available

---

## Data Migration Scope

### Mandatory

* Employee Master
* Service Book
* Leave Balances
* Salary History
* Payroll Components

### Optional

* Historical Reports
* Archived Documents

---

# Phase 8: Reporting Requirements

## HR Reports

* Employee Register
* Service History
* Retirement Forecast

## Payroll Reports

* Salary Register
* Pay Bill
* Salary Slip
* NPS Report
* GIS Report
* Income Tax Report

## Finance Reports

* Budget Utilization
* Ledger
* Cash Book
* Trial Balance
* Balance Sheet

### Requirement

Collect top 20 reports currently used every month.

---

# Technical Assessment

## Existing Infrastructure

### Questions

1. Current hosting environment?
2. Current database?
3. Current user count?
4. Peak concurrent users?

---

## Security Requirements

* Role Based Access Control
* Audit Logs
* Digital Approval Trail
* Document Security
* Backup Strategy

---

# Deliverables Before Development

The following must be collected before estimation or development begins:

1. HRMS User Manual
2. Payroll User Manual
3. Finance Process Documents
4. Sample Salary Slips
5. Sample Pay Bills
6. Sample Budget Reports
7. Sample Finance Reports
8. Existing Database Schemas
9. Approval Hierarchies
10. User Role Matrix
11. Data Migration Requirements
12. Integration Requirements

---

# Expected Outcome

At the end of the discovery phase, the project team should produce:

1. Business Requirement Document (BRD)
2. Software Requirement Specification (SRS)
3. Process Flow Diagrams
4. Data Migration Plan
5. Integration Plan
6. Module-Wise Effort Estimation
7. Development Roadmap
8. ERP Architecture Design

No development effort estimation should be finalized before completing the above discovery activities.
