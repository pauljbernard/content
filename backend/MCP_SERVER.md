# HMH CMS MCP Server

The HMH Content Management System MCP (Model Context Protocol) Server exposes the full functionality of the HMH CMS REST API to AI assistants and MCP-compatible clients.

## What is MCP?

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) is an open protocol that standardizes how AI assistants connect to external data sources and tools. The HMH CMS MCP server allows AI assistants like Claude to:

- **Search and browse** the HMH Knowledge Base (303 files, Pre-K-12)
- **Create educational content** (lessons, assessments, activities)
- **Submit content for review** through the editorial workflow
- **Review and approve** content with ratings and feedback
- **Manage curriculum configurations** for different states and subjects
- **Access standards alignment** (TEKS, CCSS, NGSS) and instructional routines

## Features

### 13 MCP Tools

The server exposes 13 tools that wrap the REST API:

#### Authentication
- **`login`** - Authenticate with email/password to get JWT access token

#### Knowledge Base (303 Files)
- **`search_knowledge_base`** - Full-text search across all knowledge files
- **`browse_knowledge_base`** - Explore directory structure and list files
- **`get_knowledge_file`** - Retrieve specific markdown file content
- **`get_knowledge_stats`** - Get statistics (total files, subjects, states)

#### Content Management
- **`list_content`** - List content with filters (status, subject, grade, author)
- **`get_content`** - Get specific content by ID with full details
- **`create_content`** - Create new lessons, assessments, or activities
- **`submit_content_for_review`** - Submit content to editorial workflow

#### Curriculum Configuration
- **`list_curriculum_configs`** - List all curriculum configurations
- **`get_curriculum_config`** - Get specific config with resolution order

#### Editorial Workflow
- **`get_pending_reviews`** - List content awaiting review
- **`create_review`** - Create editorial review with rating (1-5) and feedback

### Resources

The server exposes MCP resources for:
- Knowledge base directory structure
- Subject areas (Math, ELA, Science, Social Studies, CS, etc.)
- Statistics and metadata

### Prompts

Template prompts for common workflows:
- **`create_lesson`** - Guide for creating standards-aligned lessons
- **`review_content`** - Guide for editorial review process

## Prerequisites

1. **Backend REST API running** on `http://localhost:8000`
   ```bash
   cd backend
   python main.py
   ```

2. **Database initialized** with demo users
   ```bash
   python init_db.py
   ```

3. **MCP dependencies installed**
   ```bash
   pip install 'mcp[cli]' httpx
   ```

## Quick Start

### Option 1: Using the Startup Script

```bash
cd backend
./start_mcp_server.sh
```

The script will:
- Check if backend REST API is running
- Verify MCP dependencies
- Display demo account credentials
- Start the MCP server

### Option 2: Manual Start

```bash
cd backend
export HMH_CMS_API_URL=http://localhost:8000
export PYTHONPATH=/Users/colossus/development/content/backend
python -m mcp_server
```

## Configuration

### For Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "hmh-cms": {
      "command": "python",
      "args": ["-m", "mcp_server"],
      "cwd": "/Users/colossus/development/content/backend",
      "env": {
        "HMH_CMS_API_URL": "http://localhost:8000",
        "PYTHONPATH": "/Users/colossus/development/content/backend"
      }
    }
  }
}
```

Or copy the provided `mcp_config.json` file:
```bash
cp backend/mcp_config.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

### For Other MCP Clients

The server follows the MCP specification and should work with any MCP-compatible client. Refer to your client's documentation for configuration instructions.

## Demo Accounts

Use these demo accounts to test the MCP server:

| Role | Email | Password | Permissions |
|------|-------|----------|-------------|
| **Admin** | admin@hmhco.com | changeme | Full system access |
| **Teacher** | teacher@example.com | teacher123 | View content, browse knowledge base |
| **Author** | author@example.com | author123 | Create/edit own content, view knowledge base |
| **Editor** | editor@example.com | editor123 | Review/approve content, manage configs |

## Usage Examples

### Example 1: Search Knowledge Base

**In Claude or MCP client:**

```
First, log in:
Tool: login
- email: author@example.com
- password: author123

Then search the knowledge base:
Tool: search_knowledge_base
- query: "Math Language Routines"
- subject: "mathematics"
```

