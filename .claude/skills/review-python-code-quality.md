---
name: review-python-code-quality
agent: todo-code-quality-agent
description: Review Python code for Todo App Phase I to ensure architectural quality, maintainability, and adherence to clean code principles
---

# Skill: Review Python Code Quality

## Purpose
Analyze Python implementation code for Todo App Phase I features to identify architectural weaknesses, complexity hotspots, naming issues, and code duplication. Provide actionable refactoring recommendations that preserve functional requirements while improving maintainability.

## When to Use
- After implementing a new feature module (e.g., TodoService, TaskRepository)
- After completing CRUD operations for a domain entity
- Before committing code changes for PR
- After refactoring to verify improvements maintain quality
- When completing tasks from `specs/<feature>/tasks.md`

## Inputs
- **Required**: `target` (string) - File path, module name, or directory to review
  - Examples: `"src/todo_service.py"`, `"src/repositories/"`, `"TodoList"`
- **Optional**: `feature_context` (string) - Feature name to load related spec for alignment check
  - Example: `"create-todo"` → reads `specs/create-todo/spec.md`

## Step-by-Step Process

### Step 1: Context Gathering
1. Resolve target to specific Python file(s):
   - If file path provided: use `Read` tool on that file
   - If directory provided: use `Glob` to find all `*.py` files in directory
   - If module/class name: use `Grep` to locate definition, then read file
2. Read project constitution: `.specify/memory/constitution.md` for code standards
3. If `feature_context` provided, read `specs/<feature_context>/spec.md` to understand requirements
4. Note: Exclude test files (`test_*.py`, `*_test.py`) from architecture review (focus on production code)

### Step 2: Separation of Concerns Analysis
For each Python file:
1. **Identify layers**: Determine if code is presentation (CLI), business logic (services), or data access (repositories)
2. **Check layering violations**:
   - CLI code should NOT contain business logic (calculations, validations, transformations)
   - Business logic should NOT contain data access code (file I/O, database queries)
   - Data access should NOT contain business rules
3. **Verify Single Responsibility Principle**:
   - Each class should have one reason to change
   - Flag classes handling multiple concerns (e.g., TodoService that also manages file I/O)
4. **Check dependency direction**: High-level modules should not depend on low-level modules (flag violations)

**Flag as CRITICAL**: Database queries in CLI code, business logic mixed with I/O, god classes

### Step 3: Function Responsibility Assessment
For each function/method:
1. **Line count check**: Flag functions >30 lines as potentially too complex
2. **Abstraction level check**: Verify function operates at single level of abstraction (no mixing high-level logic with low-level details)
3. **Parameter count**: Flag functions with >4 parameters (suggest parameter object or builder)
4. **Cyclomatic complexity** (estimate):
   - Count decision points: if, elif, for, while, and, or, except
   - Flag functions with >10 decision points as high complexity
5. **Side effect detection**: Identify functions that both query and command (violate CQS)

**Flag as MODERATE**: Functions 30-50 lines, >4 parameters, complexity 10-15
**Flag as CRITICAL**: Functions >50 lines or complexity >15

### Step 4: Naming Convention Enforcement
Scan code for PEP 8 compliance:
1. **Functions/methods**: Must be `snake_case` (flag PascalCase or camelCase)
2. **Classes**: Must be `PascalCase` (flag snake_case)
3. **Constants**: Must be `UPPER_CASE` (module-level immutables)
4. **Private members**: Should start with `_` (flag public members that should be private)
5. **Clarity check**:
   - Flag abbreviations: `todo_mgr`, `usr`, `tmp` (prefer `todo_manager`, `user`, `temporary`)
   - Flag vague names: `data`, `info`, `handle`, `process` (too generic)
   - Flag single-letter names outside loop counters
6. **Boolean naming**: Check boolean variables/functions use `is_`, `has_`, `can_` prefix

**Flag as MODERATE**: Naming convention violations, unclear names

### Step 5: Code Duplication Detection
1. **Identify repeated patterns**:
   - Look for similar code blocks (>5 lines) across functions
   - Flag copy-paste patterns that differ only in variable names or literals
2. **Check for extractable logic**:
   - Similar validation logic → extract to validator function
   - Repeated error handling → extract to decorator or utility
   - Similar transformations → extract to mapper/transformer
3. **Calculate duplication severity**:
   - >10 lines duplicated = MODERATE
   - >20 lines duplicated = HIGH
   - Duplicated business logic = CRITICAL

**Flag as CRITICAL**: Business logic duplicated across modules
**Flag as MODERATE**: Utility code duplicated >10 lines

### Step 6: Complexity Hotspot Analysis
1. **Nesting depth check**: Flag code with >3 levels of indentation (suggest extraction or early returns)
2. **Conditional complexity**: Flag long if-elif chains (>5 branches) or deeply nested conditionals
3. **Class complexity**: Flag classes with >10 methods or >200 lines (potential god class)
4. **Module complexity**: Flag modules with >500 lines (suggest splitting)

**Flag as HIGH**: Nesting >4 levels, if-elif >7 branches, classes >300 lines

