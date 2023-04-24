from abc import ABC, abstractmethod
from uuid import UUID, uuid4
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from ...todos import Todo as TodoModel

Base = declarative_base()


class Todo(Base):
    """
    Todo database class
    """

    __tablename__ = "todos"

    # id is a uuid4
    id = Column(String, primary_key=True, index=True, default=uuid4)
    task = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(Boolean, index=True)


class TodoRepository(ABC):
    @abstractmethod
    async def get_todo_list(self):
        pass

    @abstractmethod
    async def delete_todo(self, todo_id: UUID):
        pass

    @abstractmethod
    async def insert_todo(self, todo_in: Todo):
        pass

# from database

# from database

# from authors

# from http
