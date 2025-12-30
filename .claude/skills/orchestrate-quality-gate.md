---
name: orchestrate-quality-gate
agent: phase1-quality-orchestrator
description: Execute comprehensive quality validation across all SDD artifacts (constitution, spec, plan, tasks) for Todo App Phase I feature before implementation or commit
---

# Skill: Orchestrate Quality Gate

## Purpose
Serve as the final quality checkpoint before feature implementation or code commit by validating all Spec-Driven Development artifacts in dependency order. Coordinate specialized quality agents, aggregate findings, and make submission-readiness determination for Todo App Phase I features.

## When to Use
- After completing `/sp.specify`, `/sp.plan`, and `/sp.tasks` workflow for a feature
- Before running `/sp.implement` to begin implementation
- Before creating a pull request with spec changes
- When user explicitly requests quality validation: "validate my specs", "check if ready to implement"
- After major spec/plan revisions to verify improvements

## Inputs
- **Required**: `feature_name` (string) - Name of feature to validate (e.g., "create-todo", "list-todos")
- **Optional**: `scope` (string) - Validation scope: "full" (default), "spec-only", "plan-only", "tasks-only"
  - Use "spec-only" after initial spec creation
  - Use "full" before implementation begins

## Step-by-Step Process

### Step 1: Initialization and Context Loading
1. **Verify feature context**:
   - Check that `specs/<feature_name>/` directory exists
   - If not found, report ERROR and exit
2. **Load project constitution**:
   - Read `.specify/memory/constitution.md`
   - If constitution missing or incomplete (has placeholders), report CRITICAL blocker: "Constitution required. Run `/sp.constitution` first."
   - Extract Phase I scope definition and quality standards from constitution
3. **Determine validation targets based on scope**:
   - `full`: Validate constitution → spec → plan → tasks
   - `spec-only`: Validate constitution → spec
   - `plan-only`: Validate constitution → spec → plan
   - `tasks-only`: Validate constitution → spec → plan → tasks
4. **Initialize tracking structure**:
   ```json
   {
     "feature": "<feature_name>",
     "timestamp": "<ISO-8601>",
     "validations": {
       "constitution": {"status": "pending", "issues": []},
       "spec": {"status": "pending", "issues": []},
       "plan": {"status": "pending", "issues": []},
       "tasks": {"status": "pending", "issues": []}
     },
     "overall_status": "pending",
     "blockers": [],
     "warnings": [],
     "next_steps": []
   }
   ```

### Step 2: Constitution Validation
**Purpose**: Verify project constitution is complete and actionable (foundation for all other validations)

1. **Structural check**:
   - Required sections: Core Principles (3+ principles), Code Standards, Testing Philosophy, Performance Requirements, Security Guidelines, Architecture Patterns
   - Each principle must have: Name, Description, Measurable criteria, Examples
2. **Completeness check**:
   - No placeholder text: `{{PLACEHOLDER}}`, `[TODO]`, `[EXAMPLE]`, `[DESCRIPTION]`
   - Each principle has concrete, Todo App-specific examples (not generic)
   - Phase I scope is explicitly defined (what's in, what's deferred)
3. **Quality check**:
   - Principles are measurable and actionable (developer can verify compliance)
   - Examples are concrete (code snippets, command examples, specific patterns)
   - No generic platitudes ("write clean code", "be agile")

**Record findings**:
- CRITICAL: Missing sections, placeholders in key principles, Phase I undefined
- MODERATE: Vague principles, missing examples
- PASS: All sections present, concrete and actionable

**Status determination**:
- FAIL: Any CRITICAL issue
- WARN: MODERATE issues only
- PASS: No issues or only MINOR suggestions

**Exit early if FAIL**: Report constitution blocker, recommend `/sp.constitution` revision, skip remaining validations

### Step 3: Specification Validation
**Purpose**: Ensure feature spec is complete, unambiguous, and properly scoped for Phase I

**Delegate to specialist**: Launch `todo-spec-auditor` agent with `validate-spec-compliance` skill
1. Use `Task` tool to invoke `todo-spec-auditor` agent:
   ```
   Task: "Execute validate-spec-compliance skill for feature '<feature_name>'"
   ```
2. Wait for audit report from specialist agent
3. Parse report findings:
   - Extract status: PASS/WARN/FAIL
   - Extract critical issues (blockers)
   - Extract high/moderate issues (warnings)
   - Extract scope leakage detections
