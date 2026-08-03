import uuid
import datetime
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, DateTime, JSON, Float
from sqlalchemy.types import Uuid
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    full_name = Column(String, index=True)
    role = Column(String, default="employee") # employer, employee
    employer_id = Column(Uuid, ForeignKey("users.id"), nullable=True) # For employees
    preferences = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")
    habits = relationship("Habit", back_populates="owner", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="owner", cascade="all, delete-orphan")
    health_logs = relationship("HealthLog", back_populates="owner", cascade="all, delete-orphan")
    learning_items = relationship("LearningItem", back_populates="owner", cascade="all, delete-orphan")
    reminders = relationship("Reminder", back_populates="owner", cascade="all, delete-orphan")
    time_logs = relationship("TimeLog", back_populates="owner", cascade="all, delete-orphan")

class TimeLog(Base):
    __tablename__ = "time_logs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    app_name = Column(String, index=True) # e.g. "github", "slack"
    duration_minutes = Column(Integer, default=0)
    date = Column(String, index=True) # YYYY-MM-DD
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="time_logs")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="todo") # todo, in_progress, done
    priority = Column(String, default="medium") # low, medium, high
    due_date = Column(DateTime(timezone=True), nullable=True)
    project_id = Column(Uuid, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    title = Column(String, index=True)
    content = Column(Text, nullable=True)
    tags = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User", back_populates="notes")

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    name = Column(String, index=True)
    frequency = Column(String, default="daily") # daily, weekly
    streak = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="habits")
    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    habit_id = Column(Uuid, ForeignKey("habits.id"))
    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    habit = relationship("Habit", back_populates="logs")

class PlannerBlock(Base):
    __tablename__ = "planner_blocks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    start_time = Column(String) # e.g. "09:00"
    end_time = Column(String) # e.g. "10:30"
    date = Column(String) # e.g. "2024-05-20"
    owner_id = Column(Uuid, ForeignKey("users.id"))
    
    owner = relationship("User")

class FinanceTransaction(Base):
    __tablename__ = "finance_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    amount = Column(Float)
    type = Column(String) # "in" or "out"
    date = Column(DateTime, default=datetime.datetime.utcnow)
    owner_id = Column(Uuid, ForeignKey("users.id"))
    
    owner = relationship("User")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="active") # active, completed, archived
    progress = Column(Integer, default=0) # 0 to 100
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text, nullable=True)
    target_date = Column(DateTime(timezone=True), nullable=True)
    progress = Column(Integer, default=0) # 0 to 100
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="goals")

class HealthLog(Base):
    __tablename__ = "health_logs"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    date = Column(String, index=True) # YYYY-MM-DD
    water_ml = Column(Integer, default=0)
    sleep_hours = Column(Float, default=0.0)
    steps = Column(Integer, default=0)
    calories = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="health_logs")

class LearningItem(Base):
    __tablename__ = "learning_items"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    title = Column(String, index=True)
    type = Column(String, default="course") # course, book, article
    status = Column(String, default="in_progress") # in_progress, completed, wishlist
    progress = Column(Integer, default=0) # 0 to 100
    url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="learning_items")

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(Uuid, ForeignKey("users.id"))
    title = Column(String, index=True)
    time = Column(DateTime(timezone=True))
    is_recurring = Column(Boolean, default=False)
    recurrence_rule = Column(String, nullable=True) # e.g. "daily", "weekly"
    sound_enabled = Column(Boolean, default=True)
    vibration_enabled = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="reminders")
