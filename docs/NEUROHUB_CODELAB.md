# NeuroHub: Multi-Agent AI for Neurotechnology Research

## What you will learn {#0}

In this codelab, you'll build NeuroHub, a comprehensive multi-agent AI platform for neurotechnology research. You'll learn how to:

- Build intelligent agents using Google's Agent Development Kit (ADK)
- Implement the Model Context Protocol (MCP) for tool integration
- Enable Agent-to-Agent (A2A) communication for complex workflows
- Deploy agents to Google Cloud Run and Vertex AI Agent Engine
- Create a complete neurotechnology research platform with AI automation

By the end of this workshop, you'll have a working system where AI agents collaborate to:
- Analyze biosignals (EEG, EMG, ECG)
- Design experiments and research protocols
- Generate documentation and reports
- Orchestrate complex research workflows

## Architecture {#1}

### AI-Powered Research with NeuroHub

NeuroHub transforms neurotechnology research by integrating multiple AI agents that work together to automate complex research tasks. The platform enables researchers to:

- Upload and analyze biosignal data
- Design experiments with AI assistance
- Automatically generate research documentation
- Collaborate with AI agents throughout the research process

### Key Architectural Elements and Technologies

**Core Technologies:**
- **Google ADK (Agent Development Kit)**: Framework for building AI agents
- **MCP (Model Context Protocol)**: Standardized tool interface for agents
- **A2A (Agent-to-Agent) Protocol**: Communication between distributed agents
- **Vertex AI**: Google's AI platform for hosting and orchestration
- **Cloud Spanner**: Distributed database for research data
- **Cloud Run**: Serverless platform for agent deployment

**NeuroHub Agents:**
1. **Signal Processor Agent**: Analyzes biosignals (EEG, EMG, ECG)
2. **Experiment Designer Agent**: Creates research protocols
3. **Documentation Agent**: Generates reports and findings
4. **Research Orchestrator**: Coordinates multi-agent workflows

### Need Google Cloud Credits?

