# AI Context

Project: [YOUR PROJECT NAME]
Version: 1.0
Last Updated: [DATE]

---

# Purpose

[YOUR PROJECT NAME] is a [brief one-line description of the application].

It manages:

- [Core entity 1]
- [Core entity 2]
- [Core entity 3]
- [Add more as needed]

The application is intended to [describe the end-to-end workflow it supports].

---

# AI Roles

> Assign AI tools to roles based on your team's preferences.

[AI Tool A]
- System Architect
- Technical Reviewer
- Specification Writer

[AI Tool B]
- Software Engineer
- Feature Implementation
- Bug Fixing
- Code Generation
- Repository Investigation

[AI Tool C]
- Documentation
- README
- API Documentation
- Release Notes

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

The frontend should not contain core domain logic.

---

# Coding Standards

[List language/style preferences here, e.g.:]

TypeScript strict mode.

No `any`.

No duplicated utilities.

Reusable components only.

Keep functions small.

Prefer composition over inheritance.

Do not introduce unnecessary dependencies.

---

# Project Structure

[frontend-dir]/
    [Frontend framework + language]

[backend-dir]/
    [Backend framework + language]

[database-dir]/
    [Database technology]

ORM
    [ORM name]

UI
    [UI library]

Data Fetching
    [Data fetching library]

---

# Business Rules

[List the non-negotiable business rules for your domain, e.g.:]

Every [critical operation] must preserve [invariant].

Never hard-delete [sensitive record type].

Prefer soft delete where historical records exist.

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

Avoid timezone ambiguity.

Always use centralized date utilities.

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

1. [Priority 1]
2. [Priority 2]
3. [Priority 3]

---

# Known Issues

Refer to:

[YOUR_BUG_MAP.md]

[YOUR_SYSTEM_MAP.md]

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

Never guess domain-specific rules.
