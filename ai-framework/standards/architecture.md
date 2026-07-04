# Project Architecture

Version: 1.0

---

# Purpose

This document describes the overall architecture of [YOUR PROJECT NAME].

It is intended for developers, architects, and AI assistants.

---

# High-Level Architecture

> Replace this diagram with your actual stack.

                    Browser

                        │

               [Frontend Framework]

                        │

                [Data Fetching Layer]

                        │

                  REST / GraphQL API

                        │

              [Backend Framework]

                        │

                 Business Logic Layer

                        │

                 [ORM / Query Layer]

                        │

                  [Database]

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

- [Framework, e.g. React / Vue / Svelte]
- [Language, e.g. TypeScript]
- [Build tool, e.g. Vite]
- [Data fetching, e.g. TanStack Query / SWR]
- [UI library, e.g. shadcn/ui / Tailwind]

Responsibilities

- Rendering
- Forms
- Validation (client-side only)
- Navigation
- User Interaction

The frontend should not contain core domain logic.

---

# Backend

Technology

- [Framework, e.g. Express / Fastify / Django]
- [Language, e.g. TypeScript / Python]
- [ORM, e.g. Drizzle / Prisma / SQLAlchemy]

Responsibilities

- Business Rules
- Validation
- Authentication
- Authorization
- Database Operations

---

# Database

Technology

[Database, e.g. PostgreSQL / MySQL / SQLite]

Source of truth for

[List your main entities]

---

# Core Modules

> List the main feature areas of your application.

- [Module 1]
- [Module 2]
- [Module 3]
- Authentication

---

# Module Relationships

> Document the dependency chain between your core entities.

[Parent Entity]

↓

[Child Entity A]

↓

[Child Entity B]

↓

[Derived / Reporting Layer]

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

# Shared Utilities

Currency / Unit Formatting

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

Domain Accuracy

---

# Future Architecture

> List planned improvements or extensions.

- [Planned feature A]
- [Planned feature B]

---

# Source Documents

ai-ProjectSpecs/project-context.md

ai-ProjectSpecs/project-rules.md

ai-ProjectSpecs/project-map.md
