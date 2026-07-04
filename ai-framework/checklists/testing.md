# Testing Checklist

Use this checklist to cover key test scenarios systematically. Adapt the sections to your project's features.

> If your project has an automated test suite, run it first. Use this checklist for manual / exploratory coverage on top.

---

## Core Flows (run after every change)

### Authentication
- [ ] Login with valid credentials
- [ ] Login with invalid credentials — expect error
- [ ] Session or token expiry handled correctly
- [ ] Logout clears session and redirects to login

### [Feature Area 1 — e.g. User Management]
- [ ] Create a new [entity] with all required fields
- [ ] Create with missing required fields — expect validation error
- [ ] Edit [entity] and verify changes persist
- [ ] Delete / archive [entity] — behaves as expected
- [ ] List view updates correctly after any change

### [Feature Area 2 — e.g. Core Workflow]
- [ ] Trigger [primary workflow action]
- [ ] Workflow produces expected side effects (records created, emails sent, etc.)
- [ ] Invalid input is rejected at client and server
- [ ] Status / state updates correctly at each step

### [Feature Area 3 — e.g. Reporting / Derived Views]
- [ ] Report / view reflects latest data
- [ ] Filtering or pagination works correctly
- [ ] Empty state renders without errors

---

## Regression Checklist (run after routing, state, or layout changes)

- [ ] Navigating between pages does not break state
- [ ] Refresh on any route does not crash the page
- [ ] Direct URL access works when authenticated
- [ ] Browser back / forward navigation works correctly

---

## Edge Cases

- [ ] Empty list renders correctly — no blank page or JS error
- [ ] Large data sets display without overflow or truncation
- [ ] Negative or zero values handled where applicable
- [ ] Very long strings do not break layout
- [ ] Required fields with only whitespace rejected

---

## API / Network

- [ ] No 4xx or 5xx errors for normal operations in browser console
- [ ] Error messages returned from the server are meaningful
- [ ] Network failure shows a user-friendly error — not a crash

---

## Browser / Environment

- [ ] No uncaught JavaScript errors in the console after any operation
- [ ] Works correctly in target browsers
- [ ] Responsive layout holds up at target screen sizes (if applicable)

---

> **How to use this checklist:**
> Copy it into your project's `ai-ProjectSpecs/` folder and replace the placeholder sections with your real feature areas. Keep it updated as the application grows.
