from database import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean
from sqlalchemy.sql import func

class ToDos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    created_date_time = Column(DateTime, default=func.now())
