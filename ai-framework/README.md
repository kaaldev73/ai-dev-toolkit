# AI Engineering Framework

> A reusable AI-assisted Software Development Lifecycle (AI-SDLC) framework for building, maintaining, and scaling software projects with multiple AI models.

---

# Overview

The AI Engineering Framework provides a standardized workflow for AI-assisted software development.

It separates **project knowledge** from **AI development standards**, allowing the same framework to be reused across any software project.

The framework is designed to work with multiple AI models, where each model is assigned work based on its strengths.

Examples:

* ChatGPT → Architecture, planning, specifications, reviews
* Claude → Implementation, refactoring, repository investigation
* OpenRouter → Documentation, guides, release notes
* Gemini (optional) → Research and analysis

The framework itself is **project-agnostic** and contains no business-specific knowledge.

---

# Goals

* Standardize AI-assisted software development
* Separate reusable AI workflow from project-specific knowledge
* Improve implementation quality
* Reduce AI hallucinations
* Keep prompts short and consistent
* Prevent architectural drift
* Enable reusable development practices across projects

---

# Core Principles

* Architecture before implementation.
* Investigate before changing code.
* Every implementation requires an approved specification.
* Every implementation is reviewed.
* AI should augment engineering, not replace engineering judgment.
* Business rules belong to the project, not the framework.

---

# Repository Structure

```text
.ai-framework/

README.md

workflow.md

coding-rules.md

prompts/
templates/
standards/
checklists/
```

---

# Folder Overview

## workflow.md

Defines the AI Software Development Lifecycle.

Examples:

* Investigation
* Specification
* Implementation Plan
* Approval
* Implementation
* Review
* Testing
* Documentation
* Release

---

## coding-rules.md

Contains reusable engineering standards including:

* TypeScript rules
* Naming conventions
* Architecture principles
* Error handling
* Performance
* Security
* Validation
* Reusability

These rules apply across all software projects.

---

## prompts/

Reusable prompts for AI models.

Examples:

* session-start
* investigation
* implementation-plan
* implementation
* review
* documentation
* bugfix
* feature
* refactor
* release

---

## templates/

Reusable document templates.

Examples:

* Specification
* Investigation
* Review
* Feature
* Bug
* Test Plan
* Release Notes
* Changelog

---

## standards/

Reusable engineering standards.

Examples:

* API Standards
* Database Standards
* UI Standards
* Frontend Standards
* Backend Standards
* Security Standards
* Performance Standards

---

## checklists/

Quality checklists used during development.

Examples:

* Implementation Checklist
* Review Checklist
* Testing Checklist
* Release Checklist
* Security Checklist

---

# Project Integration

Each software project should contain its own project-specific AI knowledge.

Example:

```text
Project/

.ai/
.ai-framework/
```

The framework remains reusable.

The project folder contains project knowledge.

---

# Project AI Folder

The project should contain

```text
.ai/

project-context.md

project-rules.md

current-sprint.md

known-issues.md

architecture-notes.md

decisions.md
```

These files are **not reusable** and should remain project-specific.

---

# Development Workflow

```text
Issue

↓

Investigation

↓

Specification

↓

Implementation Plan

↓

Approval

↓

Implementation

↓

Review

↓

Testing

↓

Documentation

↓

Merge

↓

Release
```

No implementation should begin without an approved specification.

---

# AI Responsibilities

## ChatGPT

Responsible for:

* Architecture
* Planning
* Technical Specifications
* Root Cause Analysis
* Code Reviews
* Technical Decisions
* Documentation Strategy

---

## Claude

Responsible for:

* Repository Investigation
* Feature Implementation
* Refactoring
* Bug Fixes
* Test Generation
* Large Code Changes

---

## OpenRouter

Responsible for:

* Developer Documentation
* User Documentation
* API Documentation
* README Files
* Release Notes
* Tutorials
* Knowledge Base

---

# Framework Rules

The framework must never contain project-specific business logic.

It must remain reusable across any software project.

Only project repositories should define:

* Business rules
* Domain terminology
* Product workflows
* Sprint information
* Current priorities
* Architecture decisions unique to that project

---

# Versioning

Version the framework independently from the application.

Recommended versioning:

* Major → Breaking workflow changes
* Minor → New prompts, templates, or standards
* Patch → Documentation improvements and corrections

---

# Recommended Workflow

1. Create or update the project specification.
2. Investigate the affected area.
3. Produce an implementation plan.
4. Review and approve the plan.
5. Implement the change.
6. Review the implementation.
7. Test for regressions.
8. Generate documentation if required.
9. Merge the change.

---

# Philosophy

The framework is designed to help AI behave like a disciplined engineering team rather than a code generator.

It encourages:

* Small, well-defined tasks
* Architecture-first thinking
* Repeatable workflows
* Reusable standards
* Consistent engineering practices
* High-quality software delivery

The objective is not to replace software engineering—it is to make software engineering faster, more consistent, and more reliable through structured AI collaboration.