**Response:**
```json
{
  "total_results": 8,
  "results": [
    {
      "path": "/subjects/mathematics/common/mlr/mlr1-stronger-and-clearer.md",
      "title": "MLR1: Stronger and Clearer Each Time",
      "snippet": "Students revise and refine their explanations..."
    },
    ...
  ]
}
```

### Example 2: Create a Lesson

**In Claude or MCP client:**

```
Create a 5th grade Texas math lesson on fractions:

Tool: create_content
- title: "Adding Fractions with Unlike Denominators"
- content_type: "lesson"
- subject: "mathematics"
- grade_level: "5"
- curriculum_config_id: "hmh-math-tx"
- standards: ["TEKS.5.3.K"]
- file_content: |
    # Lesson: Adding Fractions with Unlike Denominators

    ## Learning Objective
    Students will add fractions with unlike denominators using visual models and the standard algorithm.

    ## Materials
    - Fraction strips
    - Whiteboard
    - Student workbooks

    ## Lesson Flow
    [... full lesson content ...]
```

### Example 3: Review Content

**In Claude or MCP client:**

```
Get pending reviews:
Tool: get_pending_reviews

Review a specific content item:
Tool: create_review
- content_id: 42
- status: "approved"
- rating: 5
- comments: "Excellent lesson. Clear objectives, strong scaffolding for ELs, and appropriate use of MLR2 for mathematical discourse."
```

### Example 4: Browse Curriculum Configurations

**In Claude or MCP client:**

```
List all curriculum configs:
Tool: list_curriculum_configs

Get specific config details:
Tool: get_curriculum_config
- config_id: "hmh-math-tx"
```

**Response shows the 5-level knowledge resolution order:**
```json
{
  "id": "hmh-math-tx",
  "name": "HMH Math - Texas K-8",
  "subject": "mathematics",
  "district": "texas",
  "grades": ["K", "1", "2", "3", "4", "5", "6", "7", "8"],
  "knowledge_resolution": {
    "order": [
      "/reference/hmh-knowledge/subjects/mathematics/districts/texas/",
      "/reference/hmh-knowledge/subjects/mathematics/common/",
      "/reference/hmh-knowledge/districts/texas/",
      "/reference/hmh-knowledge/universal/"
    ]
  }
}
```

## Workflows

### Workflow 1: AI-Assisted Lesson Creation

1. **Login** as author
2. **Search knowledge base** for relevant standards and instructional routines
3. **Get knowledge files** for specific guidance (e.g., MLR files, TEKS standards)
4. **Create content** using the gathered knowledge
5. **Submit for review** when ready

### Workflow 2: Editorial Review

1. **Login** as editor
2. **Get pending reviews** to see what needs attention
3. **Get content** by ID to review full details
4. **Search knowledge base** to verify standards alignment
5. **Create review** with rating and feedback

### Workflow 3: Curriculum Configuration

1. **Login** as knowledge engineer (admin)
2. **List curriculum configs** to see existing configurations
3. **Get curriculum config** to understand knowledge resolution order
4. Create new configs via REST API (use frontend UI or API directly)

## Knowledge Base Structure

The MCP server provides access to the complete HMH Knowledge Base:

```
/reference/hmh-knowledge/
├── universal/                    # 15 files - ALL curricula
│   ├── frameworks/              # UDL, DOK, EB Scaffolding
│   ├── assessment/              # 8 assessment files
│   ├── accessibility/           # WCAG, CEID
│   ├── high-school/            # HS strategies, college readiness
│   ├── pre-k/                  # Pre-K pedagogy
│   └── world-languages/        # ACTFL/CEFR frameworks
│
├── subjects/                    # Subject-specific knowledge
│   ├── mathematics/
│   │   ├── common/             # 12 files - ALL math programs
│   │   │   ├── mlr/           # 8 Math Language Routines
│   │   │   └── vocab-guidelines.md
│   │   ├── districts/         # State-specific math
│   │   │   └── texas/
│   │   │       └── teks-math-alignment.md
│   │   └── high-school/       # HS math courses
│   │       ├── algebra-i-guide.md
│   │       └── ...
│   ├── ela/
│   ├── science/
│   ├── social-studies/
│   ├── computer-science/
│   ├── world-languages/
│   └── fine-arts/
│
└── districts/                   # 51 US states/districts
    ├── texas/
    │   ├── compliance/         # SBOE, IPACC
    │   └── language/           # ELPS
    ├── california/
    ├── florida/
    └── ...
```