4. **Aggregate findings into tracking structure**:
   - Add critical issues to `blockers[]`
   - Add high/moderate issues to `warnings[]`
   - Record spec validation status

**Status determination**:
- FAIL: Spec auditor returned FAIL status
- WARN: Spec auditor returned WARN status
- PASS: Spec auditor returned PASS status

**Exit early if FAIL**: Report spec blockers, skip plan/tasks validation (dependencies invalid)

### Step 4: Plan Validation
**Purpose**: Verify architectural plan addresses all required dimensions and documents decisions

**Validation checks** (orchestrator performs directly):
1. **Required sections present**:
   - [ ] Scope & Dependencies (in-scope, out-of-scope, external dependencies)
   - [ ] Key Decisions & Rationale (options considered, tradeoffs, rationale)
   - [ ] Interfaces & API Contracts (inputs, outputs, errors)
   - [ ] Non-Functional Requirements (performance, reliability, security)
   - [ ] Data Management (schema, migration, retention)
   - [ ] Operational Readiness (observability, alerting, deployment)
   - [ ] Risk Analysis (top risks, mitigation strategies)
   - [ ] Evaluation Criteria (definition of done)

2. **Decision documentation quality**:
   - Each architectural decision has documented alternatives
   - Tradeoffs are explicitly stated with pros/cons
   - Rationale references constitution principles or spec requirements
   - No unexplained "we will use X" statements

3. **ADR suggestions check**:
   - Verify plan mentions ADR creation for significant decisions
   - If plan makes architectural choices without ADR suggestion, flag as WARNING

4. **Interface specifications**:
   - CLI commands fully specified (syntax, options, arguments)
   - Expected outputs documented (success and error cases)
   - Error taxonomy defined (exit codes, error messages)

5. **Phase I compliance**:
   - No advanced features beyond constitution Phase I scope
   - Storage solutions are simple (files, JSON, CSV - no databases)
   - No networking, authentication, or multi-user features
   - No complex dependencies or frameworks

**Record findings**:
- CRITICAL: Missing required sections, architectural decisions without rationale, Phase I violations
- HIGH: Incomplete interface specs, missing risk mitigation
- MODERATE: ADR suggestions missing, minor completeness gaps

**Status determination**:
- FAIL: Any CRITICAL issue
- WARN: HIGH or MODERATE issues
- PASS: All sections present and complete

**Exit early if FAIL**: Report plan blockers, skip tasks validation (implementation guidance invalid)

### Step 5: Tasks Validation
**Purpose**: Verify task breakdown is granular, testable, and dependency-ordered

**Validation checks** (orchestrator performs directly):
1. **Task structure**:
   - Each task has: Description, Acceptance Criteria, Test Cases, Dependencies
   - Tasks are small enough for single-session completion (<4 hours estimated)
   - Dependencies are explicit (task X requires task Y to be completed first)

2. **Acceptance criteria quality**:
   - Each criterion is testable (can write pass/fail test)
   - Criteria specify observable behavior, not implementation
   - Success and failure conditions are both defined

3. **Test cases**:
   - Each task has explicit red/green test expectations
   - Test cases are concrete (input → expected output)
   - Edge cases are covered in test suite

4. **Dependency ordering**:
   - Tasks are listed in implementation order
   - No circular dependencies
   - Foundation tasks (data models, core logic) come before UI tasks

5. **Coverage check**:
   - All spec acceptance criteria are covered by tasks
   - All plan components have corresponding implementation tasks
   - No orphan tasks unrelated to spec/plan

**Record findings**:
- CRITICAL: Missing test cases, circular dependencies, spec requirements not covered
- HIGH: Tasks too large (>4 hours), vague acceptance criteria
- MODERATE: Minor dependency ordering issues, missing edge case tests

**Status determination**:
- FAIL: Any CRITICAL issue
- WARN: HIGH or MODERATE issues
- PASS: All tasks well-defined and testable

### Step 6: Cross-Artifact Consistency Check
**Purpose**: Ensure spec, plan, and tasks are aligned and mutually consistent

1. **Spec ↔ Plan alignment**:
   - All spec functional requirements addressed in plan
   - Plan decisions are justified by spec constraints or NFRs
   - No plan components that contradict spec

2. **Plan ↔ Tasks alignment**:
   - All plan components have implementation tasks
   - Tasks reference plan sections they implement
   - No tasks implementing features not in plan

3. **Spec ↔ Tasks alignment**:
   - All spec acceptance criteria have corresponding task test cases
   - Task deliverables satisfy spec requirements
   - No tasks beyond spec scope

