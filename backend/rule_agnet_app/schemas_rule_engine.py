from pydantic import BaseModel
from typing import Optional, Any, Dict

class RuleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RuleCreate(RuleBase):
    rule_string: str

class RuleUpdate(RuleBase):
    rule_string: Optional[str] = None

class Rule(RuleBase):
    id: int
    ast_json: Dict[str, Any]

    class Config:
        from_attributes = True

class UserAttributeBase(BaseModel):
    name: str
    data_type: str
    description: Optional[str] = None

class UserAttributeCreate(UserAttributeBase):
    pass

class UserAttribute(UserAttributeBase):
    id: int

    class Config:
        from_attributes = True