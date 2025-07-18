# ADR-006: Codelab-Style Documentation for Workshop

## Status
Accepted

## Context
The NeuroHub workshop is adapted from Christina Lin's InstaVibe codelab, which uses a specific step-by-step format that has proven effective for teaching multi-agent AI concepts. We needed to decide how to structure our workshop documentation while maintaining educational effectiveness and acknowledging the original work.

## Decision
We will create a comprehensive codelab document (`NEUROHUB_CODELAB.md`) that follows the exact 13-section structure of the original InstaVibe codelab, adapted for the neurotechnology domain. This will be supplemented by:
- A mapping document showing transformations
- Quick reference guides for different learning styles
- Cloud Shell-specific instructions

## Consequences

### Positive
- **Proven Structure**: The InstaVibe format has been tested and refined
- **Clear Attribution**: Properly acknowledges the original work
- **Learning Continuity**: Instructors familiar with InstaVibe can easily teach NeuroHub
- **Complete Coverage**: All technical concepts are preserved
- **Multiple Formats**: Learners can choose between detailed codelab or quick reference

### Negative
- **Maintenance Overhead**: Multiple documentation formats to keep synchronized
- **Domain Confusion**: Some references to social features might slip through
- **Length**: The full codelab is quite long (may intimidate some learners)

### Neutral
- **Translation Effort**: Required careful mapping of social → neuroscience concepts
- **File Organization**: More documentation files but better organized

## Implementation

Created three key documents:
1. `NEUROHUB_CODELAB.md` - Full 13-section workshop
2. `INSTAVIBE_TO_NEUROHUB_MAPPING.md` - Shows all transformations
3. Updated `WORKSHOP_GUIDE.md` - Quick reference version

Section mapping:
- What you will learn → Neurotechnology focus
- Event Planner Agent → Signal Processor Agent
- Social posts → Research reports
- Friends network → Research collaborations

## Alternatives Considered

1. **Complete Rewrite**: Start fresh with new structure
   - Rejected: Would lose proven educational flow
   
2. **Minimal Adaptation**: Just change names
   - Rejected: Domain differences require deeper changes
   
3. **Multiple Mini-Labs**: Break into smaller workshops
   - Rejected: Loses comprehensive multi-agent learning

## Related ADRs
- ADR-005: SQL Queries (affects database sections)
- ADR-003: MCP Protocol (unchanged in adaptation)
- ADR-004: UV Package Manager (used in setup steps)

## References
- [Original InstaVibe Codelab](https://codelabs.developers.google.com/instavibe-adk-multi-agents/)
- [NeuroHub Codelab](../../NEUROHUB_CODELAB.md)
- [Transformation Mapping](../../INSTAVIBE_TO_NEUROHUB_MAPPING.md)