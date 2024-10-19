from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from rule_agnet_app import rule_engine_models, schemas_rule_engine, crud_opearation
from rule_agnet_app.database_connect import get_db
from rule_agnet_app.rule_engine_file import evaluate_rule

router = APIRouter()

@router.post("/rules/", response_model=schemas_rule_engine.Rule)
def create_rule(rule: schemas_rule_engine.RuleCreate, db: Session = Depends(get_db)):
    return crud_opearation.create_rule_db(db=db, rule=rule)

@router.get("/rules/", response_model=List[schemas_rule_engine.Rule])
def read_rules(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    rules = crud_opearation.get_rules(db, skip=skip, limit=limit)
    return rules

@router.get("/rules/{rule_id}", response_model=schemas_rule_engine.Rule)
def read_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = crud_opearation.get_rule(db, rule_id=rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.put("/rules/{rule_id}", response_model=schemas_rule_engine.Rule)
def update_rule(rule_id: int, rule: schemas_rule_engine.RuleUpdate, db: Session = Depends(get_db)):
    db_rule = crud_opearation.update_rule(db, rule_id=rule_id, rule=rule)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.delete("/rules/{rule_id}", response_model=schemas_rule_engine.Rule)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    db_rule = crud_opearation.delete_rule(db, rule_id=rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    return db_rule

@router.post("/rules/{rule_id}/evaluate")
def evaluate_rule_endpoint(rule_id: int, data: dict, db: Session = Depends(get_db)):
    db_rule = crud_opearation.get_rule(db, rule_id=rule_id)
    if db_rule is None:
        raise HTTPException(status_code=404, detail="Rule not found")
    result = evaluate_rule(db_rule.ast_json, data)
    return {"result": result}