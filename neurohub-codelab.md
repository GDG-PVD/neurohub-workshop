# NeuroHub: Multi-Agent AI for Embodied Brain Technology

## A Workshop for BGU-Brown Summer School
### Adapted from "Google's Agent Stack in Action" by Christina Lin

---

## About this codelab

*Last updated: July 2025*

## 1. What you will learn

Welcome to NeuroHub! Today, we'll explore how to build multi-agent AI systems specifically designed for neurotechnology research and brain-computer interface development. This workshop transforms Christina Lin's excellent social media planning demo into a cutting-edge platform for the neurotech community.

### The Challenge in Neurotechnology Research

Imagine you're part of a research team developing brain-computer interfaces or analyzing biosignals. The challenges are immense:
- Processing vast amounts of EEG, EMG, or other biosignal data
- Designing rigorous experimental protocols
- Collaborating across disciplines and institutions
- Documenting findings in publication-ready formats
- Managing complex equipment configurations

This is precisely where intelligent agents can revolutionize neurotechnology research!

### What You'll Build

![NeuroHub Architecture](neurohub-architecture.png)

**Foundations with Google's ADK:** Master building intelligent agents for biosignal analysis using Google's Agent Development Kit (ADK).

**Extending with Model Context Protocol (MCP):** Equip agents with specialized neurotechnology tools for data processing, experiment design, and documentation.

**Multi-Agent Orchestration:** Design workflows where agents collaborate on complex research tasks - from signal analysis to publication preparation.

**Agent-to-Agent (A2A) Communication:** Enable distributed agents to work together, sharing findings and coordinating research activities.

**Cloud Deployment:** Deploy your neurotech AI system on Google Cloud Platform for scalable, production-ready research tools.

## 2. Architecture

### You're on the NeuroHub Research Team

Imagine you work at a cutting-edge neurotechnology research center participating in the BGU-Brown Summer School. Your team is developing next-generation brain-computer interfaces and needs to:
- Analyze complex biosignal data from multiple experiments
- Design new experimental protocols based on emerging research
- Document and share findings with the global research community
- Collaborate effectively across disciplines

### An Agent-Based Solution for Neurotechnology

You propose developing a multi-agent system to accelerate research:

![NeuroHub Use Case](neurohub-usecase.png)

* **Signal Processing Agent**: Analyzes biosignal data (EEG, EMG, ECG) from experiments, identifying patterns, anomalies, and quality metrics. Uses graph queries to understand the complete data lineage from experiment → session → signal → analysis.

* **Experiment Designer Agent**: Creates research protocols based on current literature and best practices. Searches for validated paradigms, suggests equipment configurations, and generates comprehensive experimental designs.

* **Documentation Agent (using MCP)**: Takes research findings and creates publication-ready documentation. Uses MCP tools to interact with the NeuroHub platform, creating experiment records, analysis reports, and formatted exports.

* **Orchestrator Agent**: Coordinates the research workflow. Receives requests like "analyze all motor imagery experiments from last month" and delegates tasks to specialized agents, ensuring comprehensive analysis and documentation.

### Key Architectural Elements and Technologies

![Architecture Details](neurohub-architecture-detail.png)

**Google Cloud Platform (GCP):**
* **Vertex AI**: Gemini models power agent reasoning
* **Cloud Run**: Hosts agents and the NeuroHub web application
* **Spanner**: Graph database for research relationships
* **Agent Engine**: Managed service for the orchestrator

**Core Frameworks:**
* **ADK**: Agent Development Kit for building intelligent agents
* **A2A Protocol**: Agent-to-Agent communication standard
* **MCP**: Model Context Protocol for tool integration

**Database Schema:**
Instead of social relationships, we model:
- Researchers and their collaborations
- Experiments and protocols
- Biosignal data and analyses
- Devices and configurations
- Publications and findings

## 3. Before you begin

### Workshop Context

This workshop was created for the **BGU-Brown Summer School: Embodied Brain Technology Practicum** (July 18-31, 2025). It's designed to give you hands-on experience with:
- Real neurotechnology workflows
- Multi-agent AI systems
- Cloud deployment strategies
- Collaborative research tools

### Prerequisites

- Google Cloud Project with billing enabled
- Basic Python knowledge
- Interest in neurotechnology and brain-computer interfaces
- No prior AI agent experience required!

[Setup instructions remain the same as the original, just updating names from instavibe to neurohub]

## 4. Setup Graph Database

Before we can build our intelligent agents, we need a way to store and understand the complex relationships in neurotechnology research. This includes connections between:
- Researchers and their collaborations
- Experiments and the signals they generate
- Devices and their configurations
- Analyses and their findings

