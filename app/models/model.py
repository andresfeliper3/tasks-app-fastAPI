from db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    tasks = relationship("Task", back_populates="category")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    year_of_birth = Column(Integer)
    email = Column(String)
    password = Column(String)

    created_tasks = relationship(
        "Task",
        back_populates="creator",
        foreign_keys='Task.creator_id')
    tasks_in_charge = relationship(
        "Task",
        back_populates="in_charge",
        foreign_keys='Task.in_charge_id')


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    year = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    creator_id = Column(Integer, ForeignKey("users.id"))
    in_charge_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="tasks")
    creator = relationship(
        "User",
        back_populates="created_tasks",
        foreign_keys=[creator_id])
    in_charge = relationship(
        "User",
        back_populates="tasks_in_charge",
        foreign_keys=[in_charge_id])
