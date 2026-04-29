# AIP

AIP is a Django-based recruiting platform prototype that combines role-specific portals with candidate evaluation, personality, and answer-relevancy logic.

## Repository Status

- Current role: Django recruiting platform with candidate, recruiter, maintainer, and scoring workflows
- Documentation status: refreshed for public review
- Primary audience: engineers, product reviewers, and collaborators evaluating the project context

## What This Project Does

- Django project with account, candidate, recruiter, and maintainer apps
- Algorithms for scoring, personality, and answer relevancy
- Template and static asset structure
- Role-aware web application flow

## Technology Stack

- Python and Django
- requirements.txt for Python dependencies
- Django templates and static assets
- manage.py for local operations

## Repository Map

- AIP/ contains Django project settings
- accounts/, candidate/, recruiter/, and maintainer/ contain role-specific apps
- templates/ and static/ contain frontend assets
- manage.py is the Django command entry point

## Getting Started

- Create a Python virtual environment
- Install dependencies with pip install -r requirements.txt
- Configure a safe local Django settings environment
- Run python manage.py migrate
- Run python manage.py runserver

## Documentation

- docs/overview.md - product context, users, scope, and outcomes
- docs/architecture.md - components, data flow, and sequence diagrams
- docs/product.md - user journeys, requirements, constraints, and roadmap ideas
- docs/operations.md - setup, validation, maintenance, and known risks

## Known Limitations

- Scoring workflows need fairness, explainability, and validation before real hiring use
- Candidate data handling must be reviewed carefully
- Model or heuristic outputs should support human decisions, not replace them

## Notes For Future Maintainers

This repository documents the original project intent and the implementation shape visible in the codebase. Before production use, review dependencies, environment configuration, data handling, and deployment assumptions against current standards.


