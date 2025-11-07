"""
MCP Server for HMH Content Management System

This MCP server exposes the HMH CMS functionality to MCP clients,
allowing AI assistants to interact with the knowledge base and content management system.
"""
import asyncio
import os
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, Resource, TextContent, ImageContent, EmbeddedResource
import httpx

# MCP Server instance
app = Server("hmh-cms-server")

# API base URL
API_BASE = os.getenv("HMH_CMS_API_URL", "http://localhost:8000")
API_V1 = f"{API_BASE}/api/v1"

# Authentication token storage
_auth_token: Optional[str] = None


async def get_auth_token() -> Optional[str]:
    """Get the current authentication token."""
    return _auth_token


async def set_auth_token(token: str):
    """Set the authentication token."""
    global _auth_token
    _auth_token = token


async def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None
) -> Dict[str, Any]:
    """Make an HTTP request to the HMH CMS API."""
    headers = {}
    if _auth_token:
        headers["Authorization"] = f"Bearer {_auth_token}"

    url = f"{API_V1}{endpoint}"

    async with httpx.AsyncClient() as client:
        if method == "GET":
            response = await client.get(url, params=params, headers=headers)
        elif method == "POST":
            response = await client.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = await client.put(url, json=data, headers=headers)
        elif method == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()
        return response.json()