We'll use Google Cloud Spanner's graph capabilities to model these relationships.

### Creating the NeuroHub Schema

```bash
. ~/neurohub-bootstrap/set_env.sh
export SPANNER_INSTANCE_ID="neurohub-graph-instance"
export SPANNER_DATABASE_ID="neurohub-db"

gcloud spanner instances create $SPANNER_INSTANCE_ID \
  --config=regional-us-central1 \
  --description="NeuroHub Research Graph Database" \
  --processing-units=100 \
  --edition=ENTERPRISE

gcloud spanner databases create $SPANNER_DATABASE_ID \
  --instance=$SPANNER_INSTANCE_ID \
  --database-dialect=GOOGLE_STANDARD_SQL
```

### Understanding the Research Graph

Our graph models neurotechnology research relationships:

**Nodes:**
- **Researcher**: Scientists and their expertise
- **Experiment**: Research protocols and studies
- **Device**: EEG, EMG, and other equipment
- **SignalData**: Recorded biosignals
- **Analysis**: Processing results and findings

**Edges:**
- **Collaboration**: Researchers working together
- **Leads**: PI leading experiments
- **RecordedWith**: Signals recorded using devices
- **Analyzes**: Analyses performed on signals

### Sample Graph Queries

Find all experiments using EEG devices:
```sql
Graph NeuroResearchGraph
MATCH (e:Experiment)-[:Uses]->(d:Device)
WHERE d.device_type = 'EEG'
RETURN e.name, e.status, d.name
```

Trace data lineage for an experiment:
```sql
Graph NeuroResearchGraph
MATCH path = (e:Experiment)<-[:PartOf]-(s:Session)<-[:RecordedIn]-(sig:SignalData)
WHERE e.name = 'Motor Imagery BCI Training'
RETURN SAFE_TO_JSON(path) AS data_lineage
```

## 5. Current State of NeuroHub

Let's deploy the NeuroHub web application to see what our agents will enhance:

![NeuroHub Homepage](neurohub-home.png)

The application provides:
- **Experiment Dashboard**: View active research projects
- **Signal Quality Metrics**: Monitor data collection
- **Researcher Profiles**: Expertise and collaborations
- **Analysis Reports**: Findings and publications

### Building and Deploying NeuroHub

```bash
. ~/neurohub-bootstrap/set_env.sh
cd ~/neurohub-bootstrap/neurohub/

# Build the container
gcloud builds submit . \
  --tag=${IMAGE_PATH} \
  --project=${PROJECT_ID}

# Deploy to Cloud Run
gcloud run deploy neurohub \
  --image=${IMAGE_PATH} \
  --platform=managed \
  --region=${REGION} \
  --allow-unauthenticated \
  --set-env-vars="SPANNER_INSTANCE_ID=${SPANNER_INSTANCE_ID}" \
  --set-env-vars="SPANNER_DATABASE_ID=${SPANNER_DATABASE_ID}" \
  --project=${PROJECT_ID}
```

## 6. Building Your First Agent: Experiment Designer

Now let's build our first intelligent agent using ADK. The Experiment Designer agent helps researchers create rigorous protocols for neurotechnology studies.

### Understanding ADK Components

![ADK Agent Structure](adk-structure.png)

An ADK agent consists of:
- **Model**: The LLM brain (Gemini 2.0 Flash)
- **Instructions**: What the agent should do
- **Tools**: Capabilities like web search
- **State**: Memory during execution

### Creating the Experiment Designer

In `~/neurohub-bootstrap/agents/experiment_designer/agent.py`:

```python
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="experiment_designer",
    model="gemini-2.0-flash",
    description="Agent specialized in designing neurotechnology experiments",
    instruction="""
        You are a specialized AI assistant for designing neurotechnology experiments.
        
        Given a research area (e.g., Motor Imagery, Stress Detection), duration, 
        and target biosignals (EEG, EMG, ECG), generate a comprehensive protocol.
        
        Search for:
        - Recent papers and validated paradigms
        - Appropriate analysis methods
        - Open-source implementations
        - Equipment recommendations
        
        Return a structured JSON with:
        - Research question and hypothesis
        - Participant criteria
        - Equipment configuration
        - Session structure and tasks
        - Analysis pipeline
        - Ethical considerations
        - Timeline and budget
    """,
    tools=[google_search]
)
```

### Testing with ADK Dev UI

```bash
cd ~/neurohub-bootstrap/agents
adk web
```

Try this prompt:
```
Design a 4-week motor imagery BCI experiment using EEG
```

The agent will search current research and generate a complete protocol!

[Continue with remaining sections, transforming each InstaVibe concept to NeuroHub...]