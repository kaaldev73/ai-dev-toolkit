# Testing Checklist

Fundzflow has no automated test suite. All testing is manual. Use this checklist to cover every test scenario systematically.

---

## Core Flows (run after every change)

### Authentication
- [ ] Login with valid credentials
- [ ] Login with invalid credentials (expect error)
- [ ] Session expires after 24 hours (or token tampered)
- [ ] Logout clears localStorage and redirects

### Fund Management
- [ ] Create a new fund with all required fields
- [ ] Create a fund with missing required fields (expect validation error)
- [ ] Select fund from fund list — all pages update to that fund's data
- [ ] Edit fund settings and verify changes persist
- [ ] Archive a fund — disappears from active list

### Investors
- [ ] Add a new investor — appears in investor list
- [ ] Add investor with invalid PAN (expect client-side error)
- [ ] Edit investor commitment
- [ ] Auto-created COA accounts appear after investor add (check COA tab)
- [ ] Archive investor

### Capital Calls
- [ ] Create capital call — drawdowns auto-created for all investors
- [ ] Due date before call date (expect validation error)
- [ ] Call % > 25 (expect validation error)
- [ ] Record payment for one investor — status updates to Partially Paid
- [ ] Record payment for all investors — status updates to Completed
- [ ] Journal entry auto-posted after payment (check Journal tab)
- [ ] Bank transaction auto-posted after payment (check Banking tab)
- [ ] Bank account balance increases after payment

### Journal
- [ ] Create balanced journal entry — posts successfully
- [ ] Create unbalanced entry (Σ debit ≠ Σ credit) — expect error
- [ ] Edit journal entry where amount changes — drawdown paid_amount updates
- [ ] Delete journal entry — bank transaction removed, drawdown reverted
- [ ] Void journal entry — appears as voided, not deleted
- [ ] Duplicate entry — new entry created with today's date
- [ ] Reverse entry — new entry with flipped debit/credit

### Banking
- [ ] Create bank account with opening balance
- [ ] Record Credit transaction — balance increases
- [ ] Record Debit transaction — balance decreases
- [ ] Mark transaction reconciled
- [ ] Ledger view shows correct running totals

### COA
- [ ] Add COA account with unique code
- [ ] Add COA account with duplicate code — expect error
- [ ] Edit COA account name inline
- [ ] Ledger view reflects updated account name

### Distributions
- [ ] Create Distribution type — journal DR Partner Capital / CR Bank
- [ ] Create Dividend type — journal DR Bank / CR Dividend Income
- [ ] Create Interest type — journal DR Bank / CR Interest Income

---

## Regression Checklist (after any routing or store change)

- [ ] Fund selector in header updates all pages
- [ ] Dashboard KPIs reflect the selected fund
- [ ] Back/Forward browser navigation works
- [ ] Refresh on any route does not break the page
- [ ] Direct URL access (`#/capital-calls`) works when logged in

---

## Edge Cases

- [ ] Fund with zero investors — capital call creates no drawdowns
- [ ] Investor with zero commitment — excluded from drawdowns
- [ ] Empty investor list renders correctly (no blank page / JS error)
- [ ] Large amounts (₹10 Cr+) format without overflow
- [ ] Negative amounts rejected at client and server
- [ ] Date fields with no input show correct validation message

---

## Browser Console

- [ ] No uncaught errors after any operation
- [ ] No 4xx or 5xx API errors for normal operations
- [ ] No failed network requests
