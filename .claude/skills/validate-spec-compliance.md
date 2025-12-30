---
name: validate-spec-compliance
agent: todo-spec-auditor
description: Validate that a spec.md file meets Spec-Driven Development standards and Todo App Phase I scope requirements
---

# Skill: Validate Spec Compliance

## Purpose
Ensure specification documents for Todo App Phase I features are complete, unambiguous, and properly scoped before proceeding to planning or implementation. Prevent scope creep and catch specification defects early.

## When to Use
- Immediately after creating or updating a spec.md file
- Before running `/sp.plan` to generate implementation plan
- When user requests explicit spec review
- During PR review when specs have been modified

## Inputs
- **Required**: `feature_name` (string) - Name of feature to audit (e.g., "create-todo", "list-todos")
- **Optional**: `spec_path` (string) - Direct path to spec.md file (defaults to `specs/<feature_name>/spec.md`)

## Step-by-Step Process

### Step 1: Locate and Read Specification
1. Construct spec file path: `specs/<feature_name>/spec.md`
2. Use `Read` tool to load spec.md contents
3. If file not found, report CRITICAL error and exit
4. Read project constitution: `.specify/memory/constitution.md`

### Step 2: Structural Validation
Verify presence of required sections (checklist):
- [ ] Feature title and identifier clearly stated
- [ ] User story in format: "As a [user], I want [goal], so that [benefit]"
- [ ] Acceptance criteria section with minimum 3 specific, testable criteria
- [ ] CLI command specification with syntax examples
- [ ] Success scenarios with expected CLI output
- [ ] Error scenarios with expected error messages
- [ ] Edge cases explicitly documented

**Failure**: If any required section is missing, classify as CRITICAL blocker.

### Step 3: Phase I Scope Analysis
For each requirement in the spec:
1. Check against Todo App Phase I definition (simple CRUD, local storage, no auth, no multi-user)
2. Flag requirements that introduce:
   - Database persistence beyond flat files/JSON
   - Network/API communication
   - User authentication or multi-user features
   - Complex querying or search beyond basic filters
   - Background tasks or scheduling
   - GUI/web interface (Phase I is CLI-only)
3. Document each scope violation with rationale

**Failure**: If scope leakage detected, classify as HIGH severity issue requiring spec revision.

### Step 4: Acceptance Criteria Quality Check
For each acceptance criterion:
1. Verify it is objectively testable (can write pass/fail test)
2. Check for ambiguous language: "should", "might", "could", "nice to have"
3. Ensure it specifies observable behavior, not implementation
4. Confirm it includes success condition and, where applicable, failure condition

**Failure**: If fewer than 3 criteria, or criteria are not testable, classify as CRITICAL blocker.

### Step 5: CLI Specification Verification
Check CLI command documentation:
1. Verify command syntax is complete: `todo <action> [options] [arguments]`
2. Check that all flags/options are documented with purpose
3. Ensure expected output format is shown (including example text)
4. Verify error cases specify exit codes and stderr messages
5. Confirm examples are provided for both success and error paths

**Failure**: If CLI behavior is ambiguous or incomplete, classify as HIGH severity.

### Step 6: Clarity and Ambiguity Detection
Scan spec text for:
- Vague terms: "user-friendly", "fast", "simple", "intuitive" (without measurable definition)
- Missing definitions of domain terms
- Undefined behaviors for edge cases (empty input, invalid data, etc.)
- Implicit assumptions not stated explicitly

**Failure**: If critical ambiguities found, classify as MODERATE, request clarification.

### Step 7: Constitution Alignment
1. Cross-reference spec requirements against constitution principles
2. Verify coding standards are respected (if implementation details mentioned)
3. Check that testing approach aligns with TDD mandate (if test strategy mentioned)
4. Ensure architectural patterns are consistent with constitution

**Failure**: If constitution violations found, classify severity based on principle violated.

### Step 8: Generate Audit Report
Structure findings in standard format:

```markdown
# Specification Audit Report: <feature_name>
**Date**: <YYYY-MM-DD>
**Spec File**: <path>
**Status**: ✅ PASS | ⚠️ WARNINGS | ❌ FAIL

## Executive Summary
<2-3 sentences: overall quality, key findings, recommendation>

## Critical Issues (BLOCKERS)
<List issues that MUST be fixed before proceeding to planning>
- **Missing Section**: <section_name> - <impact>
  - Recommendation: <specific action>

## High Severity Issues
<List issues that should be fixed but may not block planning>

## Scope Leakage Detected
<List requirements beyond Phase I scope>
- **Requirement**: <description> - Violates Phase I scope: <reason>
  - Recommendation: Remove or defer to Phase II

## Ambiguous Requirements
<List unclear specifications>
- **Requirement**: <text> - Ambiguity: <issue>
  - Clarification Needed: <specific question>

## Warnings (Improvements)
<List minor issues or suggestions>

## Positive Findings
<Acknowledge strengths of the spec>
- ✅ <specific good practice>

## Compliance Checklist
- [ ] User story present and well-formed
- [ ] 3+ testable acceptance criteria
- [ ] CLI behavior fully specified with examples
- [ ] Error cases documented
- [ ] No Phase I scope violations
- [ ] No critical ambiguities
- [ ] Constitution alignment verified

## Recommendations
1. <Highest priority action>
2. <Next action>
3. <Additional improvement>

## Decision
<GREEN: Ready for planning | YELLOW: Minor fixes recommended | RED: Rework required>
```

### Step 9: Determine Pass/Warn/Fail Status
- **FAIL (❌)**: Any CRITICAL issue present OR scope leakage detected OR <3 acceptance criteria
- **WARN (⚠️)**: No critical issues but 1+ HIGH or MODERATE issues identified
- **PASS (✅)**: All required sections present, criteria testable, no scope violations, minor issues only

## Output
Returns audit report (markdown format) with:
- Overall status: PASS/WARN/FAIL
- Categorized issues with severity and specific recommendations
- Compliance checklist results
- Actionable next steps for user

## Failure Handling

**If spec file not found**:
- Report: "CRITICAL: Spec file not found at `<path>`. Run `/sp.specify <feature>` first."
- Exit with error status

**If constitution.md not found**:
- Report: "WARNING: Constitution not found. Skipping constitution alignment check. Run `/sp.constitution` to create project principles."
- Continue with other validations

**If spec is completely empty or has only placeholders**:
- Report: "CRITICAL: Spec is incomplete or contains only template placeholders. Spec must be written before audit."
- Exit with FAIL status

**If multiple critical issues found**:
- List all critical issues in priority order
- Provide specific fix for each
- Set status to FAIL with clear rework requirements

## Success Criteria
- Skill completes in <30 seconds for typical spec (<2000 words)
- All findings reference specific line numbers or section headers
- Recommendations are actionable (user knows exactly what to fix)
- No false negatives (critical issues are never missed)
- Status determination is consistent and justified by evidence
