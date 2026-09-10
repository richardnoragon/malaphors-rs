# Changelog

All notable changes to this project are recorded here using semantic versioning.

## [Unreleased]

### Changed
- Normalized project documentation to semantic versioning conventions.
- Added explicit release note guidance to the README, contributing guide, and
  speckit documentation.
- Removed stale `latest` wording from speckit configuration and update notes.
- Consolidated the versioning docs into [VERSIONING.md](VERSIONING.md).
- Implemented scheduled auto-save lifecycle hooks so the app persists history and favorites in a background thread without blocking the UI.
- Verified and documented Section 2 reliability/performance work: cancellation-safe async generation, malformed-history resilience, latency benchmarking, and paginated history access.
- Added language-aware generation support to the core generator and CLI, allowing `--language`-filtered malaphor output without breaking the existing generation flow.
- Completed the UI-side language selector so the main Tkinter app can generate within a chosen language while defaulting to all available phrase sets.

## [2.0.0] - 2026-09-08

### Added
- Initialized the speckit framework with the `.specify/` directory structure.
- Added the project constitution and workflow documentation.

### Changed
- Upgraded the speckit framework to 2.0.0.
- Established the project as a specification-driven workflow with commit
  traceability.

### Notes
- Relevant commits: `4826181`, `487d099`

## [1.0.0] - 2026-09-08

### Added
- Consolidated the versioning guidance into a single canonical repository page.
