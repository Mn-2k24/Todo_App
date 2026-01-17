# Backend-Code-Quality-Agent Skills

## enforce_clean_architecture

- Checks separation of concerns (routes, services, models, utils)
- Blocks business logic in route handlers
- Allows layered architecture with clear boundaries

## audit_error_handling

- Checks that errors are caught, logged, and returned with appropriate codes
- Blocks unhandled promise rejections or swallowed errors
- Allows try-catch blocks with meaningful error responses

## validate_code_clarity

- Checks for clear function names, minimal complexity, no magic numbers
- Blocks deeply nested code or functions exceeding 50 lines
- Allows readable, self-documenting code

## verify_test_coverage

- Checks that new features have unit/integration tests
- Blocks untested business logic
- Allows code with meaningful test cases
