# Architecture: [Project Name]

**Status**: Living Document
**Owner**: [Architecture Owner/Team]
**Last Updated**: [YYYY-MM-DD]
**Priority**: High

> This is a living document that captures the current state of the system architecture. For major architectural changes, create separate specifications in `specs/features/architecture-*.md` following the feature template. Once implemented, update this document to reflect the new current state.

## System Overview

[High-level description of the system, its purpose, and how components work together]

### Visual Architecture

```
[Add ASCII diagram or reference to external architecture diagram]

Example:
┌─────────────┐      ┌──────────────┐      ┌──────────────┐
│   Client    │─────▶│  API Server  │─────▶│   Database   │
│  (Web/App)  │      │  (FastAPI)   │      │ (PostgreSQL) │
└─────────────┘      └──────────────┘      └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    Cache     │
                     │   (Redis)    │
                     └──────────────┘
```

### Technology Stack

**Languages:**
- [e.g., Python 3.11+, TypeScript, etc.]

**Frameworks:**
- [e.g., FastAPI, React, etc.]

**Databases:**
- [e.g., PostgreSQL 15, Redis 7]

**Infrastructure:**
- [e.g., Docker, Kubernetes, AWS]

**Key Libraries:**
- [List critical dependencies]

## Core Architectural Principles

> These principles guide all technical decisions and feature implementations.

1. **[Principle Name]**: [Description of principle and why it matters]
   - Example: "API-First Design: All features expose APIs before UI to enable multiple clients"

2. **[Principle Name]**: [Description]
   - Example: "Stateless Services: Application servers maintain no session state for horizontal scalability"

3. **[Principle Name]**: [Description]
   - Example: "Domain-Driven Design: Code organization follows business domains, not technical layers"

4. **[Principle Name]**: [Description]

5. **[Add more as needed]**

## Current Architecture

### Component Breakdown

#### 1. [Component Name] (e.g., API Layer)

**Purpose**: [What this component does]

**Technology**: [Framework/language used]

**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]

**Key Patterns:**
- [e.g., RESTful API design, OpenAPI specification]

**Location**: [Directory path or service name]

---

#### 2. [Component Name] (e.g., Business Logic Layer)

**Purpose**: [What this component does]

**Technology**: [Framework/language used]

**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

**Key Patterns:**
- [e.g., Service pattern, dependency injection]

**Location**: [Directory path or service name]

---

#### 3. [Component Name] (e.g., Data Layer)

**Purpose**: [What this component does]

**Technology**: [Database/ORM used]

**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

**Key Patterns:**
- [e.g., Repository pattern, database migrations]

**Location**: [Directory path or service name]

---

[Add more components as needed]

### Data Flow

Describe how data moves through the system for key operations:

#### Example: User Authentication Flow

1. Client sends credentials to `/api/auth/login`
2. API layer validates request format
3. Authentication service verifies credentials against database
4. Session token generated and stored in Redis
5. Token returned to client
6. Subsequent requests include token in Authorization header
7. Middleware validates token against Redis on each request

#### [Another Critical Flow]

[Describe another important data flow]

### Integration Points

**External Services:**
- **[Service Name]**: [Purpose, how integrated, authentication method]
- Example: **Stripe**: Payment processing, REST API, API key authentication

**Internal Services:**
- **[Service Name]**: [Purpose, communication method]
- Example: **Email Service**: Async messaging via RabbitMQ

**APIs Exposed:**
- **[API Name]**: [Purpose, consumers, authentication]
- Example: **Public REST API**: Third-party integrations, OAuth 2.0

## Design Patterns in Use

### 1. [Pattern Name] (e.g., Repository Pattern)

**Where**: [Which components use this]

**Why**: [Reasoning for using this pattern]

**Example**:
```python
# Example code snippet showing the pattern
class UserRepository:
    def get_by_id(self, user_id: str) -> User:
        # Implementation
        pass
```

### 2. [Pattern Name] (e.g., Dependency Injection)

**Where**: [Which components use this]

**Why**: [Reasoning]

**Example**: [Code or description]

### 3. [Add more patterns]

## Key Architectural Decisions

> Major decisions that shaped the current architecture. For detailed rationale, see referenced architecture-*.md specs.

### Decision 1: [Decision Title]

**Date**: [YYYY-MM-DD]

**Context**: [What problem were we solving?]

**Decision**: [What did we decide?]

**Rationale**: [Why this approach?]

**Consequences**: [Trade-offs, benefits, limitations]

**Reference**: [Link to detailed spec if exists, e.g., `specs/features/architecture-microservices.md`]

---

### Decision 2: [Decision Title]

**Date**: [YYYY-MM-DD]

**Context**: [Problem context]

