# Architecture

AIP uses Django apps to separate account, candidate, recruiter, and maintainer responsibilities. Scoring and relevancy logic sits alongside web workflows and should be treated as decision-support logic.

## Component View

```mermaid
flowchart LR
  Actor["Candidate or recruiter"] --> Entry["Django views and templates"]
  Entry --> Service["Role apps and scoring logic"]
  Service --> Data["Django database models"]
  Service --> External["Evaluation algorithms"]
```

## Key Components

- Account and role-specific Django apps
- Candidate scoring and relevancy algorithms
- Templates and static assets
- Django settings and management commands

## Main Workflow

```mermaid
sequenceDiagram
  participant User
  participant Client
  participant App
  participant Store
  User->>Client: Submits profile or reviews candidate
  Client->>App: Calls role-specific view
  App->>Store: Validate and persist state
  Store-->>App: Candidate and scoring state updated
  App-->>Client: Returns evaluation view
  Client-->>User: Present updated result
```

## Design Considerations

- Keep scoring criteria explainable
- Separate candidate input from recruiter decision flow
- Log enough context for later review and appeal


