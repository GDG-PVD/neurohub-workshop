# NeuroHub Prompt Engineering Examples

This document provides tested prompt examples for common NeuroHub development tasks. Copy and adapt these for your AI coding sessions.

## 🏗️ Project Setup and Context

### Initial Context Setting

```
I'm working on NeuroHub, a multi-agent AI platform for neurotechnology research built with:
- Python 3.11+ with type hints
- Google ADK for agents  
- A2A protocol for agent communication
- MCP for tool integration
- Flask web app with SSE
- Google Cloud Spanner with property graphs

The project structure has:
- /neurohub: Flask web application
- /agents: Individual AI agents (signal_processor, documentation, etc.)
- /tools/neurohub: MCP server with research tools
- Database entities: Researcher, Experiment, Device, SignalData, Session, Analysis
```

### Continuing a Session

```
I'm continuing work on the NeuroHub neurotechnology platform. 
Current task: [describe what you're working on]
Previous context: [what was done before]
```

## 🤖 Agent Development

### Creating a New Agent

```
Help me create a new agent for NeuroHub called "biosignal_quality_analyzer". 

Requirements:
1. Extends BaseAgent from google.genai.lib
2. Analyzes EEG/EMG/ECG signal quality
3. Returns quality metrics (SNR, artifacts, usability score)
4. Follows the pattern in agents/documentation/agent.py
5. Includes proper error handling and logging

Start by showing me the agent.py structure, then we'll implement the wrapper and A2A server.
```

### Adding Tools to an Agent

```
I need to add MCP tool access to the signal_processor agent. 

The agent should use these tools from our MCP server:
- create_analysis_report: To save analysis results
- create_session_log: To log processing sessions

Show me how to:
1. Import and configure the MCP client
2. Add tools to the agent's toolkit
3. Use the tools within the agent's process method

Reference the platform_mcp_client agent for the pattern.
```

### Implementing Sub-agents (LoopAgent)

```
Convert the signal_processor agent to use LoopAgent with sub-agents for:
1. quality_checker: Validates signal quality
2. artifact_detector: Identifies and marks artifacts  
3. feature_extractor: Extracts relevant features

Each sub-agent should:
- Have a focused responsibility
- Return structured data
- Work within the LoopAgent's iteration pattern

Base this on the social agent's multi-agent pattern.
```

## 🔧 MCP Tool Creation

### Adding a New Tool

```
Create a new MCP tool for the NeuroHub MCP server called "analyze_signal_coherence".

Requirements:
- Accepts two signal arrays and sampling rate
- Calculates coherence between signals
- Returns coherence values and dominant frequency
- Follows async pattern like other tools
- Includes proper docstring and type hints

Here's an existing tool for reference:
[paste create_experiment tool]
```

## 🗄️ Database Operations

### Complex Graph Queries

```
Write a Spanner graph query for NeuroHub that finds:
1. All researchers who have collaborated on experiments using EEG devices
2. Their h-index (count of experiments with 5+ sessions)
3. Most recent experiment date

Use the NeuroResearchGraph and return results sorted by h-index.
Include proper GQL syntax for the property graph.
```

### Adding Database Operations

```
Add a method to neurohub/db.py that:
1. Creates a new Analysis record
2. Links it to existing SignalData and Researcher
3. Updates the experiment's last_analysis_date
4. Returns the created analysis with relationships

Follow the existing transaction pattern in create_experiment().
Include error handling for missing references.
```

## 🌐 Web Interface

### Adding API Endpoints

```
Create a new Flask route in neurohub/neurohub_routes.py for:

POST /api/signal-analysis
- Accepts: signal_data (array), experiment_id, parameters
- Validates input format and experiment exists
- Calls signal_processor agent via A2A
- Returns: analysis results as JSON
- Handles errors with appropriate HTTP codes

Follow the pattern of existing API routes.
```

### SSE Implementation

```
Implement Server-Sent Events for real-time analysis updates:

1. Create /analysis/<id>/stream endpoint
2. Yield status updates as analysis progresses
3. Format events as: data: {"status": "processing", "progress": 50}
4. Handle client disconnection gracefully

Base on the existing SSE pattern in stream-protocol endpoint.
```

## 🧪 Testing

### Unit Test Generation

```
Generate comprehensive pytest tests for the signal quality analyzer function:

Function signature:
def analyze_signal_quality(signal: np.ndarray, fs: int) -> QualityMetrics:

Test cases needed:
1. Normal EEG signal (mock data)
2. Signal with artifacts
3. Empty array
4. Invalid sampling rate
5. Very long signal (performance test)

Use pytest fixtures for test data and mock any external dependencies.
```

### Integration Test

```
Write an integration test that:
1. Starts the documentation agent
2. Sends a request to create a research report
3. Verifies the report was created in the database
4. Checks the response format

Use the pattern from instavibe_test_client.py but adapt for our agent.
```

## 📚 Documentation

### README Generation

```
Based on the biosignal_quality_analyzer agent we created, generate a complete README.md following docs/templates/agent-readme.md.

Include:
- Clear purpose and capabilities
- Architecture integration
- Usage examples with actual code
- Configuration details
- Troubleshooting section

Make it specific to this agent's functionality.
```

### ADR Writing

```
Help me write an ADR for the decision to use WebSockets vs SSE for real-time updates.

Context: Need real-time signal visualization in the web UI
Decision: Chose SSE over WebSockets
Main reasons: Simpler implementation, sufficient for our needs

Format according to docs/adr/template.md
```

## 🐛 Debugging and Fixes

### Error Analysis

```
I'm getting this error in the signal_processor agent:
[paste error message]

The error occurs when: [describe when it happens]

Please:
1. Explain what's causing this error
2. Show me the problematic code section
3. Provide a fix that handles the issue properly
4. Suggest a test to prevent regression
```

### Performance Optimization

```
The experiment listing page is loading slowly. Help me optimize:

Current code:
[paste relevant code]

Requirements:
- Must maintain the same functionality  
- Should use Spanner efficiently
- Consider caching if appropriate

Explain the bottleneck and show the optimized version.
```

## 🎯 Best Practices Reminders

### Code Review Request

```
Review this code I wrote for the NeuroHub project:
[paste code]

Check for:
1. NeuroHub coding standards compliance
2. Proper error handling
3. Type hints correctness
4. Security issues
5. Performance concerns

Suggest improvements with explanations.
```

### Refactoring for Consistency

```
Refactor this function to match NeuroHub patterns:
[paste code]

Should follow:
- Our async/await patterns
- Error handling with custom exceptions
- Logging standards
- Type hints including our custom types

Show the refactored version with comments on changes.
```

## 💡 Tips for Effective Prompts

1. **Always provide context** about which part of NeuroHub you're working on
2. **Reference existing patterns** by mentioning specific files
3. **Be specific about requirements** including error handling and types
4. **Ask for explanations** when you don't understand AI suggestions
5. **Iterate on complex tasks** rather than asking for everything at once
6. **Include examples** from the codebase when asking for similar functionality

## 📝 Session Management

### Saving Context

```
Before we end this session, please summarize:
1. What we accomplished
2. Key decisions made
3. Next steps to continue
4. Any issues to resolve

Format as a markdown note I can save.
```

### Resuming Work

```
I'm resuming work on NeuroHub. Last session we:
[paste summary]

Now I need to continue with: [next task]
Please recall the context and help me proceed.
```

---

Remember: These are starting points. Adapt them to your specific needs and always review AI suggestions carefully!