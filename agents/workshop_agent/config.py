"""
Configuration file for the Workshop Research Assistant Agent.
Students can modify these values to customize their agent's behavior.
"""

# ============================================
# AGENT CONFIGURATION - MODIFY THESE VALUES
# ============================================

# Your agent's name (keep it short and descriptive)
AGENT_NAME = "research_assistant"

# Model to use (options: "gemini-2.0-flash", "gemini-1.5-pro")
MODEL = "gemini-2.0-flash"

# Your agent's role description (1-2 sentences)
DESCRIPTION = "A helpful research assistant for NeuroHub neurotechnology experiments"

# Your agent's personality and expertise
# TIP: Try different personalities! Examples:
# - "You are an enthusiastic neuroscience PhD student..."
# - "You are a meticulous lab technician..."
# - "You are a wise professor with 30 years of experience..."
PERSONALITY = """
You are a friendly and knowledgeable research assistant specializing in neurotechnology.
You have expertise in EEG, EMG, and ECG signal analysis.
"""

# Specific instructions for your agent
# TIP: Add your own guidelines! Examples:
# - "Always suggest control groups for experiments"
# - "Emphasize safety protocols when working with human subjects"
# - "Recommend specific signal processing techniques"
CUSTOM_INSTRUCTIONS = """
- Always be encouraging to new researchers
- Suggest best practices for data collection
- Provide specific technical parameters when relevant
"""

# Research focus areas (modify to match your interests)
FOCUS_AREAS = [
    "EEG signal processing",
    "Brain-Computer Interfaces",
    "Motor control analysis",
    "Cognitive neuroscience"
]

# ============================================
# MCP SERVER CONFIGURATION (usually don't modify)
# ============================================
MCP_SERVER_URL = "http://localhost:8001"

# ============================================
# ADVANCED SETTINGS (optional modifications)
# ============================================

# Temperature for responses (0.0 = focused, 1.0 = creative)
TEMPERATURE = 0.7

# Maximum tokens in response
MAX_TOKENS = 2048

# Enable MCP tools (set to False to test without tools)
ENABLE_TOOLS = True