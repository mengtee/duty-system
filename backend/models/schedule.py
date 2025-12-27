from datetime import datetime
from database.database import Base
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship

class Schedule(Base):
    """
    Schedule entity class.
    
    Attributes:
        id: Primary key
        schedule_date: The date of the schedule
        shift_type: Type of shift (morning/afternoon/night/全天)
        created_at: Record creation timestamp
        created_by: Creator identifier
    """
    
    __tablename__ = 'schedule'
    
    id = Column(Integer, primary_key=True)
    schedule_date = Column(Date, nullable=False)
    shift_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationship to schedule assignments
    assignments = relationship('ScheduleAssignment', back_populates='schedule', lazy='dynamic', cascade='all, delete-orphan')
    
    def __init__(self, schedule_date, shift_type: str, created_by: str = 'system'):
        """
        Initialize a new Schedule.
        
        Args:
            schedule_date: Date of the schedule
            shift_type: Type of shift
            created_by: Creator identifier
        """
        self.schedule_date = schedule_date
        self.shift_type = shift_type
        self.created_by = created_by
    
    def to_dict(self) -> dict:
        """
        Convert schedule object to dictionary.
        
        Returns:
            Dictionary representation of schedule with assignments
        """
        assignments = self.get_assignments()
        
        return {
            'id': self.id,
            'schedule_date': self.schedule_date.isoformat() if self.schedule_date else None,
            'shift_type': self.shift_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by,
            'assignments_count': len(assignments),
            'assignments': [
                {
                    'id': a.id,
                    'staff_id': a.staff_id,
                    'staff': {
                        'id': a.staff.id,
                        'name': a.staff.name,
                        'position': a.staff.position
                    } if a.staff else None,
                    'status': a.status,
                    'notes': a.notes
                }
                for a in assignments
            ]
        }
    
    def get_assignments(self):
        """
        Get all assignments for this schedule.
        
        Returns:
            List of ScheduleAssignment objects
        """
        return self.assignments.all()
    
    def __repr__(self):
        """String representation of Schedule object."""
        return f'<Schedule {self.schedule_date} - {self.shift_type}>'
