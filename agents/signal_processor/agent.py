import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from signal_processor.neurohub import (
    get_researcher_experiments,
    get_experiment_sessions, 
    get_session_signals,
    get_signal_analyses,
    get_researcher_id_by_name,
    get_device_specifications
)
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from typing import AsyncGenerator
import logging

from google.genai import types
from google.adk.agents.callback_context import CallbackContext
from typing import Optional

# Get a logger instance
log = logging.getLogger(__name__)

class CheckCondition(BaseAgent):
    """Checks if all requested signal analyses are complete."""
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        log.info(f"Analysis summary: {ctx.session.state.get('analysis_summary')}")
        
        status = ctx.session.state.get("analysis_status", "fail").strip()
        is_done = (status == "completed")
        
        yield Event(author=self.name, actions=EventActions(escalate=is_done))

# Signal Analysis Agent - analyzes biosignal data one at a time
signal_analyzer = LlmAgent(
    name="signal_analyzer",
    model="gemini-2.5-flash",
    description=(
        "Agent that retrieves and analyzes biosignal data from experiments. "
        "Provide the researcher's name to fetch their experiments and associated signal data."
    ),
    instruction=(
        "You are a specialized agent for analyzing biosignal data from neurotechnology experiments. "
        "You'll be given researcher names to analyze their experimental data. "
        "For each researcher, you must: "
        "1. First get their ID using get_researcher_id_by_name "
        "2. Fetch their experiments using get_researcher_experiments "
        "3. For each experiment, get sessions using get_experiment_sessions "
        "4. For each session, get recorded signals using get_session_signals "
        "5. For signals of interest, get analyses using get_signal_analyses "
        "6. If needed, get device specifications using get_device_specifications "
        "Process one researcher at a time, starting with the first one on the list. "
        "Return detailed findings about signal quality, processing status, and any analyses performed."
    ),
    tools=[
        get_researcher_id_by_name,
        get_researcher_experiments,
        get_experiment_sessions,
        get_session_signals,
        get_signal_analyses,
        get_device_specifications
    ],
)

# Summary Agent - synthesizes all signal analyses into a comprehensive report
summary_agent = LlmAgent(
    name="summary_agent",
    model="gemini-2.5-flash",
    description=(
        "Generate a comprehensive technical summary of biosignal analyses. "
        "This summary should cover signal quality, experimental protocols, and key findings."
    ),
    instruction=(
        """
        Your primary task is to synthesize biosignal analysis information into a single, comprehensive technical report.
        
        **Input Scope & Default Behavior:**
        * If specific researchers are named, focus your analysis on their data.
        * If no individuals are specified, analyze all available signal data in the current context.
        
        **For each researcher's data, you must analyze:**
        1. **Signal Quality Assessment:**
           * Review quality scores for all recorded signals
           * Identify any signals with quality issues
           * Note processing status (raw, filtered, processed, analyzed)
        
        2. **Experimental Protocol Analysis:**
           * Summarize the experiments conducted
           * Note devices used and their configurations
           * Identify session patterns and durations
        
        3. **Analysis Findings:**
           * Summarize key findings from signal analyses
           * Highlight any significant patterns or anomalies
           * Note confidence scores and analysis types performed
        
        **Output Generation (Single Technical Report):**
        * Your entire output must be a single, cohesive technical summary.
        * If analyzing a single researcher: Focus on their experimental work and findings.
        * If analyzing multiple researchers: Synthesize findings across all researchers, 
          identifying common patterns, complementary techniques, or potential collaborations.
        * The report should be suitable for presentation to research teams or funding bodies.
        
        **Key Considerations:**
        * Base your summary strictly on the available data.
        * Use technical terminology appropriate for a neurotechnology audience.
        * If data is missing or sparse, briefly acknowledge this in the report.
        """
    ),
    output_key="analysis_summary"
)

# Check Agent - determines if all analyses are complete
check_agent = LlmAgent(
    name="check_agent",
    model="gemini-2.5-flash",
    description=(
        "Check if all requested biosignal analyses have been completed. "
        "Output 'completed' or 'pending'."
    ),
    output_key="analysis_status"
)

def modify_output_after_agent(callback_context: CallbackContext) -> Optional[types.Content]:
    """Callback to extract the final analysis summary after the loop completes."""
    agent_name = callback_context.agent_name
    invocation_id = callback_context.invocation_id
    current_state = callback_context.state.to_dict()
    current_user_content = callback_context.user_content
    
    print(f"[Callback] Exiting agent: {agent_name} (Inv: {invocation_id})")
    print(f"[Callback] Current analysis_status: {current_state.get('analysis_status')}")
    print(f"[Callback] Current Content: {current_user_content}")
    
    status = current_state.get("analysis_status", "").strip()
    is_done = (status == "completed")
    
    # Retrieve the final analysis summary from the state
    final_summary = current_state.get("analysis_summary")
    print(f"[Callback] final_summary: {final_summary}")
    
    if final_summary and is_done and isinstance(final_summary, str):
        log.info(f"[Callback] Found final analysis summary, constructing output Content.")
        # Construct the final output Content object to be sent back
        return types.Content(role="model", parts=[types.Part(text=final_summary.strip())])
    else:
        log.warning("[Callback] No final summary found in state or it's not a string.")
        return None

# Root Loop Agent - orchestrates the signal analysis workflow
root_agent = LoopAgent(
    name="SignalAnalysisPipeline",
    sub_agents=[
        signal_analyzer,
        summary_agent,
        check_agent,
        CheckCondition(name="Checker")
    ],
    description="Analyze biosignal data from neurotechnology experiments",
    max_iterations=10,
    after_agent_callback=modify_output_after_agent
)
