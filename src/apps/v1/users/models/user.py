# Imports projects or 3rd party libary dependices
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.core.db.db_config import DbBase

# Association tables
class UserRoles(DbBase):
    __tablename__ = "user_roles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)

class RoleResources(DbBase):
    __tablename__ = "role_resources"
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    resource_id = Column(Integer, ForeignKey("resources.id"), primary_key=True)

class User(DbBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    full_name = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    
class Role(DbBase):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    users = relationship("User", secondary="user_roles", back_populates="roles")
    resources = relationship("Resources", secondary="role_resources", back_populates="roles")

class Resources(DbBase):
    __tablename__ = "resources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    roles = relationship("Role", secondary="role_resources", back_populates="resources")