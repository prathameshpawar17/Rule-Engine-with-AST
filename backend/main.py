from fastapi import FastAPI
from rule_engine_api.endpoints_rule_engine import rules_api
from rule_agnet_app.database_connect import engine
from rule_agnet_app import rule_engine_models

rule_engine_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rules_api.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Rule Engine API"}