**Total:** 303 files covering Pre-K-12, 51 states, 8 subjects, with 85-97% knowledge reuse.

## API Base URL Configuration

By default, the MCP server connects to `http://localhost:8000`. To use a different API URL:

```bash
export HMH_CMS_API_URL=http://your-api-server:port
./start_mcp_server.sh
```

Or set it in your MCP client configuration:
```json
{
  "env": {
    "HMH_CMS_API_URL": "http://your-api-server:port"
  }
}
```

## Troubleshooting

### Error: "Backend REST API is not running"

**Solution:** Start the backend first:
```bash
cd backend
python main.py
```

### Error: "ModuleNotFoundError: No module named 'mcp'"

**Solution:** Install MCP dependencies:
```bash
pip install 'mcp[cli]' httpx
```

### Error: "401 Unauthorized"

**Solution:** Login first using the `login` tool with valid credentials.

### Error: "403 Forbidden"

**Solution:** Your user role doesn't have permission for this operation. Check role requirements:
- **Teacher**: Read-only access
- **Author**: Create/edit own content
- **Editor**: Review and approve content
- **Knowledge Engineer**: Full system access

### Connection Issues

**Check if backend is running:**
```bash
curl http://localhost:8000/api/v1/health
```

Should return:
```json
{"status": "healthy", "version": "1.0.0"}
```

## Security Notes

1. **JWT Authentication**: The MCP server uses the same JWT authentication as the REST API. Tokens expire after 30 minutes.

2. **Demo Credentials**: The demo accounts listed above are for **development only**. Change these credentials in production.

3. **CORS**: The backend is configured to allow requests from localhost origins only. Update `BACKEND_CORS_ORIGINS` in `.env` for production.

4. **API Access**: The MCP server makes HTTP requests to the REST API. Ensure proper network security between components.

## Architecture

```
┌─────────────────┐
│   MCP Client    │  (Claude Desktop, etc.)
│  (AI Assistant) │
└────────┬────────┘
         │ MCP Protocol (stdio)
         ▼
┌─────────────────┐
│  MCP Server     │  (mcp_server.py)
│  (This Server)  │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│  FastAPI        │  (main.py)
│  Backend API    │
└────────┬────────┘
         │ SQLAlchemy
         ▼
┌─────────────────┐
│   SQLite DB     │  (content.db)
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ Knowledge Base  │  (303 markdown files)
└─────────────────┘
```

## Development

### Adding New Tools

To add new MCP tools, edit `mcp_server.py`:

1. Add tool definition to `list_tools()`:
```python
Tool(
    name="your_tool_name",
    description="What your tool does",
    inputSchema={
        "type": "object",
        "properties": {
            "param1": {"type": "string", "description": "Parameter description"},
        },
        "required": ["param1"]
    }
)
```

2. Add tool implementation to `call_tool()`:
```python
if name == "your_tool_name":
    # Make HTTP request to REST API
    response = await client.post(
        f"{API_BASE}/api/v1/your/endpoint",
        json={"param1": arguments["param1"]},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return [TextContent(type="text", text=response.text)]
```

### Testing

Test MCP server with the MCP Inspector:
```bash
npm install -g @modelcontextprotocol/inspector
mcp-inspector python -m mcp_server
```

Or test individual tools with curl:
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"author@example.com","password":"author123"}'

# Use token for other requests
curl http://localhost:8000/api/v1/knowledge-base/search?q=MLR \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Resources

- **MCP Specification**: https://modelcontextprotocol.io/
- **HMH CMS REST API**: See `README.md` in backend directory
- **Knowledge Base Documentation**: See `ENGINEER_GUIDE.md` in root directory
- **Author Guide**: See `AUTHOR_GUIDE.md` in root directory
- **Editor Guide**: See `EDITOR_GUIDE.md` in root directory

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the REST API documentation
3. Create an issue in the GitHub repository

## Version

- **MCP Server Version**: 1.0.0
- **HMH CMS API Version**: 1.0.0
- **MCP Protocol Version**: 2024-11-05
- **Last Updated**: 2025-11-06
