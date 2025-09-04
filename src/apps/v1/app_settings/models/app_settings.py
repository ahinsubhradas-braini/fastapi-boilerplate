# Imports projects or 3rd party libary dependices
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.core.db.db_config import DbBase
from sqlalchemy.dialects.postgresql import JSON

class AppSettings(DbBase):
    __tablename__ = "app_settings"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, unique=False, index=False)
    data = Column(JSON)