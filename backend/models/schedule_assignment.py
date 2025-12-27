from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship

class ScheduleAssignment(Base):
    """
    ScheduleAssignment entity class - links staff to schedules.
    
    Attributes:
        id: Primary key
        staff_id: Foreign key to staff
        schedule_id: Foreign key to schedule
        duty_date: Date of duty
        shift_type: Type of shift
        status: Assignment status (scheduled/completed/cancelled)
        notes: Additional notes
        created_at: Record creation timestamp
    """
    
    __tablename__ = 'schedule_assignment'
    
    id = Column(Integer, primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.id'), nullable=False)
    schedule_id = Column(Integer, ForeignKey('schedule.id'), nullable=False)
    duty_date = Column(Date, nullable=False)
    shift_type = Column(String(50), nullable=False)
    status = Column(String(20), default='scheduled')
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    staff = relationship('Staff', back_populates='assignments')
    schedule = relationship('Schedule', back_populates='assignments')
    
    def __init__(self, staff_id: int, schedule_id: int, duty_date, shift_type: str, notes: str = None):
        """
        Initialize a new ScheduleAssignment.
        
        Args:
            staff_id: ID of the staff member
            schedule_id: ID of the schedule
            duty_date: Date of duty
            shift_type: Type of shift
            notes: Optional notes
        """
        self.staff_id = staff_id
        self.schedule_id = schedule_id
        self.duty_date = duty_date
        self.shift_type = shift_type
        self.notes = notes
    
    def to_dict(self) -> dict:
        """
        Convert assignment object to dictionary.
        
        Returns:
            Dictionary representation of assignment
        """
        return {
            'id': self.id,
            'staff_id': self.staff_id,
            'staff_name': self.staff.name if self.staff else None,
            'schedule_id': self.schedule_id,
            'duty_date': self.duty_date.isoformat() if self.duty_date else None,
            'shift_type': self.shift_type,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def complete(self):
        """Mark the assignment as completed."""
        self.status = 'completed'
    
    def cancel(self):
        """Cancel the assignment."""
        self.status = 'cancelled'
    
    def __repr__(self):
        """String representation of ScheduleAssignment object."""
        return f'<ScheduleAssignment Staff:{self.staff_id} Date:{self.duty_date}>'
