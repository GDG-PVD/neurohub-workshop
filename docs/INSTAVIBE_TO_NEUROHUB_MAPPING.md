# InstaVibe to NeuroHub Section Mapping

This document shows how each section of the original InstaVibe codelab maps to the NeuroHub workshop.

## Section-by-Section Mapping

| InstaVibe Section | NeuroHub Section | Key Changes |
|-------------------|------------------|-------------|
| **What you will learn** | **What you will learn** | Social events → Neurotechnology research |
| **Architecture** | **Architecture** | Social planning → Research automation |
| - AI-Powered Social Planning | - AI-Powered Research | Events/friends → Experiments/biosignals |
| - Key Architectural Elements | - Key Architectural Elements | Same tech stack, different domain |
| **Before you begin** | **Before you begin** | Added Cloud Shell focus |
| - Understanding Project Structure | - Understanding Project Structure | InstaVibe folders → NeuroHub folders |
| - Setting up permission | - Setting up permission | Same APIs required |
| - Setup Map platform | - Setup Map platform | Maps for lab locations |
| **Setup Graph Database** | **Setup Database** | Property Graph → SQL queries |
| **Current state of InstaVibe** | **Current state of NeuroHub** | Social features → Research features |
| **Basic Agent, Event Planner** | **Basic Agent: Signal Processor** | Event planning → Signal analysis |
| - ADK Framework | - ADK Framework | Same ADK concepts |
| - ADK Components | - ADK Components | Different agent purpose |
| **Platform Interaction Agent** | **Platform Interaction Agent** | Same MCP concepts |
| - Model Context Protocol | - Model Context Protocol | Different tools (experiments vs events) |
| **Platform Interaction Agent (using MCP)** | **Documentation Agent** | Posts → Research reports |
| **Workflow Agent and Multi-Agents** | **Experiment Designer Agent** | Social planning → Experiment design |
| **Agent-to-Agent Communication** | **Agent-to-Agent Communication** | Same A2A protocol |
| - Enabling A2A | - Enabling A2A | Different agent capabilities |
| - Planner Agent (A2A) | - Signal Processor (A2A) | Event planning → Signal analysis |
| - Platform Agent (A2A) | - Documentation Agent (A2A) | Social posts → Research docs |
| - Social Agent (A2A) | - Experiment Designer (A2A) | Friend analysis → Protocol design |
| **Orchestrator Agent** | **Orchestrator Agent** | Social workflow → Research workflow |
| **Agent Engine and Remote Call** | **Agent Engine and Remote Call** | Same deployment pattern |
| - Testing Full Experience | - Testing Full Experience | Social features → Research features |
| - Performance Analysis | - Performance Analysis | Same monitoring approach |
| **Clean Up** | **Clean Up** | Identical cleanup steps |

## Domain Transformations

### Data Model Changes

| InstaVibe | NeuroHub | Purpose |
|-----------|----------|---------|
| Person | Researcher | User entity |
| Event | Experiment | Main activity |
| Post | Analysis Report | Generated content |
| Friendship | Collaboration | Relationships |
| Location | Device/Lab | Physical resources |
| Attendance | Session | Participation tracking |

### Agent Transformations

| InstaVibe Agent | NeuroHub Agent | Responsibilities |
|-----------------|----------------|------------------|
| Social Profiling | Signal Processor | Analyzes data (social vs biosignals) |
| Event Planner | Experiment Designer | Creates protocols (social vs research) |
| Platform Interaction | Documentation | Generates content (posts vs reports) |
| InstaVibe Orchestrator | Research Orchestrator | Coordinates workflow |

### Tool Transformations (MCP)

| InstaVibe Tool | NeuroHub Tool | Function |
|----------------|---------------|----------|
| create_event | create_experiment | Initialize new activity |
| add_attendee | create_session | Track participation |
| create_post | create_analysis_report | Document results |
| get_friends | get_collaborators | Find connections |
| find_events | find_experiments | Search activities |

## Key Differences

1. **Database**: InstaVibe uses Property Graph (Enterprise), NeuroHub uses SQL (Standard Edition)
2. **Focus**: Social networking → Scientific research
3. **Data Types**: Text/locations → Biosignals/measurements
4. **Outputs**: Social recommendations → Research insights

## Learning Objectives Remain the Same

Despite domain changes, workshop participants learn identical concepts:
- Building agents with ADK
- Implementing MCP tools
- Enabling A2A communication
- Deploying to Cloud Run
- Using Agent Engine
- Orchestrating multi-agent workflows

The neurotechnology domain provides a more academically relevant context for the BGU-Brown Summer School while maintaining all technical learning objectives from the original InstaVibe codelab.