**Record findings**:
- CRITICAL: Spec requirements missing from tasks, plan contradicts spec
- HIGH: Tasks implement features not in spec (gold-plating)
- MODERATE: Minor naming inconsistencies across artifacts

### Step 7: Aggregate Quality Assessment
**Purpose**: Synthesize findings and make final submission-readiness determination

1. **Count issues by severity**:
   - Critical: <count>
   - High: <count>
   - Moderate: <count>
   - Minor: <count>

2. **Apply decision framework**:
   - **GREEN (Submission-Ready)**:
     - Zero critical issues
     - Zero high-severity issues
     - Moderate issues ≤2 and documented
     - All artifact validations passed
     - Cross-artifact consistency verified

   - **YELLOW (Needs Minor Corrections)**:
     - Zero critical issues
     - High-severity issues ≤2 and have mitigation path
     - Moderate issues ≤5
     - Core structure is sound, fixes don't require redesign

   - **RED (Requires Rework)**:
     - Any critical issues present
     - High-severity issues >2
     - Structural problems require architectural changes
     - Spec/plan/tasks misalignment

3. **Generate recommendation**:
   - GREEN → "Ready to proceed with `/sp.implement`"
   - YELLOW → "Address listed issues, then proceed"
   - RED → "Rework required before implementation"

### Step 8: Generate Comprehensive Quality Gate Report
**Structure findings**:

```markdown
# Quality Gate Report: <feature_name>
**Date**: <YYYY-MM-DD HH:MM:SS>
**Scope**: <full|spec-only|plan-only|tasks-only>
**Overall Status**: 🟢 GREEN | 🟡 YELLOW | 🔴 RED

## Executive Summary
<2-3 sentences: overall readiness, critical findings, recommendation>

---

## Validation Results

### ✓ Constitution Validation
**Status**: <PASS|WARN|FAIL>
<Summary of constitution quality>
- Issues: <count by severity>
- Details: <if WARN or FAIL, list issues>

### ✓ Specification Validation (via todo-spec-auditor)
**Status**: <PASS|WARN|FAIL>
**Spec File**: `specs/<feature>/spec.md`
- Required Sections: <✓ or ✗>
- Acceptance Criteria: <count> (<✓ testable | ✗ vague>)
- Phase I Compliance: <✓ or ✗>
- Scope Leakage: <count violations>

**Critical Issues**:
<List from spec auditor>

**Warnings**:
<List from spec auditor>

### ✓ Plan Validation
**Status**: <PASS|WARN|FAIL>
**Plan File**: `specs/<feature>/plan.md`
- Required Sections: <X/8 complete>
- Architectural Decisions: <count> (<documented rationale: ✓|✗>)
- ADR Suggestions: <✓ present | ✗ missing>
- Phase I Compliance: <✓ or ✗>

**Issues**:
<List issues by severity>

### ✓ Tasks Validation
**Status**: <PASS|WARN|FAIL>
**Tasks File**: `specs/<feature>/tasks.md`
- Total Tasks: <count>
- Tasks with Test Cases: <count> (<✓ all | ⚠️ some | ✗ none>)
- Dependency Ordering: <✓ valid | ✗ issues>
- Spec Coverage: <✓ complete | ✗ gaps>

**Issues**:
<List issues by severity>

### ✓ Cross-Artifact Consistency
**Status**: <PASS|WARN|FAIL>
- Spec ↔ Plan: <✓ aligned | ✗ conflicts>
- Plan ↔ Tasks: <✓ aligned | ✗ gaps>
- Spec ↔ Tasks: <✓ aligned | ✗ missing coverage>

**Issues**:
<List alignment issues>

---

## Issue Summary

### 🚨 Critical Blockers (<count>)
<List critical issues with file:section references>
1. [CRITICAL] <file> - <issue>
   - Recommendation: <fix>

### ⚠️ High Severity (<count>)
<List high-severity issues>

### ℹ️ Moderate Severity (<count>)
<List moderate issues>

### 💡 Minor Suggestions (<count>)
<List minor improvements>

---

## Submission Readiness Decision

**Status**: 🟢 GREEN | 🟡 YELLOW | 🔴 RED

**Justification**:
<Explain why this status was assigned based on issue counts and severity>

**Next Steps**:
<If GREEN>
1. ✅ Proceed with implementation using `/sp.implement`
2. Create ADRs for significant architectural decisions (if applicable)
3. Monitor for scope creep during implementation

<If YELLOW>
1. ⚠️ Address <count> high-severity issues listed above
2. Review and fix moderate issues if time permits
3. Re-run quality gate after corrections: `/orchestrate-quality-gate <feature>`
4. Once issues resolved, proceed with `/sp.implement`

<If RED>
1. 🔴 STOP: Do not proceed with implementation
2. Address all <count> critical blockers immediately
3. Revise affected artifacts: <list files needing rework>
4. Re-run quality gate after major revisions
5. Consider running `/sp.clarify` if requirements are unclear

---

## Quality Metrics
- Total Issues: <count>
- Critical: <count> | High: <count> | Moderate: <count> | Minor: <count>
- Artifacts Validated: <count>/4 (constitution, spec, plan, tasks)
- Pass Rate: <percentage>%

## Validation Audit Trail
- Constitution: <timestamp> - <status>
- Spec (via todo-spec-auditor): <timestamp> - <status>
- Plan: <timestamp> - <status>
- Tasks: <timestamp> - <status>
- Cross-Artifact Check: <timestamp> - <status>

**Report Generated**: <YYYY-MM-DD HH:MM:SS>
```

