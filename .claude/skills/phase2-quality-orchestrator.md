# Phase2-Quality-Orchestrator Skills

## orchestrate_compliance_review

- Checks that all required agents have been invoked for the current feature
- Blocks merge/deployment if any agent reported failures
- Allows progression when all agent audits pass

## validate_workflow_order

- Checks that spec → plan → tasks → implementation order was followed
- Blocks implementation that lacks approved specs
- Allows implementation only after spec approval

## enforce_adr_requirements

- Checks if architecturally significant decisions have ADRs
- Blocks changes to authentication, data models, or APIs without ADRs
- Allows changes when ADRs are present and approved

## coordinate_multi_agent_checks

- Checks that dependent agents (e.g., API + Auth auditors) ran together
- Blocks isolated checks when dependencies exist
- Allows coordinated audits for cross-cutting concerns