If you're participating in the BGU-Brown Summer School or need credits for this workshop:
- Check with your workshop organizer for education credits
- Visit [Google Cloud Free Trial](https://cloud.google.com/free) for $300 in credits
- Use [Google Cloud Skills Boost](https://www.cloudskillsboost.google/) for learning credits

## Before you begin {#2}

### Prerequisites

1. **Google Cloud Project**: Create a new project or use an existing one
2. **Billing**: Enable billing (required for Spanner and Cloud Run)
3. **Cloud Shell**: We'll use Cloud Shell for all development

### Understanding the Project Structure

```
neurohub-workshop/
├── neurohub/                 # Flask web application
│   ├── app.py               # Main application
│   ├── db_neurohub.py       # SQL database queries
│   └── templates/           # UI templates
├── agents/                   # AI agents
│   ├── signal_processor/    # Biosignal analysis
│   ├── experiment_designer/ # Protocol creation
│   ├── documentation/       # Report generation
│   └── orchestrator/        # Workflow coordination
├── tools/neurohub/          # MCP tools
│   ├── mcp_server.py       # Tool server
│   └── neurohub_api.py     # Tool implementations
└── docs/                    # Documentation
```

### Setting up permission

Enable required APIs:

```bash
gcloud services enable \
  run.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  spanner.googleapis.com \
  apikeys.googleapis.com \
  iam.googleapis.com \
  compute.googleapis.com \
  aiplatform.googleapis.com \
  cloudresourcemanager.googleapis.com \
  maps-backend.googleapis.com
```

### Setup Map platform for API Keys

1. Create an API key for Maps (used for visualizing research locations):

```bash
# Create API key
export KEY_DISPLAY_NAME="NeuroHub Maps Key"
gcloud alpha services api-keys create \
  --display-name="${KEY_DISPLAY_NAME}" \
  --project="${PROJECT_ID}"

# Get the key ID
export GOOGLE_MAPS_KEY_ID=$(gcloud services api-keys list \
  --project="${PROJECT_ID}" \
  --filter="displayName='${KEY_DISPLAY_NAME}'" \
  --format="value(uid)" \
  --limit=1)

# Retrieve and save the key
export GOOGLE_MAPS_API_KEY=$(gcloud services api-keys get-key-string "${GOOGLE_MAPS_KEY_ID}" \
  --project="${PROJECT_ID}" \
  --format="value(keyString)")

echo "${GOOGLE_MAPS_API_KEY}" > ~/mapkey.txt
```

## Setup Database {#3}

### Create Spanner Instance

NeuroHub uses Cloud Spanner for storing research data with relational queries:

```bash
# Create Spanner instance
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 \
  --processing-units=100 \
  --description="NeuroHub Research Database"

# Create database
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance
```

### Load Sample Data

```bash
cd neurohub-workshop
source .venv/bin/activate
cd neurohub
python setup.py
```

This creates tables for:
- Researchers and their expertise
- Experiments and protocols
- Biosignal data recordings
- Analysis results
- Research collaborations

## Current state of NeuroHub {#4}

### Test the Base Application

1. Start the Flask application:
```bash
cd neurohub
python app.py
```

2. Access via Cloud Shell Web Preview (port 8080)

3. Explore the current features:
   - View researchers and their expertise
   - Browse experiments and protocols
   - See signal data recordings
   - Check analysis results

The application currently provides basic CRUD operations. We'll now add AI agents to automate research tasks.

## Basic Agent: Signal Processor with ADK {#5}

### ADK Framework

The Agent Development Kit (ADK) provides building blocks for creating AI agents:

- **BaseAgent**: Foundation for all agents
- **LlmAgent**: Adds language model capabilities
- **LoopAgent**: Enables iterative processing
- **Tools**: Integration with external systems

### ADK Components

Let's build our first agent - the Signal Processor:

```python
# agents/signal_processor/agent.py
from typing import Optional
from google.genai.lib import LlmAgent, adk

class SignalProcessorAgent(LlmAgent):
    AGENT_INSTRUCTION = """
    You are a biosignal analysis expert specializing in EEG, EMG, and ECG data.
    
    Your responsibilities:
    - Analyze uploaded signal data for quality and patterns
    - Identify artifacts and anomalies
    - Generate signal quality reports
    - Suggest preprocessing steps
    - Extract relevant features for research
    
    When analyzing signals:
    1. Check sampling rate and duration
    2. Assess signal quality (SNR, artifacts)
    3. Identify key patterns or events
    4. Recommend analysis approaches
    5. Generate clear, actionable reports
    """
    
    @adk.instrument(name="analyze_signal")
    async def analyze_signal(self, signal_id: str) -> str:
        """Analyze a biosignal recording."""
        # Implementation to fetch and analyze signal data
        pass
```

### Test the Signal Processor

```bash
cd agents/signal_processor
python test_agent.py
```

## Platform Interaction Agent - interact with MCP Server {#6}

### Model Context Protocol (MCP)

MCP provides a standardized way for agents to interact with external tools:

```python
# tools/neurohub/mcp_server.py
from mcp import McpServer

mcp_server = McpServer()

@mcp_server.tool()
async def create_experiment(
    title: str,
    researcher_id: str,
    hypothesis: str,
    methodology: str
) -> str:
    """Creates a new neuroscience experiment."""
    # Implementation
    
@mcp_server.tool()
async def create_analysis_report(
    signal_id: str,
    analysis_type: str,
    findings: str,
    confidence_score: float
) -> str:
    """Records analysis results."""
    # Implementation
```

## Platform Interaction Agent (using MCP) {#7}

### Documentation Agent

The Documentation Agent uses MCP tools to create research artifacts:

```python
# agents/documentation/agent.py
class DocumentationAgent(LlmAgent):
    AGENT_INSTRUCTION = """
    You are a research documentation specialist for neurotechnology.
    
    Your tasks:
    - Generate experiment reports
    - Create analysis summaries
    - Format findings for publication
    - Maintain research notebooks
    
    Use the MCP tools to:
    - create_experiment: Register new experiments
    - create_analysis_report: Document findings
    - export_findings: Generate publication-ready outputs
    """
    
    def __init__(self, mcp_client):
        super().__init__()
        self.mcp_client = mcp_client
```

## Workflow Agent and Multi-Agents in ADK {#8}

### Experiment Designer Agent

This agent creates research protocols using loop patterns:

```python
# agents/experiment_designer/agent.py
class ExperimentDesignerAgent(LoopAgent):
    AGENT_INSTRUCTION = """
    You design neuroscience experiments and research protocols.
    
    Your workflow:
    1. Understand research objectives
    2. Select appropriate devices and methods
    3. Design experimental protocols
    4. Create participant criteria
    5. Generate testing schedules
    
    Iterate until the protocol is complete and validated.
    """
    
    async def design_experiment(self, research_goal: str):
        """Design a complete experiment protocol."""
        # Uses loop to refine the design
        pass
```

## Agent-to-Agent (A2A) Communication {#9}

### Enabling A2A for NeuroHub Agents

A2A protocol enables agents to discover and communicate with each other:

```python
# agents/common/a2a_base.py
from a2a import A2AServer, AgentCard

def create_agent_card(agent_name: str, capabilities: list) -> AgentCard:
    return AgentCard(
        name=agent_name,
        description=f"NeuroHub {agent_name}",
        capabilities=capabilities,
        version="1.0.0"
    )
```

### Signal Processor Agent (A2A Enabled)

```python
# agents/signal_processor/a2a_server.py
from a2a import A2AServer
from signal_processor_agent import SignalProcessorAgent

server = A2AServer(
    agent=SignalProcessorAgent(),
    card=create_agent_card(
        "Signal Processor",
        ["analyze_eeg", "analyze_emg", "detect_artifacts"]
    )
)

if __name__ == "__main__":
    server.run(port=8003)
```

### Documentation Agent (A2A Enabled)

```python
# agents/documentation/a2a_server.py
server = A2AServer(
    agent=DocumentationAgent(mcp_client),
    card=create_agent_card(
        "Documentation",
        ["create_report", "export_findings", "generate_notebook"]
    )
)
```

### Experiment Designer Agent (A2A Enabled)

```python
# agents/experiment_designer/a2a_server.py
server = A2AServer(
    agent=ExperimentDesignerAgent(),
    card=create_agent_card(
        "Experiment Designer",
        ["design_protocol", "select_devices", "create_schedule"]
    )
)
```

## Orchestrator Agent (A2A Client) {#10}

The Research Orchestrator coordinates all other agents:

```python
# agents/orchestrator/agent.py
class ResearchOrchestratorAgent(LlmAgent):
    AGENT_INSTRUCTION = """
    You orchestrate neurotechnology research workflows by coordinating:
    - Signal Processor: For data analysis
    - Experiment Designer: For protocol creation
    - Documentation: For report generation
    
    Your workflow:
    1. Understand the research request
    2. Delegate tasks to appropriate agents
    3. Coordinate multi-step workflows
    4. Ensure proper documentation
    5. Return comprehensive results
    """
    
    def __init__(self, a2a_client):
        super().__init__()
        self.a2a_client = a2a_client
        
    async def run_research_workflow(self, request: str):
        """Orchestrate a complete research workflow."""
        # Analyze what's needed
        # Call appropriate agents via A2A
        # Coordinate results
        pass
```

### Testing the Orchestrator and the Full A2A System

1. Start all agent servers:
```bash
# Terminal 1: MCP Server
cd tools/neurohub && python mcp_server.py

# Terminal 2: Signal Processor
cd agents/signal_processor && python a2a_server.py

# Terminal 3: Documentation
cd agents/documentation && python a2a_server.py

# Terminal 4: Experiment Designer
cd agents/experiment_designer && python a2a_server.py

# Terminal 5: Orchestrator
cd agents/orchestrator && python a2a_server.py
```

2. Test with A2A Inspector:
```bash
docker run -p 5173:5173 weimeilin/a2a-inspector:latest
```

## Agent Engine and Remote Call from NeuroHub {#11}

### Deploy to Vertex AI Agent Engine

1. Create containers for each agent:
```bash
# Build and push agent containers
cd agents
gcloud builds submit --config cloudbuild.yaml
```

2. Deploy to Cloud Run:
```bash
# Deploy each agent
gcloud run deploy signal-processor \
  --image gcr.io/${PROJECT_ID}/signal-processor:latest \
  --region us-central1

# Repeat for other agents
```

3. Create Agent Engine instance:
```bash
# Deploy orchestrator to Agent Engine
gcloud agent-builder agents create neurohub-orchestrator \
  --project=${PROJECT_ID} \
  --location=us-central1 \
  --display-name="NeuroHub Research Orchestrator"
```

### Testing the Full AI-Powered NeuroHub Experience

1. Update Flask app with agent endpoints
2. Test complete workflow:
   - Upload biosignal data
   - Request AI analysis
   - Generate experiment design
   - Create documentation

### Analyzing Performance with Cloud Trace

Monitor agent performance:
```bash
# View traces
gcloud trace list --project=${PROJECT_ID}

# Check agent latencies
gcloud logging read "resource.type=cloud_run_revision" \
  --project=${PROJECT_ID} --limit=50
```

## Clean Up {#12}

### Reset environment variables

```bash
unset GOOGLE_CLOUD_PROJECT
unset SPANNER_INSTANCE_ID
unset SPANNER_DATABASE_ID
unset GOOGLE_MAPS_API_KEY
```

### Delete Agent Engine:

```bash
gcloud agent-builder agents delete neurohub-orchestrator \
  --location=us-central1
```

### Delete Cloud Run Services:

```bash
gcloud run services delete signal-processor --region=us-central1
gcloud run services delete documentation --region=us-central1
gcloud run services delete experiment-designer --region=us-central1
gcloud run services delete orchestrator --region=us-central1
```

### Stop and Remove the A2A Inspector Docker Container

```bash
docker stop a2a-inspector
docker rm a2a-inspector
```

### Delete Spanner Instance:

```bash
gcloud spanner instances delete neurohub-graph-instance
```

### Delete Artifact Registry Repository:

```bash
gcloud artifacts repositories delete neurohub-workshop \
  --location=us-central1
```

### Remove Roles from Service Account:

```bash
PROJECT_NUMBER=$(gcloud projects describe ${PROJECT_ID} --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

gcloud projects remove-iam-policy-binding ${PROJECT_ID} \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/aiplatform.user"
```

### Delete Local Workshop Files:

```bash
cd ~
rm -rf neurohub-workshop
rm mapkey.txt
rm project_id.txt
```

## Next Steps

Congratulations! You've built a complete multi-agent AI system for neurotechnology research. 

**What you've learned:**
- Building agents with Google ADK
- Implementing MCP for tool integration
- Enabling A2A communication
- Deploying to Cloud Run and Agent Engine
- Orchestrating complex AI workflows

**Further exploration:**
- Add more signal analysis algorithms
- Integrate with real biosignal devices
- Enhance the documentation generation
- Build custom visualization tools
- Create more sophisticated workflows

**Resources:**
- [Google ADK Documentation](https://github.com/google/adk)
- [MCP Specification](https://modelcontextprotocol.io/)
- [A2A Protocol](https://github.com/weimeilin79/a2a-protocol)
- [NeuroHub Repository](https://github.com/GDG-PVD/neurohub-workshop)