# Auth-Integration-Auditor Skills

## validate_jwt_implementation

- Checks JWT signing algorithm, expiration, and secret management
- Blocks hardcoded secrets or weak algorithms (e.g., HS256 with public keys)
- Allows secure JWT patterns with environment-based secrets

## enforce_stateless_backend

- Checks that backend does not store user sessions
- Blocks server-side session storage or cookies
- Allows stateless authentication via JWT in headers

## audit_authorization_checks

- Checks that protected endpoints verify user ownership
- Blocks endpoints missing authorization guards (e.g., user A accessing user B's data)
- Allows endpoints with explicit ownership/permission checks

## verify_token_lifecycle

- Checks token refresh, expiration, and revocation strategy
- Blocks infinite-lived tokens or missing refresh flows
- Allows documented token rotation and expiry policies
