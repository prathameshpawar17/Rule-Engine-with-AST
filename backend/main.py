from fastapi import FastAPI
from rule_engine_api.endpoints_rule_engine import rules_api
from rule_agnet_app.database_connect import engine
from rule_agnet_app import rule_engine_models
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables if they don't exist
try:
    rule_engine_models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(title="Rule Engine API", description="API for managing and evaluating rules")

# Include the router for rules API
app.include_router(rules_api.router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the Rule Engine API"}
