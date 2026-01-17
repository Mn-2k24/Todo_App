# Spec-Auditor-Agent Skills

## validate_acceptance_criteria

- Checks that every feature has measurable acceptance criteria
- Blocks specs with vague requirements like "good performance"
- Allows specs with quantified criteria (e.g., "< 200ms response time")

## verify_error_scenarios

- Checks that error cases, edge cases, and failure modes are documented
- Blocks specs missing "What could go wrong?" sections
- Allows specs with explicit error taxonomy and handling

## audit_spec_completeness

- Checks for required sections: scope, out-of-scope, dependencies, NFRs
- Blocks incomplete specs missing mandatory sections
- Allows specs that follow constitution template

## detect_scope_creep

- Checks for feature additions not in original spec
- Blocks implementation of undocumented features
- Allows work only within approved spec boundaries
