#!/bin/bash
# HMH CMS MCP Server Startup Script
#
# This script starts the MCP (Model Context Protocol) server for HMH CMS.
# The MCP server exposes HMH CMS functionality to AI assistants via MCP protocol.
#
# Prerequisites:
# 1. Backend REST API must be running on http://localhost:8000
# 2. Database must be initialized (run python init_db.py if needed)
# 3. MCP dependencies must be installed (pip install 'mcp[cli]' httpx)
#
# Usage:
#   ./start_mcp_server.sh                    # Start with default settings
#   HMH_CMS_API_URL=http://localhost:8000 ./start_mcp_server.sh  # Custom API URL

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL=${HMH_CMS_API_URL:-http://localhost:8000}
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}HMH CMS MCP Server Startup${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is not installed or not in PATH${NC}"
    exit 1
fi

# Check if backend REST API is running
echo -e "${YELLOW}Checking if backend REST API is running...${NC}"
if ! curl -s -f "$API_URL/api/v1/health" > /dev/null 2>&1; then
    echo -e "${RED}Error: Backend REST API is not running at $API_URL${NC}"
    echo -e "${YELLOW}Please start the backend first:${NC}"
    echo -e "  cd $SCRIPT_DIR"
    echo -e "  python main.py"
    exit 1
fi
echo -e "${GREEN}✓ Backend REST API is running${NC}"
echo ""

# Check if MCP dependencies are installed
echo -e "${YELLOW}Checking MCP dependencies...${NC}"
if ! python -c "import mcp" 2>/dev/null; then
    echo -e "${RED}Error: MCP library not installed${NC}"
    echo -e "${YELLOW}Installing MCP dependencies...${NC}"
    pip install 'mcp[cli]' httpx
fi
echo -e "${GREEN}✓ MCP dependencies installed${NC}"
echo ""

# Display configuration
echo -e "${BLUE}Configuration:${NC}"
echo -e "  API URL: $API_URL"
echo -e "  Working Directory: $SCRIPT_DIR"
echo ""

# Display demo accounts
echo -e "${BLUE}Demo Accounts (use 'login' tool first):${NC}"
echo -e "  Admin:   admin@hmhco.com / changeme"
echo -e "  Teacher: teacher@example.com / teacher123"
echo -e "  Author:  author@example.com / author123"
echo -e "  Editor:  editor@example.com / editor123"
echo ""

# Start MCP server
echo -e "${GREEN}Starting HMH CMS MCP Server...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
echo ""

cd "$SCRIPT_DIR"
export HMH_CMS_API_URL="$API_URL"
export PYTHONPATH="$SCRIPT_DIR"

python -m mcp_server
