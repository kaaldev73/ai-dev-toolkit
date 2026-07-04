# Review Checklist

Use this checklist when reviewing any implementation, PR, or code change.

---

## Specification Compliance

- [ ] Change matches the specification (scope, requirements, acceptance criteria)
- [ ] No out-of-scope changes included
- [ ] All functional requirements addressed
- [ ] All non-functional requirements addressed
- [ ] Acceptance criteria verifiable

---

## Architecture

- [ ] No new frameworks or bundlers introduced
- [ ] Feature follows the 3-layer pattern (`*.supabase.js` / `*.service.js` / `*.view.js`)
- [ ] All HTTP calls go through `scripts/lib/api.js`
- [ ] No feature view imports another feature view directly
- [ ] No circular imports introduced
- [ ] `store.selectedFundId` used correctly for fund scoping

---

## API & Backend

- [ ] Required fields validated server-side (not only client-side)
- [ ] Multi-table writes are wrapped in transactions
- [ ] `requireAuth` middleware on all new routes
- [ ] Response shape is consistent with existing routes
- [ ] No raw SQL with user-supplied strings (use `$1, $2` parameterisation)
- [ ] No new CORS or security holes introduced

---

## Database

- [ ] Schema changes use safe `IF NOT EXISTS` patterns
- [ ] New tables have appropriate indexes
- [ ] Foreign keys are explicit where possible
- [ ] No hard-deletes of records referenced by journal `lines` JSONB
- [ ] No migration that could drop data

---

## Business Rules

- [ ] Capital call `paid_amount` is always additive (never replaced)
- [ ] Journal entries are always balanced (Σ debit = Σ credit)
- [ ] COA codes used in auto-entries exist in the `coa` table
- [ ] Fund context filters are applied to all queries
- [ ] Authentication not bypassed by any navigation or API call

---

## Code Quality

- [ ] No duplicate formatting functions introduced (check `investigations/DUPLICATE_CODE.md`)
- [ ] No hardcoded `₹` symbol
- [ ] Date handling uses consistent pattern (no mix of UTC and local)
- [ ] No `console.log` debug left in server routes
- [ ] Error handling is explicit (no silent catch blocks)
- [ ] No dead code or commented-out code

---

## Testing

- [ ] Happy path tested
- [ ] Edge cases tested (empty list, null values, boundary amounts)
- [ ] No regression in related features
- [ ] Manual test steps documented in review
