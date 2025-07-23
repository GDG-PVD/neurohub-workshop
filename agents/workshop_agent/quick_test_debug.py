"""
Debug version of quick test to understand event structure.
Run this if you're having issues with response output.
"""

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from agent import workshop_agent
from config import AGENT_NAME

async def debug_test():
    """Run a debug test of the agent."""
    
    print("🔍 DEBUG: Workshop Agent Test")
    print("=" * 60)
    
    # Create services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    # Create session
    session = session_service.create_session(
        state={},
        app_name="workshop_agent_debug",
        user_id="debug_user"
    )
    print(f"DEBUG: Session created - ID: {session.id}")
    
    # Create runner
    runner = Runner(
        app_name="workshop_agent_debug",
        agent=workshop_agent,
        session_service=session_service,
        artifact_service=artifact_service
    )
    print("DEBUG: Runner created")
    
    # Test prompt
    prompt = "Hello! Tell me your name and one thing about neurotechnology."
    print(f"\n💬 You: {prompt}")
    print("-" * 60)
    
    # Create content object
    content = types.Content(role='user', parts=[types.Part(text=prompt)])
    print("DEBUG: Content object created")
    
    try:
        # Run agent
        print("DEBUG: Calling runner.run_async()...")
        events_async = runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=content
        )
        
        # Collect response with detailed debug info
        print("\nDEBUG: Processing events...")
        event_count = 0
        response_text = ""
        
        async for event in events_async:
            event_count += 1
            print(f"\nDEBUG: Event #{event_count}")
            print(f"  Type: {type(event).__name__}")
            print(f"  Attributes: {dir(event)}")
            
            # Try different ways to extract text
            if hasattr(event, '__dict__'):
                print(f"  Dict: {event.__dict__}")
            
            # Try various extraction methods
            extracted = False
            
            # Method 1: content.parts
            if hasattr(event, 'content') and hasattr(event.content, 'parts'):
                print("  Found: event.content.parts")
                for i, part in enumerate(event.content.parts):
                    if hasattr(part, 'text'):
                        print(f"    Part {i} text: {part.text[:100]}...")
                        response_text += part.text
                        extracted = True
            
            # Method 2: direct text
            if hasattr(event, 'text') and not extracted:
                print(f"  Found: event.text = {event.text[:100]}...")
                response_text += event.text
                extracted = True
            
            # Method 3: response attribute
            if hasattr(event, 'response') and not extracted:
                print(f"  Found: event.response = {str(event.response)[:100]}...")
                response_text += str(event.response)
                extracted = True
            
            if not extracted:
                print("  WARNING: Could not extract text from this event")
        
        print(f"\nDEBUG: Total events processed: {event_count}")
        print(f"DEBUG: Total response length: {len(response_text)} characters")
        
        print("\n" + "=" * 60)
        print(f"🤖 {AGENT_NAME}: {response_text if response_text else '[No response text extracted]'}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Starting debug test...")
    asyncio.run(debug_test())