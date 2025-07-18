# ADR-004: Adopt UV for Package Management

**Date:** 2024-07-18

**Status:** Accepted

**Deciders:** Workshop instructors, based on student feedback

**Tags:** tooling, performance, developer-experience

## Context

During workshop testing, we found that pip package installation was taking 2-3 minutes, which is significant in a time-constrained workshop setting. Students were spending too much time waiting for dependencies to install, reducing hands-on coding time.

Additionally, pip can have inconsistent behavior with dependency resolution, sometimes leading to conflicts that are hard to debug during a workshop.

## Decision

Replace pip with UV (by Astral) as the package manager for all Python dependency installation in the workshop.

## Considered Options

1. **UV (Astral)**: Modern, fast package installer
   - Pros:
     - 10-100x faster than pip
     - Better dependency resolution
     - Drop-in pip replacement
     - Actively maintained
     - Simple installation
   - Cons:
     - Newer tool (less familiar)
     - Additional installation step
     - Requires Rust toolchain

2. **pip (standard)**: Python's default package manager
   - Pros:
     - Universal familiarity
     - No additional installation
     - Extensive documentation
   - Cons:
     - Very slow (2-3 minutes for requirements)
     - Inconsistent dependency resolution
     - No built-in environment management

3. **Poetry**: Modern dependency management
   - Pros:
     - Good dependency resolution
     - Lock file support
     - Virtual environment management
   - Cons:
     - More complex for beginners
     - Slower than UV
     - Different command structure

## Consequences

### Positive
- Installation time reduced from 2-3 minutes to 30-60 seconds
- More consistent dependency resolution
- Students spend more time coding, less time waiting
- Better workshop experience overall
- Compatible with existing requirements.txt

### Negative
- Students must install UV first
- One more tool to learn (though commands are similar)
- May not be available on all systems by default

### Neutral
- Sets precedent for using modern tooling
- Students learn about alternative package managers

## Implementation Notes

Installation in workshop:
```bash
# One-time UV installation
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Create virtual environment
uv venv

# Install packages (replaces pip install)
uv pip install -r requirements.txt
```

All documentation updated to use UV commands:
- `pip install` → `uv pip install`
- `python -m venv env` → `uv venv`
- `.venv/` as default venv directory

## References

- [UV Documentation](https://github.com/astral-sh/uv)
- [Performance Benchmarks](https://astral.sh/blog/uv)
- Student feedback from workshop pilot

## Notes

This decision significantly improves the workshop experience by reducing wait times. The similar command structure to pip makes it easy for students to adapt, and they gain exposure to modern Python tooling.