### Step 7: Todo App Phase I Specific Checks
1. **CLI Simplicity**: Verify CLI code uses argparse or simple sys.argv (no complex frameworks)
2. **Storage Simplicity**: Verify data persistence uses JSON/CSV/text files (no SQL, no ORM)
3. **No Premature Optimization**: Flag caching, threading, async code (not needed for Phase I)
4. **Error Handling**: Check that errors print to stderr and return non-zero exit codes
5. **No External Dependencies**: Flag imports beyond stdlib (Phase I should minimize dependencies)

**Flag as HIGH**: Use of databases, web frameworks, or async in Phase I code

### Step 8: Spec Alignment Verification
If `feature_context` provided and spec.md exists:
1. Compare implemented functions against spec acceptance criteria
2. Check that CLI commands match spec's command syntax
3. Verify error messages align with spec's error scenarios
4. Flag any implementation beyond spec requirements (gold-plating)

**Flag as MODERATE**: Implementation deviates from spec requirements

### Step 9: Generate Code Quality Report
Structure findings in standard format:

```markdown
## Code Quality Review: <target>
**Date**: <YYYY-MM-DD>
**Files Reviewed**: <list of .py files>
**Total Lines of Code**: <count>

### Summary
<2-3 sentences: overall code quality status, major strengths/weaknesses>

### Architecture & Separation of Concerns
**Strengths**:
- ✅ <specific good architectural decision, with file:line reference>

**Concerns**:
- ⚠️ [CRITICAL|HIGH|MODERATE] <file:line> - <issue description>
  - Impact: <why this matters>
  - Recommendation: <specific refactoring action>

### Function Responsibilities
**Well-Scoped Functions**:
- ✅ `<function_name>` (<file:line>) - <why it's well-designed>

**Over-Complex Functions**:
- ⚠️ [CRITICAL|MODERATE] `<function_name>` (<file:line>) - <metrics>
  - Lines: <count> | Complexity: ~<estimate> | Parameters: <count>
  - Recommendation: <extraction or simplification strategy>

### Naming Conventions
**Clear Names**:
- ✅ <examples>

**Naming Issues**:
- ⚠️ [MODERATE] <file:line> - `<bad_name>` → Suggest: `<better_name>`
  - Reason: <clarity issue>

### Code Duplication
**Duplicated Logic Found**:
- ⚠️ [HIGH|MODERATE] <file1:line> and <file2:line> - <description>
  - Duplication: <# lines>
  - Recommendation: Extract to `<proposed_function_name>` in `<proposed_location>`

### Complexity Hotspots
**High Complexity Areas**:
- ⚠️ [CRITICAL|HIGH] `<function_name>` (<file:line>)
  - Cyclomatic Complexity: ~<estimate>
  - Nesting Depth: <levels>
  - Recommendation: <simplification strategy>

### Phase I Compliance
- ✅ Uses standard library only
- ✅ Simple file-based storage
- ⚠️ <any Phase I violations>

### Spec Alignment Check
<If feature_context provided>
✅ Implementation aligns with spec requirements in `specs/<feature>/spec.md`
<OR>
⚠️ Deviations detected: <list>

### Priority Actions
1. **[CRITICAL|HIGH|MODERATE]** <issue> - <recommended action>
2. **[CRITICAL|HIGH|MODERATE]** <issue> - <recommended action>
3. **[CRITICAL|HIGH|MODERATE]** <issue> - <recommended action>

### Summary Metrics
- Critical Issues: <count>
- High Severity: <count>
- Moderate Severity: <count>
- Minor/Suggestions: <count>

### Overall Assessment
<GREEN: Production-ready | YELLOW: Improvements recommended | RED: Refactoring required>
```

### Step 10: Prioritize Recommendations
1. Group issues by severity: CRITICAL → HIGH → MODERATE → MINOR
2. Within each severity, order by impact on maintainability
3. Limit recommendations to top 5 most impactful items
4. Ensure each recommendation is actionable and preserves functionality

## Output
Returns code quality report (markdown format) with:
- Categorized findings with severity, file:line references
- Specific refactoring recommendations for each issue
- Acknowledged strengths (balanced review)
- Prioritized action list (top 3-5 items)
- Overall assessment: GREEN/YELLOW/RED

## Failure Handling

**If target file not found**:
- Report: "ERROR: File not found at `<path>`. Verify path and try again."
- Exit with error status

**If target is not Python code**:
- Report: "ERROR: Target must be Python (.py) file or directory containing Python files."
- Exit with error status

**If no production code found (only tests)**:
- Report: "WARNING: Only test files found. This skill reviews production code. Specify a different target."
- Exit gracefully

**If feature_context spec doesn't exist**:
- Report: "WARNING: Spec not found at `specs/<feature>/spec.md`. Skipping spec alignment check."
- Continue with other quality checks

**If code is too large (>5000 lines total)**:
- Report: "WARNING: Large codebase detected. Review may be incomplete. Consider reviewing smaller modules individually."
- Proceed with review, focus on highest-impact issues

## Success Criteria
- Skill completes in <60 seconds for typical module (<500 lines)
- All issues include specific file:line references
- Recommendations are spec-safe (preserve functional requirements)
- Severity classifications are consistent with decision framework
- Report balances criticism with acknowledgment of strengths
- Top 3-5 recommendations are immediately actionable
