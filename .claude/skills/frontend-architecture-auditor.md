# Frontend-Architecture-Auditor Skills

## validate_component_structure

- Checks that components follow single-responsibility principle
- Blocks components exceeding 200 lines or handling multiple concerns
- Allows focused, reusable components

## enforce_state_management

- Checks that global state is managed via context or state library
- Blocks prop drilling beyond 2 levels
- Allows centralized state for shared data

## audit_api_integration

- Checks that API calls are typed and handle errors gracefully
- Blocks untyped fetch calls or missing error states
- Allows typed API clients with loading/error states

## verify_type_safety

- Checks that TypeScript strict mode is enabled and no `any` types used
- Blocks loose type definitions
- Allows explicit, narrow types throughout codebase
