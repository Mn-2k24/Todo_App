# Full-Stack-Consistency-Agent Skills

## validate_type_alignment

- Checks that frontend types match backend DTOs/models
- Blocks type mismatches between API contracts and client code
- Allows shared type definitions or generated types

## audit_error_symmetry

- Checks that backend error codes map to frontend error handling
- Blocks undefined error codes or unhandled cases
- Allows consistent error taxonomy across stack

## verify_auth_flow_consistency

- Checks that token handling is identical between frontend and backend
- Blocks mismatched auth headers or token formats
- Allows unified JWT flow with matching implementation

## enforce_data_flow_integrity

- Checks that data transformations are consistent (snake_case ↔ camelCase)
- Blocks inconsistent field naming between layers
- Allows standardized serialization/deserialization
