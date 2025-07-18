# AI-Assisted Development Guide for NeuroHub

This guide demonstrates best practices for developing with AI coding assistants in the NeuroHub workshop. Follow these patterns to maximize productivity while maintaining code quality.

## 📋 Task Planning Before Coding

### Create a TODO List First

Before asking AI for help, break down your task into clear steps. This helps both you and the AI stay focused.

**Example TODO.md for Adding a New Agent:**
```markdown
# TODO: Create Biosignal Quality Analyzer Agent

- [ ] Define agent purpose and capabilities
- [ ] Create agent directory structure
- [ ] Implement base agent logic with ADK
- [ ] Add signal quality analysis methods
- [ ] Create A2A server wrapper
- [ ] Write test client
- [ ] Document agent in README
- [ ] Add to orchestrator's available agents
```

Share this with your AI assistant to establish context:
```
I'm working on the NeuroHub project. Here's my task list for creating a new biosignal quality analyzer agent:
[paste TODO list]
Let's start with the first item - defining the agent's purpose.
```

## 🎯 Effective Prompt Engineering

### Be Specific and Provide Context

**❌ Poor Prompt:**
```
Create a function to analyze signals
```

**✅ Good Prompt:**
```
In our NeuroHub project, I need a Python function for the signal_processor agent that:
1. Accepts EEG signal data as a numpy array (sampling rate 256Hz)
2. Calculates signal quality metrics (SNR, artifact detection)
3. Returns a dict with quality_score (0-100) and detected_artifacts list
4. Follows our existing pattern in agents/signal_processor/agent.py
5. Uses our SignalQuality TypedDict for return type
```

### Provide Examples from Your Codebase

**✅ Excellent Prompt:**
```
I need to create a new MCP tool for NeuroHub. Here's an existing tool as reference:

```python
@mcp_server.tool()
async def create_experiment(
    title: str,
    researcher_id: str,
    hypothesis: str,
    methodology: str
) -> str:
    """Creates a new neuroscience experiment."""
    # implementation...
```

Now create a similar tool called 'analyze_signal_quality' that:
- Takes signal_data (list of floats), sampling_rate (int)
- Returns quality metrics
- Follows the same async pattern and decorator usage
```

### Use Iterative Prompting

Instead of asking for everything at once, build incrementally:

1. **First prompt**: "Design the high-level structure for a biosignal analyzer agent"
2. **Review AI output**
3. **Second prompt**: "Good structure. Now implement the signal_quality_check method"
4. **Third prompt**: "Add error handling for invalid signal data"

## 👥 Pair Programming Mindset

### Review Everything

Treat AI suggestions like code from a junior developer. Always:

1. **Read the code line by line**
2. **Run it in a test environment first**
3. **Ask for explanations if unclear**

**Example Review Process:**
```python
# AI suggests:
def process_eeg_signal(data):
    filtered = data * 0.95  # Simple filter
    return filtered

# Your review:
"This filter seems too simple. Can you implement a proper bandpass filter 
for EEG data (0.5-50Hz) using scipy.signal? Also, add type hints."
```

### Test AI-Generated Code

**Create tests immediately:**
```
After the AI creates a function, ask:
"Now write pytest unit tests for this function that cover:
1. Normal signal input
2. Empty array input  
3. Invalid sampling rate
4. Signal with artifacts"
```

## 📐 Enforcing NeuroHub Standards

### Share Project Conventions

**Start sessions with context:**
```
I'm working on NeuroHub, a neurotechnology research platform. Key conventions:
- Python 3.11+ with type hints
- Async/await for all agent methods
- Use our custom types: ResearcherID, ExperimentID, SignalData
- Follow ADK patterns for agents
- All public methods need docstrings
- Error handling uses our custom exceptions
```

### Enforce Naming Conventions

**Be explicit about names:**
```
Create a new class following our pattern:
- Agent classes: [Purpose]Agent (e.g., SignalProcessorAgent)
- MCP tools: snake_case verbs (e.g., analyze_signal, create_report)
- Database models: Singular nouns (e.g., Researcher, Experiment)
- Test files: test_[module_name].py
```

## 📚 Documentation as You Code

### Document Decisions with ADRs

When making architectural choices with AI assistance, record them:

**Example ADR Creation Prompt:**
```
Help me write an ADR for our decision to use scipy for signal processing.
Context: We need signal filtering and analysis
Decision: Use scipy.signal instead of building custom filters
Consequences: Dependency on scipy, but reliable tested algorithms
Format: Use our ADR template in docs/adr/template.md
```

### Generate Module Documentation

**After creating new code:**
```
Based on the signal analyzer agent we just created, generate a README.md that includes:
1. Purpose and capabilities
2. Installation and dependencies
3. Usage example with code snippet
4. API reference for public methods
5. Link to related ADR-003 about signal processing choices
```

### Create Interactive Examples

**Request runnable examples:**
```
Create a Jupyter notebook cell that demonstrates using our signal analyzer:
1. Generate sample EEG data
2. Add some artifacts
3. Run the analyzer
4. Visualize the results with matplotlib
Include markdown explanations between code cells
```

## 🔄 Continuous Improvement

### Track What Works

Keep notes on effective prompts:

**prompt_library.md:**
```markdown
## Successful Prompts

### Creating ADK Agents
"Create a new ADK agent class that extends BaseAgent for [purpose].
Include: constructor with config, main process method, error handling.
Follow the pattern in agents/documentation/agent.py"

### Writing Tests
"Write comprehensive pytest tests including edge cases, mocking external 
services using unittest.mock, and async test cases with pytest-asyncio"
```

### Adjust AI Usage

**Good for AI:**
- Boilerplate code (Dockerfiles, setup.py)
- Test case generation
- Documentation drafts
- Code refactoring
- Error handling patterns

**Handle Yourself:**
- Core algorithm design
- Security-critical code
- Architecture decisions
- Performance optimization logic

## 🚀 Workshop-Specific Tips

### For Each Module

1. **Start with planning**: Write task list in comments
2. **Prompt with context**: Reference existing NeuroHub code
3. **Review carefully**: Check against workshop requirements
4. **Document immediately**: Update README while fresh
5. **Test before moving on**: Ensure it works with the system

### Example Session Flow

```markdown
1. "I'm in Module 4 of NeuroHub workshop, building the signal processor agent"
2. "Show me the existing documentation agent structure first"
3. "Now create similar structure for signal processing"
4. "Add specific methods for EEG analysis based on our requirements"
5. "Generate unit tests for the new methods"
6. "Create documentation for what we built"
7. "What should I add to the orchestrator to use this new agent?"
```

### Leverage AI for Learning

**Ask for explanations:**
```
"Explain how the A2A protocol works in this code"
"What's the purpose of nest_asyncio in our agents?"
"How does the Spanner property graph query work?"
```

## 📋 Checklist for AI-Assisted Development

Before starting a task:
- [ ] Create clear TODO list
- [ ] Gather relevant code examples
- [ ] Define success criteria

During development:
- [ ] Provide specific, contextual prompts
- [ ] Review all AI suggestions
- [ ] Test incrementally
- [ ] Ask for explanations when needed

After completing:
- [ ] Document decisions in ADRs
- [ ] Update module README
- [ ] Create runnable examples
- [ ] Add to prompt library if helpful

## 🔗 Resources

- [ADR Template](adr/template.md)
- [Module Documentation Template](templates/module-readme.md)
- [Prompt Engineering Examples](prompt-examples.md)
- [Testing Guidelines](testing-guide.md)

---

Remember: AI is your pair programmer, not your replacement. Stay engaged, review everything, and maintain ownership of the code quality!