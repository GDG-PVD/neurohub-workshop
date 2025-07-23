"""
Interactive test script - have a conversation with your agent!
Type 'quit' to exit.
"""

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from agent import workshop_agent
from config import AGENT_NAME

async def interactive_test():
    """Run an interactive session with the agent."""
    
    print(f"🤖 Interactive Session with '{AGENT_NAME}'")
    print("=" * 60)
    print("Type your questions or 'quit' to exit")
    print("=" * 60)
    
    # Create services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    # Create session
    session = await session_service.create_session()
    
    # Create runner
    runner = Runner(
        agent=workshop_agent,
        session_service=session_service,
        artifact_service=artifact_service
    )
    
    while True:
        # Get user input
        try:
            prompt = input("\n💬 You: ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        
        if prompt.lower() in ['quit', 'exit', 'bye']:
            print("\n👋 Goodbye!")
            break
        
        if not prompt:
            continue
        
        # Get agent response
        print(f"\n🤖 {AGENT_NAME} is thinking...")
        
        try:
            result = await runner.run(
                session_id=session.session_id,
                prompt=prompt
            )
            
            print(f"\n🤖 {AGENT_NAME}: {result.response}")
            
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Try again or type 'quit' to exit")

if __name__ == "__main__":
    print("Starting interactive session...")
    asyncio.run(interactive_test())