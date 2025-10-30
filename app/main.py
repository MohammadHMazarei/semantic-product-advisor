# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import sys

from app.core.config import get_settings
from app.core.dependencies import get_product_repository
from app.api.routes import router as products_router


# Configure logging
def setup_logging(log_level: str):
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    settings = get_settings()

    # Setup logging
    setup_logging(settings.LOG_LEVEL)
    logger = logging.getLogger(__name__)

    # Startup
    logger.info("=" * 60)
    logger.info(f"🚀 Starting {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info("=" * 60)
    logger.info(f"Embedding Model: {settings.EMBEDDING_MODEL_NAME}")
    logger.info(f"Data Path: {settings.products_json_path}")
    logger.info(f"ChromaDB Path: {settings.chroma_persist_path}")
    logger.info(f"Collection: {settings.COLLECTION_NAME}")
    logger.info("=" * 60)

    try:
        # Load and index products
        repository = get_product_repository()
        products = await repository.load_products()
        logger.info(f"✅ Loaded {len(products)} products successfully")
        logger.info("=" * 60)
        logger.info("🎉 API is ready to accept requests!")
        logger.info("=" * 60)
    except Exception as e:
        logger.error(f"❌ Failed to initialize: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("👋 Shutting down gracefully...")


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    description="Digital Marketing Business Consultant Chatbot API"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products_router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.API_TITLE}",
        "version": settings.API_VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": f"{settings.API_PREFIX}/products/health"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.API_TITLE,
        "version": settings.API_VERSION
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
        log_level=settings.LOG_LEVEL.lower()
    )
