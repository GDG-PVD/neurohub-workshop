# NeuroHub Workshop - Instructor Guide

This guide is for workshop instructors and teaching assistants. It provides detailed timing, common issues, and facilitation tips for running a successful NeuroHub workshop.

## 🎯 Workshop Overview

**Duration**: 3.5 hours (with breaks)
**Participants**: 10-30 developers
**Skill Level**: Intermediate Python, basic cloud knowledge
**Format**: Hands-on coding workshop

## 📋 Pre-Workshop Checklist

### 1 Week Before
- [ ] Send participants the pre-requisites email
- [ ] Verify GitHub repository is accessible
- [ ] Test the setup process end-to-end
- [ ] Prepare backup cloud project for emergencies
- [ ] Create workshop-specific Slack/Discord channel

### 1 Day Before
- [ ] Send reminder email with links
- [ ] Pre-create some GCP projects as backup
- [ ] Test all documentation links
- [ ] Prepare presentation slides
- [ ] Have backup API keys ready

### Day of Workshop
- [ ] Arrive 30 minutes early
- [ ] Test projector/screen sharing
- [ ] Open all necessary browser tabs
- [ ] Have documentation ready
- [ ] Test microphone/audio

## ⏰ Detailed Timeline

### 0:00-0:15 - Introduction & Overview (15 min)
**Goals**: Set expectations, build excitement, ensure everyone's ready

**Talk Track**:
```
"Welcome to Building Multi-Agent AI Systems with NeuroHub! 
Today you'll build a production-ready AI platform for neuroscience research.
By the end, you'll have deployed multiple AI agents that work together on Google Cloud.

We'll use:
- Google's ADK for building agents
- Spanner for graph databases  
- Cloud Run for deployment
- Real neuroscience use cases

Let's make sure everyone has:
- Google Cloud account (raise hand if not)
- Chrome browser open
- Coffee/water ready
- Questions? Ask anytime!"
```

**Actions**:
1. Share workshop links in chat
2. Do a quick poll of experience levels
3. Assign TAs to help beginners

### 0:15-1:00 - Phase 1: Setup (45 min)

**Common Issues & Solutions**:

| Time | Issue | Solution |
|------|-------|----------|
| 0:20 | "Billing not enabled" | Have corporate billing accounts ready |
| 0:25 | "Project already exists" | Add random suffix to project name |
| 0:30 | "API enablement stuck" | It's normal, takes 2-3 min |
| 0:35 | "Permission denied" | Ensure they used `chmod +x` |
| 0:40 | "UV install fails" | Use fallback: `pip install -r requirements.txt` |
| 0:45 | "Database creation fails" | Check project ID and billing |

**Checkpoint Questions**:
- "Everyone see the NeuroHub homepage?"
- "Can everyone run the graph query in Spanner?"
- "Any red errors in your terminal?"

**TA Focus Areas**:
- Watch for people stuck on billing
- Help with environment variable issues
- Ensure everyone sources set_env.sh correctly

### 1:00-1:30 - Phase 2: Understanding & First Agent (30 min)

**Demo Script**:
```
"Let me show you what we're building...
[Open NeuroHub in browser]
- Here's our research platform
- Click on Dr. Chen - see her experiments
- This EEG data could be analyzed by AI
- Let's build an agent to help researchers!

[Open agent code]
- Agents have instructions (personality)
- Tools give them abilities
- Let's test one..."
```

**Hands-On Exercise**:
```python
# Have everyone modify the documentation agent
# In agents/documentation/agent.py, line ~35:

# Change from:
"You are a documentation specialist for NeuroHub"

# To:
"You are a friendly neuroscience research assistant named NeuroBot"
```

**Common Questions**:
- "What's the difference between ADK and LangChain?" → ADK is Google's framework, more integrated with GCP
- "Can agents call other APIs?" → Yes, through tools
- "Is this production-ready?" → With proper auth and monitoring, yes

### 1:30-1:40 - Break (10 min)
- Encourage people to stand/stretch
- TAs help anyone who's behind
- Share interesting neuroscience facts

