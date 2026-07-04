# FundzFlow Architecture

Version: 1.0

---

# Purpose

FundzFlow is a fund administration platform for Private Equity and Venture Capital funds.

This document describes the overall architecture of the system.

It is intended for developers, architects and AI assistants.

---

# High-Level Architecture

                    Browser

                        │

               React + TypeScript

                        │

                TanStack Query

                        │

                  REST API

                        │

              Express + TypeScript

                        │

                 Business Layer

                        │

                 Drizzle ORM

                        │

                  PostgreSQL

---

# Architecture Principles

The application follows a layered architecture.

UI

↓

API

↓

Business Logic

↓

Data Access

↓

Database

Every layer has a single responsibility.

---

# Frontend

Technology

- React
- TypeScript
- Vite
- TanStack Query
- Radix UI
- shadcn/ui

Responsibilities

- Rendering
- Forms
- Validation
- Navigation
- User Interaction

The frontend should not contain accounting logic.

---

# Backend

Technology

- Express
- TypeScript
- Drizzle ORM

Responsibilities

- Business Rules
- Validation
- Authentication
- Authorization
- Database Operations

---

# Database

Technology

PostgreSQL

Source of truth for

Funds

Investors

Capital Calls

COA

Journal Entries

Banking

Reports

---

# Core Modules

Funds

Investor Management

Capital Calls

Distributions

Chart of Accounts

Journal Entries

Banking

Capital Accounts

Reporting

Documents

Management Fees

Authentication

---

# Module Relationships

Funds

↓

Investors

↓

Capital Calls

↓

Drawdowns

↓

Journal Entries

↓

Bank Transactions

↓

Reports

---

# Data Flow

User

↓

Frontend

↓

API

↓

Business Logic

↓

Database

↓

API Response

↓

Frontend

---

# Business Principles

Double-entry accounting.

Auditability.

Historical integrity.

No silent data modification.

No duplicated business logic.

---

# Shared Utilities

Currency Formatting

Date Formatting

Number Formatting

Validation

Logging

Error Handling

---

# Development Workflow

Investigation

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

---

# Design Goals

Maintainability

Scalability

Readability

Performance

Security

Financial Accuracy

---

# Future Architecture

Service Layer

Background Jobs

Notification Queue

Audit Trail

Approval Workflow

Report Engine

Document Engine

Permission Engine

---

# Source Documents

ai/context.md

ai/business-rules.md

planning/BACKLOG.md

specifications/

investigations/