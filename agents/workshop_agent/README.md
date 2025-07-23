# Workshop Agent - Pre-built and Ready to Run!

This is a pre-built AI agent that's ready to use immediately. You can customize its behavior by modifying the `config.py` file.

## Quick Start (2 minutes)

1. **Navigate to this directory:**
   ```bash
   cd ~/neurohub-workshop/agents/workshop_agent
   ```

2. **Run the quick test:**
   ```bash
   python quick_test.py
   ```

3. **Have a conversation:**
   ```bash
   python interactive_test.py
   ```

## Customization (5 minutes)

Edit `config.py` to customize your agent:

1. **Change the personality:**
   ```python
   PERSONALITY = """
   You are an enthusiastic neuroscience PhD student who loves explaining complex concepts simply.
   """
   ```

2. **Modify focus areas:**
   ```python
   FOCUS_AREAS = [
       "Sleep research",
       "Memory consolidation",
       "Dream analysis",
       "Circadian rhythms"
   ]
   ```

3. **Add custom instructions:**
   ```python
   CUSTOM_INSTRUCTIONS = """
   - Always mention the importance of good experimental controls
   - Suggest relevant statistical analyses
   - Be extra helpful with beginners
   """
   ```

## Test Your Changes

After modifying `config.py`, run the tests again to see your customized agent:

```bash
python quick_test.py
```

## Understanding the Code

- **config.py**: All customizable settings in one place
- **agent.py**: The agent implementation (you don't need to modify this)
- **quick_test.py**: Simple test to verify the agent works
- **interactive_test.py**: Chat interface for conversations

## Troubleshooting

If you get errors:

1. **Activate the virtual environment:**
   ```bash
   source ~/neurohub-workshop/.venv/bin/activate
   ```

2. **Set environment variables:**
   ```bash
   source ~/neurohub-workshop/set_env.sh
   ```

3. **Install dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```

## Next Steps

1. Try different personalities and see how the agent responds
2. Add new focus areas related to your interests
3. Test with different types of questions
4. Move on to Module 3 to connect your agent to tools!