### 1:40-2:25 - Phase 3: Multi-Agent Systems (45 min)

**Key Concepts to Emphasize**:
1. **Sub-agents**: Agents can create specialized sub-agents
2. **Memory**: Agents maintain context across interactions  
3. **Coordination**: Orchestrator manages agent collaboration

**Live Coding Demo**:
```python
# Show how to add a new tool to MCP server
# In tools/neurohub/neurohub_tool_service.py:

@tool()
async def analyze_eeg_quality(
    session_id: str,
    description: str = "Check EEG signal quality"
) -> str:
    """Analyze the quality of EEG recordings."""
    # Implementation here
    return f"Signal quality for session {session_id}: Good"
```

**Group Exercise**:
"Let's trace a request through the system:
1. User asks NeuroHub Ally for help
2. Orchestrator receives request
3. Delegates to signal processor
4. Signal processor analyzes data
5. Documentation agent creates report
Who can spot where each handoff happens?"

### 2:25-2:55 - Phase 4: Deployment (30 min)

**Deployment Checklist on Screen**:
```
□ Docker builds successfully
□ Artifact Registry configured  
□ Cloud Run service deployed
□ Environment variables set
□ Service URL accessible
```

**Speed Run Option**:
If running behind, provide pre-built images:
```bash
# Instructors can share pre-built images
gcloud run deploy documentation \
  --image=us-central1-docker.pkg.dev/neurohub-workshop-demo/neurohub/documentation:latest \
  --region=us-central1
```

**Success Metrics**:
- At least one agent deployed to Cloud Run
- Web app can communicate with agent
- Participant can see agent response

### 2:55-3:15 - Phase 5: Integration & Testing (20 min)

**Final Demo**:
"Let's put it all together and help a researcher design an experiment..."

1. Open NeuroHub Ally
2. Type: "Help me design an EEG experiment for studying meditation"
3. Show agents collaborating in logs
4. Display generated experiment

**Participant Showcase**:
- Ask 2-3 participants to share screens
- Show different agent modifications
- Celebrate creative solutions

### 3:15-3:30 - Cleanup & Wrap-up (15 min)

**Essential Cleanup** (on screen):
```bash
# Save your work
zip -r ~/my-neurohub-backup.zip ~/neurohub-workshop/
cloudshell download ~/my-neurohub-backup.zip

# Quick cleanup
gcloud run services list --region=us-central1  # Note what to delete
gcloud spanner instances delete neurohub-graph-instance --quiet
```

**Closing Remarks**:
```
"Congratulations! You've built a multi-agent AI system!

You learned:
✅ Google ADK for agents
✅ Agent communication with A2A
✅ Cloud Run deployment
✅ Real-world AI applications

Next steps:
- Complete full cleanup (see guide)
- Try adding your own agent
- Explore Vertex AI Agent Builder
- Join our community [link]

Questions?"
```

## 🔧 Instructor Tools & Scripts

### Quick Environment Reset
```bash
# For helping stuck participants
cat > instructor_reset.sh << 'EOF'
#!/bin/bash
pkill -f python
cd ~/neurohub-workshop
source set_env.sh
source .venv/bin/activate
echo "Environment reset!"
EOF
```

### Participant Progress Check
```bash
# Run this to see where everyone is
cat > check_progress.sh << 'EOF'
#!/bin/bash
echo "=== Participant Progress Check ==="
echo "1. Project configured: $([ -f ~/project_id.txt ] && echo "✓" || echo "✗")"
echo "2. APIs enabled: $(gcloud services list --enabled | grep -c spanner)"
echo "3. Database exists: $(gcloud spanner databases list --instance=neurohub-graph-instance 2>/dev/null | grep -c neurohub-db)"
echo "4. Python ready: $([ -d .venv ] && echo "✓" || echo "✗")"
echo "5. App running: $(ps aux | grep -c "python app.py")"
EOF
```

