# Security Checklist

Run this checklist on any change that touches auth, API endpoints, database queries, or user input.

---

## Authentication & Authorisation

- [ ] All new API routes use `requireAuth` middleware
- [ ] JWT secret is never logged or exposed in responses
- [ ] Role checks applied where required (SuperAdmin-only routes)
- [ ] No route allows bypassing the authentication guard
- [ ] Client-side auth check (`isAuthenticated()`) is not the only guard — server also validates

---

## Input Validation

- [ ] All user-supplied strings are passed as parameterised query values (`$1`, `$2`) — never concatenated into SQL
- [ ] Numeric fields coerced and validated server-side (not only client-side)
- [ ] File upload types and sizes validated (if applicable)
- [ ] Enum fields validated against allowed values server-side
- [ ] Dates validated as valid date strings before DB insert

---

## Sensitive Data

- [ ] `.env` is in `.gitignore` and never committed
- [ ] No credentials, tokens, or secrets hardcoded in any file
- [ ] `password_hash` never returned in API responses (only selected non-sensitive fields)
- [ ] PAN, CKYC, and bank details handled with appropriate care
- [ ] `audit_log` entries do not capture full request bodies (which may contain passwords)

---

## API Security

- [ ] No endpoint accepts raw SQL from the client
- [ ] No endpoint exposes another fund's data (all queries filter by `fund_id` from the authenticated context)
- [ ] CORS is restricted to known origins in production (not `*`)
- [ ] Rate limiting considered for auth endpoints (`POST /api/auth/login`, `POST /api/auth/signup`)
- [ ] Error responses do not leak stack traces or internal query details

---

## Database

- [ ] No `DELETE` without a `WHERE` clause
- [ ] Multi-step operations use transactions so partial writes don't corrupt data
- [ ] No unrestricted `SELECT *` on tables containing credentials or sensitive data

---

## Dependencies

- [ ] No new `npm` packages with known CVEs (check `npm audit`)
- [ ] No packages that make outbound network requests without explicit need
