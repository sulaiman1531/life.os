from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from uuid import UUID
from datetime import datetime

# --- User Schemas ---
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "employee"
    employer_id: Optional[UUID] = None
    preferences: Dict[str, Any] = {}

class UserCreate(UserBase):
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# --- Task Schemas ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "todo"
    priority: Optional[str] = "medium"
    due_date: Optional[datetime] = None
    project_id: Optional[UUID] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    title: Optional[str] = None

class TaskResponse(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# --- Note Schemas ---
class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None
    tags: List[str] = []

class NoteCreate(NoteBase):
    pass

class NoteUpdate(NoteBase):
    title: Optional[str] = None

class NoteResponse(NoteBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True

# --- Habit Schemas ---
class HabitBase(BaseModel):
    name: str
    frequency: Optional[str] = "daily"

class HabitCreate(HabitBase):
    pass

class HabitUpdate(HabitBase):
    name: Optional[str] = None

class HabitResponse(HabitBase):
    id: UUID
    user_id: UUID
    streak: int
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# --- Habit Log Schemas ---
class HabitLogResponse(BaseModel):
    id: UUID
    habit_id: UUID
    completed_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

# --- Planner Schemas ---
class PlannerBlockBase(BaseModel):
    title: str
    start_time: str
    end_time: str
    date: str

class PlannerBlockCreate(PlannerBlockBase):
    pass

class PlannerBlockResponse(PlannerBlockBase):
    id: int
    owner_id: UUID
    
    class Config:
        from_attributes = True

# --- Finance Schemas ---
class FinanceTransactionBase(BaseModel):
    title: str
    amount: float
    type: str # "in" or "out"

class FinanceTransactionCreate(FinanceTransactionBase):
    pass

class FinanceTransactionResponse(FinanceTransactionBase):
    id: int
    date: datetime
    owner_id: UUID
    
    class Config:
        from_attributes = True

# --- Project Schemas ---
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[str] = "active"
    progress: Optional[int] = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    name: Optional[str] = None

class ProjectResponse(ProjectBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- Goal Schemas ---
class GoalBase(BaseModel):
    title: str
    description: Optional[str] = None
    target_date: Optional[datetime] = None
    progress: Optional[int] = 0

class GoalCreate(GoalBase):
    pass

class GoalUpdate(GoalBase):
    title: Optional[str] = None

class GoalResponse(GoalBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- HealthLog Schemas ---
class HealthLogBase(BaseModel):
    date: str
    water_ml: Optional[int] = 0
    sleep_hours: Optional[float] = 0.0
    steps: Optional[int] = 0
    calories: Optional[int] = 0

class HealthLogCreate(HealthLogBase):
    pass

class HealthLogUpdate(HealthLogBase):
    date: Optional[str] = None

class HealthLogResponse(HealthLogBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- LearningItem Schemas ---
class LearningItemBase(BaseModel):
    title: str
    type: Optional[str] = "course"
    status: Optional[str] = "in_progress"
    progress: Optional[int] = 0
    url: Optional[str] = None

class LearningItemCreate(LearningItemBase):
    pass

class LearningItemUpdate(LearningItemBase):
    title: Optional[str] = None

class LearningItemResponse(LearningItemBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- Reminder Schemas ---
class ReminderBase(BaseModel):
    title: str
    time: datetime
    is_recurring: Optional[bool] = False
    recurrence_rule: Optional[str] = None
    sound_enabled: Optional[bool] = True
    vibration_enabled: Optional[bool] = True
    is_completed: Optional[bool] = False

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(ReminderBase):
    title: Optional[str] = None

class ReminderResponse(ReminderBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# --- TimeLog Schemas ---
class TimeLogBase(BaseModel):
    app_name: str
    duration_minutes: int
    date: str

class TimeLogCreate(TimeLogBase):
    pass

class TimeLogResponse(TimeLogBase):
    id: UUID
    user_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
