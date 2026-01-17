# API-Contract-Auditor Skills

## validate_rest_contracts

- Checks that endpoints have documented request/response schemas
- Blocks endpoints without explicit status codes and error responses
- Allows endpoints with complete OpenAPI-style contracts

## enforce_versioning_strategy

- Checks that API changes follow versioning rules (breaking vs non-breaking)
- Blocks breaking changes without version bumps
- Allows backward-compatible additions

## audit_error_responses

- Checks that all error codes (4xx, 5xx) are documented with examples
- Blocks error handling without client guidance
- Allows standardized error format across all endpoints

## verify_idempotency

- Checks that POST/PUT/DELETE operations define idempotency behavior
- Blocks state-mutating operations without retry safety documentation
- Allows operations with explicit idempotency keys or guarantees