# ============================================================================
# TOOLS - Expose CMS operations as MCP tools
# ============================================================================

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name="login",
            description="Authenticate with the HMH CMS system using email and password. Returns access token for subsequent operations.",
            inputSchema={
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "User email address"
                    },
                    "password": {
                        "type": "string",
                        "description": "User password"
                    }
                },
                "required": ["email", "password"]
            }
        ),
        Tool(
            name="search_knowledge_base",
            description="Search the HMH knowledge base (303 files across Pre-K-12). Searches across subjects, states, and categories.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Filter by subject (mathematics, ela, science, etc.)"
                    },
                    "state": {
                        "type": "string",
                        "description": "Filter by state (texas, california, florida, etc.)"
                    }
                }
            }
        ),
        Tool(
            name="browse_knowledge_base",
            description="Browse the knowledge base directory structure. Returns files and subdirectories at the specified path.",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to browse (empty for root)"
                    }
                }
            }
        ),
        Tool(
            name="get_knowledge_file",
            description="Retrieve the full content of a knowledge base file (markdown format).",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Relative path to the file"
                    }
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="get_knowledge_stats",
            description="Get statistics about the knowledge base (file counts by category, subject, state).",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="list_content",
            description="List authored content (lessons, assessments, activities). Supports filtering by status, type, subject.",
            inputSchema={
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "Filter by status (draft, in_review, approved, published)"
                    },
                    "content_type": {
                        "type": "string",
                        "description": "Filter by type (lesson, assessment, activity)"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Filter by subject"
                    },
                    "grade_level": {
                        "type": "string",
                        "description": "Filter by grade level"
                    }
                }
            }
        ),
        Tool(
            name="get_content",
            description="Get a specific content item by ID with full details.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content_id": {
                        "type": "integer",
                        "description": "Content ID"
                    }
                },
                "required": ["content_id"]
            }
        ),
        Tool(
            name="create_content",
            description="Create new content (lesson, assessment, or activity). Requires author role or higher.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Content title"
                    },
                    "content_type": {
                        "type": "string",
                        "enum": ["lesson", "assessment", "activity"],
                        "description": "Type of content"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Subject area (mathematics, ela, science, etc.)"
                    },
                    "grade_level": {
                        "type": "string",
                        "description": "Grade level (K, 1-12)"
                    },
                    "file_content": {
                        "type": "string",
                        "description": "Content body (markdown format)"
                    },
                    "learning_objectives": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of learning objectives"
                    },
                    "standards_aligned": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of educational standards (TEKS, CCSS, NGSS, etc.)"
                    }
                },
                "required": ["title", "content_type", "subject", "file_content"]
            }
        ),
        Tool(
            name="submit_content_for_review",
            description="Submit content for editorial review. Changes status from draft to in_review.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content_id": {
                        "type": "integer",
                        "description": "Content ID to submit"
                    }
                },
                "required": ["content_id"]
            }
        ),
        Tool(
            name="list_curriculum_configs",
            description="List all curriculum configurations (defines how content inherits from knowledge base).",
            inputSchema={
                "type": "object",
                "properties": {
                    "subject": {
                        "type": "string",
                        "description": "Filter by subject"
                    },
                    "district": {
                        "type": "string",
                        "description": "Filter by district/state"
                    }
                }
            }
        ),
        Tool(
            name="get_curriculum_config",
            description="Get a specific curriculum configuration with knowledge resolution order.",
            inputSchema={
                "type": "object",
                "properties": {
                    "config_id": {
                        "type": "string",
                        "description": "Configuration ID (e.g., 'hmh-math-tx')"
                    }
                },
                "required": ["config_id"]
            }
        ),
        Tool(
            name="get_pending_reviews",
            description="Get list of content pending editorial review. Requires editor role or higher.",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="create_review",
            description="Create an editorial review for content. Requires editor role or higher.",
            inputSchema={
                "type": "object",
                "properties": {
                    "content_id": {
                        "type": "integer",
                        "description": "Content ID to review"
                    },
                    "status": {
                        "type": "string",
                        "enum": ["approved", "needs_revision", "rejected"],
                        "description": "Review decision"
                    },
                    "comments": {
                        "type": "string",
                        "description": "Review feedback and comments"
                    },
                    "rating": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 5,
                        "description": "Quality rating (1-5 stars)"
                    }
                },
                "required": ["content_id", "status"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Execute an MCP tool."""
    try:
        # Authentication
        if name == "login":
            # Special handling for login - use form data
            form_data = f"username={arguments['email']}&password={arguments['password']}"
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_V1}/auth/login",
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    content=form_data
                )
                response.raise_for_status()
                tokens = response.json()
                await set_auth_token(tokens["access_token"])
                return [
                    TextContent(
                        type="text",
                        text=f"✓ Successfully authenticated\nAccess token stored for subsequent operations."
                    )
                ]

        # Knowledge Base Operations
        elif name == "search_knowledge_base":
            result = await make_request("GET", "/search/", params=arguments)
            return [TextContent(type="text", text=f"Search Results:\n{result}")]

        elif name == "browse_knowledge_base":
            path = arguments.get("path", "")
            result = await make_request("GET", "/knowledge/browse", params={"path": path})
            return [TextContent(type="text", text=f"Directory Contents:\n{result}")]

        elif name == "get_knowledge_file":
            result = await make_request("GET", "/knowledge/file", params={"path": arguments["path"]})
            return [TextContent(type="text", text=f"File: {result['name']}\n\n{result['content']}")]

        elif name == "get_knowledge_stats":
            result = await make_request("GET", "/knowledge/stats")
            return [TextContent(type="text", text=f"Knowledge Base Statistics:\n{result}")]

        # Content Operations
        elif name == "list_content":
            result = await make_request("GET", "/content/", params=arguments)
            return [TextContent(type="text", text=f"Content List:\n{result}")]

        elif name == "get_content":
            result = await make_request("GET", f"/content/{arguments['content_id']}")
            return [TextContent(type="text", text=f"Content Details:\n{result}")]

        elif name == "create_content":
            result = await make_request("POST", "/content/", data=arguments)
            return [TextContent(type="text", text=f"✓ Content created:\n{result}")]

        elif name == "submit_content_for_review":
            result = await make_request("POST", f"/content/{arguments['content_id']}/submit")
            return [TextContent(type="text", text=f"✓ Content submitted for review:\n{result}")]

        # Curriculum Config Operations
        elif name == "list_curriculum_configs":
            result = await make_request("GET", "/curriculum-configs/", params=arguments)
            return [TextContent(type="text", text=f"Curriculum Configurations:\n{result}")]

        elif name == "get_curriculum_config":
            result = await make_request("GET", f"/curriculum-configs/{arguments['config_id']}")
            return [TextContent(type="text", text=f"Configuration:\n{result}")]

        # Review Operations
        elif name == "get_pending_reviews":
            result = await make_request("GET", "/reviews/pending")
            return [TextContent(type="text", text=f"Pending Reviews:\n{result}")]

        elif name == "create_review":
            result = await make_request("POST", "/reviews/", data=arguments)
            return [TextContent(type="text", text=f"✓ Review created:\n{result}")]

        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get("detail", str(e))
        return [TextContent(type="text", text=f"API Error: {error_detail}")]
    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


# ============================================================================
# RESOURCES - Expose knowledge base files as MCP resources
# ============================================================================

@app.list_resources()
async def list_resources() -> List[Resource]:
    """List available knowledge base resources."""
    try:
        # Get knowledge base statistics to show available resources
        result = await make_request("GET", "/knowledge/stats")

        resources = [
            Resource(
                uri="hmh://knowledge/stats",
                name="Knowledge Base Statistics",
                description=f"Statistics about the 303 knowledge files: {result.get('total_files', 0)} files across {result.get('total_subjects', 0)} subjects and {result.get('total_states', 0)} states",
                mimeType="application/json"
            ),
            Resource(
                uri="hmh://knowledge/subjects/mathematics",
                name="Mathematics Knowledge",
                description="All mathematics knowledge files (MLRs, problem-solving frameworks, vocabulary guidelines)",
                mimeType="text/markdown"
            ),
            Resource(
                uri="hmh://knowledge/subjects/ela",
                name="ELA Knowledge",
                description="All ELA knowledge files (close reading, literacy routines, annotation strategies)",
                mimeType="text/markdown"
            ),
            Resource(
                uri="hmh://knowledge/subjects/science",
                name="Science Knowledge",
                description="All science knowledge files (NGSS alignment, science practices, investigation frameworks)",
                mimeType="text/markdown"
            ),
            Resource(
                uri="hmh://knowledge/universal",
                name="Universal Knowledge",
                description="Universal frameworks applicable to all curricula (UDL, DOK, EB Scaffolding, WCAG, Assessment)",
                mimeType="text/markdown"
            )
        ]

        return resources
    except Exception as e:
        # Return minimal resources if API is unavailable
        return [
            Resource(
                uri="hmh://knowledge/info",
                name="Knowledge Base Information",
                description="HMH Multi-Curriculum Knowledge Base with 303 files",
                mimeType="text/plain"
            )
        ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a knowledge base resource."""
    if uri == "hmh://knowledge/stats":
        result = await make_request("GET", "/knowledge/stats")
        import json
        return json.dumps(result, indent=2)

    elif uri.startswith("hmh://knowledge/"):
        # Extract path from URI
        path = uri.replace("hmh://knowledge/", "")
        result = await make_request("GET", "/knowledge/browse", params={"path": path})
        import json
        return json.dumps(result, indent=2)

    else:
        raise ValueError(f"Unknown resource URI: {uri}")


# ============================================================================
# PROMPTS - Provide helpful prompt templates
# ============================================================================

@app.list_prompts()
async def list_prompts():
    """List available prompt templates."""
    from mcp.types import Prompt, PromptArgument

    return [
        Prompt(
            name="create_lesson",
            description="Create a standards-aligned lesson using knowledge base guidance",
            arguments=[
                PromptArgument(
                    name="subject",
                    description="Subject (mathematics, ela, science, etc.)",
                    required=True
                ),
                PromptArgument(
                    name="grade",
                    description="Grade level (K, 1-12)",
                    required=True
                ),
                PromptArgument(
                    name="topic",
                    description="Lesson topic",
                    required=True
                ),
                PromptArgument(
                    name="state",
                    description="State for standards alignment (texas, california, etc.)",
                    required=False
                )
            ]
        ),
        Prompt(
            name="review_content",
            description="Review content for quality using editorial guidelines",
            arguments=[
                PromptArgument(
                    name="content_id",
                    description="Content ID to review",
                    required=True
                )
            ]
        )
    ]


@app.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str]):
    """Get a prompt template filled with arguments."""
    from mcp.types import PromptMessage, TextContent as PromptTextContent

    if name == "create_lesson":
        subject = arguments["subject"]
        grade = arguments["grade"]
        topic = arguments["topic"]
        state = arguments.get("state", "")

        state_info = f" for {state}" if state else ""

        prompt_text = f"""You are creating a {grade} grade {subject} lesson on {topic}{state_info}.

Follow these steps:

1. First, search the knowledge base for relevant guidance:
   - Use search_knowledge_base tool with query="{topic}" and subject="{subject}"
   - Get universal frameworks (UDL, DOK, EB Scaffolding)
   - Get subject-specific routines (MLRs for math, literacy routines for ELA)

2. Create the lesson using create_content tool with:
   - Title: Clear, descriptive title
   - Content type: "lesson"
   - Subject: "{subject}"
   - Grade level: "{grade}"
   - Learning objectives: 3-5 measurable objectives using Bloom's taxonomy
   - Standards aligned: Relevant standards (TEKS, CCSS, NGSS)
   - File content: Lesson formatted in markdown with:
     * Introduction/Hook
     * Learning objectives
     * Materials needed
     * Instructional activities (with UDL and subject routines)
     * Formative assessment
     * Differentiation strategies
     * EB scaffolding for emergent bilinguals

3. After creating, submit for review using submit_content_for_review tool.

Create a high-quality, standards-aligned lesson following these guidelines."""

        return PromptMessage(
            role="user",
            content=PromptTextContent(type="text", text=prompt_text)
        )

    elif name == "review_content":
        content_id = arguments["content_id"]

        prompt_text = f"""Review content ID {content_id} for quality and provide editorial feedback.

Follow these steps:

1. Retrieve the content using get_content tool with content_id={content_id}

2. Review the content against these criteria:
   - Standards Alignment: Are learning objectives aligned to standards?
   - Pedagogical Soundness: Constructive alignment between objectives, activities, and assessments?
   - Accessibility: WCAG 2.1 AA compliant? UDL principles applied?
   - Cultural Responsiveness: Bias-free and culturally inclusive?
   - Age-Appropriate: Appropriate complexity and language for grade level?
   - Scaffolding: Adequate support for emergent bilinguals (ELPS/ELD)?
   - Assessment: Formative and summative assessment opportunities included?

3. Create a review using create_review tool with:
   - content_id: {content_id}
   - status: "approved", "needs_revision", or "rejected"
   - comments: Specific, actionable feedback
   - rating: 1-5 stars based on overall quality

Provide constructive, detailed feedback to help the author improve the content."""

        return PromptMessage(
            role="user",
            content=PromptTextContent(type="text", text=prompt_text)
        )

    else:
        raise ValueError(f"Unknown prompt: {name}")


# ============================================================================
# RUN SERVER
# ============================================================================

async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
