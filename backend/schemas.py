from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

# Staff schemas
class StaffCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=18, le=100)
    position: str = Field(..., min_length=1, max_length=100)

class StaffResponse(BaseModel):
    id: int
    name: str
    age: int
    position: str
    is_active: bool
    
    class Config:
        from_attributes = True

# Schedule schemas
class ScheduleCreate(BaseModel):
    schedule_date: date
    shift_type: str = Field(..., pattern="^(morning|afternoon|night|全天)$")
    created_by: Optional[str] = "system"

# Nested schemas for schedule response
class StaffInfo(BaseModel):
    id: int
    name: str
    position: str

class AssignmentInfo(BaseModel):
    id: int
    staff_id: int
    staff: Optional[StaffInfo]
    status: str
    notes: Optional[str]

class ScheduleResponse(BaseModel):
    id: int
    schedule_date: date
    shift_type: str
    created_by: Optional[str]
    assignments_count: int
    assignments: List[AssignmentInfo] = []
    
    class Config:
        from_attributes = True

# Assignment schemas
class AssignmentCreate(BaseModel):
    schedule_id: int
    staff_ids: List[int]
    notes: Optional[str] = None

class AssignmentResponse(BaseModel):
    id: int
    staff_id: int
    staff_name: Optional[str]
    schedule_id: int
    duty_date: date
    shift_type: str
    status: str
    notes: Optional[str]
    
    class Config:
        from_attributes = True

class AssignmentStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(scheduled|completed|cancelled)$")
