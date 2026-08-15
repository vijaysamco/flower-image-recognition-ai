# AGENTS.md

# FlowerVision AI - AI Agent Instructions

**Project:** FlowerVision AI  
**Version:** 1.0.0  
**Status:** Active Development

---

# Purpose

This document defines the responsibilities, coding standards, workflows, and project guidelines for both human contributors and AI coding assistants.

All contributors should follow these instructions to maintain a consistent, clean, and production-ready codebase.

---

# Project Goal

Build a lightweight, production-ready AI web application that classifies flower species from uploaded images using FastAPI, React, and PyTorch.

The project should prioritize:

- Simplicity
- Readability
- Maintainability
- Security
- Performance
- Scalability

---

# Tech Stack

## Frontend

- React
- Vite
- JavaScript
- CSS

## Backend

- FastAPI
- Python 3.12+

## AI

- PyTorch
- Torchvision
- Pillow
- OpenCV

## Database

- SQLite

## DevOps

- Docker
- GitHub Actions

---

# AI Agent Roles

## Backend Agent

Responsible for:

- FastAPI development
- API endpoints
- Validation
- Business logic
- Error handling
- API documentation

Never place business logic inside route handlers.

---

## Frontend Agent

Responsible for:

- React components
- Responsive layouts
- Image upload
- API integration
- Loading and error states

Keep components reusable and modular.

---

## Vision Agent

Responsible for:

- Image preprocessing
- Model loading
- AI inference
- Prediction pipeline
- Confidence calculation

Avoid unnecessary model reloads.

---

## Testing Agent

Responsible for:

- Unit tests
- Integration tests
- API tests
- Regression testing

Every new feature should include tests where practical.

---

## Documentation Agent

Responsible for:

- README
- Product specification
- API documentation
- Architecture documentation
- Setup instructions

Keep documentation synchronized with code changes.

---

## Security Agent

Responsible for:

- Input validation
- File upload restrictions
- Dependency updates
- Secret management

Never hardcode credentials, tokens, or API keys.

---

## DevOps Agent

Responsible for:

- Docker
- GitHub Actions
- Deployment configuration
- Environment variables

Keep deployments reproducible and automated.

---

# Coding Standards

## Python

- Follow PEP 8
- Use type hints
- Prefer small functions
- Use descriptive names
- Write docstrings for public functions

---

## React

- Functional components only
- Use Hooks
- Keep components focused
- Avoid duplicated logic

---

# Folder Responsibilities

backend/

- API
- AI inference
- Configuration
- Models
- Utilities

frontend/

- UI
- Components
- Pages
- Services

docs/

- Documentation

security/

- Security policies

ops/

- Deployment resources

tests/

- Test suites

---

# Development Workflow

1. Create a feature branch.
2. Implement the feature.
3. Add tests if applicable.
4. Run formatting and linting.
5. Update documentation.
6. Open a Pull Request.

---

# Git Commit Convention

Examples:

```
feat: add prediction endpoint

fix: validate uploaded image

docs: update README

refactor: simplify preprocessing

test: add API tests

chore: update dependencies
```

---

# API Design Rules

- Use REST principles.
- Return JSON responses.
- Use appropriate HTTP status codes.
- Validate all inputs.
- Handle errors consistently.

---

# Error Handling

Every endpoint should:

- Validate inputs
- Return meaningful error messages
- Avoid exposing internal details
- Log unexpected exceptions

---

# Logging

Use structured logging.

Log:

- Startup
- Shutdown
- Prediction requests
- Validation errors
- Unexpected exceptions

Avoid logging sensitive information.

---

# Performance Guidelines

- Load the AI model once during application startup.
- Reuse model instances.
- Resize images before inference.
- Minimize unnecessary disk I/O.

---

# Security Guidelines

Always:

- Validate uploaded files.
- Limit upload size.
- Sanitize inputs.
- Use environment variables.
- Keep dependencies updated.

Never:

- Store secrets in the repository.
- Trust client-side validation alone.

---

# Documentation Requirements

When introducing new features:

- Update README if user-facing behavior changes.
- Update API documentation for endpoint changes.
- Keep examples current.

---

# Testing Requirements

Test:

- Image validation
- Prediction endpoint
- Error handling
- Utility functions

Run all tests before merging changes.

---

# Out of Scope

This project does not currently include:

- User authentication
- Payments
- Cloud storage
- Model training pipelines
- Multi-user collaboration

These may be added in future releases.

---

# Guiding Principles

- Keep it simple.
- Prefer clarity over cleverness.
- Write maintainable code.
- Build reusable components.
- Design for future growth.
- Document important decisions.

---

# Definition of Done

A task is complete when:

- Code works as expected.
- Tests pass.
- Documentation is updated.
- Code follows project standards.
- No obvious security issues are introduced.

---

# Final Note

FlowerVision AI is intended to demonstrate professional AI application development practices. Every contribution should improve the project's quality, maintainability, and learning value.
