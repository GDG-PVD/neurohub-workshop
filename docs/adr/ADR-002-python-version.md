# ADR-002: Require Python 3.11+ for Development

**Date:** 2024-07-01

**Status:** Accepted

**Deciders:** Workshop organizers

**Tags:** environment, dependencies, student-experience

## Context

We need to standardize the Python version for the NeuroHub workshop to ensure:
- All students have the same experience
- Modern Python features are available
- Dependencies work consistently
- AI coding assistants have up-to-date syntax knowledge

Google Cloud Shell provides Python versions, and we need to pick one that balances modern features with stability.

## Decision

Require Python 3.11 or higher for all NeuroHub development.

## Considered Options

1. **Python 3.11+**: Current stable version
   - Pros: 
     - Improved error messages (huge benefit for students)
     - Better performance (10-60% faster)
     - Modern typing features (Self, TypeAlias)
     - All current libraries support it
   - Cons: 
     - Not the absolute latest (3.12 exists)

2. **Python 3.9**: Older stable version
   - Pros: 
     - Maximum compatibility
     - Well-tested with all libraries
   - Cons: 
     - Lacks helpful error messages
     - Missing modern type hints
     - Slower performance

3. **Python 3.12**: Latest version
   - Pros: 
     - Newest features
     - Best performance
   - Cons: 
     - Some libraries might not support it yet
     - Less tested in production

## Consequences

### Positive
- Students get clear error messages when debugging
- Can use modern Python patterns
- Better AI assistant support (trained on recent Python)
- Faster execution speeds

### Negative
- Must ensure Cloud Shell has Python 3.11
- Some older systems might need updates

### Neutral
- Sets precedent for using reasonably modern tools
- Influences dependency choices

## Implementation Notes

In setup documentation:
```bash
# Check Python version
python --version  # Should show 3.11.x or higher

# If needed, use UV to install specific version
uv venv --python 3.11
```

In all Python files:
```python
# Use modern type hints
from typing import Self, TypeAlias

# Use match statements where appropriate
match agent_type:
    case "signal_processor":
        return SignalProcessorAgent()
    case "documentation":
        return DocumentationAgent()
```

## References

- [Python 3.11 Release Notes](https://docs.python.org/3/whatsnew/3.11.html)
- [UV Python Version Management](https://github.com/astral-sh/uv)

## Notes

This decision supports our goal of teaching modern development practices while ensuring a smooth workshop experience.