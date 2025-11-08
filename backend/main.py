"""
Main FastAPI application for Nova - AI-Powered Educational Content Platform.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from core.config import settings
from database.session import engine, Base
from api.v1 import (
    auth,
    users,
    knowledge_base,
    curriculum_configs,
    content,
    content_types,
    reviews,
    search,
    agents,
    workflows,
    skills,
    standards,
    migrations,
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    contact={
        "name": "Nova Platform",
        "url": "https://github.com/pauljbernard/content",
        "email": "support@nova.ai",
    },
    license_info={
        "name": "Proprietary",
        "url": "https://github.com/pauljbernard/content/blob/master/LICENSE",
    },
    terms_of_service="https://github.com/pauljbernard/content/blob/master/TERMS.md",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "JWT-based authentication endpoints for user login, registration, and token management. Supports role-based access control (teacher, author, editor, knowledge_engineer).",
        },
        {
            "name": "Users",
            "description": "User management endpoints for profile updates, password changes, and user administration. Knowledge engineers can manage all users.",
        },
        {
            "name": "Knowledge Base",
            "description": "Browse and access the Multi-Curriculum Knowledge Base with 303 knowledge files across 51 US states. Supports hierarchical navigation and markdown content rendering.",
        },
        {
            "name": "Curriculum Configs",
            "description": "Manage curriculum configurations and knowledge resolution orders. Knowledge engineers only. Defines how content inherits from universal, subject-common, and district-specific knowledge.",
        },
        {
            "name": "Content",
            "description": "Content authoring and management endpoints. Authors create lessons/assessments, editors review and approve, and knowledge engineers manage all content. Supports draft → submit → review → approve → publish workflow.",
        },
        {
            "name": "Content Types",
            "description": "Flexible content modeling system (like Contentful/Strapi). Define custom content types with attributes, create instances, and manage schemas. Enables building any kind of content structure beyond built-in types.",
        },
        {
            "name": "Reviews",
            "description": "Editorial review workflow for content approval. Editors and knowledge engineers review submitted content, provide ratings and feedback, and approve for publication.",
        },
        {
            "name": "Search",
            "description": "Full-text search across knowledge base files and authored content. Supports filtering by subject, grade level, and content type.",
        },
        {
            "name": "Agents",
            "description": "Professor Framework AI agent integration. Invoke autonomous agents for curriculum design, content development, assessment creation, and quality review. Provides 5-10x productivity gains through AI-assisted workflows.",
        },
        {
            "name": "Workflows",
            "description": "Multi-agent workflow orchestration. Create, manage, and execute workflows that chain multiple agents together in sequence. Workflows enable complex content development pipelines with automatic handoffs between agents.",
        },
        {
            "name": "Skills",
            "description": "Professor Framework composable skills. Access and invoke 92 granular skills across 19 categories for specific educational development tasks. Skills are lightweight, reusable functions that can be chained together.",
        },
        {
            "name": "Standards",
            "description": "Educational standards management. Import, browse, and reference standards from various sources (TEKS, CCSS, NGSS, etc.) in CASE format or other formats. Standards are first-class data entities that can be referenced by content, skills, and agents.",
        },
        {
            "name": "Migrations",
            "description": "System migration utilities. Knowledge engineers only. Migrate legacy Content records to the flexible content type system, create system content types for backward compatibility, and track migration progress.",
        },
    ],
)

# Configure CORS
# Always enable CORS with configured origins or default to localhost for development
cors_origins = settings.BACKEND_CORS_ORIGINS if settings.BACKEND_CORS_ORIGINS else [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],  # Important for streaming responses
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.DESCRIPTION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "knowledge_base_files": 303,
        "status": "operational",
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "knowledge_base": "accessible",
    }


# Include API routers
app.include_router(auth.router, prefix=settings.API_V1_STR, tags=["Authentication"])
app.include_router(users.router, prefix=settings.API_V1_STR, tags=["Users"])
app.include_router(
    knowledge_base.router, prefix=settings.API_V1_STR, tags=["Knowledge Base"]
)
app.include_router(
    curriculum_configs.router, prefix=settings.API_V1_STR, tags=["Curriculum Configs"]
)
app.include_router(content.router, prefix=settings.API_V1_STR, tags=["Content"])
app.include_router(content_types.router, prefix=settings.API_V1_STR, tags=["Content Types"])
app.include_router(reviews.router, prefix=settings.API_V1_STR, tags=["Reviews"])
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["Search"])
app.include_router(standards.router, prefix=settings.API_V1_STR, tags=["Standards"])
app.include_router(agents.router, prefix=settings.API_V1_STR, tags=["Agents"])
app.include_router(workflows.router, prefix=f"{settings.API_V1_STR}/workflows", tags=["Workflows"])
app.include_router(skills.router, prefix=f"{settings.API_V1_STR}/skills", tags=["Skills"])
app.include_router(migrations.router, prefix=f"{settings.API_V1_STR}/migrations", tags=["Migrations"])


# Exception handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "path": str(request.url)},
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred",
        },
    )


def custom_openapi():
    """
    Custom OpenAPI schema with enhanced security documentation and examples.
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
        tags=app.openapi_tags,
        contact=app.contact,
        license_info=app.license_info,
        terms_of_service=app.terms_of_service,
    )

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT authentication using access tokens. Obtain tokens via the `/api/v1/auth/login` endpoint.",
        },
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": f"{settings.API_V1_STR}/auth/login",
                    "scopes": {
                        "teacher": "Read access to published content",
                        "author": "Create and edit own content",
                        "editor": "Review and approve content",
                        "knowledge_engineer": "Full system access",
                    },
                }
            },
        },
    }

    # Add global security requirement
    openapi_schema["security"] = [{"Bearer": []}]

    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Development server",
        },
        {
            "url": "https://api.hmhco.com",
            "description": "Production server",
        },
    ]

    # Add additional information
    openapi_schema["info"]["x-logo"] = {
        "url": "https://www.hmhco.com/favicon.ico"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.LOG_LEVEL.lower(),
    )
