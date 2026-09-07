# Project Constitution: Malaphors Generator

**Version:** 1.0  
**Last Updated:** 2026-09-07  
**Speckit Version:** 2.0.0

## Mission Statement

The Malaphors Generator is a playful tool for creating and exploring creative blends of phrases, idioms, and proverbs. The project aims to entertain, educate, and inspire creative language play through both Python and Rust implementations.

## Core Principles

### 1. Quality First
- All code must be well-tested and documented
- Python type hints required for all public APIs
- Maintain minimum 80% test coverage
- Follow PEP 8 style guidelines

### 2. User Experience
- Simple, intuitive interface (both UI and CLI)
- Fast performance for phrase generation
- Clear error messages and user feedback
- Cross-platform compatibility (Windows, macOS, Linux)

### 3. Maintainability
- Keep code modular and DRY (Don't Repeat Yourself)
- Document architectural decisions in ADR format
- Use semantic versioning for releases
- Maintain backward compatibility where possible

### 4. Openness
- Welcome community contributions
- Transparent development process
- License terms clearly stated (see LICENSE file)
- Collaborative problem-solving

## Architectural Guardrails

### Technology Stack
- **Primary:** Python 3.10+ with Tkinter
- **Alternative:** Rust with Tauri (experimental)
- **Dependencies:** Keep minimal and well-justified
- **Testing:** pytest framework for all test suites

### Data Management
- Phrase data stored in JSON format for portability
- No external database requirements
- Export/import functionality for data portability
- Settings stored in user-accessible JSON

### Feature Gates
- Major features require spec + plan review
- UI changes must include mockups/screenshots
- Performance-critical changes require benchmarking
- Security issues follow responsible disclosure

## Workflow Requirements

### For Specifications
- Each new feature requires spec.md in `.specify/features/{feature-name}/`
- Specifications must address: what, why, how, and acceptance criteria
- Stakeholder review checkpoint before proceeding to planning

### For Planning
- Plan must map spec requirements to implementation strategy
- Technical decisions must be documented
- Risk assessment and mitigation strategies included
- Resource and timeline estimates required

### For Implementation
- All tasks must be sourced from tasks.md
- Code reviews required for all PRs
- Tests must pass before merge
- Documentation updates required for public API changes

### For Testing
- Unit tests for all business logic (malaphor_logic.py)
- Integration tests for UI components
- Manual testing checklist for new features
- Regression test suite maintained

## Review Checkpoints

1. **Specification Review:** Ensures requirements are clear and complete
2. **Planning Review:** Validates technical approach and feasibility
3. **Implementation Review:** Confirms code quality and test coverage
4. **Release Review:** Final check before publishing

## Non-Negotiable Standards

- ✅ No feature ships without tests
- ✅ No PR merges without code review
- ✅ No breaking changes without major version bump
- ✅ No dependencies added without justification
- ✅ No security issues left unresolved
- ❌ No uncommitted environment-specific secrets
- ❌ No debug code in production commits
- ❌ No unhandled exceptions in user-facing code

## Version Management

- **Package Version:** Follows semantic versioning (MAJOR.MINOR.PATCH)
- **Speckit Version:** 2.0.0 (latest)
- **Python Version:** 3.10+ required
- **Minimum Dependencies:** Reviewed quarterly

## Dispute Resolution

When principles conflict during implementation:
1. Escalate to project maintainers
2. Reference this constitution as authority
3. Document resolution as precedent
4. Update constitution if needed to reflect new guidance

---

**Constitution Authority:** This document is non-negotiable within the speckit workflow scope. Conflicts with this constitution require explicit amendment, not reinterpretation.
