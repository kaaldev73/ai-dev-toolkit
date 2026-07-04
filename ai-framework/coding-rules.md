# AI Coding Rules

Project: FundzFlow

Version: 1.0

---

# Purpose

This document defines the mandatory coding standards for every AI-generated code change.

These rules apply to all backend, frontend, database, and shared code.

---

# General Principles

Write production-quality code.

Prefer readability over cleverness.

Optimize for maintainability.

Never optimize prematurely.

Avoid technical debt.

---

# Before Writing Code

Always

- Understand the existing implementation.
- Search for reusable code.
- Check if a similar feature already exists.
- Read related modules before modifying code.

Never write duplicate functionality.

---

# Architecture Rules

Never redesign architecture unless explicitly requested.

Extend existing modules whenever possible.

Business logic belongs in the backend.

UI should remain presentation-focused.

Do not mix concerns.

---

# File Modification Rules

Modify the fewest files possible.

Avoid unnecessary file creation.

Avoid renaming files unless instructed.

Do not move folders without approval.

---

# TypeScript Rules

Use strict typing.

Never use:

any

Avoid:

unknown

Prefer explicit interfaces.

Use readonly where appropriate.

Avoid unnecessary type assertions.

---

# Naming Rules

Variables

camelCase

Functions

camelCase

Classes

PascalCase

Interfaces

PascalCase

Enums

PascalCase

Constants

UPPER_SNAKE_CASE

Database

snake_case

---

# Function Rules

Functions should have one responsibility.

Avoid functions longer than approximately 50 lines.

Extract reusable logic.

Avoid deeply nested code.

Prefer early returns.

---

# Component Rules

Components should be reusable.

Avoid duplicated UI.

Keep state local when possible.

Avoid unnecessary props.

Prefer composition.

---

# API Rules

Validate every request.

Return consistent response shapes.

Return meaningful error messages.

Never swallow exceptions.

Never expose internal errors.

---

# Database Rules

Use transactions when updating multiple tables.

Protect referential integrity.

Avoid orphaned records.

Never hard-delete accounting data.

Use soft deletes where history matters.

---

# Validation Rules

Validate

Frontend

AND

Backend

Never trust client input.

---

# Error Handling

Always log meaningful errors.

Never leave empty catch blocks.

Return actionable error messages.

Avoid silent failures.

---

# Performance Rules

Avoid N+1 queries.

Batch database operations.

Reuse existing queries.

Avoid duplicate API requests.

Avoid unnecessary re-renders.

---

# Reuse Rules

Before writing code, search for

- utilities
- services
- components
- hooks
- validators
- formatters

Reuse before creating new code.

---

# Formatting Rules

Never hardcode

Currency

Date

Percentage

Number

Always use shared utilities.

---

# Date Rules

Never use

new Date("YYYY-MM-DD")

Use centralized date utilities.

Store dates consistently.

Avoid timezone ambiguity.

---

# Currency Rules

Never hardcode symbols.

Always derive currency from

Fund.currency

---

# Accounting Rules

Preserve double-entry accounting.

Journal entries must balance.

Never bypass validation.

Never modify historical financial records without audit.

---

# Logging Rules

Log

errors

warnings

important business events

Do not log sensitive information.

---

# Security Rules

Validate all input.

Sanitize output.

Never expose secrets.

Never hardcode credentials.

Use environment variables.

---

# Testing Rules

Every bug fix should include

Root Cause

Fix

Regression Prevention

Test manually before completion.

---

# Code Review Checklist

Confirm

✔ No duplicate logic

✔ Minimal file changes

✔ Existing patterns reused

✔ Validation added

✔ Errors handled

✔ No hardcoded values

✔ No unused imports

✔ No dead code

✔ No TypeScript errors

✔ No lint errors

---

# AI Rules

If requirements are unclear

STOP

Ask questions.

Do not invent business rules.

Do not assume accounting behavior.

Do not implement speculative features.

---

# Definition of Done

A task is complete only if

- Requirements satisfied
- Code compiles
- Existing functionality preserved
- No regressions introduced
- Documentation updated if required
- Review completed