### Step 9: Delegation Recommendations
**If YELLOW or RED status**:
1. Identify which specialist agents should be invoked for fixes:
   - Spec issues → Recommend re-running `/sp.specify` or using `todo-spec-auditor`
   - Plan issues → Recommend re-running `/sp.plan`
   - Tasks issues → Recommend re-running `/sp.tasks`
   - Constitution issues → Recommend `/sp.constitution` revision

2. Provide specific guidance for each recommended fix:
   - What file to update
   - What section needs attention
   - What the acceptance criteria for the fix is

### Step 10: Post-Validation Actions
1. **Log validation event**:
   - Create entry in `.specify/memory/quality-gate-log.jsonl` (append-only log):
     ```json
     {"feature":"<name>","timestamp":"<ISO>","status":"<GREEN|YELLOW|RED>","critical":<n>,"high":<n>,"moderate":<n>}
     ```
   - If log file doesn't exist, create it with first entry

2. **Update feature metadata** (if exists):
   - If `specs/<feature>/meta.json` exists, update `last_validation` field
   - Add validation status and timestamp

3. **Return final report to user**

## Output
Returns comprehensive quality gate report (markdown format) with:
- Overall readiness status: GREEN/YELLOW/RED with justification
- Per-artifact validation results (constitution, spec, plan, tasks)
- Categorized issues with severity and specific recommendations
- Cross-artifact consistency findings
- Prioritized next steps
- Delegation recommendations for fixes
- Quality metrics summary

## Failure Handling

**If feature directory doesn't exist**:
- Report: "ERROR: Feature directory not found at `specs/<feature>/`. Create spec first using `/sp.specify <feature>`."
- Exit with error status

**If constitution is missing or incomplete**:
- Report: "CRITICAL BLOCKER: Constitution required for quality validation. Run `/sp.constitution` to create project principles."
- Set overall status to RED
- Skip other validations
- Return report with constitution blocker

**If spec file missing (in full or spec-only scope)**:
- Report: "CRITICAL BLOCKER: Spec file not found at `specs/<feature>/spec.md`. Run `/sp.specify <feature>` first."
- Set status to RED, exit

**If plan file missing (in full or plan-only scope)**:
- Report: "CRITICAL BLOCKER: Plan file not found. Run `/sp.plan` for feature."
- Set status to RED, exit

**If tasks file missing (in full or tasks-only scope)**:
- Report: "CRITICAL BLOCKER: Tasks file not found. Run `/sp.tasks` for feature."
- Set status to RED, exit

**If specialist agent (todo-spec-auditor) fails**:
- Report: "ERROR: Spec validation agent failed. Review spec manually or retry."
- Mark spec validation as FAIL
- Continue with other validations
- Set overall status to at least YELLOW

**If validation times out (>5 minutes)**:
- Report: "WARNING: Validation timeout. Feature may be too large. Consider breaking into smaller features."
- Return partial results
- Set status to YELLOW

## Success Criteria
- Skill completes in <2 minutes for typical feature (full scope)
- All artifact validations are thorough (no false negatives)
- Status determination (GREEN/YELLOW/RED) is consistent and evidence-based
- Next steps are specific and actionable
- Report provides clear go/no-go decision for implementation
- Delegation recommendations identify right specialist agents
- Quality metrics are accurate and complete
