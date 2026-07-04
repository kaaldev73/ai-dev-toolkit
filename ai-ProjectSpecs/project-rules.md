# Business Rules

Project: [YOUR PROJECT NAME]

Version: 1.0

---

# Purpose

This document defines the business rules of [YOUR PROJECT NAME].

These rules are mandatory.

AI must never invent or modify business rules without explicit approval.

Domain correctness is more important than code simplicity.

---

# Core Principles

[YOUR PROJECT NAME] is a [domain type] platform.

Every operation must preserve:

- Data accuracy
- Data integrity
- Auditability
- Historical accuracy
- Referential integrity

---

# [Core Entity 1]

A [Entity 1] represents [description].

A [Entity 1] owns:

- [Child entity A]
- [Child entity B]
- [Child entity C]

Deleting a [Entity 1] must never silently delete historical records.

---

# [Core Entity 2]

Every [Entity 2] belongs to one or more [Entity 1]s.

Each [Entity 2] maintains:

- [Attribute A]
- [Attribute B]
- [Attribute C]

---

# [Core Workflow]

A [Workflow Event] triggers:

- [Step 1]
- [Step 2]
- [Step 3]
- [Step 4]

Changing [a workflow event] requires recalculating all dependent data.

---

# Derived Data

Derived data includes:

- [Derived entity A]
- [Derived entity B]

Derived data should be recalculated.

Never manually synchronize values.

---

# Data Integrity

[Primary records] should not be hard-deleted if referenced by other records.

Prefer:

Soft Delete

Inactive

Archived

over deletion.

---

# Audit Trail

Important operations should be traceable.

Every important change should record:

- Timestamp
- User
- Previous Value
- New Value

Never silently modify historical data.

---

# Transactions

Operations affecting multiple tables should use database transactions.

If one step fails, the entire operation should roll back.

---

# Currency / Units

[If applicable: describe how currency, units, or locale-sensitive values are handled.]

Never hardcode symbols or locale-specific formats.

Always derive formatting from a centralized configuration.

---

# Date Handling

Store dates consistently.

Avoid timezone ambiguity.

Historical dates must not change due to browser timezone.

---

# Validation

Validate:

Frontend

Backend

Database

Never rely on client validation alone.

---

# Reports / Derived Views

Reports are derived from source data.

Reports should never become the source of truth.

The database remains the source of truth.

---

# AI Rules

Never:

- Guess domain behavior.
- Assume business calculations.
- Change business rules without approval.
- Delete historical records.
- Hard-delete records referenced by other tables.
- Modify audit trails.

---

# Source of Truth

[Entity 1]
    ↓
[Entity 2]
    ↓
[Events / Transactions]
    ↓
[Reports / Derived Views]

Reports are generated from data.

Reports never own data.

---

# Current Known Risks

- [Risk 1]
- [Risk 2]
- [Risk 3]

These issues should be fixed without violating the business rules above.
