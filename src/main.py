import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import root
from src.api.item import routes as item
from src.api.product import routes as product
from src.utils.database import lifespan
from src.utils.log_config import LOGGING_CONFIG
from src.utils.settings import settings, Mode

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# Configure application mode
app_lifespan = lifespan
docs_url = "/docs"
redoc_url = "/redoc"

if settings.mode == Mode.TEST:
    logger.info("Running in TEST mode. Database connection disabled.")
    app_lifespan = None
elif settings.mode == Mode.LIVE:  # pragma: no cover
    logger.info("Running in LIVE mode. Docs disabled.")
    docs_url = None
    redoc_url = None
else:  # pragma: no cover
    logger.info("Running in DEV mode")

# Initialize FastAPI application
logger.info("Starting FastAPI application...")
app = FastAPI(
    title="An example API",
    summary="A example application",
    lifespan=app_lifespan,
    docs_url=docs_url,
    redoc_url=redoc_url
)

# Adding routes
app.include_router(root.router)
app.include_router(item.router)
app.include_router(product.router)

# Configure CORS
logger.info(f"Enabling CORS. Allowed origins set to: {settings.allow_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allow_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