### Emergency Backup Setup
If someone's environment is completely broken:
```bash
# Provide pre-configured Cloud Shell
# Have backup project IDs ready
# Share screen for pair programming
```

## 📊 Common Participant Profiles & Strategies

### The Speedster
- **Profile**: Finishes everything quickly
- **Strategy**: Give advanced challenges:
  - "Add a new node type to the graph"
  - "Create a custom visualization agent"
  - "Implement agent authentication"

### The Struggler  
- **Profile**: Having difficulty with basics
- **Strategy**: 
  - Pair with TA
  - Focus on understanding over completion
  - Use pre-built components

### The Questioner
- **Profile**: Asks detailed technical questions
- **Strategy**:
  - Answer briefly during workshop
  - Note questions for end discussion
  - Provide links for deep dives

### The Experimenter
- **Profile**: Goes off-script, tries new things
- **Strategy**:
  - Encourage creativity
  - Help merge back to main path
  - Share interesting findings with group

## 🚨 Emergency Procedures

### Critical Failure Scenarios

1. **GitHub is down**
   - Have repository ZIP file ready
   - Can share via Google Drive

2. **Spanner quota exceeded**
   - Use backup project with pre-created instance
   - Share read-only access

3. **Cloud Shell issues**
   - Direct to local development option
   - Have Codespaces backup ready

4. **API key problems**
   - Have spare Maps API keys
   - Can skip map functionality

### Partial Failure Recovery

If running significantly behind:
1. Skip to Phase 3 (First Agent)
2. Provide pre-setup environment
3. Focus on concepts over implementation
4. Share recording for full experience

## 📈 Success Metrics

Track these to improve future workshops:

### Quantitative
- % who complete Phase 1: Target 95%
- % who deploy one agent: Target 80%
- % who stay until end: Target 90%
- Average feedback score: Target 4.5/5

### Qualitative
- Energy level throughout
- Question quality/depth
- Participant collaboration
- "Aha!" moments observed

## 💡 Teaching Tips

### DO's
- ✅ Live code with participants
- ✅ Make mistakes and fix them
- ✅ Celebrate small wins
- ✅ Use participant names
- ✅ Check in regularly
- ✅ Share your screen often

### DON'Ts
- ❌ Rush through setup
- ❌ Assume knowledge
- ❌ Skip error messages
- ❌ Ignore struggling participants
- ❌ Forget about cleanup
- ❌ Run over time

### Engagement Techniques
1. **Polls**: "Raise hand if your agent responded"
2. **Pair Sharing**: "Turn to neighbor and explain what just happened"
3. **Debugging Together**: "Who can spot the error?"
4. **Celebrations**: "First deployment! 🎉"

## 📝 Post-Workshop

### Immediate (Same Day)
1. Send thank you email
2. Share recording link
3. Provide cleanup reminder
4. Request feedback

### Follow-up (Within 1 Week)
1. Share participant solutions gallery
2. Announce community channels
3. Provide advanced resources
4. Schedule office hours

### Sample Follow-up Email
```
Subject: 🧠 NeuroHub Workshop - Resources & Next Steps

Hi [Name],

Thanks for joining today's workshop! Here are your resources:

📹 Recording: [link]
📚 Slides: [link]
💻 Code: https://github.com/GDG-PVD/neurohub-workshop
🧹 Cleanup: Don't forget to delete your resources!

Next steps:
1. Complete cleanup: docs/WORKSHOP_TEARDOWN_GUIDE.md
2. Try the advanced exercises
3. Join our community: [link]

Questions? Reply to this email or join our Slack.

Happy building!
[Your name]
```

## 🔄 Continuous Improvement

### After Each Workshop
1. Review feedback forms
2. Note common issues
3. Update documentation
4. Refine timing
5. Improve examples

### Quarterly Updates
1. Update to latest ADK version
2. Refresh neuroscience examples
3. Add new agent capabilities
4. Incorporate participant projects

---
*NeuroHub Instructor Guide v1.0 | For questions: instructor-support@neurohub.dev*