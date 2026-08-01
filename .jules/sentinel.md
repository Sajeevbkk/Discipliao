## 2024-08-01 - Prevent SQL Injection via string formatting
**Vulnerability:** Constructing SQL queries using `f-strings` and dynamically generated comma-separated `VALUES` (e.g., `VALUES {placeholders}`) can lead to SQL Injection, especially if inputs are improperly validated or handled upstream.
**Learning:** Even internal ID arrays must use parameterized queries to avoid any possibility of injection. PostgreSQL provides the `unnest()` function with array casting (`unnest(?::int[])`) which cleanly accepts a Python list mapped as a single parameter.
**Prevention:** Always use `unnest(?::type[])` to parameterize variable-length collections in `IN` clauses, `JOINs`, or `WITH` queries instead of interpolating strings or joining parameter marks.
