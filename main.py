from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import users
from app.api.v1.endpoints import auth
from app.db.session import create_all_tables, engine
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    try:
        logger.info("Initializing database tables...")
        create_all_tables()
        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        raise
    
    yield  # App runs here
    
    # Shutdown code
    logger.info("Shutting down application...")
    try:
        # Properly dispose the engine if using async
        if engine.is_async:
            await engine.dispose()
        logger.info("Cleanup completed")
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    # description=settings.PROJECT_DESCRIPTION,
    # version=settings.VERSION,
    lifespan=lifespan,
    # docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    # redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None
)

# Safer CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost", "http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# app.include_router(
#     users.router,
#     prefix="/api/v1/users",
#     tags=["users"],
#     responses={404: {"description": "Not found"}}
# )

app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])

@app.get("/", include_in_schema=False)
def health_check():
    return {"status": "healthy", "version": settings.VERSION}
