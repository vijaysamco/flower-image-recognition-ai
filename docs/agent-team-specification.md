# Agent Team Specification

## Purpose

This document defines the agent team for FlowerVision AI and the process by which specialized agents collaborate to build, validate, and maintain the project. It complements the repository guidance in [AGENTS.md](../AGENTS.md) and clarifies how responsibilities are divided, how work moves through the delivery lifecycle, and how agents coordinate without creating overlap or duplicated effort.

## Team Composition

The project is organized around a small set of focused agent roles. Each agent owns a clear domain and is expected to operate within that scope while collaborating with neighboring disciplines.

### 1. Backend Agent

Responsible for:
- FastAPI application structure
- API endpoints and request handling
- Business logic and validation rules
- Error handling and response consistency
- API documentation and contract accuracy

Operating rules:
- Business logic must stay out of route handlers.
- Validation and authorization checks should happen before service logic.
- API contracts must stay aligned with the frontend and documentation.

### 2. Frontend Agent

Responsible for:
- React UI composition
- Page and component structure
- Image upload and user interaction flows
- Loading, empty, and error states
- API integration between client and backend

Operating rules:
- Prefer reusable, focused components.
- Keep the user experience simple and responsive.
- Validate that UI behaviors remain consistent with backend contracts.

### 3. Vision Agent

Responsible for:
- Image preprocessing
- Model loading and lifecycle
- Inference pipeline
- Prediction confidence computation
- Performance-sensitive AI logic

Operating rules:
- Avoid unnecessary model reloads.
- Centralize preprocessing logic and reuse it consistently.
- Ensure inference behavior is measured and reproducible.

### 4. Testing Agent

Responsible for:
- Unit tests
- Integration tests
- API and UI regression checks
- Validation of bug fixes and feature changes

Operating rules:
- Add tests when practical for new features and bug fixes.
- Verify affected behavior before completion.
- Prefer the smallest relevant test scope for fast feedback.

### 5. Documentation Agent

Responsible for:
- README updates
- Product specification and architecture docs
- Setup and usage guidance
- API documentation and examples

Operating rules:
- Keep documentation synchronized with product and code changes.
- Ensure project docs explain real behavior, not aspirational plans.

### 6. Security Agent

Responsible for:
- Input validation review
- Upload restriction and sanitization checks
- Dependency and secret hygiene
- Security risk review before merge

Operating rules:
- Never hardcode secrets, keys, or credentials.
- Require explicit validation of file upload boundaries and untrusted input.
- Treat security as a shared standard, not a separate late-stage review only.

### 7. DevOps Agent

Responsible for:
- Docker and environment setup
- CI/CD and workflow reliability
- Deployment configuration
- Environment variable management

Operating rules:
- Keep deployment reproducible and easy to run locally.
- Ensure environment and runtime assumptions are documented.

## Team Working Model

The agent team follows a disciplined collaboration model based on specialization, clear ownership, and staged review.

### 1. Work is partitioned by domain

Each agent owns a primary area of responsibility. Domain ownership prevents conflicting edits and keeps decision-making localized.

### 2. Work is coordinated by feature flow

The standard flow for a task is:
1. Define the required outcome and scope.
2. Assign the primary agent for the feature area.
3. Identify dependent concerns from other domains.
4. Implement the work within the relevant subsystem.
5. Run focused validation and tests.
6. Update documentation and release notes if the user-facing behavior changes.
7. Hand off for review and final merge.

### 3. Cross-agent handoff is expected

Complex work often requires multiple agents in sequence, for example:
- Frontend Agent delivers the UI and triggers backend contracts.
- Backend Agent implements the API and validation rules.
- Vision Agent verifies the inference pipeline and model behavior.
- Testing Agent validates the end-to-end result.
- Documentation Agent updates usage and product guidance.
- Security Agent checks the changes for unsafe assumptions.

### 4. One owner per decision

Each task should have a primary owner. That owner coordinates decisions within the task area, while other agents contribute inputs when their specialty is affected.

## Development Workflow

The project workflow is intentionally simple and repeatable:

1. Create or update a feature branch.
2. Implement the required change in the relevant subsystem.
3. Add or update tests where practical.
4. Validate formatting, linting, and functionality.
5. Update relevant documentation.
6. Open a pull request for review.

This process ensures that quality, documentation, and verification remain part of the delivery cycle rather than afterthoughts.

## Quality Standards

All agents are expected to follow the project standards defined in [AGENTS.md](../AGENTS.md), including:
- PEP 8 and readable Python code
- Small, focused functions with clear names
- Reusable React patterns
- Secure file and input handling
- Clear documentation of important decisions
- Test coverage for behavior that can regress

The project definition of done is:
- The code works as expected.
- The relevant tests pass.
- Documentation is updated when behavior changes.
- Code follows repository standards.
- No obvious security issues are introduced.

## Collaboration Principles

The agent team operates under the following principles:

- Simplicity over cleverness
- Clarity over optimization that reduces maintainability
- Clear boundaries over duplicated effort
- Shared accountability for final quality
- Explicit handoff documentation for complex tasks

## Escalation and Review

If a task crosses domain boundaries or introduces uncertainty, the responsible agent should escalate to the relevant specialists before finalizing the change. This includes:
- security-sensitive input or file handling
- model accuracy or inference assumptions
- API contract changes affecting frontend behavior
- deployment or environment changes with operational impact

Reviews should focus on correctness, maintainability, security, and alignment with the project goals.

## Summary

FlowerVision AI is designed as a collaborative, specialized agent team. Each agent is responsible for a distinct part of the product, but the success of the project depends on disciplined coordination, shared quality standards, and strong handoff practices across backend, frontend, AI, testing, documentation, security, and DevOps concerns.
