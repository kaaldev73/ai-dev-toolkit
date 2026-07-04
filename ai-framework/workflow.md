# AI Context

Project: FundzFlow
Version: 1.0
Last Updated: 2026-06-30

---

# Purpose

FundzFlow is a private equity / venture capital fund administration platform.

It manages:

- Funds
- Investors
- Capital Calls
- Distributions
- Chart of Accounts (COA)
- Journal Entries
- Banking
- Capital Accounts
- Reports
- Documents
- Management Fees

The application is intended to provide an end-to-end fund accounting workflow.

---

# AI Roles

ChatGPT
- System Architect
- Technical Reviewer
- Product Owner
- Specification Writer
- Documentation Author
- Root Cause Analysis

Claude
- Software Engineer
- Refactoring
- Feature Implementation
- Bug Fixing
- Code Generation
- Repository Investigation

OpenRouter
- Documentation
- README
- API Documentation
- User Guide
- Developer Guide
- Release Notes

Never use Claude for large documentation.

Never use OpenRouter for architectural decisions.

---

# Development Workflow

Investigation
    ↓
Architecture
    ↓
Specification
    ↓
Implementation
    ↓
Review
    ↓
Testing
    ↓
Merge

Never skip the Specification step.

---

# Architecture Rules

Do NOT redesign the project unless explicitly instructed.

Prefer extending existing modules.

Avoid duplicate business logic.

Business rules belong in the backend.

The frontend should not contain accounting logic.

---

# Coding Standards

TypeScript strict mode.

No `any`.

No duplicated utilities.

Reusable components only.

Keep functions small.

Prefer composition over inheritance.

Do not introduce unnecessary dependencies.

---

# Project Structure

client/
    React + TypeScript + Vite

server/
    Express + TypeScript

database/
    PostgreSQL

ORM
    Drizzle

UI
    ShadCN
    Radix UI

Data Fetching
    TanStack Query

---

# Business Rules

Every accounting operation must preserve double-entry accounting.

Journal Entries must always balance.

Never hard-delete accounting records.

Prefer soft delete where historical records exist.

Capital Calls affect:

- Investors
- Drawdowns
- Journal Entries
- Bank Transactions
- Reports

Changing a Capital Call requires recalculating all dependent data.

Investor Commitment changes may require drawdown recalculation.

---

# Shared Utilities

All formatting must use centralized helpers.

Never duplicate:

- Currency formatting
- Date formatting
- Percentage formatting
- Number formatting

---

# Date Rules

Store dates consistently.

Avoid direct usage of:

new Date("YYYY-MM-DD")

Always use centralized date utilities.

Avoid timezone ambiguity.

---

# Currency Rules

Never hardcode currency symbols.

Always derive currency from:

Fund.currency

---

# Validation Rules

Validate on:

Frontend

AND

Backend

Never rely solely on client validation.

---

# API Rules

Every API must:

Validate input

Return consistent responses

Return meaningful errors

Avoid silent failures

---

# Database Rules

Protect referential integrity.

Avoid orphaned records.

Use transactions where multiple tables are updated.

---

# Error Handling

Never swallow exceptions.

Always log meaningful errors.

Never leave empty catch blocks.

---

# UI Rules

Consistency over creativity.

Do not redesign layouts unless requested.

Maintain existing design language.

---

# Performance

Avoid duplicate queries.

Avoid unnecessary renders.

Reuse queries where possible.

Batch database operations when appropriate.

---

# Testing

Every bug fix should include:

- Root cause
- Fix
- Regression prevention

---

# Documentation

Implementation details belong in code.

Architecture belongs in documentation.

Do not generate verbose documentation unless requested.

---

# Current Priorities

1. Dashboard navigation

2. Edit / Save issues

3. Date handling

4. Number formatting

5. COA creation

6. Bank entry flow

7. Capital Call recalculation

8. PDF generation

9. Mail Merge

10. Management Fee

11. Capital Account Reporting

---

# Known Issues

Refer to:

BUG_MAP.md

SYSTEM_MAP.md

DATABASE_MAP.md

API_MAP.md

SAVE_FLOW.md

DEPENDENCY_GRAPH.md

TECH_DEBT.md

---

# AI Rules

Before modifying code:

1. Understand the affected module.

2. Search for existing implementations.

3. Reuse existing utilities.

4. Avoid introducing duplicate logic.

5. Minimize file changes.

6. Preserve backward compatibility.

7. Explain architectural implications before major refactors.

If requirements are unclear,

STOP

and ask for clarification.

Never guess financial or accounting rules.