from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base


class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_hash = Column(String, unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    max_ingested_chars = Column(Integer)     # per month
    max_stored_chars = Column(Integer)       # total KB size
    max_chat_tokens = Column(Integer)        # per month

class UserPlan(Base):
    __tablename__ = "user_plans"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    plan_id = Column(Integer, ForeignKey("plans.id"), nullable=False)

class Usage(Base):
    __tablename__ = "usage"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    # Monthly counters
    ingested_chars = Column(Integer, default=0)
    chat_tokens = Column(Integer, default=0)

    # Storage
    stored_chars = Column(Integer, default=0)
