## 2024-05-24 - [N+1 Query Anti-Pattern in Topic Priority Fetching]
**Learning:** Found a severe N+1 query problem where the application was iterating over all active topics and opening a *new database connection* per topic to execute three separate queries just to fetch the topic's subject priority. Creating new database connections inside a loop is a critical bottleneck in this architecture.
**Action:** Always check for `get_connection()` being called inside loops. Use `JOIN` queries to fetch related data in bulk using a single query and a single connection.
