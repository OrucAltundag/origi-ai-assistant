# DECISION_LOG

## 2026-07-07
- Use built-in `sqlite3` for MVP persistence to minimize dependencies and complexity.
- Keep business logic in services and database operations in repositories.
- Require explicit `confirm=true` for delete endpoints to guard sensitive operations.
