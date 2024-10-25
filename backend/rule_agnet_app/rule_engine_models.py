from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.sql import func
from .database_connect import Base

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    ast_json = Column(JSON, nullable=False)  # Stores the serialized AST
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)  # Indicates if the rule is active
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class UserAttribute(Base):
    __tablename__ = "user_attributes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    data_type = Column(String, nullable=False)  # The data type of the attribute, e.g., 'integer', 'string'
    description = Column(String)
