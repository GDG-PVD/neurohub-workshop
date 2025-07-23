"""
Quick test script to verify the agent is working.
Run this to see your agent in action!
"""

import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from agent import workshop_agent
from config import AGENT_NAME

# Test prompts to try
TEST_PROMPTS = [
    "Hello! Can you introduce yourself and tell me what you can help with?",
    "I want to design an EEG experiment to study attention. What should I consider?",
    "What's the difference between alpha and beta brain waves?",
]

async def quick_test():
    """Run a quick test of the agent."""
    
    print("🧪 Starting Workshop Agent Test")
    print("=" * 60)
    
    # Create services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    # Create session
    session = await session_service.create_session(
        app_name="workshop_agent_test",
        user_id="test_user"
    )
    
    # Create runner
    runner = Runner(
        agent=workshop_agent,
        session_service=session_service,
        artifact_service=artifact_service
    )
    
    # Test with first prompt
    prompt = TEST_PROMPTS[0]
    print(f"\n💬 You: {prompt}")
    print("-" * 60)
    
    try:
        result = await runner.run(
            session_id=session.session_id,
            prompt=prompt
        )
        
        print(f"🤖 {AGENT_NAME}: {result.response}")
        
        print("\n" + "=" * 60)
        print("✅ Success! Your agent is working!")
        print("\nTry these other prompts:")
        for i, p in enumerate(TEST_PROMPTS[1:], 1):
            print(f"{i}. {p}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you've activated the virtual environment")
        print("2. Check that you've set GOOGLE_CLOUD_PROJECT")
        print("3. Try running: source ~/neurohub-workshop/set_env.sh")

if __name__ == "__main__":
    print(f"🚀 Testing the '{AGENT_NAME}' agent...")
    asyncio.run(quick_test())