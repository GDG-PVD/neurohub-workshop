# ADR-005: Use SQL Queries Instead of Property Graph Queries

## Status
Accepted

## Context
The workshop initially planned to use Spanner's Property Graph feature for querying neurotechnology research data. However, during implementation, we discovered that Property Graph features require Spanner Enterprise edition, while the workshop uses Standard edition for cost efficiency.

## Decision
We will use standard SQL queries with JOIN operations instead of Property Graph queries for all data access patterns in the NeuroHub application.

## Consequences

### Positive
- **Cost Efficiency**: Standard edition is sufficient, avoiding Enterprise edition costs
- **Broader Compatibility**: SQL queries work with any Spanner edition
- **Familiar Syntax**: Workshop participants are more likely to know SQL than graph query languages
- **Simpler Mental Model**: SQL joins are well-understood by most developers
- **Better Documentation**: SQL is better documented than Spanner's graph features

### Negative
- **More Verbose Queries**: Some relationship traversals require multiple JOINs
- **Performance Considerations**: Complex relationship queries may require optimization
- **Lost Graph Benefits**: Cannot use graph-specific optimizations or algorithms

### Neutral
- **Schema Design**: The underlying schema remains unchanged (still uses nodes and edges conceptually)
- **Future Migration**: Can migrate to Property Graph when upgrading to Enterprise edition

## Implementation

Created `db_neurohub.py` with SQL-based query functions:
- `get_all_researchers()` - List researchers
- `get_experiments_by_researcher()` - Find experiments led by a researcher
- `get_experiment_details()` - Get full experiment information with devices and sessions
- `get_recent_analyses()` - List recent signal analyses
- `get_researcher_collaborations()` - Find collaboration relationships
- `get_signal_data_by_experiment()` - Get all signals for an experiment

## Related ADRs
- ADR-002: Python Version (affects SQL library compatibility)
- ADR-003: MCP Over Direct API (MCP tools will also use SQL queries)

## References
- [Spanner SQL Reference](https://cloud.google.com/spanner/docs/query-syntax)
- [Spanner Property Graph Documentation](https://cloud.google.com/spanner/docs/graph/overview) (Enterprise only)