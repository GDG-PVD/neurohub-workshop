#!/bin/bash

# NeuroHub Migration Script
# Transforms InstaVibe codebase to NeuroHub for BGU-Brown Summer School

echo "=========================================="
echo "NeuroHub Migration Script"
echo "Transforming InstaVibe → NeuroHub"
echo "=========================================="

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to report progress
report() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to warn
warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# 1. Rename main directories
echo -e "\n${BLUE}Step 1: Renaming directories...${NC}"
if [ -d "instavibe" ]; then
    mv instavibe neurohub
    report "Renamed instavibe/ → neurohub/"
else
    warn "instavibe/ directory not found"
fi

if [ -d "tools/instavibe" ]; then
    mv tools/instavibe tools/neurohub
    report "Renamed tools/instavibe/ → tools/neurohub/"
else
    warn "tools/instavibe/ directory not found"
fi

# 2. Update Python imports and references
echo -e "\n${BLUE}Step 2: Updating Python imports...${NC}"

# Update imports in all Python files
find . -name "*.py" -type f ! -path "./env/*" -exec sed -i.bak \
    -e 's/from instavibe/from neurohub/g' \
    -e 's/import instavibe/import neurohub/g' \
    -e 's/from introvertally/from neurohub_ally/g' \
    -e 's/import introvertally/import neurohub_ally/g' \
    -e 's/from ally_routes/from neurohub_routes/g' \
    -e 's/import ally_routes/import neurohub_routes/g' \
    -e 's/instavibe\./neurohub./g' \
    {} \;
report "Updated Python imports"

# 3. Update configuration files
echo -e "\n${BLUE}Step 3: Updating configuration files...${NC}"

# Update environment variables
find . -name "*.sh" -name "*.env" -name "*.yaml" -name "*.yml" -type f ! -path "./env/*" -exec sed -i.bak \
    -e 's/instavibe-graph-instance/neurohub-graph-instance/g' \
    -e 's/graphdb/neurohub-db/g' \
    -e 's/INSTAVIBE/NEUROHUB/g' \
    -e 's/InstaVibe/NeuroHub/g' \
    -e 's/instavibe/neurohub/g' \
    {} \;
report "Updated configuration files"

# 4. Rename specific files
echo -e "\n${BLUE}Step 4: Renaming specific files...${NC}"

if [ -f "neurohub/ally_routes.py" ]; then
    mv neurohub/ally_routes.py neurohub/neurohub_routes.py
    report "Renamed ally_routes.py → neurohub_routes.py"
fi

if [ -f "neurohub/introvertally.py" ]; then
    mv neurohub/introvertally.py neurohub/neurohub_ally.py
    report "Renamed introvertally.py → neurohub_ally.py"
fi

# 5. Update Dockerfiles
echo -e "\n${BLUE}Step 5: Updating Dockerfiles...${NC}"
find . -name "Dockerfile" -type f -exec sed -i.bak \
    -e 's/instavibe/neurohub/g' \
    -e 's/InstaVibe/NeuroHub/g' \
    {} \;
report "Updated Dockerfiles"

# 6. Update service names in scripts
echo -e "\n${BLUE}Step 6: Updating service names...${NC}"
find . -name "*.sh" -type f -exec sed -i.bak \
    -e 's/experiment-designer-agent/experiment-designer-agent/g' \
    -e 's/signal-processor-agent/signal-processor-agent/g' \
    -e 's/documentation-agent/documentation-agent/g' \
    -e 's/research-orchestrator/research-orchestrator/g' \
    {} \;
report "Updated service names"

# 7. Update agent directories
echo -e "\n${BLUE}Step 7: Renaming agent directories...${NC}"
if [ -d "agents/planner" ]; then
    mv agents/planner agents/experiment_designer
    report "Renamed planner/ → experiment_designer/"
fi

if [ -d "agents/social" ]; then
    mv agents/social agents/signal_processor
    report "Renamed social/ → signal_processor/"
fi

if [ -d "agents/platform_mcp_client" ]; then
    mv agents/platform_mcp_client agents/documentation
    report "Renamed platform_mcp_client/ → documentation/"
fi

if [ -d "agents/orchestrate" ]; then
    mv agents/orchestrate agents/research_orchestrator
    report "Renamed orchestrate/ → research_orchestrator/"
fi

# 8. Clean up backup files
echo -e "\n${BLUE}Step 8: Cleaning up...${NC}"
find . -name "*.bak" -type f -delete
report "Removed backup files"

# 9. Update README
echo -e "\n${BLUE}Step 9: Creating new README...${NC}"
cat > README.md << 'EOF'
# NeuroHub: Multi-Agent AI for Embodied Brain Technology

## Overview

NeuroHub is a comprehensive workshop demonstrating how to build multi-agent AI systems for neurotechnology research and development. This platform showcases the integration of Google's Agent Development Kit (ADK), Agent-to-Agent (A2A) communication protocol, and Model Context Protocol (MCP) in the context of brain-computer interfaces and biosignal analysis.

## Attribution

This workshop is adapted from Christina Lin's "Google's Agent Stack in Action: ADK, A2A, MCP on Google Cloud" codelab, originally published at https://codelabs.developers.google.com/instavibe-adk-multi-agents/. 

The original InstaVibe demo showcased multi-agent AI for social event planning. We've transformed it into NeuroHub, a platform for neurotechnology research, while maintaining the same architectural patterns and educational objectives. Used with permission from the author.

## Workshop Context

This workshop was created for the **BGU-Brown Summer School: Embodied Brain Technology Practicum** (July 18-31, 2025), a collaborative program between Brown University and Ben-Gurion University.

## Quick Start

1. Clone this repository
2. Follow the setup instructions in `docs/workshop-guide.md`
3. Deploy the agents and start experimenting!

## Documentation

- [Workshop Guide](docs/workshop-guide.md)
- [Architecture Overview](docs/architecture.md)
- [Agent Documentation](docs/agents.md)

## License

This workshop is provided for educational purposes. Please refer to the original codelab's terms and Google's ADK documentation for licensing details.
EOF
report "Created new README.md"

# 10. Create attribution file
echo -e "\n${BLUE}Step 10: Creating attribution file...${NC}"
cat > ATTRIBUTION.md << 'EOF'
# Attribution

This NeuroHub workshop is adapted from:

**Original Work:** "Google's Agent Stack in Action: ADK, A2A, MCP on Google Cloud"
**Author:** Christina Lin
**Source:** https://codelabs.developers.google.com/instavibe-adk-multi-agents/
**License:** [Refer to original codelab terms]

## Modifications

This adaptation transforms the original social event planning platform (InstaVibe) into a neurotechnology research platform (NeuroHub) for the BGU-Brown Summer School on Embodied Brain Technology.

Key transformations:
- Social profiles → Researcher profiles and expertise
- Event planning → Experiment protocol design
- Social listening → Biosignal analysis
- Platform posting → Research documentation

The core architecture, patterns, and educational approach remain faithful to the original work.

## Acknowledgments

Special thanks to Christina Lin for creating the original codelab and granting permission for this educational adaptation.
EOF
report "Created ATTRIBUTION.md"

echo -e "\n${GREEN}=========================================="
echo "Migration Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Review the changes"
echo "2. Update neurohub/setup.py with the new schema"
echo "3. Update agent implementations in agents/*"
echo "4. Update HTML templates in neurohub/templates/*"
echo "5. Test the application"
echo ""
echo "Repository ready for: git@github.com:GDG-PVD/neurohub-workshop.git"