**Decision**: [What was decided]

**Rationale**: [Why]

**Consequences**: [Trade-offs]

**Reference**: [Link to spec]

---

[Add more key decisions]

## Constraints and Non-Negotiables

**Technical Constraints:**
- [e.g., "Must run on Python 3.11+ for security patches"]
- [e.g., "All data must be encrypted at rest (compliance requirement)"]
- [e.g., "Response time < 200ms for 95th percentile (SLA requirement)"]

**Business Constraints:**
- [e.g., "Must support offline mode (product requirement)"]
- [e.g., "Multi-tenancy required (business model)"]

**Operational Constraints:**
- [e.g., "Zero-downtime deployments required"]
- [e.g., "Must be deployable to air-gapped environments"]

## Security Architecture

**Authentication**: [How users/services authenticate]

**Authorization**: [How permissions are managed]

**Data Protection**:
- At rest: [Encryption method]
- In transit: [TLS version, certificates]
- Sensitive data handling: [PII, secrets management]

**Security Patterns**:
- [e.g., "Defense in depth", "Least privilege"]
- [e.g., "Input validation at all boundaries"]

**Compliance**:
- [e.g., GDPR, HIPAA, SOC 2]

## Scalability Strategy

**Horizontal Scaling**:
- [Which components scale horizontally?]
- [Load balancing strategy]

**Vertical Scaling**:
- [Which components scale vertically?]
- [Resource limits]

**Bottlenecks**:
- [Known bottlenecks and mitigation strategies]

**Caching Strategy**:
- [What is cached, where, and for how long]

**Database Scaling**:
- [Read replicas, sharding, partitioning strategy]

## Reliability & Operations

**Monitoring**:
- [Metrics collected]
- [Alerting strategy]
- [Observability tools]

**Logging**:
- [Logging framework]
- [Log aggregation]
- [Retention policy]

**Error Handling**:
- [Error handling philosophy]
- [Retry strategies]
- [Circuit breakers]

**Disaster Recovery**:
- [Backup strategy]
- [RTO/RPO targets]
- [Failover procedures]

## Development Workflow Impact

**Local Development**:
- [How developers run the system locally]
- [Docker Compose, local services, etc.]

**Testing Strategy**:
- [Test pyramid: unit, integration, e2e]
- [Test environments]

**Deployment Pipeline**:
- [CI/CD approach]
- [Deployment frequency]
- [Rollback strategy]

**Code Organization**:
- [Directory structure philosophy]
- [Module boundaries]
- [Dependency management]

## Future Considerations

> Potential architectural evolutions under consideration. When these become concrete plans, create dedicated `architecture-*.md` specs.

1. **[Future Direction]**: [Brief description of potential change]
   - **Drivers**: [What would motivate this change]
   - **Challenges**: [What makes this difficult]

2. **[Future Direction]**: [Description]

3. **[Add more as needed]**

## Architectural Change Process

When architecture needs to change:

1. **Assess Impact**: Determine if change is minor (update this doc) or major (requires spec)

2. **Major Changes Require Specs**:
   - Create `specs/features/architecture-[change-name].md`
   - Use the standard feature template
   - Include: Purpose, Requirements, Acceptance Criteria, Migration Plan
   - Follow Specify → Plan → Implement → Validate workflow

3. **Minor Updates**:
   - Small refinements to existing architecture
   - Update this document directly
   - Update "Last Updated" timestamp
   - Document in Implementation History below

4. **After Implementation**:
   - Update this document to reflect new current state
   - Mark architecture-*.md spec as "Implemented"
   - Add decision to "Key Architectural Decisions" section

### Examples of Major vs. Minor Changes

**Major Changes (Require Specs):**
- Migrating from monolith to microservices
- Changing primary database technology
- Adding event-driven architecture
- Multi-region deployment strategy
- New authentication/authorization system

**Minor Changes (Update This Doc):**
- Adding a caching layer to existing component
- Upgrading framework version (same framework)
- Refactoring internal component structure
- Adding monitoring/logging improvements

## Implementation History

**Recent Architectural Updates:**

- **[YYYY-MM-DD]**: [Brief description of change made]
  - Spec: [Link to architecture-*.md if applicable, or "Direct update"]

- **[YYYY-MM-DD]**: [Description]
  - Spec: [Link]

[Add more as architecture evolves]

## References

**Related Specifications:**
- [Link to relevant architecture-*.md specs]
- [Link to related feature specs]

**External Documentation:**
- [Link to API documentation]
- [Link to deployment guides]
- [Link to runbooks]

**Architecture Diagrams:**
- [Link to detailed diagrams, C4 models, etc.]

---

**Template Version**: 1.0
**Last Updated**: 2026-01-19
