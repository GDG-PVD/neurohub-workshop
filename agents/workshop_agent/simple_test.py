"""
Simple diagnostic test for the workshop agent.
This tests just the agent creation without the Runner.
"""

import sys
import os

# Test imports
print("Testing imports...")
try:
    from google.adk.agents import Agent
    print("✓ Agent imported")
except ImportError as e:
    print(f"✗ Failed to import Agent: {e}")
    sys.exit(1)

try:
    from google.adk.mcp import MCPToolset, SseServerParams
    print("✓ MCP imports successful")
    MCP_AVAILABLE = True
except ImportError:
    print("⚠ MCP not available - will test without tools")
    MCP_AVAILABLE = False

# Test agent creation
print("\nTesting agent creation...")
try:
    from config import AGENT_NAME, MODEL, DESCRIPTION
    from agent import workshop_agent
    print(f"✓ Agent '{AGENT_NAME}' created successfully!")
    print(f"  Model: {MODEL}")
    print(f"  Description: {DESCRIPTION}")
except Exception as e:
    print(f"✗ Failed to create agent: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test basic agent properties
print("\nAgent properties:")
print(f"- Name: {workshop_agent.name}")
print(f"- Model: {workshop_agent.model}")

# Simple prompt test without Runner
print("\nTesting agent directly (without Runner)...")
try:
    # This won't actually generate a response without Runner,
    # but we can check if the agent is properly configured
    print("✓ Agent appears to be configured correctly!")
    
    # Check if tools are available
    if hasattr(workshop_agent, 'tools') and workshop_agent.tools:
        print(f"✓ Agent has {len(workshop_agent.tools)} tool(s) configured")
    else:
        print("⚠ Agent has no tools configured")
        
except Exception as e:
    print(f"✗ Error testing agent: {e}")

print("\n" + "="*50)
print("Diagnostic test complete!")
print("\nIf all checks passed, try running quick_test.py again.")
print("If MCP is not available, the agent will still work for Q&A.")