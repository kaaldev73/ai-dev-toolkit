# Implementation Checklist

Use this checklist before marking any implementation task complete.

---

## Before Writing Code

- [ ] Read `ai/context.md`
- [ ] Read `ai/coding-rules.md`
- [ ] Read `ai/business-rules.md`
- [ ] Read the specification in `specifications/`
- [ ] Confirm the spec is Approved status
- [ ] Identify all files that will change
- [ ] Confirm no architecture changes are needed

---

## Investigation

- [ ] Root cause confirmed from code (not assumed)
- [ ] Affected files identified
- [ ] Dependent modules identified
- [ ] Database impact assessed
- [ ] API impact assessed

---

## Implementation

- [ ] Smallest possible change made
- [ ] No unrelated code modified
- [ ] No new dependencies added (unless spec requires)
- [ ] No bundler/build step introduced
- [ ] ES module imports use relative paths
- [ ] Fund context (`store.selectedFundId`) passed correctly
- [ ] All API calls go through `scripts/lib/api.js`
- [ ] snake_case used for all API request/response fields
- [ ] No hardcoded currency symbol `₹` (use fund.currency)
- [ ] No hardcoded GL codes in frontend

---

## Database

- [ ] Schema changes use `IF NOT EXISTS` / `DO $$ BEGIN IF NOT EXISTS`
- [ ] New indexes added for FK and JSONB columns
- [ ] No hard deletes on records referenced by journal lines
- [ ] `journal_id` foreign keys are FK-enforced or noted as risk

---

## API

- [ ] Server validates required fields
- [ ] Numbers coerced with `Number(x) || 0` pattern
- [ ] Multi-table writes use `BEGIN / COMMIT / ROLLBACK` transactions
- [ ] All routes use `requireAuth` middleware
- [ ] Response returns the affected record(s)

---

## Testing

- [ ] Tested the primary happy path
- [ ] Tested with missing/empty data
- [ ] Tested error state (API failure)
- [ ] No console errors in browser
- [ ] No regression in related features
- [ ] Browser refresh works
- [ ] Back/Forward navigation works (if route change)

---

## Code Quality

- [ ] No commented-out code left in
- [ ] No `console.log` debug statements in server routes
- [ ] No TODO left without a ticket reference
- [ ] Function names describe what they do
- [ ] No duplicate logic introduced (check `investigations/DUPLICATE_CODE.md`)

---

## Final Sign-off

- [ ] Specification acceptance criteria all met
- [ ] Review requested (if required by workflow)
