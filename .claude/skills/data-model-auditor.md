# Data-Model-Auditor Skills

## validate_schema_correctness

- Checks that models match database schemas and TypeScript types
- Blocks mismatched types between backend and frontend
- Allows consistent type definitions across stack

## enforce_data_isolation

- Checks that queries filter by user/tenant ID for multi-tenant data
- Blocks queries that could leak cross-user data
- Allows queries with explicit ownership filters

## audit_migration_safety

- Checks that schema changes include rollback plans
- Blocks destructive migrations without backups
- Allows migrations with forward/backward compatibility

## verify_data_validation

- Checks that required fields, constraints, and foreign keys are enforced
- Blocks models without validation logic
- Allows models with explicit validation rules
