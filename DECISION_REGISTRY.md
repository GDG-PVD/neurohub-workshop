# Decision Registry

This registry tracks all architectural and technical decisions for the NeuroHub project. For detailed information about each decision, see the linked ADR.

## Quick Reference

### 🏗️ Architecture Decisions

| Decision | Date | Impact | Status | Link |
|----------|------|--------|--------|------|
| Use SciPy for signal processing | 2024-07-01 | High | ✅ Accepted | [ADR-001](docs/adr/ADR-001-signal-processing-library.md) |
| MCP for agent-platform communication | 2024-07-15 | High | ✅ Accepted | [ADR-003](docs/adr/ADR-003-mcp-over-direct-api.md) |
| A2A protocol for agent communication | 2024-07-15 | High | ✅ Accepted | [ADR-004](docs/adr/ADR-004-a2a-protocol.md) |
| SQL queries over Property Graph | 2025-07-18 | High | ✅ Accepted | [ADR-005](docs/adr/ADR-005-sql-queries-over-graph.md) |
| NeuroHub Ally AI Assistant | 2025-07-22 | High | ✅ Accepted | [ADR-007](docs/adr/007-neurohub-ally-integration.md) |
| MCP Server native implementation | 2025-07-22 | High | ✅ Accepted | [ADR-008](docs/adr/008-mcp-server-implementation.md) |

### 🛠️ Technology Choices

| Decision | Date | Impact | Status | Link |
|----------|------|--------|--------|------|
| Python 3.11+ requirement | 2024-07-01 | Medium | ✅ Accepted | [ADR-002](docs/adr/ADR-002-python-version.md) |
| UV package manager | 2024-07-18 | Low | ✅ Accepted | [ADR-004](docs/adr/ADR-004-uv-package-manager.md) |
| Flask for web framework | 2024-07-01 | Medium | ✅ Accepted | [ADR-006](docs/adr/ADR-006-flask-framework.md) |
| Docker for containerization | 2024-07-01 | Medium | ✅ Accepted | [ADR-007](docs/adr/ADR-007-docker-containers.md) |

### 📚 Documentation Standards

| Decision | Date | Impact | Status | Link |
|----------|------|--------|--------|------|
| ADR format for decisions | 2024-07-18 | Low | ✅ Accepted | [ADR Template](docs/adr/template.md) |
| Codelab-style documentation | 2025-07-18 | High | ✅ Accepted | [ADR-006](docs/adr/ADR-006-codelab-documentation.md) |
| Modular documentation approach | 2024-07-18 | Medium | ✅ Accepted | [ADR-008](docs/adr/ADR-008-modular-docs.md) |
| AI-assisted development practices | 2024-07-18 | Medium | ✅ Accepted | [ADR-009](docs/adr/ADR-009-ai-practices.md) |

### 🚀 Deployment Decisions

| Decision | Date | Impact | Status | Link |
|----------|------|--------|--------|------|
| Google Cloud Run for agents | 2024-07-01 | High | ✅ Accepted | [ADR-010](docs/adr/ADR-010-cloud-run.md) |
| Vertex AI Agent Engine | 2024-07-15 | Medium | ✅ Accepted | [ADR-011](docs/adr/ADR-011-agent-engine.md) |
| Cloud Shell for development | 2025-07-18 | Medium | ✅ Accepted | [Cloud Shell Guide](docs/CLOUD_SHELL_GUIDE.md) |

## Decision Impact Levels

- **High**: Affects system architecture or requires significant rework to change
- **Medium**: Affects multiple components or development workflow
- **Low**: Limited scope, easily reversible

## Decision Status

- ✅ **Accepted**: Decision is active and implemented
- 🔄 **Proposed**: Under discussion, not yet implemented
- ⚠️ **Deprecated**: No longer recommended but still in use
- ❌ **Superseded**: Replaced by another decision

## Making New Decisions

1. Copy the [ADR template](docs/adr/template.md)
2. Document context, options, and rationale
3. Add entry to this registry
4. Link related decisions
5. Update affected documentation

## Principles Guiding Decisions

1. **Workshop-First**: Optimize for learning and teaching
2. **Simplicity**: Choose straightforward over clever
3. **Modern Practices**: Use current tools and patterns
4. **Documentation**: Every decision must be recorded
5. **Flexibility**: Allow for future improvements

## Review Schedule

- Quarterly review of deprecated decisions
- Annual review of all high-impact decisions
- Continuous updates as new decisions are made

Last updated: 2025-07-22