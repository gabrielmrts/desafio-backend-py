from sqlalchemy import Column, String, Boolean, Integer
from app.database.base_class import Base
from sqlalchemy.sql import false

class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, nullable=False)
	description = Column(String, nullable=False)
	completed = Column(Boolean, default=False, server_default=false())
