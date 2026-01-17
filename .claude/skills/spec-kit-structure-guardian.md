# Spec-Kit-Structure-Guardian Skills

## enforce_directory_structure

- Checks that new files follow `.specify/`, `specs/`, `history/` hierarchy
- Blocks file creation in unauthorized locations (e.g., root-level utils)
- Allows files only in designated monorepo boundaries

## validate_naming_conventions

- Checks that files follow naming patterns (spec.md, plan.md, tasks.md)
- Blocks non-standard filenames in spec directories
- Allows files matching established conventions

## protect_template_integrity

- Checks that templates in `.specify/templates/` remain unmodified
- Blocks direct edits to base templates
- Allows template usage via proper instantiation

## verify_artifact_linking

- Checks that specs reference correct plans, plans reference tasks
- Blocks orphaned artifacts with broken cross-references
- Allows properly linked spec → plan → tasks chains
