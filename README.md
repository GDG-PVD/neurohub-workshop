# NeuroHub: Multi-Agent AI for Embodied Brain Technology

## Overview

NeuroHub is a comprehensive workshop demonstrating how to build multi-agent AI systems for neurotechnology research and development. This platform showcases the integration of Google's Agent Development Kit (ADK), Agent-to-Agent (A2A) communication protocol, and Model Context Protocol (MCP) in the context of brain-computer interfaces and biosignal analysis.

## Attribution

This workshop is adapted from Christina Lin's "Google's Agent Stack in Action: ADK, A2A, MCP on Google Cloud" codelab, originally published at https://codelabs.developers.google.com/instavibe-adk-multi-agents/. 

The original InstaVibe demo showcased multi-agent AI for social event planning. We've transformed it into NeuroHub, a platform for neurotechnology research, while maintaining the same architectural patterns and educational objectives. Used with permission from the author.

## Workshop Context

This workshop was created for the **BGU-Brown Summer School: Embodied Brain Technology Practicum** (July 18-31, 2025), a collaborative program between Brown University and Ben-Gurion University focusing on:
- Neurotechnology development
- Brain-computer interfaces
- Biosignal processing
- Entrepreneurship in neurotech

## What You'll Learn

1. **Foundations with Google's ADK**: Build intelligent agents for biosignal analysis and experiment design
2. **Model Context Protocol (MCP)**: Create tools for data processing and research documentation
3. **Agent Orchestration**: Design workflows for complex research tasks
4. **A2A Communication**: Enable collaboration between distributed research agents
5. **Cloud Deployment**: Deploy your multi-agent system on Google Cloud Platform

## Architecture Overview

NeuroHub transforms the original social media architecture into a neurotechnology research platform:

### Original InstaVibe → NeuroHub Transformation

| InstaVibe Component | NeuroHub Component | Purpose |
|---------------------|-------------------|----------|
| Social Profiling Agent | Signal Processing Agent | Analyzes EEG, EMG, and other biosignals |
| Event Planning Agent | Experiment Designer Agent | Creates research protocols and schedules |
| Platform Interaction Agent | Documentation Agent | Generates research reports and findings |
| Posts & Events | Signal Data & Experiments | Research data and experimental protocols |
| Friends Network | Research Collaborations | Team connections and expertise |

### Key Components

1. **Signal Processing Agent**
   - Analyzes uploaded biosignal data (EEG, EMG, heart rate)
   - Identifies patterns and anomalies
   - Generates signal quality reports
   - Tracks signal → experiment → researcher relationships

2. **Experiment Designer Agent**
   - Creates experimental protocols based on research goals
   - Suggests equipment configurations
   - Generates testing schedules
   - Recommends participant criteria

3. **Documentation Agent**
   - Creates formatted research notebooks
   - Generates experiment reports
   - Publishes findings to the platform
   - Exports data for publication

4. **Orchestrator Agent**
   - Coordinates multi-step research workflows
   - Manages data flow between agents
   - Ensures proper documentation of all activities

## Technical Stack

- **Google Cloud Platform**: Vertex AI, Cloud Run, Spanner (Standard Edition), Agent Engine
- **Frameworks**: Google ADK, A2A Protocol, MCP
- **Database**: Spanner with SQL queries for research relationships
- **Language Models**: Gemini 2.0 Flash
- **Development Environment**: Google Cloud Shell (cloud-native)

## Prerequisites

- Google Cloud Project with billing enabled
- Basic knowledge of Python and cloud services
- Understanding of AI agents and LLMs
- Interest in neurotechnology applications

## Quick Start (Google Cloud Shell)

1. Open Cloud Shell: [![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/GDG-PVD/neurohub-workshop&page=editor&open_in_editor=README.md)
2. Run the initialization: `bash init.sh && source set_env.sh`
3. Follow the [Workshop Guide](docs/WORKSHOP_GUIDE.md) or [Cloud Shell Guide](docs/CLOUD_SHELL_GUIDE.md)
4. Access the app via Cloud Shell's Web Preview on port 8080

## Documentation

### 🎯 Essential Workshop Guides
- [**Workshop Master Guide**](docs/WORKSHOP_MASTER_GUIDE.md) - Complete workshop flow and overview
- [**Complete Setup Guide**](docs/WORKSHOP_COMPLETE_SETUP_GUIDE.md) - Detailed step-by-step GCP setup
- [**Troubleshooting Guide**](docs/WORKSHOP_TROUBLESHOOTING_GUIDE.md) - Comprehensive solutions to common issues
- [**Teardown Guide**](docs/WORKSHOP_TEARDOWN_GUIDE.md) - Complete cleanup and resource removal
- [**Instructor Guide**](docs/WORKSHOP_INSTRUCTOR_GUIDE.md) - For workshop facilitators and TAs

### 📚 Workshop Materials
- [**NeuroHub Codelab**](docs/NEUROHUB_CODELAB.md) - Complete step-by-step workshop following the codelab format
- [**Workshop Guide**](docs/WORKSHOP_GUIDE.md) - Quick reference guide for the workshop
- [**Cloud Shell Guide**](docs/CLOUD_SHELL_GUIDE.md) - Cloud-native development instructions
- [**Quick Reference**](docs/QUICK_REFERENCE.md) - Command cheat sheet
- [**Setup Checklist**](docs/SETUP_CHECKLIST.md) - Pre-workshop verification
- [**Detailed Setup Guide**](docs/DETAILED_SETUP_GUIDE.md) - Comprehensive setup with screenshots
- [**Troubleshooting Guide**](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [**InstaVibe to NeuroHub Mapping**](docs/INSTAVIBE_TO_NEUROHUB_MAPPING.md) - How we adapted the original codelab

### 🤖 Development Guides
- [**AI Development Guide**](docs/AI_DEVELOPMENT_GUIDE.md) - Best practices for AI-assisted coding
- [**Prompt Examples**](docs/prompt-examples.md) - Tested prompts for NeuroHub development
- [**C4 Architecture**](C4_ARCHITECTURE.md) - System architecture diagrams
- [**Decision Registry**](DECISION_REGISTRY.md) - Quick reference for all decisions

### 📐 Architecture Decisions
- [**ADR Index**](docs/adr/index.md) - All architecture decision records
- [**ADR Template**](docs/adr/template.md) - Template for new decisions

### 📝 Templates
- [**Module README Template**](docs/templates/module-readme.md)
- [**Agent README Template**](docs/templates/agent-readme.md)

## Use Cases

- **Research Teams**: Collaborate on biosignal analysis projects
- **Students**: Learn about brain-computer interfaces through hands-on development
- **Startups**: Prototype neurotechnology applications rapidly
- **Hackathons**: Build innovative brain-tech solutions

## Contributing

This is an educational workshop. Feel free to fork and adapt for your own neurotechnology projects!

## License

This workshop is provided for educational purposes. Please refer to the original codelab's terms and Google's ADK documentation for licensing details.

## Acknowledgments

Special thanks to:
- Christina Lin for creating the original InstaVibe codelab
- The BGU-Brown Summer School organizing team
- Google's ADK team for the excellent framework