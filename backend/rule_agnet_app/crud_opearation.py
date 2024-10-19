from sqlalchemy.orm import Session
from . import rule_engine_models, schemas_rule_engine
from .rule_engine_file import create_rule

def create_rule_db(db: Session, rule: schemas_rule_engine.RuleCreate):
    ast = create_rule(rule.rule_string)
    db_rule = rule_engine_models.Rule(name=rule.name, description=rule.description, ast_json=ast.to_dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_rule(db: Session, rule_id: int):
    return db.query(rule_engine_models.Rule).filter(rule_engine_models.Rule.id == rule_id).first()

def get_rules(db: Session, skip: int = 0, limit: int = 100):
    return db.query(rule_engine_models.Rule).offset(skip).limit(limit).all()

def update_rule(db: Session, rule_id: int, rule: schemas_rule_engine.RuleUpdate):
    db_rule = db.query(rule_engine_models.Rule).filter(rule_engine_models.Rule.id == rule_id).first()
    if db_rule:
        update_data = rule.dict(exclude_unset=True)
        if 'rule_string' in update_data:
            update_data['ast_json'] = create_rule(update_data['rule_string']).to_dict()
            del update_data['rule_string']
        for key, value in update_data.items():
            setattr(db_rule, key, value)
        db.commit()
        db.refresh(db_rule)
    return db_rule

def delete_rule(db: Session, rule_id: int):
    db_rule = db.query(rule_engine_models.Rule).filter(rule_engine_models.Rule.id == rule_id).first()
    if db_rule:
        db.delete(db_rule)
        db.commit()
    return db_rule