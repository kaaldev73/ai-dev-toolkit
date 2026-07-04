# Business Rules

Project: FundzFlow

Version: 1.0

---

# Purpose

This document defines the business rules of FundzFlow.

These rules are mandatory.

AI must never invent or modify business rules without explicit approval.

Financial correctness is more important than code simplicity.

---

# Core Principles

FundzFlow is a fund administration platform.

Every operation must preserve:

- Financial accuracy
- Data integrity
- Auditability
- Historical accuracy
- Referential integrity

---

# Funds

A Fund represents an investment vehicle.

A Fund owns

- Investors
- Capital Calls
- Distributions
- Journal Entries
- Bank Accounts
- Reports
- Documents

Deleting a Fund must never silently delete historical accounting records.

---

# Investors

Every Investor belongs to one or more Funds.

Each Investor maintains

- Commitment
- Contributions
- Distributions
- Capital Account
- Drawdowns

Investor Commitment is the source for future capital call calculations.

---

# Investor Commitment

Changing an Investor Commitment affects

- Future Capital Calls

It may also require recalculation of

- Drawdowns
- Capital Accounts
- Reports

Historical accounting entries must not be modified automatically.

---

# Capital Calls

A Capital Call requests capital from Investors.

Changing a Capital Call affects

- Drawdowns
- Capital Accounts
- Investor Status
- Journal Entries
- Reports
- PDFs
- Email Notifications

Changing call percentage requires recalculating dependent records.

---

# Drawdowns

Drawdowns are derived data.

They should never become inconsistent with

- Investor Commitment
- Capital Call Percentage

Derived data should be regenerated rather than manually edited.

---

# Distributions

Distributions represent capital returned to Investors.

Distributions affect

- Capital Accounts
- Journal Entries
- Reports
- Investor History

Historical distributions must remain auditable.

---

# Chart of Accounts (COA)

Every Journal Entry references valid COA accounts.

COA accounts should not be hard-deleted if referenced.

Prefer

Soft Delete

Inactive

Archived

over deletion.

---

# Journal Entries

Journal Entries follow double-entry accounting.

Rules

Total Debit == Total Credit

Every line references a valid COA account.

Journal Entries become part of the permanent audit trail.

---

# Banking

Bank Transactions are generated from accounting events.

Editing historical bank records may require recalculating balances.

Balance history must remain consistent.

---

# Capital Accounts

Capital Accounts summarize

- Commitments
- Contributions
- Distributions
- NAV
- Balance

Capital Accounts are reporting objects.

Avoid manual editing.

---

# Reports

Reports are derived from accounting data.

Reports should never become the source of truth.

The database remains the source of truth.

---

# Documents

Documents

- Capital Call Notices
- Distribution Notices
- Statements

must reflect the latest approved data.

Documents generated before edits may require regeneration.

---

# Currency

Every Fund has its own currency.

Currency formatting must always use

Fund.currency

Never hardcode

₹

$

€

£

or any symbol.

---

# Date Handling

Store dates consistently.

Avoid timezone ambiguity.

Historical dates must not change due to browser timezone.

---

# Validation

Validate

Frontend

Backend

Database

Never rely on client validation alone.

---

# Derived Data

Derived data includes

- Drawdowns
- Capital Accounts
- Reports
- PDFs

Derived data should be recalculated.

Never manually synchronize values.

---

# Audit Trail

Financial operations should be traceable.

Every important change should record

- Timestamp
- User
- Previous Value
- New Value

Never silently modify historical financial data.

---

# Transactions

Operations affecting multiple tables should use database transactions.

Examples

Capital Call

↓

Drawdowns

↓

Journal

↓

Bank

↓

Reports

If one step fails,

the entire operation should roll back.

---

# Financial Integrity

Financial correctness has higher priority than

- Performance
- UI
- Convenience

Never sacrifice accounting correctness.

---

# AI Rules

Never

Guess accounting behavior.

Assume financial calculations.

Change business rules.

Delete historical accounting records.

Hard-delete COA records.

Modify journal entries without understanding downstream impact.

---

# Source of Truth

Funds

↓

Investors

↓

Capital Calls

↓

Journal Entries

↓

Bank Transactions

↓

Reports

Reports are generated from data.

Reports never own data.

---

# Current Known Risks

- Capital Call edits may not propagate correctly.
- Drawdowns can become stale.
- Currency formatting is duplicated.
- Date handling is inconsistent.
- COA validation is incomplete.
- Bank balances may become inconsistent after edits.

These issues should be fixed without violating the business rules above.