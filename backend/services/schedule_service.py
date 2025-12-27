from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import Session
from models.schedule import Schedule
from models.schedule_assignment import ScheduleAssignment
from models.staff import Staff

class ScheduleService:
    """
    Service class for schedule operations.
    Handles schedule creation, assignment, and queries.
    """
    
    def __init__(self, db: Session):
        """
        Initialize ScheduleService with database session.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def create_schedule(self, schedule_date: date, shift_type: str, created_by: str = 'system') -> Schedule:
        """
        Create a new schedule.
        
        Args:
            schedule_date: Date of the schedule
            shift_type: Type of shift
            created_by: Creator identifier
            
        Returns:
            Created Schedule object
        """
        schedule = Schedule(
            schedule_date=schedule_date,
            shift_type=shift_type,
            created_by=created_by
        )
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule
    
    def assign_staff(self, schedule_id: int, staff_ids: List[int], notes: str = None) -> List[ScheduleAssignment]:
        """
        Assign staff members to a schedule.
        
        Args:
            schedule_id: ID of the schedule
            staff_ids: List of staff IDs to assign
            notes: Optional notes
            
        Returns:
            List of created ScheduleAssignment objects
            
        Raises:
            ValueError: If schedule not found or staff not found
        """
        schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError(f"Schedule with ID {schedule_id} not found")
        
        assignments = []
        for staff_id in staff_ids:
            # Verify staff exists
            staff = self.db.query(Staff).filter(Staff.id == staff_id, Staff.is_active == True).first()
            if not staff:
                raise ValueError(f"Staff with ID {staff_id} not found or inactive")
            
            assignment = ScheduleAssignment(
                staff_id=staff_id,
                schedule_id=schedule_id,
                duty_date=schedule.schedule_date,
                shift_type=schedule.shift_type,
                notes=notes
            )
            self.db.add(assignment)
            assignments.append(assignment)
        
        self.db.commit()
        for assignment in assignments:
            self.db.refresh(assignment)
        
        return assignments
    
    def get_schedules(self, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Schedule]:
        """
        Get schedules within a date range.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of Schedule objects
        """
        query = self.db.query(Schedule)
        
        if start_date:
            query = query.filter(Schedule.schedule_date >= start_date)
        if end_date:
            query = query.filter(Schedule.schedule_date <= end_date)
        
        return query.order_by(Schedule.schedule_date).all()
    
    def get_staff_schedule(self, staff_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[ScheduleAssignment]:
        """
        Get schedule for a specific staff member.
        
        Args:
            staff_id: Staff ID
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            List of ScheduleAssignment objects
        """
        query = self.db.query(ScheduleAssignment).filter(ScheduleAssignment.staff_id == staff_id)
        
        if start_date:
            query = query.filter(ScheduleAssignment.duty_date >= start_date)
        if end_date:
            query = query.filter(ScheduleAssignment.duty_date <= end_date)
        
        return query.order_by(ScheduleAssignment.duty_date).all()
    
    def update_assignment_status(self, assignment_id: int, status: str) -> bool:
        """
        Update the status of an assignment.
        
        Args:
            assignment_id: Assignment ID
            status: New status (scheduled/completed/cancelled)
            
        Returns:
            True if updated, False if not found
        """
        assignment = self.db.query(ScheduleAssignment).filter(ScheduleAssignment.id == assignment_id).first()
        if assignment:
            assignment.status = status
            self.db.commit()
            return True
        return False
    
    def get_schedule_with_assignments(self, schedule_id: int) -> Optional[dict]:
        """
        Get schedule with all its assignments.
        
        Args:
            schedule_id: Schedule ID
            
        Returns:
            Dictionary with schedule and assignments data
        """
        schedule = self.db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            return None
        
        assignments = schedule.get_assignments()
        
        return {
            'schedule': schedule.to_dict(),
            'assignments': [a.to_dict() for a in assignments]
        }
