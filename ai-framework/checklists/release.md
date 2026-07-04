# Release Checklist

Use this checklist before every release.

---

## Pre-Release Verification

- [ ] All planned features and bug fixes are merged to `main`
- [ ] No open critical (P0) or high (P1) bugs in `planning/BACKLOG.md`
- [ ] `planning/CHANGELOG.md` updated with this release's changes
- [ ] Version number updated in `package.json`

---

## Database

- [ ] `server/schema.sql` is up to date with all table changes
- [ ] Schema has been applied to local PostgreSQL: `psql -d fundzflow -f server/schema.sql`
- [ ] Schema has been applied to Neon production DB: `DATABASE_URL=... psql -f server/schema.sql`
- [ ] No pending migrations left unapplied
- [ ] Existing data tested against new schema (no broken constraints)

---

## Environment

- [ ] `.env.example` updated if new environment variables were added
- [ ] `JWT_SECRET` is set and not the default dev value in production
- [ ] `SMTP_HOST` configured or intentionally left in simulation mode
- [ ] `DATABASE_URL` points to production Neon DB
- [ ] CORS `Access-Control-Allow-Origin` is restricted (not `*`) if public-facing

---

## Testing

- [ ] Login / logout tested
- [ ] Fund create and fund select tested
- [ ] Investor add and edit tested
- [ ] Capital call create, payment, and status update tested
- [ ] Journal entry create, edit, delete tested
- [ ] Bank transaction create and reconcile tested
- [ ] Distribution create tested
- [ ] NAV snapshot create tested
- [ ] Reports load without errors
- [ ] No JavaScript console errors on any page

---

## Documentation

- [ ] `docs/CHANGELOG.md` (or `planning/CHANGELOG.md`) updated
- [ ] Any new features documented in `docs/USER_GUIDE.md`
- [ ] Any new API endpoints documented in `investigations/API_MAP.md`
- [ ] Any new tables documented in `investigations/DATABASE_MAP.md`

---

## Post-Release

- [ ] Production server restarted
- [ ] Login works on production URL
- [ ] No error spike in server logs
- [ ] `planning/BACKLOG.md` updated — resolved items closed
