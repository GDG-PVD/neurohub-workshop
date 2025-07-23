# ADR-009: Pre-Built Workshop Agent Pattern

## Status
Accepted

## Context
During workshop development, we identified several challenges with the original approach of having students build agents from scratch:
- File creation via heredocs was getting truncated in Cloud Shell
- Import errors with MCP modules caused confusion
- Students spent too much time debugging setup issues instead of learning concepts
- The time to first success was too long (>15 minutes)

## Decision
We will provide a pre-built workshop agent that:
1. Works immediately upon running
2. Uses a simple configuration file for customization
3. Gracefully handles missing dependencies (e.g., MCP tools)
4. Provides clear feedback via console output
5. Includes both quick test and interactive test scripts

## Consequences

### Positive
- Students see a working agent in <5 minutes
- Focus shifts from debugging to understanding and customization
- Eliminates file creation issues
- Provides a clear pattern for agent development
- Reduces workshop support burden

### Negative
- Students don't experience building an agent from scratch
- May create dependency on pre-built patterns
- Need to maintain the workshop agent alongside other agents

## Implementation Details

The workshop agent consists of:
- `config.py`: All customizable variables in one place
- `agent.py`: Robust implementation with error handling
- `quick_test.py`: Immediate verification of functionality
- `interactive_test.py`: Conversational interface
- `README.md`: Clear instructions

Key design decisions:
1. Use `from config import *` for simplicity (acceptable in workshop context)
2. Try multiple MCP import paths for compatibility
3. Log using Python logging module for production readiness
4. Graceful degradation when MCP unavailable

## Related ADRs
- ADR-003: MCP Integration Pattern
- ADR-006: Documentation and Codelab Structure
- ADR-008: MCP Server Implementation

## Date
2024-01-23