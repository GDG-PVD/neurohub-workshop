# Architecture Decision Records (ADR) Index

This index tracks all architectural decisions made for the NeuroHub project.

## Decision Registry

| ID | Title | Date | Status | Tags | Summary |
|----|-------|------|--------|------|---------|
| [ADR-001](ADR-001-signal-processing-library.md) | Use SciPy for Biosignal Processing | 2024-07-01 | Accepted | architecture, signal-processing | Chose SciPy over custom implementation for reliable signal analysis |
| [ADR-002](ADR-002-python-version.md) | Require Python 3.11+ | 2024-07-01 | Accepted | environment, dependencies | Standardized on Python 3.11+ for modern features and better errors |
| [ADR-003](ADR-003-mcp-over-direct-api.md) | Use MCP for Agent-Platform Communication | 2024-07-15 | Accepted | architecture, integration | MCP provides standardized tool interface for agents |
| [ADR-004](ADR-004-uv-package-manager.md) | Adopt UV for Package Management | 2024-07-18 | Accepted | tooling, performance | UV replaces pip for 10-100x faster package installation |
| [ADR-005](ADR-005-sql-queries-over-graph.md) | Use SQL Queries Over Property Graph | 2025-07-18 | Accepted | architecture, database, cost | SQL queries on Spanner Standard Edition instead of Enterprise Property Graph |
| [ADR-006](ADR-006-codelab-documentation.md) | Codelab-Style Documentation | 2025-07-18 | Accepted | documentation, workshop | Follow InstaVibe's 13-section structure adapted for neurotechnology |
| [ADR-007](007-neurohub-ally-integration.md) | NeuroHub Ally AI Assistant Integration | 2025-07-22 | Accepted | architecture, integration, workshop | Web-based AI assistant interface with A2A agent connectivity and SSE streaming |
| [ADR-008](008-mcp-server-implementation.md) | MCP Server Implementation Without ADK Tools | 2025-07-22 | Accepted | architecture, integration, tooling | Direct MCP implementation to resolve ADK import issues |

## How to Use This Index

1. **Finding Decisions**: Use the tags to find relevant decisions (e.g., all "architecture" decisions)
2. **Adding New ADRs**: 
   - Copy the [template](template.md)
   - Name it `ADR-XXX-brief-title.md`
   - Add entry to this index
3. **Updating Status**: Mark as "Deprecated" or "Superseded" when decisions change

## ADR States

- **Proposed**: Under discussion
- **Accepted**: Approved and implemented
- **Deprecated**: No longer valid but kept for history
- **Superseded**: Replaced by another ADR (link to new one)

## Tags Used

- `architecture`: System design decisions
- `signal-processing`: Biosignal analysis choices
- `database`: Database and data model decisions
- `dependencies`: External library decisions
- `documentation`: Documentation approach decisions
- `environment`: Development environment choices
- `tooling`: Development tool selections
- `integration`: System integration approaches
- `performance`: Performance-related decisions
- `cost`: Cost optimization decisions
- `workshop`: Workshop-specific decisions
- `ai-generated`: Decisions made with AI assistance
- `security`: Security-related choices
- `testing`: Testing approach decisions

## Guidelines

- Write ADRs for significant decisions that affect the codebase
- Include context about why the decision was needed
- Document alternatives that were considered
- Be honest about trade-offs
- Note if AI tools helped with the decision